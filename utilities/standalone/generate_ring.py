def generate_ring():
    num_nodes = int(input("Enter the number of nodes in the ring: "))

    nodes = list(range(1, num_nodes + 1))

    networks = [[nodes[i - 1], nodes[i]] for i in range(1, num_nodes)]
    # connect the last node to the first to close the ring
    networks.append([nodes[-1], nodes[0]])

    print("nodes:")
    print("  core:", nodes)
    print("networks:")
    print("  core:", networks)


if __name__ == "__main__":
    generate_ring()
