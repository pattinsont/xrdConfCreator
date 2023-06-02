import unittest

from xrdConfCreator import prepare_networks_data


class TestPrepareNetworksData(unittest.TestCase):

    def test_prepare_networks_data(self):
        yaml_data = {
            'networks': {
                'core': [[2, 3], [2, 6], [3, 7], [6, 7]],
                'access': [[1, 'None'], [1, 2], [2, 4], [3, 4], [3, 5], [5, 'None']]
            }
        }
        expected_networks_data = [
            {'network_type': 'access', 'source_node': 1, 'source_interface': 0, 'destination_node': None,
             'destination_interface': None},
            {'network_type': 'access', 'source_node': 1, 'source_interface': 1, 'destination_node': 2,
             'destination_interface': 0},
            {'network_type': 'core', 'source_node': 2, 'source_interface': 1, 'destination_node': 3,
             'destination_interface': 0},
            {'network_type': 'access', 'source_node': 2, 'source_interface': 2, 'destination_node': 4,
             'destination_interface': 0},
            {'network_type': 'core', 'source_node': 2, 'source_interface': 3, 'destination_node': 6,
             'destination_interface': 0},
            {'network_type': 'access', 'source_node': 3, 'source_interface': 1, 'destination_node': 4,
             'destination_interface': 1},
            {'network_type': 'access', 'source_node': 3, 'source_interface': 2, 'destination_node': 5,
             'destination_interface': 0},
            {'network_type': 'core', 'source_node': 3, 'source_interface': 3, 'destination_node': 7,
             'destination_interface': 0},
            {'network_type': 'access', 'source_node': 5, 'source_interface': 1, 'destination_node': None,
             'destination_interface': None},
            {'network_type': 'core', 'source_node': 6, 'source_interface': 1, 'destination_node': 7,
             'destination_interface': 1}
        ]

        #This is the number of connections per node
        expected_node_connections = {1: 2, 2: 4, 3: 4, 4: 2, 5: 2, 6: 2, 7: 2}

        networks_data, node_connections = prepare_networks_data(yaml_data)

        self.assertEqual(networks_data, expected_networks_data)
        self.assertEqual(node_connections, expected_node_connections)

if __name__ == '__main__':
    unittest.main()

