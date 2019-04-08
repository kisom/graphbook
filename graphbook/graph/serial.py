# -*- coding: utf-8 -*-
"""
Serial handles dumping to YAML.
"""

import yaml
from typing import Any, Dict


def to_yaml(obj: Dict[str, Any]) -> str:
    """Return the YAML representation of ``obj``."""
    return yaml.dump(obj, Dumper=yaml.SafeDumper)


def from_yaml(data: str) -> Dict[str, Any]:
    """Parse ``data`` as an obj."""
    return yaml.load(data, Loader=yaml.SafeLoader)
