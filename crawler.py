import requests
import os
import json

try:
    GROUP_ID = os.environ['SMSGRUPP_GROUP_ID']
    TOKEN = os.environ['SMSGRUPP_TOKEN']
except KeyError:
    print('Environment variables not setup')
    exit(-1)

N_MESSAGES = int(os.environ.get('SMSGRUPP_BUFFER_SIZE', 4000))
BASE_URL = f'https://api.getsupertext.com/v1/conversations/{GROUP_ID}'


def check_ok(response, *_, **__):
    response.raise_for_status()


def get_messages(session, last_message_before=None):
    headers = {'Message-Count': str(N_MESSAGES)}
    if last_message_before is not None:
        headers['before'] = last_message_before
    return session.get(f'{BASE_URL}/messages', headers=headers).json()


def crawl_group():
    session = requests.Session()
    session.headers.update({
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Client-Token': 'web_v3',
        'Client-Version': '1',
        'Auth-Token': TOKEN,
    })
    session.hooks['response'].append(check_ok)

    group_info = session.get(BASE_URL).json()['conversation']

    print(f'Found conversation with {len(group_info["users"])} users and '
          f'{group_info["message_count"]} messages!')

    messages = []
    previous = None
    while (incoming := get_messages(session, previous))['messages']:
        messages.extend(incoming['messages'])
        previous = messages[-1]['message']['id']
        print(f'{len(messages)}/{group_info["message_count"]} downloaded')

    with open('messages.json', 'w', encoding='utf-8') as f:
        json.dump({'conversation': group_info, 'messages': messages},
                  f, indent=2, ensure_ascii=False)
    for user in group_info['users']:
        id_ = user['user']['id']
        nick = user['user']['nickname']
        user_messages = [m for m in messages if m['message']['user_id'] == id_]
        with open(f'messages_{nick}.json', 'w', encoding='utf-8') as f:
            json.dump(user_messages, f, indent=2, ensure_ascii=False)
        print(f'{nick} authored {len(user_messages)} messages')


if __name__ == '__main__':
    crawl_group()
