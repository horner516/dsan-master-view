import unittest
from unittest.mock import MagicMock, patch
from discovery import scan_network, scan_targets


class DiscoveryTests(unittest.TestCase):
    def test_bounds_and_ports(self):
        self.assertEqual(scan_targets({'subnet':'10.21.0.119/32', 'ports':[6120]}), [('10.21.0.119', 6120)])
        for subnet in ['10.0.0.0/8', '8.8.8.8/32', '::1/128', 'invalid']:
            with self.assertRaises(ValueError):
                scan_targets({'subnet':subnet, 'ports':[6120]})
        with self.assertRaises(ValueError):
            scan_targets({'subnet':'10.0.0.1/32', 'ports':[0]})

    def test_multiple_results_and_existing_connection_not_probed(self):
        with patch('discovery.socket.create_connection', return_value=MagicMock()) as connect:
            results = scan_network({'subnet':'10.21.0.0/30', 'ports':[6120]}, [('10.21.0.1', 6120)])
        self.assertEqual([item['host'] for item in results], ['10.21.0.1', '10.21.0.2'])
        connect.assert_called_once_with(('10.21.0.2', 6120), timeout=0.4)

    def test_closed_port_is_not_reported(self):
        with patch('discovery.socket.create_connection', side_effect=OSError):
            self.assertEqual(scan_network({'subnet':'10.21.0.1/32', 'ports':[6120]}), [])


if __name__ == '__main__':
    unittest.main()
