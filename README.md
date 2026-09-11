# GraphFlow

GraphFlow is a knowledge-graph-oriented framework for context-aware traffic
management in software-defined networks. This repository currently implements
only the reliable SDN foundation for Phases 1 and 2: Ryu/OpenFlow 1.3,
Mininet, a four-switch multi-path topology, traffic generation, and real
network telemetry.

Phase 3 (Neo4j, a dynamic context graph, CADE, weighted scoring, and
intelligent path selection) is intentionally not implemented.

## Architecture and topology

```text
                 s2
                /  \
               /    \
      h1 ----- s1    s4 ----- h2
               \    /
                \  /
                 s3
```

The two available paths are:

* `h1 -> s1 -> s2 -> s4 -> h2`
* `h1 -> s1 -> s3 -> s4 -> h2`

## Requirements

Run all commands in Ubuntu/WSL, not Windows Python:

* Python 3.10
* Mininet 2.3.0
* Open vSwitch 3.7.1
* Ryu source in `~/graphflow/ryu`
* Ryu virtual environment in `~/graphflow/ryu-venv`

The Mininet and OVS commands require the normal system privileges for network
namespaces and the OVS database.

## Setup

```bash
cd ~/graphflow
python3.10 -m venv ryu-venv
source ryu-venv/bin/activate
python -m pip install pbr
python -m pip install -e ~/graphflow/ryu
```

Ryu's historical `hooks.py` expected the removed
`easy_install.get_script_args` API. The vendored compatibility patch maps that
API to `ScriptWriter.get_args` and keeps the original callable for pbr. Modern
Python 3.10 environments also need current `eventlet`, `dnspython`, and
`packaging` versions:

```bash
python -m pip install --upgrade eventlet dnspython packaging
PYTHONPATH=~/graphflow/ryu python ~/graphflow/ryu/bin/ryu-manager --version
```

The expected result is `ryu-manager 4.34`. The repository does not commit
`ryu-venv`.

## Run the controller and topology

Terminal 1:

```bash
cd ~/graphflow
source ryu-venv/bin/activate
PYTHONPATH=~/graphflow/ryu python ~/graphflow/ryu/bin/ryu-manager \
    controller.graphflow_switch
```

Terminal 2:

```bash
cd ~/graphflow
sudo mn -c
sudo PYTHONPATH=. python3.10 topology.py
```

The topology uses remote controller `127.0.0.1:6633`, OVS, and OpenFlow 1.3.
Inside the Mininet CLI, use:

```text
pingall
h1 ping -c 5 h2
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

## Traffic and telemetry

The `traffic.generator.TrafficGenerator` class runs real `ping` and `iperf`
commands inside Mininet host namespaces:

```python
from traffic.generator import TrafficGenerator

traffic = TrafficGenerator()
traffic.normal_traffic(net["h1"], net["h2"])
traffic.high_load_traffic(net["h1"], net["h2"])
```

`telemetry.collector.TelemetryCollector` records endpoint latency, packet
loss, and throughput, and reads Linux interface byte counters for receive and
transmit rates. Link status comes from the Mininet interface; utilization is
calculated only when Mininet exposes a link speed, so no utilization value is
fabricated. Records can be serialized with `telemetry.collector.to_json`.

## Verification

```bash
python3.10 -m unittest discover -s tests -v
python3.10 -m py_compile topology.py traffic/generator.py \
    telemetry/collector.py controller/graphflow_switch.py
```

For the live integration check, start the controller and topology, then run
`pingall`, the endpoint ping, an `iperf` measurement through
`TrafficGenerator`, and `ovs-ofctl -O OpenFlow13 dump-flows` for each switch.
The controller log should report datapaths 1 through 4.

## Current limitations and Phase 3 handoff

The current release does not select a path intelligently, maintain a graph
database, classify application context, or score routes. It supplies future
phases with structured endpoint and link records containing timestamps,
endpoints, latency, throughput, packet loss, interface rates, utilization when
available, and link status.
