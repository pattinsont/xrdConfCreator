Purpose
-------

This Python script is intended to read a YAML configuration file which describes a network topology and associated settings. Based on this input, the script will generate necessary configuration files, such as Docker Compose files and node configuration files, for establishing a network environment in line with the given specification.

User Interface
--------------

### Command Line Arguments

Users interact with the script through command line arguments. The script accepts two optional arguments:

1.  `--config` : Specifies the path to the YAML configuration file. By default, this is set to `./network_config.yml`.
    
    Example usage: `python script.py --config path/to/config.yml`
    
2.  `--help` : Displays the help message and exits.
    
    Example usage: `python script.py --help`
    

Inputs
------

### YAML Configuration File

The script requires a YAML configuration file as input. The file should be structured as follows:

```java
nodes:
    <node_type>: [list of node ids]

networks:
    <network_type>: [list of [source, destination]]

settings:
    host_prefix: <string>
    config_suffix: <string starting with .>
    output_path: <string> (optional)
    global_template: <boolean> (optional)
```

For example:

```java
nodes:
  core: [2, 3, 6, 7]
  access: [1, 4, 5]

networks:
  core: [[2, 3], [2, 6], [3, 7], [6, 7]]
  access: [[1, None], [1, 2], [2, 4], [3, 4], [3, 5], [5, None]]

settings:
  host_prefix: xr-
  config_suffix:  .cfg
  output_path: ./
  global_template: True
```

#### Nodes

The `nodes` section describes the nodes to be part of the network. The key is the type of the node (e.g., `core`, `access`), and the value is a list of node IDs.

The node type signifies the configuration template to be used. For instance, `core` would use one configuration template, while `access` could use another (some other examples `aggregation`, `route reflector`, `pce` etc).

#### Networks

The `networks` section defines the network connections in the environment. Each type of connection (e.g., `core`, `access`) is the key, and the value is a list of pairs indicating the source and destination nodes. Each connection pair is an ordered list with two node IDs.

The network type is used to select values within a configuration file. For instance, if node 2 connects to node 3, it might use an interface with `core` configuration (e.g. metric 10), and if node 2 connects to node 1, it might use an interface with `access` configuration (e.g. metric 100).

*   The first node ID is the source, and the second node ID is the destination.
    
*   If a network should be provisioned without a connection to a destination, for example to connect to a host interface, `None` should be used as the destination.
    
*   The order of these connections is significant. In the provided example, for node 1 (\[1, None\], \[1, 2\]), the first interface (gi0/0/0/0) will connect to `None` and the second interface (gi0/0/0/1) will connect to node 2.
    

#### Settings

*   The `settings` section provides additional settings for the network environment:
    
    *   `host_prefix`: This is a prefix string that will be added to the hostname for each node. In this example, it is set to `xr-`.
        
    *   `config_suffix`: This is a suffix string (starting with a dot) that will be added to each generated configuration file. In this example, it's `.cfg`.
        
    *   `output_path`: This setting specifies the directory where the generated files will be saved. In this example, it is the current directory (`./`).
        
    *   `global_template`: (Optional) A boolean flag to control the directory from which templates are loaded. If set to true, templates are loaded from the script directory. If false or omitted, templates are loaded from the current directory.
        

Outputs
-------

The script generates the following output:

1.  Docker Compose configuration file: This file, named `docker-compose.xr.yml`, is generated in the directory specified by `output_path` in the settings. This file contains the Docker environment configuration settings in accordance with the input configuration.
    
2.  Node configuration files: For each node defined in the YAML file, a separate configuration file is created in the directory specified by `output_path` in the settings. The file name is formed by appending the `host_prefix`, node ID, and `config_suffix`. For instance, the file for