#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random
import traceback
import time
import sys


soc_dic = '/data/GooglePlus/Projects/reviewMining/data/soc-dic.txt'
graph_reci = 'jason_results/graph_filtered.txt'
rating = 'jason_results/rating_filtered.txt'
results = 'jason_results/randomModel.txt'
# results = 'randomModel.txt'
# soc_dic = 'soc-dic-min.txt'
# graph_reci = 'graph-reci-min.txt'
# rating = 'rating-min.txt'


num_key_error = 0
def buildIDMap():
    mapIDToGoogleID = {}
    for line in map(lambda x: x.strip(),
                    open(soc_dic
                    ).readlines()):
        line = line.split('[[[NeilZhenqiangGong]]]')
        mapIDToGoogleID[line[1]] = line[0]
    return mapIDToGoogleID



def countTotalNumberApps():
    apps = set()
    t1 = map(lambda x: x.strip(),
             open(rating
             ).readlines())
    users_app_list = {}
    global total_user
    total_user = 0
    for line in t1:
        total_user += 1
        line_decoded = json.loads(line)
        apps.update(list(line_decoded['apps']))
    return len(apps)

def popularityBasedRandomApp():
    return popularlist[random.randrange(len(popularlist))]

def build_app_id_map():
    global app_id_map
    app_id_map = {}
    t1 = map(lambda x: x.strip(), open(rating).readlines())
    for line in t1:
        apps = json.loads(line)['apps']
        for app in apps:
            app_id_map[app] = len(app_id_map)

def build_user_apps_map():
    global user_apps_map
    user_apps_map = {}
    t1 = map(lambda x: x.strip(), open(rating).readlines())
    for line in t1:
        line_decoded = json.loads(line)
        user_apps_map[line_decoded['id']] = []
        apps = json.loads(line)['apps']
        for app in apps:
            user_apps_map[line_decoded['id']] += [app_id_map[app]]

def buildAppPopularityList():
    global users_appCount_list
    users_appCount_list = {}
    t1 = map(lambda x: x.strip(), open(rating).readlines())
    for line in t1:
        apps = json.loads(line)['apps']
        for app in apps:
            users_appCount_list[app] = users_appCount_list.get(app, 0) + 1
    global popularlist
    popularlist = []
    for app in list(users_appCount_list):
        popularlist += [app_id_map[app]] * users_appCount_list[app]

def buildUserAppCountMap():
    users_appCount_map = {}
    for line in map(lambda x: x.strip(),open(rating).readlines()):
        line_decoded = json.loads(line)
        users_appCount_map[line_decoded['id']] = len(line_decoded['apps'])
    return users_appCount_map


def jaccard(x, y):
    try:
        num_same_apps = len(set(x).intersection(set(y)))
        num_total_apps = len(set(x).union(set(y)))
        return num_same_apps / num_total_apps
    except:
        return -1

def randomApp():
    return random.randrange(num_total_apps)

id_map = buildIDMap()
print("finished building id map")
num_total_apps = countTotalNumberApps() #good
users_appCount_map = buildUserAppCountMap() #good
print("finished building app count map")        
if sys.argv[1] == 'popular':
    print("building app id map")
    build_app_id_map()
    print("building popularity list")
    buildAppPopularityList()
    randomApp = lambda : popularityBasedRandomApp()
if sys.argv[1] == 'fixed_friends':
    print("building app id map")
    build_app_id_map()
    print("building user apps map")
    build_user_apps_map()
    print("build app popularity list")
    buildAppPopularityList()
    randomApp = lambda : popularityBasedRandomApp()

total_edges = 0

x_labels = ['0', '0-0.05', '0.05-0.1', '0.1-0.15', '0.15-0.2', '>0.2']

buckets = {}
for x in x_labels:
    buckets[x] = 0 

def randomApp():
    if sys.argv[1] == 'random':
        return random.randrange(num_total_apps)
    else:
        return popularityBasedRandomApp();


def random_user_apps_map():
    global random_user_apps_map
    random_user_apps_map = {}
    for user in list(users_appCount_map):
        app_count = users_appCount_map[user]
        def gen_random_app_list(app_count):
            app_list = []
            for i in range(app_count):
                app = randomApp()
                while (app in app_list):
                    app = randomApp()
                app_list += [app]
            return app_list
        random_user_apps_map[user] = gen_random_app_list(app_count)

print("generating random user-apps map")
random_user_apps_map()

print("computing jaccard scores")
user_count = 0
total_user = len(random_user_apps_map)
with open(graph_reci) as file:
    for line in file:
        user_count += 1
        # print(str(user_count))
        if (user_count == int(total_user / 10) * 1): print("10%")
        if (user_count == int(total_user / 10) * 2): print("20%")
        if (user_count == int(total_user / 10) * 3): print("30%")
        if (user_count == int(total_user / 10) * 4): print("40%")
        if (user_count == int(total_user / 10) * 5): print("50%")
        if (user_count == int(total_user / 10) * 6): print("60%")
        if (user_count == int(total_user / 10) * 7): print("70%")
        if (user_count == int(total_user / 10) * 8): print("80%")
        if (user_count == int(total_user / 10) * 9): print("90%")

        line = line.strip().split()

        self_id = id_map[line[0]]
        for i in range(4, int(line[2]) + 4):
            try:
                friend_id = id_map[line[i]]
                jaccard_score = -1
                if sys.argv[1] == 'fixed_friends':
                    jaccard_score = jaccard(random_user_apps_map[self_id], user_apps_map[friend_id])
                else:
                    jaccard_score = jaccard(random_user_apps_map[self_id], random_user_apps_map[friend_id])
                if jaccard_score != -1:
                    total_edges += 1
                    if jaccard_score == 0:
                        buckets['0'] += 1
                    elif jaccard_score < 0.05:
                        buckets['0-0.05'] += 1
                    elif jaccard_score < 0.1:
                        buckets['0.05-0.1'] += 1
                    elif jaccard_score < 0.15:
                        buckets['0.1-0.15'] += 1
                    elif jaccard_score < 0.2:
                        buckets['0.15-0.2'] += 1
                    else:
                        buckets['>0.2'] += 1
            except KeyError:
                num_key_error += 1
                pass
            except:
                traceback.print_exc()
                pass






with open(results, 'w') as the_file:
    for x in x_labels:
        the_file.write(str(buckets[x]) + '\n')
    the_file.write(str(total_edges))


            
