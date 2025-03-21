#!/usr/bin/env python3

from systemd import journal
from time import sleep
import requests

notify = {
    'service': 'https://ntfy.sh/',
    'topic': '' #should probably be a random generated token as technichly a password if info is sensitive.
}

# Add more triggers if needed
# syntax 'text to search for':'Message to send'
triggerText = {
    'find1':'send1',
    'find2':'send2',
    'find3':'send3'
}


def main():
    j = journal.Reader()
    j.seek_tail()
    j.get_previous()
    if (notify['topic'] == ''):
        print ('notify[topic] is empty, please set a topic in the script')
        return
    while True:
        event = j.wait(-1)
        if event == journal.APPEND:
            for entry in j:
                searchTrigger(entry['MESSAGE'])

def sendNotification(sendMessage):
    requests.post(notify['service'] + notify['topic'],
                data=sendMessage,
                )

def searchTrigger(logEntry):
    for triggerKey, triggerValue in triggerText.items() :
        if (logEntry.find(triggerKey) != -1):
            sendNotification(triggerValue)

if __name__ == '__main__':
    main()