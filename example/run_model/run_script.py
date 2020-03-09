import os
import sys
from pprint import pprint

from iqtest import *

MODEL_ROOT = os.path.dirname(__file__)
SRC_DIR_ROOT = os.path.abspath(os.path.join(MODEL_ROOT, "../.."))
WORK_ROOT = os.path.abspath(os.path.join(MODEL_ROOT, ".."))
DATA_ROOT = os.path.join(SRC_DIR_ROOT, "data")
CONFIG_FILE = os.path.join(DATA_ROOT, "config.json")


def _mock_server_run():
    sys.argv = [sys.argv[0], "-s", "-c", CONFIG_FILE, '-w', WORK_ROOT, MODEL_ROOT]
    run_model.run()


def server_mode():
    """ server mode procedure into
    #
    # evaluation model (to run your model on test set)
    # analysis model (to collection results)
    the process is very similar in server
    """
    _mock_server_run()
    eval_result.run_analysis(DATA_ROOT, WORK_ROOT, DATA_ROOT)


def pack_model():
    """ pack model used for upload
    """
    pack_models.pack_models(os.path.dirname(__file__))


def client_mode():
    # disable multi processors run
    # output result directly
    sys.argv = [sys.argv[0], "-c", CONFIG_FILE,
                "--verbose", "--output", "-w", WORK_ROOT, MODEL_ROOT]
    pprint(run_model.run())


if __name__ == "__main__":
    # client mode
    client_mode()
    # # server mode
    # server_mode()
    # # pack model
    # # python -m iqtest run_eval [-e [exclude..]] [-p [pattern..]]
    # pack_model()
