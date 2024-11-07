import json

DATA_FILE = "mac_registry.json"

def load_registry():
    """Load MAC address registry from a file."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_registry(mac_registry):
    """Save MAC address registry to a file."""
    with open(DATA_FILE, "w") as file:
        json.dump(mac_registry, file, indent=4)
