from apscheduler.schedulers.blocking import BlockingScheduler
from random import *
import json
import os.path


def some_job():
    print("Decorated job")
    # Pick a user count from 0 to 1000
    users_count = randint(0, 1000)

    # Pick a mode from the below list
    mode_list = ['VOD', 'Live']
    mode = choice(mode_list)

    # Pick a platform from the below list
    platform_list = ['TV', 'Mobile', 'Computer']
    platform = choice(platform_list)

    # Create a JSON Object from the random output
    data = {}
    data['platform'] = platform
    data['mode'] = mode
    data['users'] = users_count
    json_data = json.dumps(data)

    # Print the JSON object in console
    print(json_data)

    # Save the JSON object in the log file
    directory = 'D:/logs_folder/'
    file = os.path.join(directory, 'logs.json')
    print('file name ', file)

    save_file = open(file, "w")
    # json.dump(json_data, save_file)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    save_file.close()

    print('End')


# Scheduling every 5 minutes
scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', minutes=1)
scheduler.start()
