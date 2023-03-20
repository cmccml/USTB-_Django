from django.shortcuts import render
from django.http import JsonResponse
import json
from django.db import connection
from get_infos.models import Problems
from get_infos.models import RepresentativeTags
from get_infos.models import ProblemsRepresentatives
from get_infos.models import Solutions
from get_infos.models import Tags
from get_infos.models import ProblemsRepresentatives
from django.http import HttpResponse

# Create your views here.

def search_prob(request):
    pro_id = request.GET.get('pro_id','')
    pro_id = '%' + pro_id + '%'
    pro_title = request.GET.get('pro_title','')
    pro_title = '%' + pro_title + '%'
    tag_tile = request.GET.get('tag',None)
    dif_down = request.GET.get('dif_down','0')
    dif_up = request.GET.get('dif_up','100000')
    ratio_down = request.GET.get('ratio_down','0')
    ratio_up = request.GET.get('ratio_up','1')
    sub_down = request.GET.get('sub_down','0')
    sub_up = request.GET.get('sub_up','100000000')
    ac_down = request.GET.get('ac_down','0')
    ac_up = request.GET.get('ac_up','100000000')
    # obj_rawqueryset = Problems.objects.raw("SELECT * FROM solutions,(SELECT * FROM problems WHERE id LIKE %s && title LIKE %s \
    #     && difficulty BETWEEN %s AND %s \
    #     && ac_ratio BETWEEN %s AND %s\
    #     && submitted BETWEEN %s AND %s\
    #     && accepted BETWEEN %s AND %s) AS PRO\
    #     WHERE PRO.id = Solutions.problem_id",[pro_id,pro_title,dif_down,dif_up,ratio_down,ratio_up,sub_down,sub_up,ac_down,ac_up])
    obj_rawqueryset = Problems.objects.raw("SELECT * FROM problems WHERE id LIKE %s && title LIKE %s \
        && difficulty BETWEEN %s AND %s \
        && ac_ratio BETWEEN %s AND %s\
        && submitted BETWEEN %s AND %s\
        && accepted BETWEEN %s AND %s",[pro_id,pro_title,dif_down,dif_up,ratio_down,ratio_up,sub_down,sub_up,ac_down,ac_up])    
    #print(obj_rawqueryset)
    json_data = {}
    data_list = []
    for obj in obj_rawqueryset:
        flag = 0  # 初值为0，表明这个题目的标签不符合搜索条件中的标签
        if (tag_tile == None) :
            flag = 1      #用户没有搜索条件中没有标签，那么这个题目肯定符合搜索条件
        data = {}     # 要在遍历里面创建字典用于存数据
        sol_list = []
        tag_list = []
        # sol_data = {}
        # tag_data = {}
        sol_rawqueryset = Solutions.objects.raw("SELECT * FROM solutions WHERE problem_id = %s",[obj.id])
        tag_rawqueryset = RepresentativeTags.objects.raw("SELECT * FROM representative_tags WHERE id IN\
            (SELECT representative_id FROM problems_representatives WHERE problem_id = %s)",[obj.id])
        #print(tag_rawqueryset)
        for sol in sol_rawqueryset:
            sol_data={}
            sol_data["title"] = sol.title
            sol_data["url"] = sol.url
            sol_list.append(sol_data)
        for tag in tag_rawqueryset:
            # tag_data={}
            # tag_data["name"] = tag.name
            if (not flag and tag_tile == tag.name):
                flag = 1
            tag_list.append(tag.name)
        if (not flag):
            continue
        data["id"] = obj.id
        data["title"] = obj.title
        data["submitted"] = obj.submitted
        data["accepted"] = obj.accepted
        data["ac_ratio"] = obj.ac_ratio
        data["url"] = obj.url
        data["difficulty"] = obj.difficulty
        # data["solutions"] = sol_data
        # data["tag"] = tag_data
        data["solutions"] = sol_list
        data["tag"] = tag_list
        data_list.append(data)
    json_data['ret'] = 0
    json_data['data'] = data_list
    return JsonResponse(json_data,json_dumps_params={"ensure_ascii":False})

