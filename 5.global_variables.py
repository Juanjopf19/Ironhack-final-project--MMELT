import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from IPython.display import Image


genres = {"Chill House": ["tropical house",
                                  "deep house", 
                                  "deep euro house", 
                                  "deep tropical house"],
                  
                  "Indie": ["neo mellow", 
                            "downtempo", 
                            "indietronica", 
                            "chamber pop", 
                            "freak folk", 
                            "indie pop", 
                            "toronto indie", 
                            "slow core", 
                            "folk-pop", 
                            "stomp and holler", 
                            "indie rock"],
                  
                  "Pop": ["pop",
                          "spanish pop", 
                          "colombian pop", 
                          "spanish hip hop",
                          "mexican pop",
                          "post-teen pop", 
                          "cumbia pop",
                          "dance pop", 
                          "alternative dance", 
                          "britpop"], 
                  
                  "Rock": ["rock en espanol", 
                           "latin rock", 
                           "spanish rock", 
                           "rock", 
                           "rock-and-roll", 
                           "rockabilly", 
                           "british alternative rock", 
                           "modern rock"],
                  
                  "Latin": ["reggaeton flow", 
                            "latin",
                            "latin hip hop", 
                            "reggaeton", 
                            "panamanian pop", 
                            "latin pop", 
                            "latin talent show", 
                            "colombian hip hop", 
                            "latin arena pop", 
                            "mexican pop", 
                            "musica canaria",
                            "electro latino", 
                            "r&b en espanol"], 
                  
                  "Electronic/Dance": ["dance pop", 
                                       "edm", 
                                       "uk dance",
                                       "big room", 
                                       "tech house", 
                                       "alternative dance", 
                                       "house", 
                                       "progressive house", 
                                       "dutch house", 
                                       "deep big room", 
                                       "future house"
                                       "pop edm"],
                                                         
                  "Trap": ["trap latino", 
                           "latin hip hop"],
                                       
                  "Techno": ["german techno", 
                             "leipzig electronic",
                             "minimal techno"], 
                                             
                  "Hip hop": ["gangster rap", 
                              "hip hop", 
                              "pop rap", 
                              "rap", 
                              "west coast rap", 
                              "atl hip hop", 
                              "detroit hip hop", 
                              "g funk", 
                              "pop rap", 
                              "rap rock"]}

client_ID = "0c91692caa1743d8a868fbf9ce149f23"

with open("secret.txt") as file:
    client_secret = file.read()[:-1]
    
sp = spotipy.Spotify(
    client_credentials_manager = SpotifyClientCredentials(
        "{}".format(client_ID), "{}".format(client_secret)))

host = "ubzr4ngighfyu4fn3iuy40io9"

find_URI = Image("find_spotify_URI.png", width = 400, height = 50)