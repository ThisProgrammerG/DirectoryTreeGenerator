import os
from os import path
import argparse
from itertools import filterfalse, tee
from typing import Iterable, Callable

SEP = '/'
TEE = '├── '
CORNER = '└── '
SPACER = '│   '

def partition(func: Callable, iterable: Iterable) -> tuple[Iterable, Iterable]:
    first, second = tee(iterable, 2)
    return filterfalse(func, first), filter(func, second)

def file_ignores(file: str) -> bool:
    return file.find('.') != 0

def folder_ignores(folder: str) -> bool:
    return folder.find('pycache') < 0 and folder.find('venv') < 0 and folder.find('.') < 0

def filter_ignores(files: Iterable, folders: Iterable) -> tuple[tuple, tuple]:
    return tuple(filter(file_ignores, files)), tuple(filter(folder_ignores, folders))

def _print_files(files: tuple, indent: str) -> None:
    for file in files:
        shape = CORNER if file == files[-1] else TEE
        print(f'{indent}{shape}{file}')

def _print_folders(root_directory: str, folders: tuple, indent: str) -> None:
    for folder in folders:
        shape = CORNER if folder == folders[-1] else TEE
        print(f'{indent}{shape}{folder}{SEP}')

        next_directory_path = os.path.join(root_directory, folder)
        print_directory_tree(next_directory_path, f'{indent}{SPACER}')

def print_directory_tree(root_directory: path, indent: str = '') -> None:
    contents = os.listdir(root_directory)
    files, folders = partition(lambda item: os.path.isdir(os.path.join(root_directory, item)), contents)
    files, folders = filter_ignores(files, folders)

    _print_files(files, indent)
    _print_folders(root_directory, folders, indent)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the directory path to process', nargs="?", action='store')
    args = parser.parse_args()

    directory_path = args.path if args.path else os.getcwd()
    directory_path = os.path.normpath(directory_path)

    print(f'{os.path.basename(directory_path)}{SEP}')
    print_directory_tree(directory_path)


if __name__ == '__main__':
    main()
