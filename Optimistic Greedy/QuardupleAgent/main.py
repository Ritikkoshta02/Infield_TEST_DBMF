import numpy as np
import random
from collections import defaultdict
# import matplotlib.pyplot as plt
import os
import time

# Import obstacles, footprints (now edges), grid dimensions, start position, and name
from Assays.Multi_REMIA import OBSTICALS, FOOTPRINT_1, FOOTPRINT_2, FOOTPRINT_3, FOOTPRINT_4, GRID_DIM_R, GRID_DIM_C, Start_1, Start_2, Start_3, Start_4, Name
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
FOOTPRINTS_3 = [
    tuple(sorted(edge)) for edge in FOOTPRINT_3  # Normalize edges during initialization
]
total_edges_3 = len(FOOTPRINTS_3)
FOOTPRINTS_4 = [
    tuple(sorted(edge)) for edge in FOOTPRINT_4  # Normalize edges during initialization
]
total_edges_4 = len(FOOTPRINTS_4)

# Initialize Q-table
Q_table_1 = defaultdict(lambda: np.full(NUM_ACTIONS, 1000.0))
Q_table_2 = defaultdict(lambda: np.full(NUM_ACTIONS, 1000.0))
Q_table_3 = defaultdict(lambda: np.full(NUM_ACTIONS, 1000.0))
Q_table_4 = defaultdict(lambda: np.full(NUM_ACTIONS, 1000.0))


# Hyperparameters
alpha = 0.0009  # Learning rate
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

    agent_pos_3 = Start_3  # Starting position
    agent_pos_4 = Start_4  # Starting position
    covered_edges_3 = set()  # Track covered edges
    covered_edges_4 = set()  # Track covered edges
    has_entered_inner_grid_3 = False  # Track if agent enters the inner grid
    has_entered_inner_grid_4 = False  # Track if agent enters the inner grid

    time_step = 0  # Initialize time step
    return agent_pos_1, agent_pos_2, agent_pos_3, agent_pos_4, covered_edges_1, covered_edges_2, covered_edges_3, covered_edges_4, has_entered_inner_grid_1, has_entered_inner_grid_2, has_entered_inner_grid_3, has_entered_inner_grid_4, time_step

