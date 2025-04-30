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
start_node = (1, 10)
ending_node = (0, 1)
edges = [((6, 8), (6, 9)), ((11, 5), (12, 5)), ((8, 4), (9, 4)), ((12, 8), (13, 8)), ((4, 7), (5, 7)), ((11, 6), (11, 7)), ((8, 5), (9, 5)), ((13, 1), (14, 1)), ((2, 6), (2, 7)), ((13, 8), (14, 8)), ((2, 2), (3, 2)), ((5, 6), (5, 7)), ((10, 6), (11, 6)), ((11, 7), (11, 8)), ((3, 2), (4, 2)), ((12, 1), (12, 2)), ((5, 8), (6, 8)), ((3, 9), (4, 9)), ((8, 3), (8, 4)), ((11, 4), (11, 5)), ((1, 3), (2, 3)), ((10, 4), (11, 4)), ((11, 6), (12, 6)), ((5, 5), (5, 6)), ((5, 1), (5, 2)), ((11, 5), (11, 6)), ((11, 8), (11, 9)), ((5, 7), (5, 8)), ((11, 7), (12, 7)), ((4, 8), (5, 8)), ((6, 8), (7, 8)), ((5, 4), (5, 5)), ((10, 5), (11, 5)), ((13, 8), (13, 9)), ((14, 2), (14, 3)), ((8, 5), (8, 6)), ((5, 8), (5, 9)), ((14, 1), (14, 2)), ((10, 6), (10, 7)), ((2, 3), (3, 3)), ((3, 2), (3, 3)), ((4, 4), (5, 4)), ((12, 1), (13, 1)), ((1, 3), (1, 4)), ((12, 3), (13, 3)), ((10, 7), (11, 7)), ((11, 4), (12, 4)), ((12, 5), (12, 6)), ((9, 5), (10, 5))]

# Run the algorithm
transitions, total_cost = greedy_edge_coverage(start_node, ending_node, edges)

# Output the results
print("Transition sequence:", transitions)
print("Total cost:", total_cost)
