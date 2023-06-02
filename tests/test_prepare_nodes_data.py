import unittest

from xrdConfCreator import prepare_nodes_data


class TestPrepareNodesData(unittest.TestCase):

    def test_prepare_nodes_data(self):

        yaml_data = {
            'nodes': {
                'core': [2, 3, 6, 7],
                'access': [1, 4, 5]
            },
            'settings': {
                'host_prefix': 'host-'
            }
        }
        node_connections = {1: 2, 2: 4, 3: 4, 4: 2, 5: 2, 6: 2, 7: 2}

        expected_nodes_data = [
            {'node_id': 1, 'node_type': 'access', 'interfaces': [0, 1]},
            {'node_id': 2, 'node_type': 'core', 'interfaces': [0, 1, 2, 3]},
            {'node_id': 3, 'node_type': 'core', 'interfaces': [0, 1, 2, 3]},
            {'node_id': 4, 'node_type': 'access', 'interfaces': [0, 1]},
            {'node_id': 5, 'node_type': 'access', 'interfaces': [0, 1]},
            {'node_id': 6, 'node_type': 'core', 'interfaces': [0, 1]},
            {'node_id': 7, 'node_type': 'core', 'interfaces': [0, 1]}
        ]

        nodes_data = prepare_nodes_data(yaml_data, node_connections)

        self.assertEqual(nodes_data, expected_nodes_data)
