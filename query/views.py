from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponse, HttpResponseRedirect, Http404
from .models import QueryModel, Questions

# 问题在数据集中的起始序号
QUSETION_START_POS = 0

# 问题总数
QUSETION_NUM = 5

# 是否打乱问题顺序
QUESTION_SHUFFLE = False

# 数据集和结果保存路径
QUESTION_DATA = 'query/test_data'
SAVE_PATH = 'query/results/'

all_questions = Questions(QUESTION_DATA, QUESTION_SHUFFLE)
model = QueryModel(QUSETION_START_POS, QUSETION_NUM, all_questions)

# homepage
def homepage(request):
    if request.POST.get('user_name'):
        user_name = request.POST['user_name']

        # 根据是否存在当前用户来定位问题
        if model.has_user(user_name):
            question_id = model.get_user_ques_id(user_name)
            return HttpResponseRedirect(reverse('query:questions', args=(question_id, user_name,)))
        else:
            model.add_new_user(user_name)
            return HttpResponseRedirect(reverse('query:tips', args=(user_name,)))
    else:
        return render(request, 'query/homepage.html')

# tips page
def tips(request, user_name):
    return render(request, 'query/tips.html', {'num': len(model), 'user_name': user_name})

# process function
def process_question_post(request, question_id, user_name):
    if question_id < 0 or question_id > len(model):
        raise Http404("Question does not exist!")

    # score为单张图片标注分数
    if request.POST.get('score') != None:
        ans = int(request.POST.get('score'))
        time_cost = int(request.POST.get('time_cost'))
        model.set_ans(user_name, question_id-1, ans, time_cost)

    # 返回下一个问题的名字，图片文件名，图片描述
    if question_id != len(model):
        img_name, img1, des = model.get_question(question_id)
        img1 = 'query/images/' + img1 + '.jpg'
        content = {'img_name': img_name, 'img1': img1, 'des': des}
        content['question_id'] = question_id + 1
        content['user_name'] = user_name
        return content
    else:
        return None

def questions(request, question_id, user_name):
    content = process_question_post(request, question_id, user_name)
    if content == None:
        model.save(user_name, SAVE_PATH)
        return HttpResponseRedirect(reverse('query:thanks'))
    else:
        return render(request, 'query/one_picture.html', content)

# final page
def thanks(request):
    return render(request, 'query/thanks.html', {})


