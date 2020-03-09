class IQTestModelBase:
    def pre_run(self):
        """ run before solve
        setup your model in this function 
        """

    def solve(self, question):
        """ 
        :param question: question information 
        :type question: map 
        :return: (question id, choice no or text solve)
        :rtype: tuple or list
        """
        # return [question['id'], 1]
        raise Exception("unimplemented eval_question")


class IQTestEvalBase:
    def eval_questions(self, question_list):
        raise Exception("unimplemented eval_question")
        # return [[question['id'], 1] for question in question_list]


class IQTestEvalDefault(IQTestEvalBase):
    model_object = None

    def __init__(self, model_object):
        self.model_object = model_object

    def __eval_questions(self, question_list):
        # run pre_run to setup environment
        self.model_object.pre_run()

        solve_list = [None] * len(question_list)

        for no, q in enumerate(question_list):
            solve_list[no] = self.model_object.solve(q)

        return solve_list

    def eval_questions(self, question_list):
        """ prepare multi processing and other presetup steps for running models

        :param question_list:  
        :type question_list: list 
        :return: solve list, score 
        :rtype: tuple 
        """
        if len(question_list) == 0:
            return list()

        return self.__eval_questions(question_list)
