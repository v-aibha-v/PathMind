# GraphFlow

GraphFlow is a knowledge-graph-oriented framework for context-aware traffic
management in Software-Defined Networks (SDN).

The current implementation provides the reliable SDN foundation for Phase 1
and Phase 2: Ryu/OpenFlow 1.3, Mininet, a four-switch multipath topology,
real traffic generation, and network telemetry.

The complete GraphFlow framework is planned across four phases. Phase 3 and
Phase 4 are not yet implemented. They will extend the current telemetry
foundation with application context, a dynamic knowledge graph, CADE,
context-aware scoring, and intelligent path selection.

## Complete GraphFlow Pipeline

The intended end-to-end GraphFlow pipeline is:

                         USER REQUEST
                              |
                              v
                    APPLICATION CONTEXT
                  +----------------------+
                  | Application Type    |
                  | Request Type        |
                  | Priority            |
                  | Service             |
                  | Criticality         |
                  | Dependencies        |
                  +----------+-----------+
                             |
                             v
                  DYNAMIC CONTEXT GRAPH
                           (Neo4j)
                             ^
                             |
             +---------------+---------------+
             |                               |
             v                               v
       NETWORK TELEMETRY              NETWORK TOPOLOGY
             |                               |
      +------+---------+              +------+--------+
      | Latency        |              | Switches      |
      | Throughput     |              | Servers       |
      | Packet Loss    |              | Links         |
      | Utilization    |              | Paths         |
      | Link Status    |              +---------------+
      +------+---------+
             |
             v
            CADE
  Context-Aware Decision Engine
             |
             v
      Candidate Path Discovery
             |
             v
       Context-Aware Evaluation
             |
             v
       Path Suitability Score
             |
             v
       BEST SUITABLE PATH
             |
             v
        SDN CONTROLLER
           (Ryu/ONOS)
             |
             v
        OpenFlow Rules
             |
             v
       NETWORK SWITCHES
             |
             v
           TRAFFIC

The score is only one part of the decision process. The intended approach
combines application and service context with current network state before
selecting the most suitable path.

## Implementation Phases

| Phase | Description | Status |
|---|---|---|
| Phase 1 | SDN foundation, multipath topology, and traffic generation | Completed |
| Phase 2 | Real network telemetry and structured network records | Completed |
| Phase 3 | Application context, Neo4j Dynamic Context Graph, and CADE | Planned |
| Phase 4 | Context-aware scoring, intelligent path selection, and evaluation | Planned |

## Phase 1 - SDN Network Foundation

Phase 1 establishes the basic SDN environment required by GraphFlow.

### Implemented

- Ryu SDN controller
- OpenFlow 1.3
- Mininet
- Open vSwitch
- Four-switch multipath topology
- Host-to-host connectivity
- Real traffic generation
- Multiple available paths

### Architecture and Topology

                 s2
                /  \
               /    \
      h1 ----- s1    s4 ----- h2
               \    /
                \  /
                 s3

The two available paths are:

h1 -> s1 -> s2 -> s4 -> h2

h1 -> s1 -> s3 -> s4 -> h2

The multipath topology provides alternative routes between h1 and h2.
These alternative paths will be used by later phases for path evaluation.

## Phase 2 - Network Telemetry

Phase 2 adds real network observation to the SDN foundation.

The telemetry layer collects measurements from the actual Mininet network
rather than using fabricated values.

### Collected Telemetry

- Endpoint latency
- Packet loss
- Throughput
- Interface receive rate
- Interface transmit rate
- Link status
- Link utilization when link speed information is available

### Current Phase 1-2 Pipeline

Mininet Network
       |
       v
Traffic Generation
   ping / iperf
       |
       v
Telemetry Collector
       |
       v
Network Measurements
       |
       v
Structured Telemetry Records

Utilization is calculated only when Mininet exposes a link speed. No
utilization value is fabricated.

Records can be serialized into JSON for use by future phases.

## Current Architecture

                 +---------------------+
                 |   Ryu Controller    |
                 |    OpenFlow 1.3     |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 |   Mininet / OVS     |
                 |   Multipath Network |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 |  Traffic Generator  |
                 |     ping / iperf    |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Telemetry Collector |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Structured Network  |
                 |      Telemetry      |
                 +---------------------+

## Phase 3 - Application Context and Dynamic Context Graph

Status: Planned

Phase 3 will extend the current network telemetry foundation with
application and service context.

### Planned Components

- Application Context
- Neo4j
- Dynamic Context Graph
- Context-Aware Decision Engine (CADE)

Application context will describe what a network request represents,
including information such as:

Application Type
Request Type
Priority
Service
Criticality
Dependencies

The Dynamic Context Graph will represent relationships between entities
such as:

User
  |
  v
Application
  |
  v
Service
  |
  v
Server
  |
  v
Database
  |
  v
Switch
  |
  v
Network Path

The graph will combine application/service relationships with network
telemetry and topology information.

## Phase 4 - Context-Aware Routing

Status: Planned

Phase 4 will implement the routing intelligence.

The planned decision pipeline is:

Application Context
        +
Network Telemetry
        +
Network Topology
        |
        v
Dynamic Context Graph
        |
        v
CADE
        |
        v
Candidate Paths
        |
        v
Context-Aware Evaluation
        |
        v
Path Suitability Score
        |
        v
Best Suitable Path
        |
        v
SDN Controller
        |
        v
OpenFlow Forwarding

The planned scoring mechanism will consider multiple factors, including:

- Network conditions
- Application priority
- Service criticality
- Dependency information
- Availability