def problem_stats(request):
    field = request.GET.get('field',None)
    interval = request.GET.get('interval',None)
    # obj_rawqueryset = Problems.objects.raw("SELECT COUNT(*) FROM PROBLEMS WHERE id LIKE 'CF' ")
    # print(obj_rawqueryset)
    json_data = {}
    data_list = []
    json_data['ret'] = 0 
    if field == 'tag':
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM Tags")
            num_set = cur.fetchone()
            cur.close()
        num = num_set[0]
        #print(num)
        for i in range(0,num):
            data = {}
            with connection.cursor() as cur:
                cur.execute("SELECT name FROM Tags LIMIT %s,1",[i])
                value_set = cur.fetchone()
            data['value'] = value_set[0]  #标签名
            with connection.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM problems_representatives WHERE representative_id=%s",[i])
                count_set = cur.fetchone()
            data['count'] = count_set[0]
            data_list.append(data)
    else:
        if field == 'ac_ratio':
            value_left = 1.0
            value_minn = 0.0
            interval = float(interval)
            value_right = value_left - interval
            print(value_left,value_right)
        else:
            with connection.cursor() as cur:
                print(field)
                # cur.execute("SELECT MAX(ac_ratio) FROM problems")
                # cur.execute("SELECT MAX(%s) FROM problems",[field])
                # cur.execute("SELECT %s FROM problems ORDER BY %s DESC LIMIT 1",[field,field])
                # # cur.execute("SELECT * FROM problems WHERE %s=0.0",[field])
                if (field == 'submitted'):
                    cur.execute("SELECT MAX(submitted) FROM problems")
                if (field == 'accepted'):
                    cur.execute("SELECT MAX(accepted) FROM problems")
                if (field == 'difficulty'):
                    cur.execute("SELECT MAX(difficulty) FROM problems")
                value_set = cur.fetchone()
                # print(value_set)
                value_maxn = int(value_set[0])  #该元素的最大值
            # with connection.cursor() as cur:
                # cur.execute("SELECT ac_ratio FROM problems WHERE %s = (SELECT MIN(%s) FROM problems)",[field,field])
                # value_set = cur.fetchone()
                if (field == 'submitted'):
                    cur.execute("SELECT MIN(submitted) FROM problems")
                if (field == 'accepted'):
                    cur.execute("SELECT MIN(accepted) FROM problems")
                if (field == 'difficulty'):
                    cur.execute("SELECT MIN(difficulty) FROM problems")
                value_set = cur.fetchone()
                # print(value_set)
                value_minn = int(value_set[0])  #该元素的最小值
            value_left = value_maxn   #区间两端的值
            interval = int(interval)
            value_right = value_left - interval
        # print(value_maxn,value_minn)
        while value_left > value_minn:
            # print(value_left,value_right)
            with connection.cursor() as cur:
                if (value_right == value_minn):   #如果已经到最小值了，就包括右端点统计
                #     cur.execute("SELECT COUNT(*) FROM problems WHERE %s <= %s && %s >= %s",[field,value_left,field,value_right])
                    if (field == 'submitted'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (submitted <= %s) && (submitted >= %s)",[value_left,value_right])
                    if (field == 'accepted'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (accepted <= %s) && (accepted >= %s)",[value_left,value_right])
                    if (field == 'difficulty'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (difficulty <= %s) && (difficulty >= %s)",[value_left,value_right])
                    if (field == 'ac_ratio'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (ac_ratio <= %s) && (ac_ratio >= %s)",[value_left,value_right])
                else :  #否则就不包括右端点统计
                    # cur.execute("SELECT COUNT(*) FROM problems WHERE (%s <= %s) && (%s >= %s)",(field,value_left,field,value_right))
                    if (field == 'submitted'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (submitted <= %s) && (submitted > %s)",[value_left,value_right])
                    if (field == 'accepted'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (accepted <= %s) && (accepted > %s)",[value_left,value_right])
                    if (field == 'difficulty'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (difficulty <= %s) && (difficulty > %s)",[value_left,value_right])
                    if (field == 'ac_ratio'):
                        cur.execute("SELECT COUNT(*) FROM problems WHERE (ac_ratio <= %s) && (ac_ratio >= %s)",[value_left,value_right])
                    # test = 10000
                    # teststr = "submitted"
                    # cur.execute("SELECT COUNT(*) FROM problems WHERE %s >= %s",[teststr,test])
                count_set = cur.fetchone()
            data={}
            data['value'] = str(value_left) + '~' + str(value_right)
            data['count'] = count_set[0]
            data_list.append(data)
            value_left = value_right
            value_right = max(round(value_left - interval,3),value_minn)
    json_data['ret'] = 0
    json_data['data'] = data_list
    return JsonResponse(json_data,json_dumps_params={"ensure_ascii":False})        

def add_tag(request):
    id = request.GET.get('id',None)
    name = request.GET.get('name',None)
    rep = request.GET.get('representative',None)
    # obj_rawqueryset = Problems.objects.raw("INSERT INTO Tags(id,name,representative) VALUES('%s,%s,%s')",[id,name,rep])
    with connection.cursor() as cur:
        cur.execute("INSERT INTO Tags(id,name,representative) VALUES('%s,%s,%s')",[id,name,rep])
