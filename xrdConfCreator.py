import argparse
import os
import pprint

import yaml
from jinja2 import Environment, FileSystemLoader


def validate_yaml(data):
    """Validate the loaded YAML data."""

    # Ensure keys exist
    required_keys = ['nodes', 'networks', 'settings']
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required key(s) in YAML file: {', '.join(missing_keys)}")

    node_types = data['nodes']
    networks = data['networks']
    settings = data['settings']

    # Check nodes
    all_nodes = []
    for node_type, nodes in node_types.items():
        if not isinstance(nodes, list)  :
            raise ValueError(f"Nodes for '{node_type}' are not provided as a list.")
        all_nodes += nodes

    # Check networks
    for network_type, connections in networks.items():
        if not isinstance(connections, list):
            raise ValueError(f"Network connections for '{network_type}' are not provided as a list.")
        for connection in connections:
            if not isinstance(connection, list) or len(connection) != 2:
                raise ValueError(
                    f"Invalid network connection for '{network_type}': {connection}. Expected list of two elements.")
            source, destination = connection
            if source not in all_nodes or (
                    destination is not None and destination != 'None' and destination not in all_nodes):
                raise ValueError(
                    f"Invalid network connection for '{network_type}': {connection}. Source and/or destination not found in nodes.")


    # Check settings
    required_settings = ['host_prefix', 'config_suffix']
    for setting in required_settings:
        if setting not in settings:
            raise ValueError(f"Missing required setting: '{setting}'.")
        if setting == 'config_suffix' and not settings[setting].startswith('.'):
            raise ValueError(f"Invalid 'config_suffix': '{settings[setting]}'. It should start with '.'.")
    optional_settings = ['output_path', 'global_template']
    for setting in optional_settings:
        if setting in settings and setting == 'global_template' and not isinstance(settings[setting], bool):
            raise ValueError(f"Invalid 'global_template' setting: '{settings[setting]}'. Expected a boolean value.")


