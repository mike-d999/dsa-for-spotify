# import the tekore library for working with the spotify web api, os library for os level functions
import os
import tekore

""" 
User authentication with the Spotify Web API.
"""
# client id and client secret values from spotify application
client_id = '<replace this with your spotify for developers app client id>'
client_secret = '<replace this with your spotify for developers app client secret>'

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

# if user_config file does not exist - sign in to spotify to get the initial user token and paste the redirect URL into the
# terminal - the program will save a user_config file so you don't need to sign back into spotify again.
else:
    user_token = tekore.prompt_for_user_token(client_id, client_secret, redirect_uri, scope=tekore.scope.every)
    user_config = (client_id, client_secret, redirect_uri, user_token.refresh_token) 
    tekore.config_to_file('user_config.cfg', user_config)

# replace the app token with the user token for access to the user's playlists and such
spotify.token = user_token

""" 
Retrieve data from a playlist given a playlist ID.
"""

# input a playlist of your choice by pasting the URL here
playlist_id = input("Enter a Spotify playlist ID: ")
playlist = spotify.playlist(playlist_id)

# retrieve track names, artists, albums data
track_names = spotify.playlist_items(playlist_id, fields='tracks.items(track(name))')
artists = spotify.playlist_items(playlist_id, fields='tracks.items(track(artists(name)))')
albums = spotify.playlist_items(playlist_id, fields='tracks.items(track(album(name)))')