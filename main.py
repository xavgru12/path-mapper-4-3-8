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


def main(folder1, folder2, output_json):
    files1 = collect_by_filename(folder1)
    files2 = collect_by_filename(folder2)

    mapped = []

    # Match by filename
    for filename in sorted(files1.keys() & files2.keys()):
        list1 = files1[filename]
        list2 = files2[filename]

        # Cartesian product to handle multiple matches safely
        for p1 in list1:
            for p2 in list2:
                mapped.append((p1, p2))

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(mapped, f, indent=2)

    print(f"Mapped {len(mapped)} file pairs")
    print(f"Output written to {output_json}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <folderA> <folderB> <output.json>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])

