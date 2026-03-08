#!/usr/bin/env python3
"""Assembles individual cell files into a Jupyter notebook (.ipynb)."""
import json, os, glob

cells_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells")
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KG_Verify_V4_Thesis.ipynb")

files = sorted(glob.glob(os.path.join(cells_dir, "c*.txt")))

notebook = {
    "nbformat": 4,
    "nbformat_minor": 4,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "version": "3.10.12"
        },
        "accelerator": "GPU",
        "gpuClass": "standard"
    },
    "cells": []
}

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    lines = content.split('\n')
    cell_type = "code"
    if lines[0].strip().startswith("#TYPE:"):
        cell_type = lines[0].strip().split(":")[1].strip()
        lines = lines[1:]

    source_text = '\n'.join(lines)
    # Build source as list of lines with \n (notebook format)
    raw_lines = source_text.split('\n')
    source_lines = []
    for i, line in enumerate(raw_lines):
        if i < len(raw_lines) - 1:
            source_lines.append(line + '\n')
        else:
            if line:  # skip trailing empty
                source_lines.append(line)

    cell = {"cell_type": cell_type, "metadata": {}, "source": source_lines}
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    notebook["cells"].append(cell)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook created: {output_path}")
print(f"Total cells: {len(notebook['cells'])}")
for i, cell in enumerate(notebook['cells']):
    ctype = cell['cell_type']
    nlines = len(cell['source'])
    preview = cell['source'][0].strip()[:60] if cell['source'] else ''
    print(f"  Cell {i+1:2d} [{ctype:8s}] {nlines:4d} lines | {preview}")
