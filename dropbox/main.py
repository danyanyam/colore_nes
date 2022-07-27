import click
from src.utils import get_root_path
from api import ImgDownloader


@click.command()
@click.option('--dropbox-folder', help='Number of greetings.')
@click.option('--local-folder',
              default=str(get_root_path() / 'dropbox/downloaded'),
              help='path to a folder, where all of the images will'
              ' be downloaded')
@click.option('--files', prompt='File names to download',
              help='The path to text file with ids')
def main(dropbox_folder, local_folder, files):

    dbx = ImgDownloader()
    dbx.set_download_folder(local_folder)

    with open(files, 'r') as f:
        dbx.set_download_files([str(i).strip() for i in f.readlines()])

    dbx.download_folder(dropbox_folder)


if __name__ == "__main__":
    main()
