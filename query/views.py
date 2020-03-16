from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponse, HttpResponseRedirect, Http404
from .models import QueryModel, Questions

# 问题在数据集中的起始序号
QUSETION_START_POS = 0

# 问题总数
QUSETION_NUM = 300

# 是否打乱问题顺序
QUESTION_SHUFFLE = True

# 数据集和结果保存路径
QUESTION_DATA = 'query/platform_data'
IMG_PATH = 'query/images/'
SAVE_PATH = 'query/results/'

all_questions = Questions(QUESTION_DATA, QUESTION_SHUFFLE)
model = QueryModel(QUSETION_START_POS, QUSETION_NUM, all_questions)

# homepage
def homepage(request):
    if request.POST.get('user_name'):
        environment = str(request.POST['environment'])
        user_name = request.POST['user_name']

        # 根据是否存在当前用户来定位问题
        if model.has_user(user_name):
            question_id = model.get_user_ques_id(user_name)
            return HttpResponseRedirect(reverse('query:questions', args=(question_id, user_name, environment)))
        else:
            model.add_new_user(user_name)
            return HttpResponseRedirect(reverse('query:questions', args=(0, user_name, environment)))
    else:
        return render(request, 'query/homepage.html')

# tips page
def tips(request, user_name):
    return render(request, 'query/tips.html', {'num': len(model), 'user_name': user_name})

# process function
def process_question_post(request, question_id, user_name, environment):

    if question_id < 0 or question_id > len(model):
        raise Http404("Question does not exist!")

    # grade为标注类别，1~8
    if request.POST.get('grade') != None:
        ans = int(request.POST.get('grade'))
        t1 = int(request.POST.get('time_s1'))
        t2 = int(request.POST.get('time_s2'))
        model.set_ans(user_name, question_id-1, ans, t1, t2)

    # 返回下一个问题的名字，图片文件名，图片描述
    if question_id != len(model):
        query, intent, img1, img2, img3 = model.get_question(question_id)
        content = {
            'query': query,
            'intent': intent,
            'img1': IMG_PATH + img1,
            'img2': IMG_PATH + img2,
            'img3': IMG_PATH + img3,
        }
        content['question_id'] = question_id + 1
        content['user_name'] = user_name
        content['environment'] = environment
        return content
    else:
        return None

def questions(request, question_id, user_name, environment):
    content = process_question_post(request, question_id, user_name, environment)
    if content == None:
        model.save(user_name, environment, SAVE_PATH)
        return HttpResponseRedirect(reverse('query:thanks'))
    else:
        return render(request, 'query/one_picture.html', content)

# final page
def thanks(request):
    return render(request, 'query/thanks.html', {})


