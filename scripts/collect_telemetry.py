"""Example integration entry point for a running Mininet network."""

from telemetry.collector import TelemetryCollector, to_json


def collect(net):
    """Return a real endpoint telemetry record from a Mininet instance."""
    collector = TelemetryCollector()
    result = collector.endpoint_record(net["h1"], net["h2"])
    return to_json(result)
