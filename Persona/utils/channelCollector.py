import time
import requests
from dotenv import load_dotenv

load_dotenv()

import os

client_id = os.getenv('TWITCH_API_ID')
client_secret = os.getenv('TWITCH_API_SECRET')

class Channel:
    def __init__(self, id, login_name, channel_name, language, last_game_name, last_game_id, stream_title, stream_tags, classification_labels, is_branded_content):
        self.id = id
        self.login_name = login_name
        self.channel_name = channel_name
        self.language = language
        self.last_game_name = last_game_name
        self.last_game_id = last_game_id
        self.stream_title = stream_title
        self.stream_tags = stream_tags
        self.classification_labels = classification_labels
        self.is_branded_content = is_branded_content

def retry_on_exception(max_retries=3, delay=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Exception occurred: {e}. Retrying {attempts + 1}/{max_retries}...")
                    attempts += 1
                    time.sleep(delay)
            raise Exception(f"Failed after {max_retries} retries")
        return wrapper
    return decorator


def get_access_token(client_id, client_secret):

    try:
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, params=params)
        data = response.json()
        return data.get('access_token')
    except Exception as e:
        print(f"Failed to get access token: {e}")
        return None


def twitchApiRequestBase(endpoint, params=None):
    try:
        base_url = 'https://api.twitch.tv/helix/'
        headers = {
            'Client-ID': client_id,
            'Authorization': f'Bearer {get_access_token(client_id, client_secret)}'
        }
        response = requests.get(base_url + endpoint, headers=headers, params=params)
        return response.json()
    except Exception as e:
        print(f"Failed to make request: {e}")
        return None
    
def searchChannels(query, live_only, first=1):
    endpoint = 'search/channels'
    params = {'query': query, 'live_only': live_only, 'first': first}
    response = twitchApiRequestBase(endpoint, params)
    if response['data']:
        channel_id = response['data'][0]['id']
        login = response['data'][0]['broadcaster_login']
        print(f"Channel found: {login} with ID: {channel_id}")
        return channel_id
    else:
        raise Exception("No channels found")

def getChannelInfo(broadcasterName):
    try:
        broadcaster_id = searchChannels(broadcasterName, False) 
        endpoint = 'channels'
        params = {'broadcaster_id': broadcaster_id}
        response = twitchApiRequestBase(endpoint, params)
        print(response)
        if response['data']:
            channel_info = response['data'][0]
            newChannel = Channel(channel_info['broadcaster_id'], channel_info['broadcaster_login'], channel_info['broadcaster_name'],
                                channel_info['broadcaster_language'], channel_info['game_name'], channel_info['game_id'],
                                channel_info['title'], channel_info['tags'], channel_info['content_classification_labels'],
                                channel_info['is_branded_content'])
            print(newChannel.channel_name, newChannel.stream_tags, newChannel.classification_labels, newChannel.is_branded_content)
            return newChannel
        else:
            print("No channel info found")
            raise Exception("No channel info found")
    except Exception as e:
        print(f"Failed to get channel info: {e}")
        return None