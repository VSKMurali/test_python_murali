
from random import *
import json
import os.path

users_count = randint(1, 100)   # Pick a random number between 1 and 100.

mode_list = ['VOD', 'Live']
mode = choice(mode_list)

platform_list = ['TV','Mobile','Computer']
platform = choice(platform_list)

data={}
data['platform'] = platform
data['mode'] = mode
data['users'] = users_count
json_data = json.dumps(data)

print(json_data)

directory = 'D:/elk/logs_folder/'
file = os.path.join(directory,'test.json')
print('file name ',file)

save_file = open(file, "w")
#json.dump(json_data, save_file, indent = 6)
#save_file.close()

with open(file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
save_file.close()
print('end')
