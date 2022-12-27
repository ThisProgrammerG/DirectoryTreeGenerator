import os
from os import path
import argparse
from filters import partition, is_directory, filter_excludes

SEPARATOR = '/'
TEE = '├── '
CORNER = '└── '
SPACER = '│   '

def _print_files(files: tuple, indent: str) -> None:
    for file in files:
        shape: str = CORNER if file == files[-1] else TEE
        print(f'{indent}{shape}{file}')

def _print_folders(current_directory: path, directories: tuple, indent: str) -> None:
    for directory in directories:
        shape: str = CORNER if directory == directories[-1] else TEE
        print(f'{indent}{shape}{directory}{SEPARATOR}')

        next_directory_path = os.path.join(current_directory, directory)
        print_directory_tree(next_directory_path, f'{indent}{SPACER}')

def print_directory_tree(current_directory: path, indent: str = '') -> None:
    contents = os.listdir(current_directory)
    files, directories = partition(lambda item: is_directory(current_directory, item), contents)
    files, directories = filter_excludes(files, directories)

    _print_files(files, indent)
    _print_folders(current_directory, directories, indent)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the directory path to display', nargs="?", action='store')
    args = parser.parse_args()

    directory_path = args.path if args.path else os.getcwd()
    directory_path = os.path.normpath(directory_path)

    print(f'{os.path.basename(directory_path)}{SEPARATOR}')
    print_directory_tree(directory_path)


if __name__ == '__main__':
    main()
