import os
import re
import sys
import json
import tarfile
import argparse

CONFIG_FILE = "entry.json"


def _gathering_directory(root, excludes, exclude_pattern):
    compiled_pattern = [re.compile(pattern) for pattern in exclude_pattern]

    def _filter_proc(item):
        if item in excludes:
            # excludes still take effect, cause only take account base name
            return False

        for p in compiled_pattern:
            if p.fullmatch(item):
                return False

        return True

    collect_files = []
    for abs_root, folders, files in os.walk(root, topdown=True):
        if excludes or compiled_pattern:
            folders[:] = list(filter(_filter_proc, folders))
            files = list(filter(_filter_proc, files))

        collect_files.extend([os.path.join(abs_root, item) for item in files])
    return collect_files


def _pack_check(path):
    config_file = os.path.join(path, CONFIG_FILE)
    if not os.path.isfile(config_file):
        error = "%s doesn't exist under %s" % (CONFIG_FILE, path)
        raise Exception(error)

    with open(config_file, "r", encoding="utf-8") as fh:
        entry = json.load(fh)["model"]
    entry_file = os.path.join(path, entry + ".py")
    if not os.path.isfile(entry_file):
        error = "%s.py specified in %s doesn't exist" % (entry, CONFIG_FILE)
        raise Exception(error)


def pack_models(model_root: str, tar_file: str = None, dry: bool = False, excludes: list = ["run_script.py", "upload.tar.gz", "__pycache__"], exclude_pattern: list = []):
    """ packing model root using tar, gz
    file or directory would be filtered by excludes and exclude_pattern, only base name takes effect
    eg. exclude = [a/b], takes no effect, model_root/a/b won't be remove

    if tar_file not specified,  model_root/upload.tar.gz would be generated

    :param model_root: model script dir
    :type model_root: str
    :param dry: only for test
    :type dry: bool
    :param excludes: defaults to ["run_script.py"]
    :type excludes: list, optional
    :param exclude_globa: defaults to None
    :type excludes: list, optional
    """
    model_root = os.path.abspath(model_root)
    _pack_check(model_root)

    if tar_file and (tar_file.find("/") >= 0 or tar_file.find("\\") >= 0):
        raise Exception("tar file must be a file name")

    if not tar_file:
        tarfile_name = "upload.tar.gz"
    elif tar_file.endswith(".tar.gz"):
        tarfile_name = tar_file
    else:
        tarfile_name = tar_file + ".tar.gz"

    # exclude tarfile_name
    excludes.append(tarfile_name)
    tar_file = os.path.join(model_root, tarfile_name)

    model_dir = os.path.dirname(model_root)
    collect_files = _gathering_directory(model_root, excludes, exclude_pattern)
    if dry:
        print('\n'.join([os.path.relpath(x, model_dir)
                         for x in collect_files]))
    else:
        with tarfile.open(tar_file, "w:gz") as gz:
            for x in collect_files:
                gz.add(x, os.path.relpath(x, model_dir), False)
        print("gz file: %s" % tar_file)
