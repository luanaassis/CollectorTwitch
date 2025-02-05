import time
import requests

client_id = 'f3etkvwrpvxhymoohuxbjxraeg7f0o'
client_secret = 'xv7chjlx0eprbzcazuvyopenj3awhx'

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

@retry_on_exception()
def get_access_token(client_id, client_secret):


    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data.get('access_token')

@retry_on_exception()
def twitchApiRequestBase(endpoint, params=None):
    base_url = 'https://api.twitch.tv/helix/'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {get_access_token(client_id, client_secret)}'
    }
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    return response.json()

@retry_on_exception()
def getChannelInfo(broadcaster_id):
    endpoint = 'channels'
    params = {'broadcaster_id': broadcaster_id}
    response = twitchApiRequestBase(endpoint, params)
    if response['data']:
        channel_info = response['data'][0]
        newChannel = Channel(channel_info['broadcaster_id'], channel_info['broadcaster_login'], channel_info['broadcaster_name'],
                             channel_info['broadcaster_language'], channel_info['game_name'], channel_info['game_id'],
                             channel_info['title'], channel_info['tags'], channel_info['content_classification_labels'],
                             channel_info['is_branded_content'])
        print(newChannel.channel_name, newChannel.stream_tags, newChannel.classification_labels, newChannel.is_branded_content)
        return newChannel
    else:
        raise Exception("No channel info found")