from pathlib import Path


def get_root_path() -> Path:
    return Path(__file__).parents[1]
