def generate_grid():
    num_rows = int(input("Enter the number of rows: "))
    num_columns = int(input("Enter the number of columns: "))

    nodes = list(range(1, num_rows * num_columns + 1))

    networks = []
    for i in range(num_rows):
        for j in range(num_columns):
            node = i * num_columns + j + 1
            # connect to right node if exists
            if j + 1 < num_columns:
                networks.append([node, node + 1])
            # connect to node below if exists
            if i + 1 < num_rows:
                networks.append([node, node + num_columns])

    print("nodes:")
    print("  core:", nodes)
    print("networks:")
    print("  core:", networks)


if __name__ == "__main__":
    generate_grid()
