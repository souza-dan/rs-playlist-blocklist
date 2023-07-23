# rs-playlist-blocklist
 Helper scripts for adding songs to the [RS Playlist](https://rsplaylist.com/) blocklist.

# Configuration
The program reads its configuration from a JSON file named `config.json`. This file should contain the following options:

songsDirectory: The path to the directory containing the JSON files with song information.
blockDirectory: The path to the directory where the output files will be saved.
sessionId: The session ID to use for the GET requests. Login to https://rsplaylist.com/ and use your browswer's network tools to inspect the requests after you login. Check for what "PHPSESSID" is set to in your session cookies.
sleepSeconds: The number of seconds to sleep between requests.

Here’s an example config.json file:
```
{
    "songsDirectory": "songs",
    "blockDirectory": "blocked",
    "sessionId": "12345",
    "sleepSeconds": 10
}
```

# Usage
To use this program, make sure you have Python 3 installed and the required libraries (glob, json, os, requests, time, and urllib.parse) are available. Run `pip install -r requirements.txt` to install the required libraries.

1. Create a newline separated list of songs you would like to add to the block list. See rocksmithdlc.txt for an example.
2. Create a config.json file with your configuration options (see above). Make sure to login to [rs-playlist](https://rsplaylist.com/) to set the `sessionId` and set `songList` to the file created above.
3. Run the fetch script using the following command:
```
python fetch-song-details.py
```
This will fill the `songsDirectory` with song metadata to add to the blocklist.
4. Run the block program to add the songs in `songsDirectory` to your block list:
```
python block_songs.py
```

# License
This project is licensed under the terms of the MIT license.

