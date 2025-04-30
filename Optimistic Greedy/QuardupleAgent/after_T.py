def greedy_edge_coverage(start_node, ending_node, edges):
    import math

    # Initialize variables
    current_node = start_node
    remaining_edges = set(edges)
    transitions = []
    total_cost = 0

    # Helper function to calculate L1 norm
    def l1_distance(node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    # Main loop to visit all edges
    while remaining_edges:
        # Check if current node is an endpoint of an edge
        covered = False
        for edge in remaining_edges:
            if current_node in edge:
                covered = True
                remaining_edges.remove(edge)
                next_node = edge[1] if current_node == edge[0] else edge[0]
                transitions.append((current_node, next_node))
                total_cost += l1_distance(current_node, next_node)
                current_node = next_node
                break

        if not covered:
            # Find the nearest endpoint among remaining edges
            nearest_node = None
            min_cost = math.inf
            for edge in remaining_edges:
                for endpoint in edge:
                    cost = l1_distance(current_node, endpoint)
                    if cost < min_cost:
                        min_cost = cost
                        nearest_node = endpoint
            # Transition to the nearest endpoint
            transitions.append((current_node, nearest_node))
            total_cost += min_cost
            current_node = nearest_node

    # After covering all edges, move to the ending node
    if current_node != ending_node:
        transitions.append((current_node, ending_node))
        total_cost += l1_distance(current_node, ending_node)

    return transitions, total_cost


# Test case
start_node = (9, 13)
ending_node = (1, 23)
edges = [((1, 11), (1, 12)), ((7, 23), (8, 23)), ((1, 12), (1, 13)), ((2, 12), (3, 12)), ((3, 12), (4, 12)), ((1, 14), (1, 15)), ((1, 23), (2, 23))]

# Run the algorithm
transitions, total_cost = greedy_edge_coverage(start_node, ending_node, edges)

# Output the results
print("Transition sequence:", transitions)
print("Total cost:", total_cost)
