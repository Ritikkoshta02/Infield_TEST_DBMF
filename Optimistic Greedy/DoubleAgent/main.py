import numpy as np
import random
from collections import defaultdict
# import matplotlib.pyplot as plt
import os
import time

# Import obstacles, footprints (now edges), grid dimensions, start position, and name
from Assays.Multi_inv import OBSTICALS, FOOTPRINT_1, FOOTPRINT_2, GRID_DIM_R, GRID_DIM_C, Start_1, Start_2, Name
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
FOOTPRINTS_1 = [
    tuple(sorted(edge)) for edge in FOOTPRINT_1  # Normalize edges during initialization
]
total_edges_1 = len(FOOTPRINTS_1)

FOOTPRINTS_2 = [
    tuple(sorted(edge)) for edge in FOOTPRINT_2  # Normalize edges during initialization
]
total_edges_2 = len(FOOTPRINTS_2)

# Define full Q-table (non-sparse)
# Q_table_1 = np.zeros((GRID_WIDTH, GRID_HEIGHT, TIME_STEPS, NUM_ACTIONS))
# Q_table_2 = np.zeros((GRID_WIDTH, GRID_HEIGHT, TIME_STEPS, NUM_ACTIONS))

# Initialize Q-table
Q_table_1 = defaultdict(lambda: np.full(NUM_ACTIONS, 1000.0))
Q_table_2 = defaultdict(lambda: np.full(NUM_ACTIONS, 1000.0))


# Hyperparameters
alpha = 0.001  # Learning rate
alpha_gain = 1.00009
alpha_max = 0.9
gamma = 0.99  # Discount factor
epsilon = 0.1  # Exploration rate


# Normalize edge to ensure bidirectionality
def normalize_edge(edge):
    return tuple(sorted(edge))

# Initialize the environment
def init_environment():
    agent_pos_1 = Start_1  # Starting position
    agent_pos_2 = Start_2  # Starting position
    covered_edges_1 = set()  # Track covered edges
    covered_edges_2 = set()  # Track covered edges
    has_entered_inner_grid_1 = False  # Track if agent enters the inner grid
    has_entered_inner_grid_2 = False  # Track if agent enters the inner grid
    time_step = 0  # Initialize time step
    return agent_pos_1, agent_pos_2, covered_edges_1, covered_edges_2, has_entered_inner_grid_1, has_entered_inner_grid_2, time_step