Priority is therefore an input to the decision, not the sole basis for
selecting a path.

## Requirements

Run all commands in Ubuntu/WSL, not Windows Python.

- Python 3.10
- Mininet 2.3.0
- Open vSwitch 3.7.1
- Ryu source in ~/graphflow/ryu
- Ryu virtual environment in ~/graphflow/ryu-venv

The Mininet and Open vSwitch commands require the normal system privileges
for network namespaces and the OVS database.

## Setup

cd ~/graphflow
python3.10 -m venv ryu-venv
source ryu-venv/bin/activate

python -m pip install pbr
python -m pip install -e ~/graphflow/ryu

Ryu's historical hooks.py expected the removed
easy_install.get_script_args API.

The vendored compatibility patch maps that API to ScriptWriter.get_args
and keeps the original callable required by pbr.

Modern Python 3.10 environments also need current versions of eventlet,
dnspython, and packaging:

python -m pip install --upgrade eventlet dnspython packaging

Verify Ryu:

PYTHONPATH=~/graphflow/ryu \
python ~/graphflow/ryu/bin/ryu-manager --version

Expected result:

ryu-manager 4.34

The repository does not commit ryu-venv.

## Run the Controller and Topology

### Terminal 1 - Ryu Controller

cd ~/graphflow
source ryu-venv/bin/activate

PYTHONPATH=~/graphflow/ryu \
python ~/graphflow/ryu/bin/ryu-manager \
    controller.graphflow_switch

### Terminal 2 - Mininet

cd ~/graphflow

sudo mn -c

sudo PYTHONPATH=. python3.10 topology.py

The topology uses:

- Remote controller: 127.0.0.1:6633
- Open vSwitch
- OpenFlow 1.3

## Phase 1 Verification

Inside the Mininet CLI:

pingall

This verifies host-to-host connectivity.

Test the endpoint directly:

h1 ping -c 5 h2

Inspect OpenFlow rules:

sh ovs-ofctl -O OpenFlow13 dump-flows s1

The controller log should report datapaths 1 through 4.

## Traffic Generation

The traffic.generator.TrafficGenerator class executes real ping and
iperf commands inside Mininet host namespaces.

Example:

from traffic.generator import TrafficGenerator

traffic = TrafficGenerator()

traffic.normal_traffic(
    net["h1"],
    net["h2"]
)

traffic.high_load_traffic(
    net["h1"],
    net["h2"]
)

This provides real traffic for the telemetry layer.

## Telemetry Collection

telemetry.collector.TelemetryCollector records network observations
including:

- Latency
- Packet Loss
- Throughput
- Interface Receive Rate
- Interface Transmit Rate
- Link Status
- Utilization when available

Example conceptual flow:

Traffic
   |
   v
Network
   |
   v
TelemetryCollector
   |
   v
Measurements
   |
   v
Structured Records
   |
   v
JSON

Telemetry records can be serialized using:

telemetry.collector.to_json

## Verification

Run the unit tests:

python3.10 -m unittest discover -s tests -v

Run syntax verification:

python3.10 -m py_compile topology.py traffic/generator.py \
    telemetry/collector.py controller/graphflow_switch.py

## Live Integration Check

For the complete Phase 1-2 demonstration:

1. Start the Ryu controller.

2. Start the Mininet topology.

3. Verify connectivity using pingall.

4. Test endpoint latency using:

   h1 ping -c 5 h2

5. Generate traffic using TrafficGenerator.

6. Collect telemetry using TelemetryCollector.

7. Inspect the collected network metrics.

8. Verify OpenFlow rules using:

   sh ovs-ofctl -O OpenFlow13 dump-flows s1

Repeat the OpenFlow verification for the remaining switches as required.

The controller log should report datapaths 1 through 4.

## Current Status

Phase 1 - Completed

- SDN controller
- OpenFlow 1.3
- Mininet
- Open vSwitch
- Four-switch multipath topology
- Real traffic generation

Phase 2 - Completed

- Real network telemetry
- Latency measurement
- Packet-loss measurement
- Throughput measurement
- Interface receive/transmit rates
- Link status
- Utilization when link speed is available
- Structured telemetry records

Phase 3 - Planned

- Application context
- Neo4j
- Dynamic Context Graph
- CADE

Phase 4 - Planned

- Candidate path evaluation
- Context-aware scoring
- Intelligent path selection
- SDN controller execution
- Performance evaluation

## Current Limitations and Phase 3 Handoff

The current release does not:

- Select a path intelligently
- Maintain a Neo4j graph database
- Classify application context
- Implement the Dynamic Context Graph
- Implement CADE
- Calculate context-aware route scores
- Perform intelligent path selection

Instead, the current release provides the reliable SDN and telemetry
foundation required by the later phases.

The Phase 1-2 implementation supplies future phases with structured
endpoint and link records containing:

- Timestamps
- Endpoints
- Latency
- Throughput
- Packet loss
- Interface receive rates
- Interface transmit rates
- Utilization when available
- Link status

These records will serve as inputs to the application-context and
knowledge-graph layers in the later phases.

## Project Progress

The current implementation progress is:

Phase 1
SDN Network Foundation
        |
        v
Phase 2
Real Network Telemetry
        |
        v
Phase 3
Application Context
+
Dynamic Context Graph
+
CADE
        |
        v
Phase 4
Context-Aware Scoring
+
Intelligent Path Selection
        |
        v
SDN Controller
        |
        v
Traffic Forwarding

Current milestone: Phase 1 + Phase 2 completed.
