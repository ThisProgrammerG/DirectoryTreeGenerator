import os
import argparse
from itertools import filterfalse, tee

SEP = '/'

def partition(func, iterable):
    first, second = tee(iterable, 2)
    return filterfalse(func, first), filter(func, second)

def filter_ignores(files, folders):
    out_file_ignore = lambda file: file.find('.') != 0
    out_folder_ignore = lambda folder: folder.find('pycache') < 0 and folder.find('venv') < 0 and folder.find('.') < 0
    return tuple(filter(out_file_ignore, files)), tuple(filter(out_folder_ignore, folders))

def _print_files(files, indent):
    for file in files:
        if file == files[-1]:
            print(f'{indent}└── {file}')
        else:
            print(f'{indent}├── {file}')

def _print_folders(root_directory, folders, indent):
    for folder in folders:
        item_path = os.path.join(root_directory, folder)
        if folder == folders[-1]:
            print(f'{indent}└── {folder}{SEP}')
        else:
            print(f'{indent}├── {folder}{SEP}')

        print_directory_tree(item_path, f'{indent}│   ')

def print_directory_tree(root_directory, indent=''):
    contents = os.listdir(root_directory)
    files, folders = partition(lambda item: os.path.isdir(os.path.join(root_directory, item)), contents)
    files, folders = filter_ignores(files, folders)

    _print_files(files, indent)
    _print_folders(root_directory, folders, indent)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the name of the file to process', nargs="?", action='store')
    args = parser.parse_args()

    directory_path = args.path if args.path else os.getcwd()
    directory_path = os.path.normpath(directory_path)

    print(f'{os.path.basename(directory_path)}{SEP}')
    print_directory_tree(directory_path)


if __name__ == '__main__':
    main()
