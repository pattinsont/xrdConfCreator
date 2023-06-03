def get_user_input(prompt):
    return int(input(prompt))

def get_user_input_str(prompt):
    return input(prompt)

def generate_tree(net_type, start_node=1, parent_node=None):
    num_levels = get_user_input("Enter the number of levels: ")
    num_children = get_user_input("Enter the number of children nodes per parent node: ")
    nodes = {net_type: []}
    networks = {net_type: []}
    node_count = start_node
    prev_level_nodes = []
    if parent_node:
        networks[net_type].append([parent_node, start_node])
    for level in range(num_levels):
        level_nodes = list(range(node_count, node_count + num_children ** level))
        nodes[net_type].extend(level_nodes)
        if prev_level_nodes:
            for i, parent_node in enumerate(prev_level_nodes):
                start = i * num_children
                end = start + num_children
                children_nodes = level_nodes[start:end]
                networks[net_type].extend([[parent_node, child_node] for child_node in children_nodes])
        prev_level_nodes = level_nodes
        node_count += len(level_nodes)
    return nodes, networks

def generate_fat_tree(net_type, start_node=1, parent_node=None):
    num_levels = get_user_input("Enter the number of levels: ")
    multiplier = get_user_input("Enter the multiplier per level: ")
    nodes = {net_type: []}
    networks = {net_type: []}
    node_count = start_node
    prev_level_nodes = []
    if parent_node:
        networks[net_type].append([parent_node, start_node])
    for level in range(num_levels):
        level_nodes = list(range(node_count, node_count + multiplier ** level))
        nodes[net_type].extend(level_nodes)
        if prev_level_nodes:
            for parent_node in prev_level_nodes:
                networks[net_type].extend([[parent_node, child_node] for child_node in level_nodes])
        prev_level_nodes = level_nodes
        node_count += len(level_nodes)
    return nodes, networks

def generate_grid(net_type, start_node=1, parent_node=None):
    num_rows = get_user_input("Enter the number of rows: ")
    num_columns = get_user_input("Enter the number of columns: ")
    nodes = {net_type: list(range(start_node, start_node + num_rows * num_columns))}
    networks = {net_type: []}
    if parent_node:
        networks[net_type].append([parent_node, start_node])
    for i in range(num_rows):
        for j in range(num_columns):
            node = i * num_columns + j + start_node
            if j + 1 < num_columns:
                networks[net_type].append([node, node + 1])
            if i + 1 < num_rows:
                networks[net_type].append([node, node + num_columns])
    return nodes, networks

def generate_mesh(net_type, start_node=1, parent_node=None):
    num_nodes = get_user_input("Enter the number of nodes in the mesh: ")
    nodes = {net_type: list(range(start_node, start_node + num_nodes))}
    networks = {net_type: [[nodes[net_type][i], nodes[net_type][j]] for i in range(num_nodes) for j in range(i+1, num_nodes)]}
    if parent_node:
        networks[net_type].insert(0, [parent_node, start_node])
    return nodes, networks

def generate_ring(net_type, start_node=1, parent_node=None):
    num_nodes = get_user_input("Enter the number of nodes in the ring: ")
    nodes = {net_type: list(range(start_node, start_node + num_nodes))}
    networks = {net_type: [[nodes[net_type][i - 1], nodes[net_type][i]] for i in range(1, num_nodes)]}
    networks[net_type].append([nodes[net_type][-1], nodes[net_type][0]])
    if parent_node:
        networks[net_type].insert(0, [parent_node, start_node])
    return nodes, networks

def print_result(nodes, networks):
    print("nodes:")
    for key, value in nodes.items():
        print(f"  {key}: {value}")
    print("\nnetworks:")
    for key, value in networks.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print("Choose the network topology you want to generate:")
    print("1. Tree")
    print("2. Fat Tree")
    print("3. Grid")
    print("4. Mesh")
    print("5. Ring")

    choice = int(input("Enter your choice (1, 2, 3, 4, or 5): "))
    is_child = get_user_input_str("Is this a child network? (y/n): ")
    start_node = 1
    parent_node = None
    if is_child.lower() == 'y':
        parent_node = get_user_input("What is the parent node: ")
        start_node = get_user_input("What is the starting node number: ")

    net_type = get_user_input_str("Enter network and node type: ")

    if choice == 1:
        nodes, networks = generate_tree(net_type, start_node, parent_node)
    elif choice == 2:
        nodes, networks = generate_fat_tree(net_type, start_node, parent_node)
    elif choice == 3:
        nodes, networks = generate_grid(net_type, start_node, parent_node)
    elif choice == 4:
        nodes, networks = generate_mesh(net_type, start_node, parent_node)
    elif choice == 5:
        nodes, networks = generate_ring(net_type, start_node, parent_node)
    else:
        print("Invalid choice.")
        exit(1)
    print_result(nodes, networks)
