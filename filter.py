import json

# rating_filename = "rating-min.txt"
# graph_reci_filename = "graph-reci-min.txt"
rating_filename = "/data/GooglePlus/Projects/reviewMining/data/rating.txt"
graph_reci_filename = "/data/GooglePlus/Projects/reviewMining/data/graph-reci.txt"
soc_dic_filename = "/data/GooglePlus/Projects/reviewMining/data/soc-dic.txt"
rating_filtered_filename = "jason_results/rating_filtered.txt"
graph_reci_filtered_filename = "jason_results/graph_filtered.txt"

#construct file writer
rating_file_writer = open(rating_filtered_filename,'w')
graph_reci_file_writer = open(graph_reci_filtered_filename,'w')

def build_id_map():
    global id_map
    id_map = {}
    for line in map(lambda x: x.strip(),open(soc_dic_filename).readlines()):
        line = line.split('[[[NeilZhenqiangGong]]]')
        id_map[line[1]] = line[0]

build_id_map()
print("finished building id map")

def build_user_ratings_map():
    global users_ratings_map
    users_ratings_map = {}
    for line in map(lambda x: x.strip(), open(rating_filename).readlines()):
        line_decoded = json.loads(line)
        users_ratings_map[line_decoded['id']] = line

build_user_ratings_map()
print("finished building user ratings map")

def exist_in_rating(user):
    return id_map[user] in users_ratings_map

user_count = 0
total_user = len(users_ratings_map)

for line in map(lambda x: x.strip(), open(graph_reci_filename).readlines()):
    user_count += 1
    if (user_count == int(total_user / 10) * 1):
        print("10%")
    if (user_count == int(total_user / 10) * 2):
        print("20%")
    if (user_count == int(total_user / 10) * 3):
        print("30%")
    if (user_count == int(total_user / 10) * 4):
        print("40%")
    if (user_count == int(total_user / 10) * 5):
        print("50%")
    if (user_count == int(total_user / 10) * 6):
        print("60%")
    if (user_count == int(total_user / 10) * 7):
        print("70%")
    if (user_count == int(total_user / 10) * 8):
        print("80%")
    if (user_count == int(total_user / 10) * 9):
        print("90%")
    line_parameter_list = line.split()
    friend_count = int(line_parameter_list[2])
    new_friend_list = []
    for i in range(4, 4 + friend_count):
        # print(line_parameter_list[i])
        if (exist_in_rating(line_parameter_list[i])):
            new_friend_list += [line_parameter_list[i]]
    # print(new_friend_list)
    def filtered_graph_reci_line(line_parameter_list, new_friend_list):
        line = str(line_parameter_list[0]) + ' ' + str(line_parameter_list[1]) + ' ' + str(len(new_friend_list)) + ' ' + str(line_parameter_list[3])
        for x in new_friend_list:
            line += ' ' + x
        return line + '\n'
    if (len(new_friend_list) > 0):
        graph_reci_file_writer.write(filtered_graph_reci_line(line_parameter_list, new_friend_list))
        rating_file_writer.write(users_ratings_map[id_map[line_parameter_list[0]]] + '\n')

rating_file_writer.close()
graph_reci_file_writer.close()


