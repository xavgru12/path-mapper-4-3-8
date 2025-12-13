#!/usr/bin/env python3

import os
import json
import sys
from collections import defaultdict


def collect_by_filename(folder):
    """
    Returns:
    { filename : [absolute_path, ...] }
    """
    result = defaultdict(list)
    for root, _, files in os.walk(folder):
        for name in files:
            abs_path = os.path.join(root, name)
            result[name].append(abs_path)
    return result


def main(folderA, folderB, output_json):
    filesA = collect_by_filename(folderA)
    filesB = collect_by_filename(folderB)

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
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <folderA> <folderB> <output.json>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])

