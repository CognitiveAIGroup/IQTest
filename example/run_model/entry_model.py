from iqtest import iqtest_base
import torch
import numpy as np

class IQTestModelSample(iqtest_base.IQTestModelBase):
    def pre_run(self):
        # setup your model here
        pass

    def solve(self, question):
        # please ignore hint field, it's only used for sample
        # question_id, answer_list
        return [question['id'], [1]]


class IQTestModelDiagramSample(iqtest_base.IQTestModelBase):
    def pre_run(self):
        # setup your model here
        pass

    def solve(self, question):
        # question_id, answer_list
        return [question['id'], [1]]


def get_model_object(category: str) -> object:
    """ model by category
    if don't support category, return None 

    :param category: test category 
    :type category: str
    :return: Model 
    :rtype: object
    """
    if category == 'seq':
        return IQTestModelSample()
    elif category == 'diagram':
        return IQTestModelDiagramSample()
    elif category == 'verbal':
        return None
    return None

def global_pre_run():
    """ global pre run function used to set up environment
    """
    device = torch.device("cuda:0")
    try:
        data = torch.tensor(np.random.rand(10), device=device)
        print(data)
    except:
        pass