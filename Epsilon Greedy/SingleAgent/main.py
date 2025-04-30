import numpy as np
import random
from collections import defaultdict
# import matplotlib.pyplot as plt
import os
import time

# Import obstacles, footprints (now edges), grid dimensions, start position, and name
from Assays.assayInVitro7x7 import OBSTICALS, FOOTPRINT, GRID_DIM_R, GRID_DIM_C, Start, Name

# Grid dimensions and actions
GRID_SIZE_R = GRID_DIM_R
GRID_SIZE_C = GRID_DIM_C
NUM_ACTIONS = 5

# Create output directory and subdirectory for Q-tables
def create_output_dirs():
    if not os.path.exists(Name):
        os.makedirs(Name)
    if not os.path.exists(f'{Name}/qTables'):
        os.makedirs(f'{Name}/qTables')

# Action mapping
ACTION_MAPPING = {
    0: (1, 0),  # Up
    1: (-1, 0), # Down
    2: (0, -1), # Left
    3: (0, 1),  # Right
    4: (0, 0)   # No movement
}

# Obstacle pattern over time
T = OBSTICALS

# Footprints (now edges) that the agent needs to cover
FOOTPRINTS = [
    tuple(sorted(edge)) for edge in FOOTPRINT  # Normalize edges during initialization
]
total_edges = len(FOOTPRINTS)

# Define full Q-table (non-sparse)
# Q_table_1 = np.zeros((GRID_WIDTH, GRID_HEIGHT, TIME_STEPS, NUM_ACTIONS))

# Initialize Q-table
Q_table = defaultdict(lambda: np.zeros(NUM_ACTIONS))

# Hyperparameters
alpha = 0.001  # Learning rate
alpha_gain = 1.00005
alpha_max = 0.8
gamma = 0.99  # Discount factor
epsilon = 1.0  # Exploration rate
epsilon_min = 0.05
epsilon_decay = 0.99999

# Normalize edge to ensure bidirectionality
def normalize_edge(edge):
    return tuple(sorted(edge))

# Initialize the environment
def init_environment():
    agent_pos = Start  # Starting position
    covered_edges = set()  # Track covered edges
    has_entered_inner_grid = False  # Track if agent enters the inner grid
    time_step = 0  # Initialize time step
    return agent_pos, covered_edges, has_entered_inner_grid, time_step

# Choose an action using epsilon-greedy policy
def choose_action(state):
    if np.random.rand() <= epsilon:
        return random.choice(range(NUM_ACTIONS))
    else:
        return np.argmax(Q_table[state])

# Get the state representation
def get_state(agent_pos, time_step):
    return (agent_pos, time_step)

# Update the agent's position based on the action
def take_action(agent_pos, action, has_entered_inner_grid):
    move = ACTION_MAPPING[action]
    new_pos = (agent_pos[0] + move[0], agent_pos[1] + move[1])
    # Check if the agent is still in the outer layer
    if not has_entered_inner_grid:
        # Check if new position is still in the outer layer
        if (new_pos[0] <= 0 or new_pos[0] >= GRID_SIZE_R - 1 or 
            new_pos[1] <= 0 or new_pos[1] >= GRID_SIZE_C - 1):
            return agent_pos  # No movement if still in outer layer
        else:
             # Move into the inner grid
            has_entered_inner_grid = True
            return new_pos
    else:
        # In inner grid, proceed with normal movement
        if (new_pos[0] <= 0 or new_pos[0] >= GRID_SIZE_R - 1 or 
            new_pos[1] <= 0 or new_pos[1] >= GRID_SIZE_C - 1):
            return agent_pos  # No movement if still in outer layer
        else:
            return new_pos
        
def is_in_obstacle_area(agent_pos, obstacle_pos):
    # Check if the agent is within a 3x3 area around the obstacle
    ax, ay = agent_pos
    ox, oy = obstacle_pos
    return (ox - 1 <= ax <= ox + 1) and (oy - 1 <= ay <= oy + 1)

# Define the reward function for edge-based model
def get_reward(agent_pos, new_pos, covered_edges, target_edges, obstacles, Start):
    edge = normalize_edge((agent_pos, new_pos))

    # Check if the agent collides with an obstacle
    if any(is_in_obstacle_area(new_pos, obs) for obs in obstacles) and (Start != new_pos):
        return -20, 0  # Large penalty for colliding with an obstacle
    
    # Check if the edge is a target and hasn't been covered
    if edge in target_edges and edge not in covered_edges:
        covered_edges.add(edge)  # Add the edge to the set of covered edges
        return 10, 1  # Reward for covering a new edge

    # Default small penalty for non-rewarding moves
    return -1.5, 0


# Main Q-learning loop
def q_learning(episodes=2500):
    global epsilon
    global alpha
    
    maxReward =  -2**31
    thatEp = 0
    vis = 0
    create_output_dirs()
    start_time = time.time()

    for episode in range(episodes):

        agent_pos, covered_edges, has_entered_inner_grid, time_step = init_environment()
        state = get_state(agent_pos, time_step)
        total_reward = 0
        collision_Flag = False
        covered = 0

        action_sequence = ""
        for _ in range(len(T)-1 ):

            action = choose_action(state)
            # Append action index to action_sequence
            action_sequence += str(action)

            new_pos = take_action(agent_pos, action, has_entered_inner_grid)

            time_step += 1

            if(time_step<=(len(T)-1)):
                obstacles = T[time_step]  # Get obstacles for the current time step
            else:
                obstacles = []

            reward, flag = get_reward(agent_pos, new_pos, covered_edges, FOOTPRINTS , obstacles, Start)
            covered += flag

            if new_pos != Start:
                if any(is_in_obstacle_area(new_pos, obs) for obs in obstacles):
                    collision_Flag = True

            if(time_step==len(T)-1):
                reward += (50*(covered/total_edges))

            new_state = get_state(new_pos, time_step)
            best_future_q = np.max(Q_table[new_state])
            Q_table[state][action] += alpha * (reward + gamma * best_future_q - Q_table[state][action])
            
            agent_pos = new_pos
            state = new_state
            total_reward += reward

            if collision_Flag:
                break

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        alpha = min(alpha_max, alpha * alpha_gain )
              
        if (maxReward) <= total_reward and (collision_Flag == False)  :
            q_table_file = os.path.join(f'{Name}', 'qTables', f'q_table_{episode + 1}.npy')
            np.save(q_table_file, dict(Q_table))
            maxReward = total_reward
            
            if(vis < covered):
                vis = covered
                thatEp = episode
                print({vis})
                print({action_sequence})
                print(agent_pos)
                # Calculate remaining edges
                remaining_edges = set(FOOTPRINTS) - covered_edges
                print(f"Episode {episode + 1}: Remaining edges: {list(remaining_edges)}")

        if(thatEp + 200000 ) < episode :
            break    
        

    end_time = time.time()
    # Calculate running time
    running_time = end_time - start_time
    print(f"Running time: {running_time:.6f} seconds")
    print(f"visited: {vis}")

# Run the Q-learning algorithm and plot the results
q_learning(episodes=550000)



