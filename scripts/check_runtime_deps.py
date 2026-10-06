"""Fail if a deployed Fritzing folder needs a DLL that neither ships in it nor comes with Windows.

The point is a build that runs after a plain download/extract: no Visual C++ redistributable,
no Qt, no extra installs. Usage: check_runtime_deps.py <folder containing Fritzing.exe>
"""
import os
import pathlib
import sys

import pefile

# Present on the build machine's System32, but not guaranteed on a user's machine, so they must ship.
MUST_BE_BUNDLED_PREFIXES = ("msvcp", "vcruntime", "concrt", "vcomp", "libomp")
# Resolved by the Windows loader itself (API sets are virtual DLLs)
VIRTUAL_PREFIXES = ("api-ms-win-", "ext-ms-win-")


def imported_dlls(path):
    pe = pefile.PE(str(path), fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"],
        pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT"],
    ])
    names = set()
    for attr in ("DIRECTORY_ENTRY_IMPORT", "DIRECTORY_ENTRY_DELAY_IMPORT"):
        for entry in getattr(pe, attr, []):
            names.add(entry.dll.decode().lower())
    pe.close()
    return names


def main(folder):
    root = pathlib.Path(folder)
    if not (root / "Fritzing.exe").exists():
        sys.exit(f"{root / 'Fritzing.exe'} not found")

    bundled = {p.name.lower() for p in root.rglob("*.dll")}
    system32 = pathlib.Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32"

    problems = {}
    binaries = [root / "Fritzing.exe", *root.rglob("*.dll")]
    for binary in binaries:
        for dll in imported_dlls(binary):
            if dll in bundled or dll.startswith(VIRTUAL_PREFIXES):
                continue
            if dll.startswith(MUST_BE_BUNDLED_PREFIXES) or not (system32 / dll).exists():
                problems.setdefault(dll, set()).add(str(binary.relative_to(root)))

    print(f"checked {len(binaries)} binaries, {len(bundled)} bundled DLLs")
    if problems:
        print("\nThese DLLs are imported but neither bundled nor part of Windows:")
        for dll, users in sorted(problems.items()):
            shown = ", ".join(sorted(users)[:4]) + (" ..." if len(users) > 4 else "")
            print(f"  {dll:24} needed by {shown}")
        sys.exit(1)
    print("ok: the folder is self-contained")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
