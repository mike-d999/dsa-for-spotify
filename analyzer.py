# import tekore for working with the spotify web api, os for os level functions
import os
import tekore

""" 
User authentication with the Spotify Web API.
"""
# open the app config file containing the client id and client secret and write them to a list
app_config_file = open('app_config.txt', 'r')
app_config = []

for eachLine in app_config_file:
    app_config.append(eachLine.strip())

# client id and client secret values from spotify application are populated in from the list
client_id = app_config[0]
client_secret = app_config[1]

# generate an app token using the client id and client secret values from the spotify application
app_token = tekore.request_client_token(client_id, client_secret)

# assign the generated app token to an object
spotify = tekore.Spotify(app_token)

# set the redirect uri to the default value
redirect_uri = 'https://example.com/callback'

# if user_config file already exists, just load the existing values and refresh the user token - no need for a full reauth.
if os.path.exists('user_config.cfg'):
    user_config = tekore.config_from_file('user_config.cfg', return_refresh=True)
    user_token = tekore.refresh_user_token(*user_config[:2], user_config[3])
    print()
    print("--------------------------------------------------------")
    print("Welcome back to the Duplicate Song Analyzer for Spotify!")
    print("--------------------------------------------------------")
    print()

# if user_config file does not exist - sign in to spotify to get the initial user token and paste the redirect URL into the
# terminal - the program will save a user_config file so you don't need to sign back into spotify again.
else:
    print()
    print("---------------------------------------------------")
    print("Welcome to the Duplicate Song Analyzer for Spotify!")
    print("---------------------------------------------------")
    print()
    print("Since this is your first time using the program, please authorize your account with Spotify to continue.")
    print("You will only have to do this once, as a file will be generated that saves your login information.")
    print("(Note: If you delete 'user_config.cfg', you'll have to go through this setup again.)")
    print()
    user_token = tekore.prompt_for_user_token(client_id, client_secret, redirect_uri, scope=tekore.scope.every)
    user_config = (client_id, client_secret, redirect_uri, user_token.refresh_token) 
    tekore.config_to_file('user_config.cfg', user_config)
    print()
    print("Authorization successful!")
    print()

# replace the app token with the user token for access to the user's playlists and such
spotify.token = user_token

""" 
Retrieve data from a playlist given a playlist ID.
"""
# input a playlist of your choice by pasting the URL here
playlist_id = input("Please enter a Spotify playlist ID: ")
playlist = spotify.playlist(playlist_id)
print()
print("Playlist found! Please wait while the program writes your playlist's song titles and artists to disk...")
print()

# create an index for iterating through track names and create a file for storing track names
current_index = 0
song_data = open('song_data.txt', 'w')

# iterate through the first 100 tracks and artists and write them to the song data file
while current_index < 100:
    try:
        song_data.write(spotify.playlist_items(playlist.id).items[current_index].track.name + " " + "- ")
        song_data.write(spotify.playlist_items(playlist.id).items[current_index].track.artists[0].name)
        song_data.write('\n')
        print("Wrote track name and artist data for song", current_index+1, "to disk.")
        current_index += 1
    except:
        song_data.close()
        break

with open('song_data.txt', 'r') as song_data:
    lines_list = song_data.readlines()