"""Official script for IQTest version 0.1.

Provide basic functionality for IQTest.
Inheritate IQTestModelBase and override solve method to provide prediction.
Provide get_model_object and return the customized instance of IQTestModelBase.
Read README.md for more details.
"""
import os
import sys
import importlib
import argparse
import json
import stat
from .iqtest_base import *
from .eval_result import analysis_data
from .utils import *
from .version import version_report, version_check, update_local_data_version
import traceback


def _log(*args, **kwargs):
    pass


def _parse_arguments():
    parser = argparse.ArgumentParser("")

    parser.add_argument('--config', '-c', metavar='suite_config',
                        default="config.json", help="test suites config")
    parser.add_argument('--server', '-s', action='store_true',
                        default=False, help='[server mode]')
    parser.add_argument('--output', '-o', action='store_true', default=False,
                        help="output predicate result to output.answer.json, [server mode] overrides this flag to true")
    parser.add_argument('--answer-root', '-a', default=None,
                        help="dir for answers, only work when [server mode] is False")
    parser.add_argument('--work-root', '-w', default=None,
                        help="output dir default is getcwd")
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    parser.add_argument('model_root', help="model dir")
    return parser.parse_args()


def _run_suite_eval(eval_object, test_suite_file):
    with open(test_suite_file, "r", encoding="utf-8") as fh:
        question_list = json.load(fh)
    return eval_object.eval_questions(question_list)


@safe_one_retval_wrapper
def run_eval(eval_obj, data_root, test_collection):
    predict_suites = {}
    for suite in test_collection:
        suite_file = os.path.join(data_root, suite + ".json")
        solve_list = _run_suite_eval(eval_obj, suite_file)
        predict_suites[suite] = solve_list
    return predict_suites


def _load_eval_objects(entry_config, suites_config):
    # load model entry by model config setting
    with open(entry_config, "r", encoding="utf-8") as fh:
        model_entry_def = json.load(fh)["model"]
    model_entry = importlib.import_module(model_entry_def)

    symbols = dir(model_entry)
    # get eval_object_map
    # get_model_object has higher priority
    eval_object_map = {}
    if "get_model_object" in symbols:
        for kind in suites_config:
            model = model_entry.get_model_object(kind)
            eval_object_map[kind] = IQTestEvalDefault(model) if model else None
    elif "get_eval_cls" in symbols:
        for kind in suites_config:
            eval_object_map[kind] = model_entry.get_eval_cls(kind)
    else:
        raise Exception(
            'no "def get_model_object(category: str) ->object:" or "def get_eval_cls(category: str) -> object:" found')

    global_pre_run = model_entry.global_pre_run if 'global_pre_run' in symbols else None
    return eval_object_map, global_pre_run


def _verbose_data_models(eval_object_map):
    for k, v in eval_object_map.items():
        if v.__class__ == IQTestEvalDefault:
            _log("%s: %s" % (k, v.model_object.__class__.__name__))
        else:
            _log("%s: %s" % (k, v.__class__.__name__))


def unsafe_run():
    arguments = _parse_arguments()
    if not arguments.server:
        version_report()
        version_check()

    # setup verbose
    if arguments.verbose:
        global _log
        _log = print

    # setup arguments
    _log("========== setup config =============")
    config = os.path.abspath(arguments.config)
    server_mode = arguments.server

    data_root = os.path.dirname(config)

    if server_mode:
        answer_root = None
        output = True
    else:
        answer_root = os.path.abspath(data_root if arguments.answer_root is None else arguments.answer_root)
        output = arguments.output

    if arguments.work_root:
        os.chdir(arguments.work_root)

    work_root = os.path.abspath(os.getcwd())
    model_root = os.path.abspath(arguments.model_root)
    entry_config = os.path.join(model_root, "entry.json")

    _log("========== loading config =============")
    _log("data root:%s" % data_root)
    _log("work root:%s" % work_root)
    _log("model root:%s" % model_root)
    _log("entry config:%s" % entry_config)
    _log("suite config:%s" % config)

    # add model root to sys
    if not os.path.exists(work_root):
        os.makedirs(work_root)
    sys.path.insert(0, model_root)

    with open(config, "r", encoding="utf-8") as fh:
        data_config = json.load(fh)
    suites_config = data_config["test_suites"]
    data_version = data_config.get('version', '0.1.0.0')
    if not arguments.server:
        update_local_data_version(data_version)

    # load eval object
    _log("========== loading eval models =============")
    eval_object_map, global_pre_run = _load_eval_objects(entry_config, suites_config)

    _verbose_data_models(eval_object_map)

    def get_solve_result(predict_suites=None, message=None):
        if message is not None:
            return {"pass": 0, "predict_suites": predict_suites, "message": message}
        elif predict_suites is not None:
            return {"pass": 1, "predict_suites": predict_suites, "message": None}

        return {"pass": -1, "predict_suites": None, "message": None}

    _log("========== starting pre evaluation =============")
    solve_results = dict()
    pre_run_success = True
    try:
        if global_pre_run:
            global_pre_run()
    except:
        pre_run_success = False
        message = traceback.format_exc()
        for kind, suite_collection in suites_config.items():
            solve_results[kind] = get_solve_result(message=message)

    _log("========== starting evaluation =============")
    # run eval

    if pre_run_success:
        for kind, suite_collection in suites_config.items():
            _log("---------- evaluate %s ----------" % kind)
            if not suite_collection:
                # skip empty test suite collection
                continue

            eval_object = eval_object_map[kind]
            if eval_object:
                msg, predict = run_eval(eval_object, data_root, suite_collection)
                solve_results[kind] = get_solve_result(predict, msg)
            else:
                # no model
                solve_results[kind] = get_solve_result()

    _log("========== starting analysis =============")
    if output:
        # output result, for user to debug
        out_file = os.path.join(work_root, "output.answer.json")
        with open(out_file, "w", encoding="utf-8") as fh:
            json.dump(solve_results, fh, ensure_ascii=False)

    analysis_result = dict()
    if not server_mode:
        for kind, result in solve_results.items():
            analysis_result[kind] = analysis_data(answer_root, kind, result)

    # server mode doesn't do analysis
    return analysis_result


@safe_one_retval_wrapper
def run():
    return unsafe_run()
