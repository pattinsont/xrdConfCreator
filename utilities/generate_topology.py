def generate_fat_tree():
    num_levels = int(input("Enter the number of levels: "))
    multiplier = int(input("Enter the multiplier per level: "))
    nodes = {'core': []}
    networks = {'core': []}
    node_count = 1
    prev_level_nodes = []
    for level in range(num_levels):
        level_nodes = list(range(node_count, node_count + multiplier ** level))
        nodes['core'].extend(level_nodes)
        if prev_level_nodes:
            for parent_node in prev_level_nodes:
                networks['core'].extend([[parent_node, child_node] for child_node in level_nodes])
        prev_level_nodes = level_nodes
        node_count += len(level_nodes)
    return nodes, networks


def generate_grid():
    num_rows = int(input("Enter the number of rows: "))
    num_columns = int(input("Enter the number of columns: "))
    nodes = {'core': list(range(1, num_rows * num_columns + 1))}
    networks = {'core': []}
    for i in range(num_rows):
        for j in range(num_columns):
            node = i * num_columns + j + 1
            if j + 1 < num_columns:
                networks['core'].append([node, node + 1])
            if i + 1 < num_rows:
                networks['core'].append([node, node + num_columns])
    return nodes, networks


def generate_mesh():
    num_nodes = int(input("Enter the number of nodes in the mesh: "))
    nodes = {'core': list(range(1, num_nodes + 1))}
    networks = {'core': [[nodes['core'][i], nodes['core'][j]] for i in range(num_nodes) for j in range(i+1, num_nodes)]}
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
    print("1. Fat Tree")
    print("2. Grid")
    print("3. Mesh")
    choice = int(input("Enter your choice (1, 2, or 3): "))
    if choice == 1:
        nodes, networks = generate_fat_tree()
    elif choice == 2:
        nodes, networks = generate_grid()
    elif choice == 3:
        nodes, networks = generate_mesh()
    else:
        print("Invalid choice.")
        exit(1)
    print_result(nodes, networks)
