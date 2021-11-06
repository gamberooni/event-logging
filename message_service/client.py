# this script makes POST requests to the '/messages' path of the message_service server 
# to publish messages to the 'message_topic' in kafka

import datetime
import requests
import json
import random
from time import sleep

import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import config

usernames = [
    "johndoe",
    "janedoe",
    "billyjean",
    "mikael94",
    "lilditto420",
    "charizard62",
    "barrenash",
    "muckzuckerbirb",
    "adoreyou",
    "sukunaforeva",
    "unmeiyokokonideyo",
    "umeboshidesu",
    "pinkblack",
    "elonmusker",
    "ultaman",
    "jeffnotbezos",
    "throwaway",
    "winniethepoof",
    "defonotspidey",
    "ohnonononono",
    "coffindance69",
    "thenoobhunter",
    "kevinheart<3",
    "agent470",
    "notyouraveragejoe",
    "nevergonna",
    "x996",
    "apeklejen",
    "overflowdesuka",
    "ackermannyyds",
    "86izgud",
    "jealuc"
]

# just lorem ipsum things
texts = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
    "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium",
    "totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo",
    "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit",
    "sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt",
    "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit",
    "sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem",
    "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam",
    "nisi ut aliquid ex ea commodi consequatur?",
    "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur",
    "vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
    "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos",
    "dolores et quas molestias excepturi sint occaecati cupiditate non provident",
    "similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga",
    "Et harum quidem rerum facilis est et expedita distinctio",
    "Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus",
    "omnis voluptas assumenda est, omnis dolor repellendus",
    "Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudianda",
    "sint et molestiae non recusandae",
    "Itaque earum rerum hic tenetur a sapiente delectus",
    "ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat"
]

# select a random pair of sender and recipient from the usernames list
def select_sender_recipient(usernames):
    users = usernames # make a copy so that it doesn't affect the original list
    sender = random.choice(users)
    users.remove(sender) # ensure that the recipient is not the sender
    recipient = random.choice(users)
    return sender, recipient

def main():
    while True:
        sender, recipient = select_sender_recipient(usernames)
        message = {'sent_at': str(datetime.datetime.now()), 'sender': sender, 'text': random.choice(texts), 'recipient': recipient}
        requests.post(
            'http://localhost:8000/messages',
            data=json.dumps(message), # convert the message dict into a json string for the post request
        )
        print(f'Published message {message} to {config.topic}')
        sleep(random.random()) # sleep for a duration of randomly between 0 and 1 second

if __name__ == "__main__":
    main()
    