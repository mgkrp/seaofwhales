import vk_api
import re
import string
import math

def main():

    login, password = 'your_login', 'your_password' #!!!!!!!!!!!!!!!!!!!!
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    tools = vk_api.VkTools(vk_session)

    stop_words = []
    f = open('1grams-3.txt',encoding='utf-8', mode='r')
    for i in range(100):
        line = f.readline().split("\t")
        stop_words.append(line[1][:-1])
    test_Bgroups = [-93711854,-109387848, -123869452, -58193491, -127224753, -108488701, -76624702, -131797206, -48055932, -123117893]
    test_Ggroups = [-15956248,-79916681,-100235553, -76982440, -312524, -34689126, -39009769, -33165854, -22798006, -43215063, -22822305, -56106344, -26669118, -8862419, -126514423, -106106922, -41781422]

    testfold = []
    testfoldClass = []
    result = []
    bad_count = 0
    good_count = 0
    total_count = 0
    bad_words = {}
    good_words = {}
    total_words = {}
    for group in test_Bgroups:
        print(group)
        try:
            wall = tools.get_all('wall.get', 100, {'owner_id': group})
        except:
            pass
        for item in wall['items']:
            foo = []
            bad_count += 1
            total_count += 1
            for word in item['text'].split():
                if word not in stop_words:
                    if word in total_words.keys():
                        total_words[word] += 1
                    else:
                        total_words[word] = 1
                    if word in bad_words.keys():
                        bad_words[word] += 1
                    else:
                        bad_words[word] = 1
                    foo.append(word.strip(string.punctuation).lower())
            testfold.append(foo)
            testfoldClass.append(1)
    for group in test_Ggroups:
        print(group)
        try:
            wall = tools.get_all('wall.get', 100, {'owner_id': group})
        except:
            pass
        for item in wall['items']:
            good_count += 1
            total_count += 1
            foo = []
            for word in item['text'].split():
				weight = 1
                if word in stop_words:
					weight = 0.2
				if word in total_words.keys():
					total_words[word] += 1
				else:
					total_words[word] = 1
				if word in good_words.keys():
					good_words[word] += 1
				else:
					good_words[word] = 1
				foo.append(word.strip(string.punctuation).lower())
            testfold.append(foo)
            testfoldClass.append(0)


    is_new = True
    all_groups = set()
    connections = []
    groups = tools.get_all('groups.get', 100, {'user_id': "389429030"})
    f = open("groups.txt", "w")
    f.writelines("groupid,badpostscount,goodpostscount"+"\n")
    for i in range(3):
        is_new = False
        current_newgroup = set()
        for group in groups['items']:
            print('Current group:', group)
            all_groups.add(group)
            goodposts_count = 0
            badposts_count = 0
            wall['items'] = []
            try:
                wall = tools.get_all('wall.get', 100, {'owner_id': -int(group)})
            except:
                pass
            for item in wall['items']:
                good_probability = math.log2(good_count / total_count)
                bad_probability = math.log2(bad_count / total_count)
                for word in item['text'].split():
					weight = 1
                    if word in stop_words:
						weight = 0.2
					if word in bad_words.keys():
						bad_probability = bad_probability + math.log2(bad_words[word] / bad_count)
					else:
						bad_probability = bad_probability - math.log2(bad_count)
					if word in good_words.keys():
						good_probability = good_probability + math.log2(good_words[word] / good_count)
					else:
						good_probability = good_probability - math.log2(good_count)

                if item['text'] != "":
                    if bad_probability > good_probability:
                        badposts_count += 1
                    else:
                        goodposts_count += 1
						
                new_groups = re.findall('\[club(.+?)\|', item['text'])
                for new_group in new_groups:
                    connections.append([group, new_group])
                    if new_group not in all_groups and new_group not in current_newgroup:
                        current_newgroup.add(new_group)
                        is_new = True
            badposts_count*=1.2
            if badposts_count <= goodposts_count:
                result.append([group, 0])
            else:
                result.append([group, 1])
            f.writelines(str(group)+","+ str(badposts_count)+","+ str(goodposts_count)+"\n")

        all_groups.union(current_newgroup)
        groups['items'] = current_newgroup
        print(current_newgroup)
    f = open("output.txt", "w")
    f.writelines("groupid,class"+"\n")
    for item in result:
        f.writelines(str(item[0])+","+str(item[1])+"\n")
    f = open("connections.txt", "w")
    f.writelines("groupid,groupid_connected"+"\n")
    for item in connections:
        f.writelines(str(item[0])+","+str(item[1])+"\n")


if __name__ == '__main__':
    main()