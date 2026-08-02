#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

import xml.etree.ElementTree as ET
from copy import deepcopy

ET.register_namespace("", "http://www.w3.org/2000/svg")

tree = ET.parse("./roboglance.svg")

for element in tree.iter():
    if element.tail and not element.tail.strip():
        element.tail = None
    if element.text and not element.text.strip():
        element.text = None

layer_names = [
    layer.attrib["layer"]
    for layer in tree.findall(".//{http://www.w3.org/2000/svg}g[@layer]")
    if layer.attrib["layer"] != "Background"
]

for i, layer_name in enumerate(layer_names):
    layer_tree = deepcopy(tree)

    for layer in layer_tree.findall(".//{http://www.w3.org/2000/svg}g[@layer]"):
        if layer.attrib["layer"] != layer_name:
            layer_tree.getroot().remove(layer)

    layer_tree.write(f"./RoboGlance.icon/Assets/{layer_name}.svg")
