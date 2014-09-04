import json
import math

soc_dic = '/data/GooglePlus/Projects/reviewMining/data/soc-dic.txt'
graph_reci = '/data/GooglePlus/Projects/reviewMining/data/graph-reci.txt'
rating = '/data/GooglePlus/Projects/reviewMining/data/rating.txt'
results = 'jason_results/randomModel.txt'
# results = 'randomModel.txt'
# soc_dic = 'soc-dic-min.txt'
# graph_reci = 'graph-reci-min.txt'
# rating = 'rating-min.txt'

"""computes the jaccard coefficients of two users represented in json formats"""
num_neg = 0
def jaccard(x, y):
	try:
		x_app_list = list(users_app_list[x])
		y_app_list = list(users_app_list[y])
		num_same_apps = len(set(x_app_list).intersection(set(y_app_list)))
		num_total_apps = len(set(x_app_list).union(set(y_app_list)))
		return num_same_apps / num_total_apps
	except:
		global num_neg
		num_neg += 1
		return -1

def buildIDMap():
	mapIDToGoogleID = {}
	for line in map(lambda x: x.strip(), open(soc_dic).readlines()):
		line = line.split("[[[NeilZhenqiangGong]]]")
		mapIDToGoogleID[line[1]] = line[0]
	return mapIDToGoogleID

def buildUserAppList():
	users_app_list = {}
	for line in map(lambda x: x.strip(), open(rating).readlines()):
		line_decoded = json.loads(line)
		users_app_list[line_decoded["id"]] = line_decoded["apps"]
	return users_app_list



# x = '{"apps": {"apps/details?id=com.touchtype.swiftkey": [-1, 1, 0], "apps/details?id=com.inxile.BardTale": [-1, 1, "1.99"], "apps/details?id=panorama.activity": [-1, 1, 0]}, "id": "107247689168467263487", "name": "Francisco Mu\u00f1oz Larreta"}'
# y = '{"apps": {"apps/details?id=com.snp": [-1, 1, 0]}, "id": "105815514482120589317", "name": "Jacky Lai"}'
# jaccard(x,y)

x_labels = ['0', '0-0.05', '0.05-0.1', '0.1-0.15', '0.15-0.2', '>0.2']


buckets = {}
buckets['0'] = 0
buckets['0-0.05'] = 0
buckets['0.05-0.1'] = 0
buckets['0.1-0.15'] = 0
buckets['0.15-0.2'] = 0
buckets['>0.2'] = 0

users_friend_list = map(lambda x: x.strip(), open(graph_reci).readlines())
users_app_list = buildUserAppList()
# print(users_app_list)
id_map = buildIDMap()
# print(id_map)
total_edges = 0

for user_friend_list in users_friend_list:
	user_friend_list = user_friend_list.split()
	friendCount = user_friend_list[2]

	user = id_map[user_friend_list[0]]
	for i in range(4, 4 + int(friendCount)):
		friend = id_map[user_friend_list[i]]
		jaccard_score = jaccard(user, friend)
		# print(jaccard_score)
		if (jaccard_score != -1):
			total_edges += 1
			if (jaccard_score == 0):
				buckets['0'] += 1
			elif (jaccard_score < 0.05):
				buckets['0-0.05'] += 1
			elif (jaccard_score < 0.1):
				buckets['0.05-0.1'] += 1
			elif (jaccard_score < 0.15):
				buckets['0.1-0.15'] += 1
			elif (jaccard_score < 0.2):
				buckets['0.15-0.2'] += 1
			else:
				buckets['>0.2'] += 1

with open(results, 'w') as the_file:
    for x in x_labels:
        the_file.write(str(buckets[x]) + '\n')
    the_file.write(str(total_edges))





