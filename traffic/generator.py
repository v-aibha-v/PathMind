"""Generate real endpoint traffic from Mininet host objects."""

from dataclasses import dataclass
import re
import shlex
import time


@dataclass(frozen=True)
class PingResult:
    transmitted: int
    received: int
    packet_loss_percent: float
    rtt_average_ms: float | None
    raw_output: str


@dataclass(frozen=True)
class ThroughputResult:
    megabits_per_second: float
    raw_output: str


class TrafficGenerator:
    """Run ping and iperf commands through Mininet's host namespaces."""

    def ping(self, source, destination, count: int = 5) -> PingResult:
        if count < 1:
            raise ValueError("count must be positive")
        output = source.cmd("ping", "-c", str(count), destination.IP())
        loss = re.search(r"([\d.]+)% packet loss", output)
        rtt = re.search(r"=\s*[\d.]+/([\d.]+)/", output)
        transmitted = re.search(r"(\d+) packets transmitted", output)
        received = re.search(r"(\d+) received", output)
        if not loss or not transmitted or not received:
            raise RuntimeError(f"Could not parse ping output:\n{output}")
        return PingResult(
            transmitted=int(transmitted.group(1)),
            received=int(received.group(1)),
            packet_loss_percent=float(loss.group(1)),
            rtt_average_ms=float(rtt.group(1)) if rtt else None,
            raw_output=output,
        )

    def iperf(self, source, destination, duration: int = 5, bitrate: str | None = None) -> ThroughputResult:
        if duration < 1:
            raise ValueError("duration must be positive")
        port = 5001
        server_log = "/tmp/graphflow-iperf-server.log"
        destination.cmd(
            "sh", "-c",
            f"iperf -s -p {port} -1 > {shlex.quote(server_log)} 2>&1 &",
        )
        time.sleep(0.2)
        args = ["iperf", "-c", destination.IP(), "-p", str(port), "-t", str(duration)]
        if bitrate:
            args.extend(["-b", bitrate])
        output = source.cmd(*args)
        match = re.findall(r"([\d.]+)\s+([KMG])bits/sec", output)
        if not match:
            raise RuntimeError(f"Could not parse iperf output:\n{output}")
        value, unit = match[-1]
        multiplier = {"K": 0.001, "M": 1.0, "G": 1000.0}[unit]
        return ThroughputResult(float(value) * multiplier, output)

    def normal_traffic(self, source, destination, count: int = 5) -> PingResult:
        return self.ping(source, destination, count)

    def high_load_traffic(self, source, destination, duration: int = 5) -> ThroughputResult:
        return self.iperf(source, destination, duration, bitrate="10M")
