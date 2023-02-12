import argparse
from pathlib import Path
from normalize import normalize
from threading import Thread
import logging

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", required=True, help="Source folder")
parser.add_argument("--output", "-o", default="dist")
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")

folders = []
files = []


def read_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            Thread(target=read_folder, args=(el,))


def replace_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                el.replace(new_path / normalize(el.name))
                files.append(normalize(el.name))
            except OSError as e:
                logging.error(e)


def start_program(sort_folder: Path):
    print(f'Сортуємо папку: {sort_folder}')
    threads = []
    th_1 = Thread(target=read_folder, args=(sort_folder,))
    th_1.start()
    folders.append(sort_folder)
    th_1.join()
    for folder in folders:
        th = Thread(target=replace_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print(f'Сортування папки: {sort_folder} завершено!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%9=(threadName)s %(message)s')
    sort_folder = Path(source)
    output_folder = Path(output)
    start_program(sort_folder)





