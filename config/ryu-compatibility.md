# Ryu compatibility

The vendored Ryu checkout uses `ryu/hooks.py` during installation. Modern
setuptools removed `easy_install.get_script_args`; the compatibility hook maps
that name to `easy_install.ScriptWriter.get_args` before pbr replaces the
script writer.

On Python 3.10, the historical Ryu pins also require runtime compatibility
updates:

```bash
source ~/graphflow/ryu-venv/bin/activate
python -m pip install pbr
python -m pip install -e ~/graphflow/ryu
python -m pip install --upgrade eventlet dnspython packaging
PYTHONPATH=~/graphflow/ryu python ~/graphflow/ryu/bin/ryu-manager --version
```

This produces `ryu-manager 4.34` in the validated environment.
