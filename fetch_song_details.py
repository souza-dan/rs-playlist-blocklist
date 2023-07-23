import json
import os
import time
import urllib.parse
import requests

def search_song(song):
    # Encode the line for use in a URL
    encoded_line = urllib.parse.quote(song)
    url = f'https://rsplaylist.com/api/search.php?search={encoded_line}'
    print(f'Making request: {url}')
    response = requests.get(url)
    data = response.json()
    return data

def remove_invalid_chars(filename, translation_table=str.maketrans('', '', '<>:"/\\|?*')):
    # Use a translation table that maps each invalid character for filenames to None
    # Use the translate method to remove the invalid characters
    return filename.translate(translation_table)

def save_data(line, data, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Save the data to a file
    valid = remove_invalid_chars(line)
    output_file = os.path.join(output_dir, f'{valid}.json')
    with open(output_file, 'w') as f:
        json.dump(data, f)

def load_data(line, output_dir):
    # Check if the data has already been saved to a file
    valid = remove_invalid_chars(line)
    output_file = os.path.join(output_dir, f'{valid}.json')
    if os.path.exists(output_file):
        print(f'Reading: {output_file}')
        with open(output_file, 'r') as f:
            data = json.load(f)
        return data
    return None

def process_line(line, output_file, sleepSeconds=10):
    # Check if the data has already been saved to a file
    data = load_data(line,output_file)
    if data is None:
        # Get the data from the RESTful endpoint
        data = search_song(line)
        save_data(line, data, output_file)
        time.sleep(sleepSeconds)
    return data

def load_config(config_file = 'config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def process_file(config):
    with open(config['songList'], 'r') as f:
        lines = f.readlines()
    total_lines = len(lines)
    for i, line in enumerate(lines):
        line = line.strip()
        print(f'Processing line {i+1} of {total_lines}: {line}')
        data = process_line(line, config['songsDirectory'], config['sleepSeconds'])
        print(f'Data: {data}')

if __name__ == '__main__':
    config = load_config()
    process_file(config)