# Choose an action using epsilon-greedy policy
def choose_action(Q_table,state):
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
        return 15, 1  # Reward for covering a new edge

    # Default small penalty for non-rewarding moves
    return -1, 0


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

        agent_pos_1, agent_pos_2, covered_edges_1, covered_edges_2, has_entered_inner_grid_1, has_entered_inner_grid_2, time_step = init_environment()
        state_1 = get_state(agent_pos_1, time_step)
        state_2 = get_state(agent_pos_2, time_step)
        total_reward_1 = 0
        total_reward_2 = 0
        collision_Flag_1 = False
        collision_Flag_2 = False
        covered_1 = 0
        covered_2 = 0

        action_sequence_1 = ""
        action_sequence_2 = ""

        for _ in range(len(T)-1 ):

            action_1 = choose_action(Q_table_1, state_1)
            action_2 = choose_action(Q_table_2, state_2)
            

            new_pos_1 = take_action(agent_pos_1, action_1, has_entered_inner_grid_1)
            new_pos_2 = take_action(agent_pos_2, action_2, has_entered_inner_grid_2)

            time_step += 1

            if(time_step<=(len(T)-1)):
                obstacles = T[time_step]  # Get obstacles for the current time step
            else:
                obstacles = []

            if((new_pos_2 == new_pos_1)):
                # Priority System
                new_pos_2 = agent_pos_2
                action_2 = 4
                reward_2 += 3
                if((new_pos_2 == new_pos_1)):
                    collision_Flag_1 = True
                    reward_1 += -15
                    # print(f"Collision {time_step} and {episode}")
            
            # Append action index to action_sequence
            action_sequence_1 += str(action_1)
            action_sequence_2 += str(action_2)

            reward_1, flag_1 = get_reward(agent_pos_1, new_pos_1, covered_edges_1, FOOTPRINTS_1 , obstacles , Start_1 )
            covered_1 += flag_1

            reward_2, flag_2 = get_reward(agent_pos_2, new_pos_2, covered_edges_2, FOOTPRINTS_2 , obstacles, Start_2 )
            covered_2 += flag_2

            

               

            if new_pos_1 != Start_1:
                if any(is_in_obstacle_area(new_pos_1, obs) for obs in obstacles):
                    collision_Flag_1 = True
            if new_pos_2 != Start_2:
                if any(is_in_obstacle_area(new_pos_2, obs) for obs in obstacles):
                    collision_Flag_2 = True

            if(time_step==len(T)-1):
                reward_1 += (50*(covered_1/total_edges_1))
                reward_2 += (50*(covered_2/total_edges_2))

            new_state_1 = get_state(new_pos_1, time_step)
            new_state_2 = get_state(new_pos_2, time_step)
            best_future_q_1 = np.max(Q_table_1[new_state_1])
            best_future_q_2 = np.max(Q_table_2[new_state_2])

            Q_table_1[state_1][action_1] += alpha * (reward_1 + gamma * best_future_q_1 - Q_table_1[state_1][action_1])
            Q_table_2[state_2][action_2] += alpha * (reward_2 + gamma * best_future_q_2 - Q_table_2[state_2][action_2])
            
            agent_pos_1 = new_pos_1
            agent_pos_2 = new_pos_2

            state_1 = new_state_1
            state_2 = new_state_2

            total_reward_1 += reward_1
            total_reward_2 += reward_2

            if collision_Flag_1 or collision_Flag_2:
                # print(f"Collision_Obstical {time_step} and {episode}")
                break

        alpha = min(alpha_max, alpha * alpha_gain )
              
        if (maxReward) <= (total_reward_1 + total_reward_2) and (collision_Flag_1 == False) and (collision_Flag_2 == False)  :
            # q_table_file_1 = os.path.join(f'{Name}', 'qTables', f'q_table_Agent_1{episode + 1}.npy')
            # np.save(q_table_file_1, dict(Q_table_1))
            # q_table_file_2 = os.path.join(f'{Name}', 'qTables', f'q_table_Agent_2{episode + 1}.npy')
            # np.save(q_table_file_2, dict(Q_table_2))
            maxReward = (total_reward_1 + total_reward_2)
            
            if(vis < (covered_1 + covered_2)):
                vis = (covered_1 + covered_2)
                thatEp = episode
                # Open the log file in append mode
                with open('log.txt', 'a') as log_file:
                    log_file.write(f"{vis}\n")
                    log_file.write(f"{action_sequence_1}\n")
                    log_file.write(f"{action_sequence_2}\n")
                    log_file.write(f"Agent 1 Position: {agent_pos_1}\n")
                    log_file.write(f"Agent 2 Position: {agent_pos_2}\n")

                    # Calculate remaining edges
                    remaining_edges_1 = set(FOOTPRINTS_1) - covered_edges_1
                    remaining_edges_2 = set(FOOTPRINTS_2) - covered_edges_2

                    log_file.write(f"Episode {episode + 1}: Remaining edges_1: {list(remaining_edges_1)}\n")
                    log_file.write(f"Episode {episode + 1}: Remaining edges_2: {list(remaining_edges_2)}\n")
                    log_file.write("\n")  # Add a blank line for better readability


         
        

    end_time = time.time()
    # Calculate running time
    running_time = end_time - start_time
    print(f"Running time: {running_time:.6f} seconds")
    print(f"visited: {vis}")

# Run the Q-learning algorithm and plot the results
q_learning(episodes=700000)



