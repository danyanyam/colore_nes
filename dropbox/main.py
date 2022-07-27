from typing import List
import dropbox
import dotenv
from src.utils import get_root_path


class ImgDownloader:
    def __init__(self) -> None:
        token = self._get_token()
        self.dbx = dropbox.Dropbox(token)

    def _get_token(self, env_name: str = 'DROPBOX_TOKEN'):
        env = dotenv.find_dotenv()
        assert dotenv.load_dotenv(env)
        token = dotenv.get_key(env, key_to_get="DROPBOX_TOKEN")
        assert token
        return token

    def cur_acc(self) -> None:
        return self.dbx.users_get_current_account()

    def list_all_files(self, directory: str) -> List[str]:
        return self.dbx.files_list_folder(directory).entries

    def get(self, from_path: str, to_path: str) -> None:
        self.dbx.files_download_to_file(to_path, from_path)

    def upload(self, from_path: str, to_path: str) -> None:
        self.dbx.files_upload(open(from_path, 'rb').read(), to_path)


def main():
    dbx = ImgDownloader()
    files = dbx.list_all_files('/Документы')
    downloadable = [f for f in files if f.is_downloadable]

    for n, i in enumerate(downloadable):
        dbx.get(i.path_display,
                get_root_path() / 'data/external' / f'{n}.jpeg')


if __name__ == "__main__":
    main()
