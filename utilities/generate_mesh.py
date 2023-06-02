def generate_mesh():
    num_nodes = int(input("Enter the number of nodes in the mesh: "))

    nodes = list(range(1, num_nodes + 1))

    networks = [[nodes[i], nodes[j]] for i in range(num_nodes) for j in range(i+1, num_nodes)]

    print("nodes:")
    print("  core:", nodes)
    print("networks:")
    print("  core:", networks)

if __name__ == "__main__":
    generate_mesh()
