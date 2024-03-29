# Duplicate Song Analyzer for Spotify

Spotify does a fairly good job on its own of notifying you when you're about to add a song that already matches one in your playlist.

However... when it comes to playlist enthusiasts like myself that sometimes add hundreds or even thousands of songs to a single playlist, we sometimes end up inadvertently adding identical songs. Either we're quickly adding songs to a playlist and Spotify decides not to notify us that we're adding a duplicate song to one of our playlists, or we just straight up forgot the song was already there. By the time you realize that you may have duplicates in your playlist, you're a thousand songs deep, and it's a very tedious and lengthy process to go back through *all* of your songs one by one and make sure you don't have duplicates of each one - it can take hours to fix your mistake, depending on how many songs you've added.

This is where my program, Duplicate Song Analyzer for Spotify, comes in.

## Requirements
To use Duplicate Song Analyzer for Spotify, you will need:
- A Spotify account
- A Client ID and Client Secret (obtained by creating an app on the [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard))
- At least one playlist that you'd like to search for duplicates in
- [Python 3.9+](https://www.python.org/downloads/)

## How to Use
- Download the program.
- Create an app on the [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard) to obtain a Client ID and Client Secret.
- Navigate to the directory where you downloaded the program and run ```make install``` to install all the required dependencies.
- Create a file in the directory named ```app_config.cfg```. **Place your Client ID in the first line and your Client Secret in the second line.**
- Run the program with ```make run```.
  - On your first run, you will be prompted to login with your Spotify Account and grant access to the program. Paste the link that the webpage gives you after signing into the program. You will only have to do this once - unless you delete the ```app_config.cfg``` file.
- Follow the detailed instructions given in the program.

## Notes
- Currently, I am unable to get the program to work with more than 100 songs. If your playlist contains more than 100 songs - the program will still work, but the program will quit analyzing after you hit song number 100. A workaround for this "problem" is to create a new playlist for each chunk of 100 songs you want to analyze for duplicates and run the program on each playlist. After running the program on each playlist, move all the songs from the 'cleaned' playlists into a new playlist.
- Since you create your own application in the developer dashboard, I do not receive **any** personal data about you. You can delete the application in your Spotify developer portal at any time if you decide you'd not like to use the program any longer. The application itself is also fully removable using the ```make clean``` command.
