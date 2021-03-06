# import os for os level functions, sys for Python version checking, tekore for working with the spotify web api
import os
import sys
import tekore

def main():
    # check if the user has Python version 3.9 or higher installed - if not, do not allow the user to run the program
    if sys.version_info < (3,9):
        print("This program requires Python version 3.9 or higher. Please update your Python installation to use this program.")
        quit()

    """ 
    User authentication with the Spotify Web API.
    """
    # check if the app config file exists - do not allow the program to proceed if it doesn't
    try:
        # open the app config file containing the client id and client secret
        app_config_file = open('app_config.cfg', 'r')
    except:
        print()
        print("The 'app_config.cfg' file was not found!") 
        print("Please ensure that you created the file and that it contains your Client ID and Client Secret.")
        print()
        cleanup()
        quit()
    
    # check if the app config file is empty - do not allow the program to proceed if it's empty
    if os.path.getsize('app_config.cfg') == 0:
        print()
        print("The 'app_config.cfg' file is empty!") 
        print("Please ensure that the file contains your Client ID and Client Secret.")
        print()
        cleanup()
        quit()
    else:    
        # write the client id and client secret to a list
        app_config = []
        for eachLine in app_config_file:
            app_config.append(eachLine.strip())

    # client id and client secret values from spotify application are populated in from the list
    try:
        client_id = app_config[0]
        client_secret = app_config[1]
    except:
        print()
        print("The information you supplied in 'app_config.cfg' is invalid!") 
        print("Please ensure that the Client ID and Client Secret inside of the file is correct.")
        print()
        cleanup()
        quit()

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
        print("(Note: If you delete 'user_config.cfg', you'll have to go through this setup process again.)")
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
    Retrieve data from a playlist given a playlist ID or URL.
    """
    # create a variable for checking if a valid response was provided for playlist
    pid_valid_response_provided = False

    # input a playlist of your choice by pasting the playlist ID or URL here, or 'q' to quit. check to ensure it is valid.
    while pid_valid_response_provided == False:
        playlist_id = input("Please enter a Spotify playlist ID or URL, or type 'q' to quit: ")
        
        if playlist_id == 'q':
            pid_valid_response_provided = True
            print()
            print("Thank you for using the Duplicate Song Analyzer for Spotify!")
            cleanup()
            quit()

        # convert the URL to just the playlist ID portion so the program can work with it
        spotify_url_prefix = 'https://open.spotify.com/playlist/'

        if spotify_url_prefix in playlist_id:
            playlist_id = playlist_id.removeprefix(spotify_url_prefix)

        # if a valid URL or ID is given, write the contents to disk - otherwise, prompt until a valid response is given.
        try:
            playlist = spotify.playlist(playlist_id)
            pid_valid_response_provided = True
            print()
            print("Playlist found! Please wait while the program writes your playlist's data to disk...")
            print()
        except:
            print()
            print("The playlist ID or URL you specified was invalid.")

    # create an index for iterating through track names and create a file for storing track info
    current_index = 0
    song_data = open('song_data.txt', 'w')

    # create a dictionary for storing each song's URI - needed for duplicate removal
    song_uris_dict = {}

    # iterate through the first 100 tracks and artists and write to the song data file
    for current_index in range(0,100):
        try:
            track = spotify.playlist_items(playlist.id).items[current_index].track.name
            artist = spotify.playlist_items(playlist.id).items[current_index].track.artists[0].name
            album = spotify.playlist_items(playlist.id).items[current_index].track.album.name
            song_data_to_write = " ".join([track, "-", artist, "-", album])
            song_data.write("".join(song_data_to_write + '\n'))
            retrieve_song_uris = spotify.playlist_items(playlist.id).items[current_index].track.uri
            song_uris_dict[song_data_to_write] = retrieve_song_uris
            print("Wrote data for song", current_index+1, "to disk.")
            current_index += 1
        except:
            song_data.close()
            break

    # open the song data file and read it into list items (unformatted)
    with open('song_data.txt', 'r') as song_data:
        song_data_list_unformatted = song_data.readlines()

    # create a new list (formatted) for storing song data
    song_data_list = []

    # for each item in the unformatted list, strip the newline character and append each item to a new list (formatted)
    for eachItem in song_data_list_unformatted:
        song_data_list.append(eachItem.strip())

    # create lists for storing already seen song/artist combinations and unique ones
    unique_songs = []
    duplicate_songs = []

    # loop through the formatted song data list and identify if a song is unique or a duplicate - keep track by directing the song to its respective list.
    for eachItem in song_data_list:
        if eachItem not in unique_songs:
            unique_songs.append(eachItem)
        else:
            duplicate_songs.append(eachItem)
    
    # notify the user of the duplicates found (or if none were found)
    if len(duplicate_songs) == 0:
        print()
        print("No duplicates were found in this playlist!")
        print()
        run_again()

    else:
        print()
        print("There were", len(duplicate_songs), "duplicate songs found in your playlist: ")
        print(", ".join(duplicate_songs))
        print()
        remove_duplicates = input("Would you like to remove the duplicate songs from your playlist? ")
        
        # create a variable for checking if a valid response was provided for removing duplicates
        rd_valid_response_provided = False
        
        # check for a valid response as to if the program should remove duplicates or not and respond accordingly 
        while rd_valid_response_provided == False:
            if remove_duplicates == 'y':
                rd_valid_response_provided = True

                # create a list for storing uri values that need to be removed
                song_uris_list = []

                # get the uri values from the song uri dictionary and append them to a list
                for eachSong in duplicate_songs:
                    if song_uris_dict[eachSong] not in song_uris_list:
                        song_uris_list.append(song_uris_dict[eachSong])

                # remove all copies of the songs from the playlist entirely
                spotify.playlist_remove(playlist.id, song_uris_list)

                # add back a single copy of each of the songs removed
                spotify.playlist_add(playlist.id, song_uris_list)

                print("The duplicate songs were successfully removed from your playlist!")
                print()

            elif remove_duplicates == 'n':
                rd_valid_response_provided = True
                print()

            else:
                print()
                print("The response you provided was invalid. The valid responses are 'y' for yes and 'n' for no.")
                remove_duplicates = input("Would you like to remove the duplicate songs from your playlist? ")

        run_again()

def run_again():
    # create a variable for checking if a valid response was provided for running the program again
    ra_valid_response_provided = False

    # ask the user if they'd like to run the program again or not
    run_again = input("Would you like to check for duplicates in another playlist? ")

    # check for a valid response as to if the program should run again or not and respond accordingly 
    while ra_valid_response_provided == False:
        if run_again == 'y':
            ra_valid_response_provided = True
            main()
        elif run_again == 'n':
            ra_valid_response_provided = True
            print()
            print("Thank you for using the Duplicate Song Analyzer for Spotify!")
            cleanup()
            quit()
        else:
            print()
            print("The response you provided was invalid. The valid responses are 'y' for yes and 'n' for no.")
            run_again = input("Would you like to check for duplicates in another playlist? ")

def cleanup():
    # remove the following files after using the program
    if os.path.exists('.DS_Store'):
        os.remove('.DS_Store')
    if os.path.exists('song_data.txt'):
        os.remove('song_data.txt')
    
# run the program
main()