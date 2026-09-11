import unittest

from topology import HOSTS, LINKS, PATHS, SWITCHES, GraphFlowTopo


class GraphFlowTopologyTests(unittest.TestCase):
    def test_required_nodes_and_links(self):
        topo = GraphFlowTopo()
        self.assertEqual(set(HOSTS), {"h1", "h2"})
        self.assertEqual(set(SWITCHES), {"s1", "s2", "s3", "s4"})
        self.assertEqual(
            {frozenset(link) for link in topo.links()},
            {frozenset(link) for link in LINKS},
        )

    def test_required_paths_are_documented(self):
        self.assertEqual(PATHS[0], ("h1", "s1", "s2", "s4", "h2"))
        self.assertEqual(PATHS[1], ("h1", "s1", "s3", "s4", "h2"))


if __name__ == "__main__":
    unittest.main()
