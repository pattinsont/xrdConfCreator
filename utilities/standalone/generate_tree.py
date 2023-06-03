def generate_network_config():
    # Get user input
    num_levels = int(input("Enter the number of levels: "))
    num_children = int(input("Enter the number of children nodes per parent node: "))

    # Initialize nodes and networks
    nodes = {'core': []}
    networks = {'core': []}

    # Node count will help us assign unique ids to each node
    node_count = 1

    # Previous level nodes holds the nodes of the previous level (parent nodes)
    prev_level_nodes = []

    for level in range(num_levels):
        # At each level we generate nodes and add them to nodes list
        level_nodes = list(range(node_count, node_count + num_children ** level))
        nodes['core'].extend(level_nodes)

        # If there are any nodes in the previous level, we connect them with the current level nodes
        if prev_level_nodes:
            for i, parent_node in enumerate(prev_level_nodes):
                # Each parent node is connected to a specific set of children nodes
                start = i * num_children
                end = start + num_children
                children_nodes = level_nodes[start:end]
                networks['core'].extend([[parent_node, child_node] for child_node in children_nodes])

        # The current level nodes will be the parent nodes for the next level
        prev_level_nodes = level_nodes
        node_count += len(level_nodes)

    return nodes, networks


# Call the function and print the result
nodes, networks = generate_network_config()
print("nodes:")
for key, value in nodes.items():
    print(f"  {key}: {value}")

print("\nnetworks:")
for key, value in networks.items():
    print(f"  {key}: {value}")
