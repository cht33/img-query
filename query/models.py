from django.db import models
import random
import os

class Questions:
    '''
    读取所有问题的类

    '''
    def __init__(self, fileuser_id, QUESTION_SHUFFLE):
        with open(fileuser_id, 'r', encoding='utf8') as f:
            questions = f.readlines()
            questions = [t.strip().split() for t in questions]
            self.questions = questions
            self.question_shuffle = QUESTION_SHUFFLE

    # 返回从开始位置往后的num个问题及问题序号
    def get_questions(self, start_pos, num):
        end_pos = min(start_pos + num, len(self.questions))
        questions_id = list(range(start_pos, end_pos))
        if self.question_shuffle:
            random.shuffle(questions_id)
        questions = [self.questions[i] for i in questions_id]
        return questions_id, questions

class QueryModel:
    '''
    questions_id 记录问卷的所有问题的id
    questions 记录问卷的所有问题的内容
    user_data 记录所有用户的问卷结果和当前问题序号
             --user_data[user_id]['ans_list'] 结果列表
             --user_data[user_id]['curr_id'] 当前问题序号
    '''
    def __init__(self, start_pos=0, num=0, all_questions=None):
        self.questions_id = []
        self.questions = []
        self.user_data = {}
        if all_questions != None:
            self.reset_questions(start_pos, num, all_questions)

    # 返回问卷中第index个问题
    def get_question(self, index):
        if index >= 0 and index < len(self.questions):
            return self.questions[index]
        else:
            return None

    # 重置问题集
    def reset_questions(self, start_pos, num, all_questions):
        self.questions_id, self.questions = all_questions.get_questions(start_pos, num)

    # 判断用户是否已存在
    def has_user(self, user_id):
        return self.user_data.get(user_id, None) != None

    # 返回已存在用户当前的问题序号
    def get_user_ques_id(self, user_id):
        return self.user_data[user_id]['curr_id']

    # 添加新用户，问卷结果初始值为-1，表示该问题未被回答
    def add_new_user(self, user_id):
        self.user_data[user_id] = {}
        self.user_data[user_id]['ans_list'] = [-1] * len(self.questions)
        self.user_data[user_id]['time_s1'] = [-1] * len(self.questions)
        self.user_data[user_id]['time_s2'] = [-1] * len(self.questions)
        self.user_data[user_id]['curr_id'] = 0

    # 保存某个用户第index个问题的答案和当前问题序号以及花费时间
    def set_ans(self, user_id, index, ans, t1, t2):
        self.user_data[user_id]['ans_list'][index] = ans
        self.user_data[user_id]['time_s1'][index] = t1
        self.user_data[user_id]['time_s2'][index] = t2
        self.user_data[user_id]['curr_id'] = index + 1

    # 返回问题总数
    def __len__(self):
        return len(self.questions)

    # 将问卷结果保存至本地文件
    def save(self, user_id, filepath=None):
        s = ''
        ans_list = self.user_data[user_id]['ans_list']
        t1 = self.user_data[user_id]['time_s1']
        t2 = self.user_data[user_id]['time_s2']
        for i in range(0, len(self.questions)):
            s += '{}\t{}\t{}\t{}\n'.format(self.questions_id[i], t1[i], t2[i], ans_list[i])
        if filepath == None:
            print(s)
        else:
            filename = user_id + '.txt'

            # 判断是否已保存该用户的数据，避免重复保存
            for root, dirs, files in os.walk(filepath):
                if filename in files: return

            filename = filepath + filename
            with open(filename, 'a', encoding='utf8') as fout:
                print(s, file=fout)

    # 仅测试使用
    def get_all(self):
        return self.user_data, self.questions_id, self.questions



# unit test
if __name__ == '__main__':
    all_questions = Questions(fileuser_id='test_data_1', QUESTION_SHUFFLE=False)
    num = 1
    m = QueryModel()
    m.reset_questions(start_pos=0, num=num, all_questions=all_questions)
    print('size: {}'.format(len(m)))
    print(m.has_user('aaa'))
    m.add_new_user('aaa')
    print(m.has_user('aaa'))
    m.add_new_user('bbb')
    for i in range(num):
        m.set_ans('aaa', i, 35, 233, 2333)

    user_data, questions_id, questions = m.get_all()
    print(user_data)
    print(questions_id)
    print(questions)

    m.save('aaa', filepath='results/')
    m.save('bbb')
