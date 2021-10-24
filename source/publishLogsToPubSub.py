"""
This script imports a function to 
generate fake user log data and then
publishes it to a pub/sub topic 
"""


from stream_logs import generate_log_line
import logging
from google.cloud import pubsub_v1
import random
import time
import configparser

import requests
import os
import time
import json
import configparser
from google.cloud import pubsub_v1

class Publish:
    def __init__(self, config):
        self.project_id = str(config['PROJECT']['PROJECT_ID'])
        self.topic_id = str(config['TOPIC']['TOPIC_ID'])
        self.api_url = str(config['API']['API_URL'])+str(config['API']['API_KEY'])
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(config['AUTH']['CRED_FILE'])

    def publish(self, message):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id,self.topic_id)
        data = message.encode('utf-8')
        return publisher.publish(topic_path, data = data)



    def callback(self, message_future):
        # When timeout is unspecified, the exception method waits indefinitely.
        if message_future.exception(timeout=30):
            print('Publishing message on {} threw an Exception {}.'.format(
                self.topic_id, message_future.exception()))
        else:
            print(message_future.result())


if __name__=='__main__':
    #read configuration file
    config = configparser.ConfigParser()
    config.read('utils/config.cfg')
    
    pub = Publish(config)

    while True:
        line = generate_log_line()
        print(line)
        message_future = pub.publish(line)
        message_future.add_done_callback(pub.callback)

        sleep_time = random.choice(range(1, 3, 1))
        time.sleep(sleep_time)