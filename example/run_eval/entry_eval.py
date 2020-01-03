from iqtest import iqtest_base
""" example for eval cooperates with model

1) IQTestEvalSeq uses IQTestModelSeq to solve question
2) IQTestEvalDiag raise exception test for exception handling
3) IQTestEvalVerbal now no test suite 

:raises Exception: test error 
"""


class IQTestEvalSeqSample(iqtest_base.IQTestEvalBase):
    def eval_questions(self, question_list):
        # full question list would be passed here
        return [[question['id'], [1]] for question in question_list]


class IQTestEvalDiagramSample(iqtest_base.IQTestEvalBase):
    def eval_questions(self, question_list):
        # full question list would be passed here
        raise Exception("test exception")


class IQTestEvalVerbalSample(iqtest_base.IQTestEvalBase):
    def eval_questions(self, question_list):
        # full question list would be passed here
        return [[question['id'], [2]] for question in question_list]


def get_eval_cls(category: str) -> object:
    """ optional, if ignore, IQTestEvalBase would be used

    :param category:
    :type category: str
    :return: [description]
    :rtype: object
    """
    if category == "seq":
        return IQTestEvalSeqSample()
    elif category == "diagram":
        return IQTestEvalDiagramSample()
    elif category == "verbal":
        return IQTestEvalVerbalSample()
    return None


def global_pre_run():
    """ global pre run function used to set up environment
    """