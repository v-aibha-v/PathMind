# Phase 1 environment

Run the following checks in Ubuntu/WSL:

```bash
python3.10 --version
pip --version
mn --version
ovs-vsctl --version
git --version
```

The project uses `~/graphflow/ryu-venv` for Ryu-related Python commands and
expects the Ryu source checkout at `~/graphflow/ryu`. Virtual environments and
the source checkout are intentionally not committed.
