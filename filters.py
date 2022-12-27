from os import path
from itertools import filterfalse, tee
from typing import Iterable, Callable

def partition(func: Callable, iterable: Iterable) -> tuple[Iterable, Iterable]:
    first, second = tee(iterable, 2)
    return filterfalse(func, first), filter(func, second)

def is_directory(current_directory: path, item: str) -> bool:
    return path.isdir(path.join(current_directory, item))

def file_excludes(file: str) -> bool:
    starts_with_dot = file.find('.') == 0
    return not starts_with_dot

def folder_excludes(folder: str) -> bool:
    has_pycache = folder.find('pycache') > -1
    has_venv = folder.find('venv') > -1
    starts_with_dot = folder.find('.') == 0
    return all([not has_pycache, not has_venv, not starts_with_dot])

def filter_excludes(files: Iterable, folders: Iterable) -> tuple[tuple, tuple]:
    return tuple(filter(file_excludes, files)), tuple(filter(folder_excludes, folders))
































