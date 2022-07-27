import dropbox
import dotenv
from typing import List
from src.utils import get_root_path
from pathlib import Path
import datetime as dt
from tqdm import tqdm


class ImgDownloader:
    def __init__(self) -> None:
        token = self._get_token()
        self._activated = False
        self._download_to = get_root_path() / 'dropbox/downloaded'
        self._download_only = []

        try:
            self.dbx = dropbox.Dropbox(token)
            self.dbx.users_get_current_account()
            self._activated = True

        except dropbox.exceptions.AuthError as e:
            print('Regenerate key', str(e))

    def _get_token(self, env_name: str = 'DROPBOX_TOKEN'):
        env = dotenv.find_dotenv()
        assert dotenv.load_dotenv(env)
        token = dotenv.get_key(env, key_to_get=env_name)
        assert token
        return token

    def set_download_files(self, list_of_files: List[str]) -> None:
        self._download_only = list_of_files
        print(f'Added {len(self._download_only)} to download procedure')

    def set_download_folder(self, path: Path) -> None:
        now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        path = Path(path) / now
        path.mkdir(exist_ok=True, parents=True)
        self._download_to = path

    def download_folder(self, path) -> None:
        contents = self.list_all_files(path)
        donwloaded = 0

        if self._download_only:
            contents = [i for i in contents if i.name.split('.')[0] in self._download_only]
            print(f'Found {len(contents)} of {len(self._download_only)} files')

        for content in tqdm(contents):
            self.get(Path(content.path_display))
            donwloaded += 1

        print(f'Downloaded {donwloaded} files')

    def list_all_files(self, directory: str) -> List[str]:
        if not self._activated:
            return

        return self.dbx.files_list_folder(directory).entries

    def get(self, from_path: str) -> None:
        if not self._activated:
            return

        fname = Path(from_path).name
        local_path = Path(self._download_to) / fname
        self.dbx.files_download_to_file(str(local_path), str(from_path))

    def upload(self, from_path: str, to_path: str) -> None:
        if not self._activated:
            return

        self.dbx.files_upload(open(from_path, 'rb').read(), to_path)