# Choose an action using epsilon-greedy policy
def choose_action(Q_table,state, episode):
    if np.random.rand() <= epsilon and (episode % 100000 != 0) and (episode >= 350000):
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
    if any(is_in_obstacle_area(new_pos, obs) for obs in obstacles) and (new_pos != Start):
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
        if(episode % 100000 == 0):
            print(episode)
        agent_pos_1, agent_pos_2,agent_pos_3, agent_pos_4, covered_edges_1, covered_edges_2, covered_edges_3, covered_edges_4, has_entered_inner_grid_1, has_entered_inner_grid_2, has_entered_inner_grid_3, has_entered_inner_grid_4, time_step = init_environment()
        state_1 = get_state(agent_pos_1, time_step)
        state_2 = get_state(agent_pos_2, time_step)
        total_reward_1 = 0
        total_reward_2 = 0
        collision_Flag_1 = False
        collision_Flag_2 = False
        covered_1 = 0
        covered_2 = 0

        state_3 = get_state(agent_pos_3, time_step)
        state_4 = get_state(agent_pos_4, time_step)
        total_reward_3 = 0
        total_reward_4 = 0
        collision_Flag_3 = False
        collision_Flag_4 = False
        covered_3 = 0
        covered_4 = 0

        action_sequence_1 = ""
        action_sequence_2 = ""
        action_sequence_3 = ""
        action_sequence_4 = ""
        
        for _ in range(len(T)-1 ):

            action_1 = choose_action(Q_table_1, state_1,episode)
            action_2 = choose_action(Q_table_2, state_2,episode)
            action_3 = choose_action(Q_table_3, state_3,episode)
            action_4 = choose_action(Q_table_4, state_4,episode)
            

            new_pos_1 = take_action(agent_pos_1, action_1, has_entered_inner_grid_1)
            new_pos_2 = take_action(agent_pos_2, action_2, has_entered_inner_grid_2)
            new_pos_3 = take_action(agent_pos_3, action_3, has_entered_inner_grid_3)
            new_pos_4 = take_action(agent_pos_4, action_4, has_entered_inner_grid_4)

            time_step += 1

            if(time_step<=(len(T)-1)):
                obstacles = T[time_step]  # Get obstacles for the current time step
            else:
                obstacles = []

            reward_1, flag_1 = get_reward(agent_pos_1, new_pos_1, covered_edges_1, FOOTPRINTS_1 , obstacles, Start_1 )
            covered_1 += flag_1

            reward_2, flag_2 = get_reward(agent_pos_2, new_pos_2, covered_edges_2, FOOTPRINTS_2 , obstacles, Start_2 )
            covered_2 += flag_2

            reward_3, flag_3 = get_reward(agent_pos_3, new_pos_3, covered_edges_3, FOOTPRINTS_3 , obstacles, Start_3 )
            covered_3 += flag_3

            reward_4, flag_4 = get_reward(agent_pos_4, new_pos_4, covered_edges_4, FOOTPRINTS_4 , obstacles, Start_4 )
            covered_4 += flag_4

            # if(is_in_obstacle_area(new_pos_2,new_pos_1)):
            #     # Priority System
            #     # new_pos_2 = agent_pos_2
            #     # action_2 = 4
            #     # reward_2 += 3

            #     # Equality
            #     collision_Flag_1 = True
            #     collision_Flag_2 = True
            #     reward_1 += -5
            #     reward_2 += -5

            # Agent 2 checks collision with Agent 1
            if is_in_obstacle_area(new_pos_2, new_pos_1):
                new_pos_2 = agent_pos_2  # Reset Agent 2 to its previous position
                action_2 = 4  # Default action for collision
                reward_2 += 3  # Reward Agent 2 for resolving collision
                if is_in_obstacle_area(new_pos_2, new_pos_1):
                    collision_Flag_1 = True
                    reward_1 += -15

            # Agent 3 checks collision with Agents 1 and 2
            if is_in_obstacle_area(new_pos_3, new_pos_2) or is_in_obstacle_area(new_pos_3, new_pos_1):
                new_pos_3 = agent_pos_3  # Reset Agent 3 to its previous position
                action_3 = 4  # Default action for collision
                reward_3 += 3  # Reward Agent 3 for resolving collision
                if is_in_obstacle_area(new_pos_3, new_pos_2):
                    collision_Flag_2 = True
                    reward_2 += -15
                if is_in_obstacle_area(new_pos_3, new_pos_1):
                    collision_Flag_1 = True
                    reward_1 += -15

            # Agent 4 checks collision with Agents 1, 2, and 3
            if (is_in_obstacle_area(new_pos_4, new_pos_2) or 
                is_in_obstacle_area(new_pos_4, new_pos_3) or 
                is_in_obstacle_area(new_pos_4, new_pos_1)):
                new_pos_4 = agent_pos_4  # Reset Agent 4 to its previous position
                action_4 = 4  # Default action for collision
                reward_4 += 3  # Reward Agent 4 for resolving collision
                if is_in_obstacle_area(new_pos_4, new_pos_3):
                    collision_Flag_3 = True
                    reward_3 += -15
                if is_in_obstacle_area(new_pos_4, new_pos_2):
                    collision_Flag_2 = True
                    reward_2 += -15
                if is_in_obstacle_area(new_pos_4, new_pos_1):
                    collision_Flag_1 = True
                    reward_1 += -15

            # Append action index to action_sequence
            action_sequence_1 += str(action_1)
            action_sequence_2 += str(action_2)
            action_sequence_3 += str(action_3)
            action_sequence_4 += str(action_4)

            if new_pos_1 != Start_1:
                if any(is_in_obstacle_area(new_pos_1, obs) for obs in obstacles):
                    collision_Flag_1 = True
            if new_pos_2 != Start_2:
                if any(is_in_obstacle_area(new_pos_2, obs) for obs in obstacles):
                    collision_Flag_2 = True
            if new_pos_3 != Start_3:
                if any(is_in_obstacle_area(new_pos_3, obs) for obs in obstacles):
                    collision_Flag_3 = True
            if new_pos_4 != Start_4:
                if any(is_in_obstacle_area(new_pos_4, obs) for obs in obstacles):
                    collision_Flag_4 = True

            if(time_step==len(T)-1):
                reward_1 += (100*(covered_1/total_edges_1)+50)
                reward_2 += (100*(covered_2/total_edges_2)+50)
                reward_3 += (100*(covered_3/total_edges_3)+50)
                reward_4 += (100*(covered_4/total_edges_4)+50)

            new_state_1 = get_state(new_pos_1, time_step)
            new_state_2 = get_state(new_pos_2, time_step)
            best_future_q_1 = np.max(Q_table_1[new_state_1])
            best_future_q_2 = np.max(Q_table_2[new_state_2])

            new_state_3 = get_state(new_pos_3, time_step)
            new_state_4 = get_state(new_pos_4, time_step)
            best_future_q_3 = np.max(Q_table_3[new_state_3])
            best_future_q_4 = np.max(Q_table_4[new_state_4])

            Q_table_1[state_1][action_1] += alpha * (reward_1 + gamma * best_future_q_1 - Q_table_1[state_1][action_1])
            Q_table_2[state_2][action_2] += alpha * (reward_2 + gamma * best_future_q_2 - Q_table_2[state_2][action_2])

            Q_table_3[state_3][action_3] += alpha * (reward_3 + gamma * best_future_q_3 - Q_table_3[state_3][action_3])
            Q_table_4[state_4][action_4] += alpha * (reward_4 + gamma * best_future_q_4 - Q_table_4[state_4][action_4])
            
            agent_pos_1 = new_pos_1
            agent_pos_2 = new_pos_2
            agent_pos_3 = new_pos_3
            agent_pos_4 = new_pos_4

            state_1 = new_state_1
            state_2 = new_state_2
            state_3 = new_state_3
            state_4 = new_state_4

            total_reward_1 += reward_1
            total_reward_2 += reward_2
            total_reward_3 += reward_3
            total_reward_4 += reward_4

            if collision_Flag_1 or collision_Flag_2 or collision_Flag_3 or collision_Flag_4:
                break

        alpha = min(alpha_max, alpha * alpha_gain )
              
        if (maxReward) <= (total_reward_1 + total_reward_2 + total_reward_4 + total_reward_4) and (collision_Flag_1 == False) and (collision_Flag_2 == False) and (collision_Flag_3 == False) and (collision_Flag_4 == False)  :
            # q_table_file_1 = os.path.join(f'{Name}', 'qTables', f'q_table_Agent_1{episode + 1}.npy')
            # np.save(q_table_file_1, dict(Q_table_1))
            # q_table_file_2 = os.path.join(f'{Name}', 'qTables', f'q_table_Agent_2{episode + 1}.npy')
            # np.save(q_table_file_2, dict(Q_table_2))
            maxReward = (total_reward_1 + total_reward_2 + total_reward_3 + total_reward_4)
            
            if(vis < (covered_1 + covered_2 + covered_3 + covered_4)):
                vis = (covered_1 + covered_2 + covered_3 + covered_4)
                thatEp = episode
                # Open the log file in append mode
                with open('log.txt', 'a') as log_file:
                    # Save visited nodes
                    log_file.write(f"Visited Nodes: {vis}\n")
                    
                    # Save action sequences
                    log_file.write(f"Action Sequence 1: {action_sequence_1}\n")
                    log_file.write(f"Action Sequence 2: {action_sequence_2}\n")
                    log_file.write(f"Action Sequence 3: {action_sequence_3}\n")
                    log_file.write(f"Action Sequence 4: {action_sequence_4}\n")
                    
                    # Save agent positions
                    log_file.write(f"Agent 1 Position: {agent_pos_1}\n")
                    log_file.write(f"Agent 2 Position: {agent_pos_2}\n")
                    log_file.write(f"Agent 3 Position: {agent_pos_3}\n")
                    log_file.write(f"Agent 4 Position: {agent_pos_4}\n")
                    
                    # Calculate and save remaining edges
                    remaining_edges_1 = set(FOOTPRINTS_1) - covered_edges_1
                    remaining_edges_2 = set(FOOTPRINTS_2) - covered_edges_2
                    remaining_edges_3 = set(FOOTPRINTS_3) - covered_edges_3
                    remaining_edges_4 = set(FOOTPRINTS_4) - covered_edges_4
                    log_file.write(f"Episode {episode + 1}: Remaining edges_1: {list(remaining_edges_1)}\n")
                    log_file.write(f"Episode {episode + 1}: Remaining edges_2: {list(remaining_edges_2)}\n")
                    log_file.write(f"Episode {episode + 1}: Remaining edges_3: {list(remaining_edges_3)}\n")
                    log_file.write(f"Episode {episode + 1}: Remaining edges_4: {list(remaining_edges_4)}\n")
                    
                    # Add a separator for readability
                    log_file.write("------------------------------------------------------------\n")
                
        

    end_time = time.time()
    # Calculate running time
    running_time = end_time - start_time
    print(f"Running time: {running_time:.6f} seconds")
    print(f"visited: {vis}")

# Run the Q-learning algorithm and plot the results
q_learning(episodes=1500000)



