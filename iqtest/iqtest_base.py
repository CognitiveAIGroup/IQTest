import multiprocessing
import traceback


def _spawn_model(self, conn, question_list):
    try:
        self.set_override_multi_process()
        solve_list = self.eval_questions(question_list)
        result = (None, solve_list)
    except Exception:
        result = (traceback.format_exc(), list())
    conn.send(result)
    conn.close()


class IQTestModelBase(object):
    def pre_run(self):
        """ run before solve
        setup your model in this function 
        """
        pass

    def solve(self, question):
        """ 
        :param question: question information 
        :type question: map 
        :return: (question id, choice no or text solve)
        :rtype: tuple or list
        """
        # return [question['id'], 1]
        raise Exception("unimplemented eval_question")


class IQTestEvalBase(object):
    def eval_questions(self, question_list):
        raise Exception("unimplemented eval_question")
        # return [[question['id'], 1] for question in question_list]


class IQTestEvalDefault(IQTestEvalBase):
    model_object = IQTestEvalBase()
    override_multi_process = False

    def __init__(self, model_object, multi_process=True):
        self.no_multi_process = not multi_process
        self.model_object = model_object

    def __eval_questions_single_process(self, question_list):
        solve_list = [None] * len(question_list)
        self.model_object.pre_run()

        for no, q in enumerate(question_list):
            solve_list[no] = self.model_object.solve(q)

        return solve_list

    @staticmethod
    def __simple_deploy_policy(question_num):
        cpu_cores = multiprocessing.cpu_count()

        batch_size = int((question_num + cpu_cores - 1) / cpu_cores)
        batch_remainder = question_num % cpu_cores

        # if divided exactly, then full batch cores = cpu_cores
        full_batch_cores = batch_remainder if batch_remainder > 0 else cpu_cores

        # batch_size == 1 means question_num <= cpu_cores
        process_num = full_batch_cores if batch_size == 1 else cpu_cores
        return process_num, full_batch_cores, batch_size

    def __eval_questions_multi_process(self, question_list):
        process_num, full_batch_cores, batch_size = IQTestEvalDefault.__simple_deploy_policy(
            len(question_list))

        process_list = [None] * process_num
        parent_cons = [None] * process_num
        child_cons = [None] * process_num
        current_start = 0
        remainder_no = process_num - 1
        for i in range(process_num):
            if i < full_batch_cores:
                next_start = current_start + batch_size
            else:
                next_start = current_start + batch_size - 1

            parent_cons[i], child_cons[i] = multiprocessing.Pipe()
            process_name = "eval_solve#%d" % i
            p = multiprocessing.Process(name=process_name, target=_spawn_model, args=(
                self, child_cons[i], question_list[current_start:next_start]))
            p.start()
            current_start = next_start
            process_list[i] = p

        solve_list = list()

        error_msg = None
        for i in range(process_num):
            message, result = parent_cons[i].recv()
            if message is None:
                solve_list.extend(result)
            else:
                # error handling, throw exception after processing all processor
                if error_msg:
                    error_msg = "%s\n==================%s" % (
                        error_msg, message)
                else:
                    error_msg = message

        for i in range(process_num):
            process_list[i].join()

        if error_msg is not None:
            raise Exception(error_msg)

        return solve_list

    def set_override_multi_process(self):
        self.override_multi_process = True

    def eval_questions(self, question_list):
        """ prepare multi processing and other presetup steps for running models

        :param question_list:  
        :type question_list: list 
        :return: solve list, score 
        :rtype: tuple 
        """
        if len(question_list) == 0:
            return list()

        if self.override_multi_process or self.no_multi_process:
            solve_list = self.__eval_questions_single_process(question_list)
        else:
            multiprocessing.set_start_method('spawn', True)
            solve_list = self.__eval_questions_multi_process(question_list)

        return solve_list
