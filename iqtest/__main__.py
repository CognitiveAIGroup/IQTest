import os
import sys
import json
import argparse
from .pack_models import *
from .version import version_report


if __name__ == "__main__":
    version_report()
    parser = argparse.ArgumentParser("iqtest", description="help pack user model packages")
    parser.add_argument("--excludes", "-e", metavar="excludes", nargs="*",
                        default=["run_script.py", "upload.tar.gz", "__pycache__"])
    parser.add_argument("--exclude-pattern", "-p",
                        metavar="exclude_pattern", nargs="*", default=list())
    parser.add_argument("--dry", "-d", metavar="dry_run")
    parser.add_argument("path", metavar="model_path")
    parser.add_argument("tar_file", metavar="tar_file",
                        nargs='?', default=None)
    args = parser.parse_args()

    pack_models(args.path, args.tar_file, args.dry,
                args.excludes, args.exclude_pattern)