def load_yaml(yaml_path):
    """Load a yaml file and return its content."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    validate_yaml(data)
    return data



def prepare_networks_data(yaml_data):
    node_connections = {}
    networks_data = []
    combined_networks = []

    for network_type, networks in yaml_data['networks'].items():
        combined_networks.extend([(network, network_type) for network in networks])

    # Sort combined_networks by source_node and destination_node
    # 'None' and None will be sorted first in the destination
    sorted_networks = sorted(combined_networks, key=lambda x: (x[0][0], float('-inf') if x[0][1] in [None, 'None'] else x[0][1]))

    for network, network_type in sorted_networks:
        source_node = network[0]
        destination_node = network[1] if network[1] not in [None, 'None'] else None

        # Count connections for source_node
        if source_node not in node_connections:
            node_connections[source_node] = 0
        source_interface = node_connections[source_node]
        node_connections[source_node] += 1

        # Count connections for destination_node if it's not None
        if destination_node is not None:
            if destination_node not in node_connections:
                node_connections[destination_node] = 0
            destination_interface = node_connections[destination_node]
            node_connections[destination_node] += 1
        else:
            destination_interface = None

        networks_data.append({
            'network_type': network_type,
            'source_node': source_node,
            'source_interface': source_interface,
            'destination_node': destination_node,
            'destination_interface': destination_interface,
        })

    return networks_data, node_connections


def prepare_nodes_data(yaml_data, node_connections):
    nodes_data = []
    combined_nodes = []

    for node_type, node_ids in yaml_data['nodes'].items():
        combined_nodes.extend([(node_id, node_type) for node_id in node_ids])

    # Sort combined nodes in ascending order based on node_id
    sorted_combined_nodes = sorted(combined_nodes, key=lambda x: x[0])

    nodes_number = len(sorted_combined_nodes)

    for node in sorted_combined_nodes:
        node_id, node_type = node
        node_name = f"{yaml_data['settings']['host_prefix']}{node_id}"
        interfaces = list(range(node_connections.get(node_id, 0)))
        nodes_data.append({
            'node_id': node_id,
            'node_type': node_type,
            'interfaces': interfaces
        })

        # Adding the print statement
        print(f"Node {node_id} of type {node_type} has been imported with {len(interfaces)} interfaces.")
        if node_id == nodes_number:
            print(
                f"-----------------------------------------------------"
                f"-----------------------------------------------------")

            print(f"{nodes_number} nodes have been successfully imported.")
            print(
                f"-----------------------------------------------------"
                f"-----------------------------------------------------")

    return nodes_data


def prepare_data(yaml_path):
    """Prepare data from the yaml file for further processing."""
    yaml_data = load_yaml(yaml_path)

    # Prepare networks data and count connections per node
    networks_data, node_connections = prepare_networks_data(yaml_data)

    # Prepare nodes data
    nodes_data = prepare_nodes_data(yaml_data, node_connections)

    # Combine nodes, networks, and settings data into one data structure
    data = {
        'nodes': nodes_data,
        'networks': networks_data,
        'settings': yaml_data['settings'],
    }

    return data


def get_env(config):
    if data['settings'].get('global_template', False) and not config:
        base_directory = os.path.dirname(os.path.abspath(__file__))
    else:
        base_directory = os.getcwd()

    template_path = os.path.join(base_directory, 'templates')

    env = Environment(loader=FileSystemLoader(template_path))

    print (env)

    return env


def render_docker_compose(data):
    nodes_data = data['nodes']
    networks_data = data['networks']
    settings = data['settings']

    # Load Jinja2 template
    env = get_env(False)
    template = env.get_template('docker-compose.xr.jinja2')

    # Render the template with the data
    output = template.render(nodes=nodes_data, networks=networks_data, settings=settings)

    # Save the output to a file
    with open(settings['output_path'] + 'docker-compose.xr.yml', 'w') as f:
        f.write(output)

    print(f"----------------------------------------------------------------------------------------------------------")
    print(f"docker-compose.xr.yml configuration file is created at  {settings['output_path']}docker-compose.xr.yml")
    print(f"----------------------------------------------------------------------------------------------------------")


def render_node_config(data):
    # Create the Jinja2 environment and load templates from the filesystem
    env = get_env(True)

    # Loop over each node
    for node in data['nodes']:
        # Select the template based on the node_type
        template = env.get_template(f"{node['node_type']}.jinja2")

        # Get the networks related to the current node
        related_networks = [network for network in data['networks']
                            if network['source_node'] == node['node_id']
                            or (network['destination_node'] == node['node_id'] and network['destination_node'] is not None)]

        # Create the transformed interfaces
        interfaces = []
        for network in related_networks:
            if network['source_node'] == node['node_id']:
                interface = {
                    'interface_id': network['source_interface'],
                    'peer_node': network['destination_node'],
                    'peer_interface': network['destination_interface'],
                    'interface_type': network['network_type']
                }
            else:  # network['destination_node'] == node['node_id']
                interface = {
                    'interface_id': network['destination_interface'],
                    'peer_node': network['source_node'],
                    'peer_interface': network['source_interface'],
                    'interface_type': network['network_type']
                }
            interfaces.append(interface)

        # Create the list of other nodes
        other_nodes = [n for n in data['nodes'] if n['node_id'] != node['node_id']]

        # Combine the node data, interfaces, and settings
        config_data = {
            'node': node,
            'interfaces': interfaces,
            'other_nodes': other_nodes,
            'settings': data['settings']
        }
        pp = pprint.PrettyPrinter(indent=4, compact=True)
        print()
        pp.pprint(config_data)

        # Render the template with the data
        config = template.render(config_data)

        # Create the config file path
        config_file = f"{data['settings']['output_path']}{data['settings']['host_prefix']}{node['node_id']}{data['settings']['config_suffix']}"

        # Write the config to a file
        with open(config_file, 'w') as f:
            f.write(config)

        print(f"Node {node['node_id']} configuration file is created at {config_file}")



def print_help():
    help_text = """
    This script reads a network configuration from a YAML file and generates corresponding configuration files 
    based on Jinja2 templates. 

    YAML file structure:
    --------------------
    nodes:
        <node_type>: [list of node ids]

    networks:
        <network_type>: [list of [source, destination]]

    settings:
        host_prefix: <string>
        config_suffix: <string starting with .>
        output_path: <string> (optional)
        global_template: <boolean> (optional)

    Generated Files:
    ----------------
    - Docker compose configuration file
    - Node configuration files

    Example usage:
    --------------
    python script.py --config <path to YAML file>
    """
    print(help_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script processes a network config YAML file.',
                                     add_help=False)
    parser.add_argument('--config', type=str, default='./network_config.yml', help='Path to the YAML config file.')
    parser.add_argument('--help', action='store_true', help='Show this help message and exit.')

    args = parser.parse_args()

    if args.help:
        print_help()
        exit()

    yaml_path = args.config  # get the path to the YAML file from command line arguments
    data = prepare_data(yaml_path)

    render_docker_compose(data)
    render_node_config(data)

