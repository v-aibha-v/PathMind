"""Collect structured measurements from Mininet and Linux interface counters."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import re
import time

from traffic.generator import PingResult, ThroughputResult, TrafficGenerator


@dataclass(frozen=True)
class TelemetryRecord:
    timestamp: str
    source: str
    destination: str
    latency_ms: float | None
    throughput_mbps: float | None
    packet_loss_percent: float | None


@dataclass(frozen=True)
class LinkTelemetry:
    timestamp: str
    source: str
    interface: str
    peer: str
    status: str
    utilization_percent: float | None
    rx_bytes_per_second: float | None
    tx_bytes_per_second: float | None


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _counter(node, interface: str, name: str) -> int:
    output = node.cmd("cat", f"/sys/class/net/{interface}/statistics/{name}")
    match = re.search(r"\d+", output)
    if not match:
        raise RuntimeError(f"Could not read {name} for {interface}: {output}")
    return int(match.group())


class TelemetryCollector:
    """Collect measurements without inventing values when a command fails."""

    def __init__(self, traffic: TrafficGenerator | None = None):
        self.traffic = traffic or TrafficGenerator()

    def endpoint_record(self, source, destination, ping: PingResult | None = None,
                        throughput: ThroughputResult | None = None) -> TelemetryRecord:
        result = ping or self.traffic.ping(source, destination)
        return TelemetryRecord(
            timestamp=_timestamp(),
            source=source.name,
            destination=destination.name,
            latency_ms=result.rtt_average_ms,
            throughput_mbps=throughput.megabits_per_second if throughput else None,
            packet_loss_percent=result.packet_loss_percent,
        )

    def link(self, source, interface: str, peer: str, interval_seconds: float = 1.0) -> LinkTelemetry:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")
        status = "UP" if source.intf(interface).isUp() else "DOWN"
        rx_before = _counter(source, interface, "rx_bytes")
        tx_before = _counter(source, interface, "tx_bytes")
        time.sleep(interval_seconds)
        rx_after = _counter(source, interface, "rx_bytes")
        tx_after = _counter(source, interface, "tx_bytes")
        rx_rate = (rx_after - rx_before) / interval_seconds
        tx_rate = (tx_after - tx_before) / interval_seconds
        link_speed = source.intf(interface).params.get("speed")
        utilization = None
        if link_speed:
            utilization = (max(rx_rate, tx_rate) * 8 / (link_speed * 1_000_000)) * 100
        return LinkTelemetry(
            timestamp=_timestamp(),
            source=source.name,
            interface=interface,
            peer=peer,
            status=status,
            utilization_percent=utilization,
            rx_bytes_per_second=rx_rate,
            tx_bytes_per_second=tx_rate,
        )


def to_json(record) -> str:
    return json.dumps(asdict(record), sort_keys=True)
