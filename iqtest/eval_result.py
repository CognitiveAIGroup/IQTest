import os
import json
from .utils import *


def _unique_predict(solve_list):
    valid_solve_list = filter(lambda x: x[0] is not None, solve_list)
    valid_solve_list = sorted(valid_solve_list, key=lambda x: x[0])
    unique_solve_list = list()
    current_no = -1
    for e in valid_solve_list:
        if current_no != e[0]:
            current_no = e[0]
            unique_solve_list.append(e)
    return unique_solve_list


@safe_one_retval_wrapper
def _analysis_data(answer_root, kind, result):
    if result["pass"] != 1:
        result["score"] = -1
        raise Exception(result['message'])

    predict_suites = result["predict_suites"]
    total = 0
    correct = 0

    # unique predict suites

    for suite in predict_suites:
        with open(os.path.join(answer_root, suite + ".answer.json"), "r", encoding="utf-8") as fh:
            answer_dict = json.load(fh)
        # get unique solve list by id (the first element)
        solve_list = _unique_predict(predict_suites[suite])

        total = total + len(answer_dict)

        for q in solve_list:
            if q[1] == answer_dict[str(q[0])]['answer']:
                correct = correct + 1
    total = total if total else 1
    return correct / total


def analysis_data(answer_root, kind, result):
    if result.get('pass') == -1:
        return {"pass": -1, "score": -1, "message": None}

    message, score = _analysis_data(answer_root, kind, result)
    if message is None:
        return {"pass": 1, "score": score, "message": message}

    return {"pass": 0, "score": -1, "message": message}


@safe_one_retval_wrapper
def _run_analysis(data_root, work_root, answer_root):
    with open(os.path.join(data_root, "config.json"), "r", encoding="utf-8") as fh:
        config = json.load(fh)
    predict_file = os.path.join(work_root, "output.answer.json")
    with open(predict_file, "r", encoding="utf-8") as fh:
        predict = json.load(fh)

    analysis_result = {}
    for kind, result in predict.items():
        analysis_result[kind] = analysis_data(answer_root, kind, result)
    path = os.path.join(work_root, "result.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(analysis_result, fh, ensure_ascii=False)
    return True


def run_analysis(data_root, work_root, answer_root):
    msg, code = _run_analysis(data_root, work_root, answer_root)
    result_file = os.path.join(work_root, "result.json")
    if msg is None:
        print("Succ:output to %s" % result_file)
    else:
        with open(result_file, "w", encoding="utf-8") as fh:
            fh.write(msg)

        print("Fail:output to %s" % result_file)
    return msg, code
