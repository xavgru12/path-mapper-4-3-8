#!/usr/bin/env python3

import os
import json
import sys
import argparse
from collections import defaultdict


def collect_by_filename(folder, relative):
    """
    Returns:
    { filename : [path, ...] }
    """
    result = defaultdict(list)
    for root, _, files in os.walk(folder):
        for name in files:
            abs_path = os.path.join(root, name)
            if relative:
                path = os.path.relpath(abs_path, folder)
            else:
                path = os.path.abspath(abs_path)
            result[name].append(path)
    return result


def main(folderA, folderB, output_json, relative):
    filesA = collect_by_filename(folderA, relative)
    filesB = collect_by_filename(folderB, relative)

    mapped = []

    for filename in sorted(filesA.keys() & filesB.keys()):
        pathsA = filesA[filename]
        pathsB = filesB[filename]

        for pA in pathsA:
            if len(pathsB) == 1:
                mapped.append((pA, pathsB[0]))
            else:
                mapped.append((pA, pathsB))

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(mapped, f, indent=2)

    print(f"Mapped {len(mapped)} entries")
    print(f"Output written to {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folderA")
    parser.add_argument("folderB")
    parser.add_argument("output_json")
    parser.add_argument(
        "--relative",
        action="store_true",
        help="Store paths relative to the input folders (default: absolute paths)",
    )

    args = parser.parse_args()

    main(args.folderA, args.folderB, args.output_json, args.relative)
