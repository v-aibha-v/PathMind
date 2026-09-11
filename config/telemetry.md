# Telemetry record contract

`TelemetryRecord` contains an UTC timestamp, source and destination names,
latency in milliseconds, throughput in megabits per second, and packet loss
percentage. Values come from endpoint `ping` and `iperf` output.

`LinkTelemetry` contains the source node, interface, peer, UP/DOWN status,
receive and transmit byte rates, and utilization when the Mininet interface
exposes a configured link speed. Rates are sampled from Linux interface
counters over a caller-supplied interval; they are never hardcoded.
