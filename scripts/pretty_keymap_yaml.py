#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["PyYAML>=6.0"]
# ///
"""Rewrite raw keymap-drawer YAML labels for Endgame custom behaviors."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

LAYER_NAMES = {
    "0": "Default",
    "1": "Extras",
    "2": "Device",
    "3": "Scroll",
    "4": "Snipe",
    "5": "User",
    "LAYER_DEFAULT": "Default",
    "LAYER_EXTRAS": "Extras",
    "LAYER_DEVICE": "Device",
    "LAYER_SCROLL": "Scroll",
    "LAYER_SNIPE": "Snipe",
    "LAYER_USER": "User",
}

MOUSE_BUTTONS = {
    "LCLK": "Left Click",
    "MCLK": "Middle Click",
    "RCLK": "Right Click",
    "MB4": "Mouse 4",
    "MB5": "Mouse 5",
}

EXACT_LABELS: dict[str, Any] = {
    "&trans": {"t": "▽", "type": "trans"},
    "&bst_copy": "Copy",
    "&bst_paste": "Paste",
    "&bst_cut": "Cut",
    "&bst_undo": "Undo",
    "&zbs_adv": "Output next",
    "&bst_tog ZBS_TOG": "Bistable toggle",
    "&af_toggle AF_TOG": "Feedback toggle",
    "&studio_unlock": "Studio unlock",
    "&soft_off": "Soft off",
    "&rrl 1": "Report rate",
}

SENS_LABELS = {
    ("&sens", "P2SM_DEC"): "Pointer -sens",
    ("&sens", "P2SM_INC"): "Pointer +sens",
    ("&scrlsens", "P2SM_DEC"): "Scroll -sens",
    ("&scrlsens", "P2SM_INC"): "Scroll +sens",
}


def layer_name(value: str) -> str:
    return LAYER_NAMES.get(value, value)


def mouse_label(value: str) -> str:
    return MOUSE_BUTTONS.get(value, value)


def prettify_string(value: str) -> Any:
    if value in EXACT_LABELS:
        return EXACT_LABELS[value]
    if value.startswith("&mkp "):
        return mouse_label(value.split(maxsplit=1)[1])
    if match := re.fullmatch(r"&ltmkp (\S+) (.+)", value):
        return {"t": match.group(2), "h": layer_name(match.group(1))}
    if match := re.fullmatch(r"&ltm (\S+) (.+)", value):
        return {"t": mouse_label(match.group(2)), "h": layer_name(match.group(1))}
    if match := re.fullmatch(r"&cdch (\S+) 0", value):
        return {"t": "Copy/Paste", "h": layer_name(match.group(1))}
    parts = value.split()
    if len(parts) >= 2 and (parts[0], parts[1]) in SENS_LABELS:
        return SENS_LABELS[(parts[0], parts[1])]
    return value


def prettify(value: Any) -> Any:
    if isinstance(value, str):
        return prettify_string(value)
    if isinstance(value, list):
        return [prettify(item) for item in value]
    if isinstance(value, dict):
        return {key: prettify(item) for key, item in value.items()}
    return value


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: pretty_keymap_yaml.py <raw-yaml>", file=sys.stderr)
        return 2
    data = yaml.safe_load(Path(sys.argv[1]).read_text())
    yaml.safe_dump(prettify(data), sys.stdout, sort_keys=False, allow_unicode=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
