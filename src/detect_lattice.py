import json
import sys
from typing import Literal


def detect_lattice_type(cadnano_json) -> Literal["sq", "he"]:
    """
    Detect whether the design uses square or honeycomb lattice from the cadnano file.
    Uses Cadnano2's base count logic to determine the lattice type.
    Returns: "sq" or "he"
    """
    if "vstrands" not in cadnano_json:
        return "sq"  # Default to square if no vstrands

    # Get number of bases from first non-empty vstrand
    numBases = 0
    for helix in cadnano_json["vstrands"]:
        if "scaf" in helix and len(helix["scaf"]) > 0:
            numBases = len(helix["scaf"])
            break

    if numBases == 0:
        return "sq"  # Default to square if no bases found

    # Use Cadnano2's logic for determining lattice type
    if numBases % 21 == 0 and numBases % 32 == 0:
        while True:
            response = input("Is this a square lattice design? [sq/he] ").lower()
            if response in ["sq", "he"]:
                return response
            else:
                print("Invalid input. Please enter 'sq' for square or 'he' for honeycomb.")
    elif numBases % 21 == 0:  # Honeycomb has 21 bases per step
        return "he"
    elif numBases % 32 == 0:  # Square has 32 bases per step
        return "sq"
    else:
        raise ValueError(f"Unknown lattice type for {numBases} bases")


def get_lattice_type(file_path):
    """
    Read a cadnano file and determine its lattice type.
    Returns: "sq" or "he"
    """
    try:
        with open(file_path) as json_data:
            cadnano = json.load(json_data)
            return detect_lattice_type(cadnano)
    except IOError:
        print(f"File '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print(f"Invalid json file '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error while parsing '{file_path}': {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE:", file=sys.stderr)
        print(f"\t{sys.argv[0]} cadnano_file", file=sys.stderr)
        sys.exit(1)

    lattice_type = get_lattice_type(sys.argv[1])
    print(lattice_type)
