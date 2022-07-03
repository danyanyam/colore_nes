from pathlib import Path
from typing import List
import pandas as pd


def get_root_path() -> Path:
    return Path(__file__).parents[1]


def get_user_info() -> pd.DataFrame:
    return pd.read_csv(
        get_root_path() / 'data/raw/user_info_original_from_dropbox.csv')


def get_imgs_paths() -> List[Path]:
    return list((get_root_path() / 'data/raw/Collageszip').glob('*.jpg'))
