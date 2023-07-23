import glob
import json
import os
import requests
import time
import urllib.parse

def block_song(id, title, session_id):

    request_cookies = {
		"PHPSESSID": session_id
    }
    encoded_title = urllib.parse.quote(title)
    url = f'https://rsplaylist.com/ajax/update-settings.php?action=update-settings&blacklist-blacklisted_songs[{id}][song_id]={id}&blacklist-blacklisted_songs[{id}][song_title]={encoded_title}&channel=turtleverse64'
    response = requests.get(url, cookies=request_cookies)
    data = response.json()
    return data

def save_data(id, data, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Don't save the result if the query was not a success
    if data['result'] != 'Success':
        print(f'Not saving data because result was unsuccessful: {data["message"]}')
        return

    # Save the data to a file
    output_file = os.path.join(output_dir, f'{id}.json')
    with open(output_file, 'w') as f:
        json.dump(data, f)

def load_data(id, output_dir):
    # Check if the data has already been saved to a file
    output_file = os.path.join(output_dir, f'{id}.json')
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            data = json.load(f)
        # Don't load the result if the query was not a success
        if data['result'] != 'Success':
            print(f'Not returning saved data from {output_file} because result was unsuccessful: {data["message"]}')
            return None
        return data
    return None

def process_file(file, request_dir, session_id, sleep_seconds=10):
    with open(file, 'r') as f:
        data = json.load(f)
    id = data[0]['id']
    title = f'{data[0]["artist"]} - {data[0]["title"]}'
    # Check if the block request has already been saved to a file
    data = load_data(id, request_dir)
    if data is None:
        # Get the data from the RESTful endpoint
        data = block_song(id, title, session_id)
        save_data(id, data, request_dir)
        time.sleep(sleep_seconds)
    return data

def load_config(config_file = 'config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def main(config):
    files = glob.glob(os.path.join(config['songsDirectory'], '*.json'))
    total_files = len(files)
    for i, file in enumerate(files):
        print(f'Processing file {i+1} of {total_files}: {file}')
        data = process_file(file, config["blockDirectory"], config["sessionId"], config["sleepSeconds"])
        print(f'Data: {data}')

if __name__ == '__main__':
    config = load_config()
    main(config)
