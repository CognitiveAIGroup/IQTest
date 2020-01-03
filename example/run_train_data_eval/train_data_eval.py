from iqtest import iqtest_base
""" example for eval cooperates with model
Please download GoogleNews-vectors-negative300.bin and upload to ftp
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
        result_list = list()
        import gensim
        from scipy.spatial.distance import cosine as dist_cosine
        model = gensim.models.KeyedVectors.load_word2vec_format(
            './train_data/GoogleNews-vectors-negative300.bin', binary=True)
        for question in question_list:
            max_sim, curr_idx = 0, 0
            # if word not in model_vocabulary, return a fixed answer [1]
            if question['stem'] not in model:
                result_list.append([question['id'], [1]])
                continue
            flag = False
            for idx, answer in enumerate(question['options']):
                if answer in model:
                    flag = True
                else:
                    continue
                if not flag:
                    result_list.append([question['id'], [1]])
                sim = 1 - dist_cosine(model[question['stem']], model[answer])
                if sim > max_sim:
                    max_sim = sim
                    curr_idx = idx
            result_list.append([question['id'], [curr_idx+1]])

        return result_list


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
    # setup your model here
    print("loading content from ftp uploaded train data")
    with open("./train_data/user_train_data.bin", "r") as fh:
        print(fh.read())

