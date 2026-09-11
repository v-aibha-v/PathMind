"""The Phase 2 two-path Mininet topology."""

from mininet.topo import Topo


HOSTS = ("h1", "h2")
SWITCHES = ("s1", "s2", "s3", "s4")
LINKS = (
    ("h1", "s1"),
    ("s1", "s2"),
    ("s2", "s4"),
    ("s1", "s3"),
    ("s3", "s4"),
    ("s4", "h2"),
)
PATHS = (
    ("h1", "s1", "s2", "s4", "h2"),
    ("h1", "s1", "s3", "s4", "h2"),
)


class GraphFlowTopo(Topo):
    """Hosts connected by two independent switch paths."""

    def build(self):
        for host in HOSTS:
            self.addHost(host)
        for switch in SWITCHES:
            self.addSwitch(switch, protocols=["OpenFlow13"])
        for left, right in LINKS:
            self.addLink(left, right)


topos = {"graphflow": GraphFlowTopo}


def run():
    """Start the topology against a remote OpenFlow 1.3 controller."""
    from mininet.cli import CLI
    from mininet.net import Mininet
    from mininet.node import RemoteController, OVSSwitch

    net = Mininet(
        topo=GraphFlowTopo(),
        controller=None,
        switch=OVSSwitch,
        autoSetMacs=True,
        build=False,
    )
    net.addController("c0", controller=RemoteController, ip="127.0.0.1", port=6633)
    net.build()
    net.start()
    try:
        CLI(net)
    finally:
        net.stop()


if __name__ == "__main__":
    run()
