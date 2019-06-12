# **MMELT**

This project consists on the development of an API that analyses the profiles of a group of Spotify users, and directly creates on Spotify a sorted playlist with the most popular tracks amongst them.

![logo_melt](https://github.com/Juanjopf19/Ironhack-final-project--MMELT/blob/master/logo_melt.png)


## **How it works**

The API receives a list of profile URIs, and interacts with the users to let them select:
· Which playlists they would like to upload for the merge
· If they would like to filter the tracks by genre
· The name of the new playlist on Spotify

By using Spotipy, a lightweight Python library for the Spotify Web API, MMelt obtains and handles the necessary information from the users' profiles, in the form of JSONs, to sort all of their music by merged popularity, create the playlist on Spotify, and return its URL to the users.

To do so, tokens from oauths are obtained by using the client keys from MMelt's developer Spotify account.

## **Next steps**

Develop an APP so that, through social loggin, users can concede permissions to MMelt so that the API can also obtain the list of each user's favourite tracks.
This way it would be possible to develop a system within the API to evaluate each track's popularity by, in addition to its number of occurrences in the different profiles:
· Its appearance or not in the list of favourites 
· The overall attraction of the users to the genre of the track
· The overal attraction of the users to the artist of the track
     
Furthermore, it would be convenient to offer the posibility to scan the Spotify codes of the users, instead of making them search for their URIs. 
