#############################################
# IMPORTS
#############################################

# Librerías para llamar a la API de Spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

# Librerías para la manipulación de datos
import pandas as pd
from collections import Counter
from random import shuffle
from datetime import datetime as dt
from IPython.display import Image
import time
import json

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_colwidth", 1000)


#############################################
# GLOBAL VARIABLES
#############################################

# Importo las variables globales de otros archivos
import global_variables as gv
genres = gv.genres
client_ID = gv.client_ID
client_secret = gv.client_secret
sp = gv.sp
host = gv.host
find_URI = gv.find_URI

# La variable artists_genres se nutre cada vez que una canción nueva pasa por mi pipeline
with open('artists_genres.json') as json_file:  
    artists_genres = json.load(json_file)


#############################################
# USERS IDENTIFICATION
#############################################

# Recibo los Spotify URI's de los usuarios que van a linkear su música

def receive_users():
    
    print("Enter the Spotify URLs of the profiles you would like to link.\n")
    print("You can easily find your profile URL on the Spotify mobile app by following these 4 steps:\n")
    
    users_URLs = input("\n Paste your Spotify URLs here, separating them by ', ':"
                        ).split(", ")
    
# Creo un diccionario donde guardo los URIs de los usuarios con su display_name
# correspondiente.

    users_URIs = {}
    
# A partir de las URLs, obtengo los URIs de los usuarios:
    
    for user_url in users_URLs:
        display_name = sp.user(user_url[30:].split("?")[0])["display_name"]
        if display_name != None:
            users_URIs[user_url[30:].split("?")[0]] = display_name
        else:
            users_URIs[user_url[30:].split("?")[0]] = user_url[30:]
            
    # print(users_URIs)
        
# Devuelvo esa diccionario
    return users_URIs


#############################################
# OBTAIN USERS' PLAYLISTS
#############################################

# Para que los usuarios puedan escoger de entre sus playlists, las obtengo a través de
# sp.user_playlists, y se las muestro para que puedan seleccionarlas sin volver a Spotify.

def get_user_playlists(users_URIs):

# Creo un diccionario donde relaciono cada usuario con los nombres de sus playlists y sus respectivos
# URIs. Me va a servir tanto para mostrar el listado de sus playlists a cada usuario, como para
# obtener las URIs a partir de los nombres de playlists que los usuarios me pasen.

#                  {user1: {pl1_name: pl1_URI, pl2_name: pl2_URI}, ...}

    users_playlists_names_URIs = {}

# Para cada usuario, obtengo sus playlists, y guardo sus datos en el diccionario.

    for user_uri in users_URIs:
        playlists = sp.user_playlists(user_uri)
        users_playlists_names_URIs[user_uri] = {}
        
        for i, playlist in enumerate(playlists["items"]):
            users_playlists_names_URIs[user_uri][playlist["name"]] = playlist['uri'][17:]
        
    #print(users_playlists_names_URIs)


# Creo una variable que va a contener los datos de la petición (playlist por usuario, 
# género a filtrar, y nombre de la nueva lista).
  
#                mygroup = {"users": {user1: [playlists_to_select], 
#                                     user2: [playlists_to_select]},
#                           "genres": [genres_to_select],
#                           "new_playlist_name": name}

    mygroup = {"users": {}}
    for user_uri in users_URIs:
        mygroup["users"][user_uri] = {} 
        

# Doy la opción a los usuarios de escoger si quieren seleccionar todas sus playlists
# o no, para que, en caso de querer seleccionar todas, no tengan que ir uno a uno 
# escribiendo "all".

    select_playlists = input("""
     If you would like to select which playlists from your profiles to submit, write 'select'. 
                             
     If you rather want to submit them all, write 'all'
                             
     """)
    
# Si han escogido "all", entonces en mygroup se guarda ["all"] en playlists_to_select
# para todos los usuarios.
        
    if select_playlists == "all":
        for user_uri in users_URIs:
            mygroup["users"][user_uri] = []
            for playlist in users_playlists_names_URIs[user_uri]:
                mygroup["users"][user_uri].append(playlist)
        
# Si han escogido "select", entonces en playlists_to_select se guarda la lista de 
# playlists que introduzcan en el siguiente input, donde muestro su display_name
# y el nombre de todas sus playlists.

    else:    
        for user_uri in users_URIs:
            selected_playlists = input(
                """
                ·················································
                ·················································
                ·················································

                {} , enter the Spotify playlists you would like to submit. 

                These are all your public playlists: 

                {} 
                
                If you want to submit all, just write "all"
                
                This time, separate the playlists by '//'.

                """
                .format(users_URIs[user_uri], 
                        list(users_playlists_names_URIs[user_uri].keys()))).split("//")
                
            if selected_playlists == ["all"]:
                mygroup["users"][user_uri] = []
                for playlist in users_playlists_names_URIs[user_uri]:
                    mygroup["users"][user_uri].append(playlist)
            else: 
                mygroup["users"][user_uri] = selected_playlists

# Una vez han seleccionado las playlists que quieran subir, les ofrezco el filtro 
# por género. Recibo su respuesta a través de un input donde le muestro los géneros
# generales de entre los que pueden seleccionar (guardados en mi variable global genres),
# y la guardo en mygroup["genres"].

    mygroup["genres"] = input(
            """
            ·················································
            ·················································
            ·················································
            
            Now select the genres of the songs for your new playlist.
                        
            You can select out of the following:
    
            {} 
            
            
            If you don't want to filter by genre, just write "any"
            
            Again, separate by '//'
                        
            """
            .format(list(genres.keys()))).split("//")

# Finalmente, escriben el nombre de la nueva playlist, y lo guardo en 
# mygroup["new_playlist_name"]

    mygroup["new_playlist_name"] = input(
            """
            ·················································
            ·················································
            ·················································
            
            And finally, write the name for your new combined playlist :D            
            
            """
            )
    
    #print("PL_NAMES_URIS:", users_playlists_names_URIs)
    #print("MYGROUP:", mygroup)
    

# Devuelvo el diccionario donde relaciono los nombres de las playlists de un usuario con 
# sus URIs, mygroup, y el diccionario que relaciona URIs de usuarios y sus display_names.

    return users_URIs, users_playlists_names_URIs, mygroup



#############################################
# SAVE PLAYLISTS
#############################################

# Ahora que ya tengo las playlists que cada usuario quiere subir, guardo sus URIs y la 
# información de sus temas en la variable global playlists_tracks.
# Si ya tengo una playlist guardada de una petición anterior, entonces no tendré que
# llamar a la API para obtener la información de sus temas.

def save_playlists_tracks(users_URIs, users_playlists_names_URIs, mygroup):
    
# Guardo la hora para calcular cuánto tarda desde aquí hasta el final.
    
    start_time = time.time()
    

# Creo una variable donde voy a guardar la información relevante de los temas de cada playlist

# user_playlists_tracks = 

# {user1_uri: [{playlist1_uri: [{"track_uri": track1_uri, 
#                               "track_name": track1_name, 
#                               "artist": [track1_artist_name, track1_artist_uri], 
#                               "date_added": track1_date},
#                              {"track_uri": track2_uri, 
#                               "track_name": track2_name, 
#                               "artist": [track1_artist_name, track1_artist_uri], 
#                               "date_added": track2_date}],
#              playlist2_uri: [...]}],
#  user2_uri: ...}


    user_playlists_tracks = {}
    
# Itero sobre cada usuario de la petición, guardando sus playlists con sus respectivos
# temas en playlists_tracks:
        
    for user_uri in users_URIs:
        
        print("Obtaining tracks info from {}".format(users_URIs[user_uri]))
        
        user_playlists_tracks[user_uri] = []
        
        count = 0
            
        for playlist in mygroup["users"][user_uri]:
            playlist_uri = users_playlists_names_URIs[user_uri].get(playlist)
            user_playlists_tracks[user_uri].append({playlist_uri: []})
            tracks_info = sp.user_playlist_tracks(user_uri, playlist_id = playlist_uri)
            for track in tracks_info["items"]:
                if track["track"] != None:
                    if track["track"]["id"] != None:
                        #print(user_playlists_tracks[user_uri])
                        date_added = dt.strptime(track["added_at"][:10], '%Y-%m-%d').date()
                        user_playlists_tracks[user_uri][count][playlist_uri].append({"track_uri": track["track"]["id"], 
                                                                                     "track_name": track["track"]["name"], 
                                                                                     "artist": [track["track"]["artists"][0]["name"],
                                                                                                track["track"]["artists"][0]["id"]],
                                                                                     "date_added": date_added})
            
            count += 1                      
                                                              
    # print("PLAYLISTS TRACKS:", user_playlists_tracks)         
    
    return users_URIs, mygroup, start_time, user_playlists_tracks   


#############################################
# OBTAIN FINAL TRACKS
#############################################

# Ya tengo toda la info de los temas de las playlists a combinar. 
# Ahora tengo que obtener los temas finales, filtrando por género/fecha de subida en 
# caso de que se haya especificado así.

def get_final_tracks(users_URIs, mygroup, start_time, user_playlists_tracks):
    
# Creo un diccionario donde voy a guardar la información de los temas con los que me 
# voy a quedar.      final_tracks = {track_URI: {track_name: artist}}
    
    final_tracks = {}
    
# Creo listas vacías para introducir después sus valores en final_tracks.
# Si introdujese directamente los valores en final_tracks, al ser un diccionario,
# no guardaría repetidos, sino que reescribiría los valores de las key repetidas.

# Sin embargo, yo voy a necesitar la lista final_track_IDs con repetidos, para poder 
# así calcular más adelante la frecuencia de cada tema.
    
    final_track_URIs = []
    final_track_names = []
    final_track_artists = []
    
# Itero sobre cada usuario

    for user_uri in user_playlists_tracks:
        
        print("Obtaining final tracks from {}".format(users_URIs[user_uri]))
        
        # Para cada usuario creo una lista de sus canciones con valores únicos. 
        # Esto lo hago para evitar que un usuario con la misma canción en distintas
        # playlists incluya varias veces la canción en la lista final, dándole mayor 
        # popularidad porque se repite entre sus listas, pero sin que realmente sea 
        # popular entre los distintos perfiles.
        
        user_track_URIs = []
        user_track_names = []
        user_track_artists = []
        

# Itero sobre cada playlist de cada usuario

        for pl in user_playlists_tracks[user_uri]:
        
        # Itero sobre cada tema de cada playlist
        
            for playlist_uri in pl:
             #   print(pl)
                
                for track in pl[playlist_uri]:
                
                    if track["track_name"] not in user_track_names:  # Aquí evito repetición.
                            
                        # Si los usuarios no han filtrado por género, cojo todos.
                            
                        if mygroup["genres"] == ["any"]:
                            user_track_URIs.append(track["track_uri"])
                            user_track_names.append(track["track_name"])
                            user_track_artists.append(track["artist"][0])
                                
                        # Si los usuarios sí que han filtrado por género, cojo el
                        # URI del artista de la canción, y utilizo sp.artist para obtener
                        # el género del artista.

                        else:
                            artist_uri = track["artist"][1]
                                
                    # Tengo una variable global (artists_genres), donde voy guardando 
                    # artistas y sus géneros, para evitar llamadas a la API y reducir así
                    # el tiempo del proceso entero. 
                    # Si no tengo guardado a ese artista en la variable, entonces llamo a la
                    # API, y lo guardo en la variable con su género correspondiente.
                                
                            if artist_uri not in artists_genres:
                                artist_info = sp.artist(artist_uri)
                                artists_genres[artist_uri] = artist_info["genres"]
                                
                    # Hay artistas de reggaeton que incluyen "pop" entre sus géneros. 
                    # Evito que sus canciones puedan ser seleccionados como pop.

                            if "reggaeton" in artists_genres[artist_uri]:
                                artists_genres[artist_uri] = ["reggaeton"]
                                                    
                                    
                    # Si alguno de los géneros incluidos en el general_genre que me han pasado 
                    # los usuarios aparece en el listado de géneros del artista (guardado ya en
                    # artists_genres), entonces meto la canción en la lista de canciones finales
                    # del usuario.

                            genre_in_artist = 0

                            for general_genre in mygroup["genres"]:
                                 for genre in genres[general_genre]:
                                    if genre in artists_genres[artist_uri]:
                                        genre_in_artist += 1
                            if genre_in_artist > 0:
                                user_track_URIs.append(track["track_uri"])
                                user_track_names.append(track["track_name"])
                                user_track_artists.append(track["artist"][0])

# Introduzco las listas de canciones finales del usuario en las listas globales de todos
# los usuarios. (Recuerda que lo he hecho para evitar repetición dentro de un mismo usuario).
                            
        for i in range(len(user_track_names)):
            final_track_URIs.append(user_track_URIs[i])
            final_track_names.append(user_track_names[i]) 
            final_track_artists.append(user_track_artists[i])    
            
# Y guardo las listas globales en el diccionario global (donde no se podrá medir la frecuencia).
    
    for i in range(len(final_track_URIs)):
        final_tracks[final_track_URIs[i]] = [final_track_names[i], final_track_artists[i]]
        
    
    # Hago este shuffle antes de ordenarlos por popularidad para evitar que las canciones con 
    # el mismo número de repeticiones se ordenen según el orden de introducción de los 
    # nombres de usuarios. Lo quiero aleatorio:
    
    shuffle(final_track_URIs)
    
    # Ordeno los temas por popularidad en una nueva variable
    
    final_track_URIs_pop = [item for items, c in Counter(final_track_URIs).most_common() for item in [items] * c]
    
    # Creo una lista para obtener valores únicos de los temas finales, ordenados por
    # popularidad
    
    final_track_URIs_unique_all = []
    
    for track_URI in final_track_URIs_pop:
        if track_URI not in final_track_URIs_unique_all:
            final_track_URIs_unique_all.append(track_URI)
            
    # Creo otra lista con solo los temas que aparecen repetidos, para utilizarla
    # después al mostrar el dataframe:
    
    final_track_URIs_unique_repeated = []
    
    for track in final_track_URIs_unique_all:
        if final_track_URIs_pop.count(track) > 1:
            final_track_URIs_unique_repeated.append(track)
            
    # La lista final en Spotify va a tener como máximo 50 canciones:
            
    if len(final_track_URIs_unique_all) > 50: 
        final_track_URIs_unique = final_track_URIs_unique_all[:50]
    else:
        final_track_URIs_unique = final_track_URIs_unique_all
            
    print("READY!")
    
# Devuelvo el diccionario que relaciona URIs con nombres de temas y artistas, la lista de temas
# finales con valores únicos, la lista de temas finales con repetidos, mygroup y start_time

    return users_URIs, mygroup, start_time, final_tracks, final_track_URIs_pop, final_track_URIs_unique, user_playlists_tracks, final_track_URIs_unique_repeated


#############################################
# CREATE DATAFRAME FOR DJ
#############################################

# Creo un dataframe que me muestre las canciones finales ordenadas por popularidad:
# su URI, nombre, artista y frecuencia.

def create_dataframe(users_URIs, mygroup, start_time, final_tracks, final_track_URIs_pop, 
                     final_track_URIs_unique, user_playlists_tracks, final_track_URIs_unique_repeated):
    
# Creo listas que voy a utilizar como columnas en el dataframe

    tracks = []
    artists = []
    frequency = []

# Obtengo los datos de la lista ordenada de URIs finales, buscando sus datos correspondientes
# en el diccionario final_tracks, y contando la frecuencia de los temas en final_track_URIs_pop.

    for URI in final_track_URIs_unique_repeated:
            tracks.append(final_tracks.get(URI)[0])
            artists.append(final_tracks.get(URI)[1])
            frequency.append(final_track_URIs_pop.count(URI))
            
# Busco en qué listas aparecen las canciones:
    
    users = []
    
    count = 0

    for track_uri in final_track_URIs_unique_repeated:
        users.append([])
        for user_uri in user_playlists_tracks:
            for i in user_playlists_tracks[user_uri]:
                for playlist_uri in i:
                    for e in i[playlist_uri]:
                        if track_uri in e["track_uri"]:
                            users[count].append(users_URIs.get(user_uri))
                            
        count += 1
        
            
# Creo el dataframe

    final_tracks_df = pd.DataFrame(data = [final_track_URIs_unique_repeated, tracks, artists, frequency, users],
                                   columns = range(len(final_track_URIs_unique_repeated)), 
                                   index = ["ID", "Track", "Artist", "Frequency", "Users"]).T
    
    display(final_tracks_df)
    
# Devuelvo la lista de URIs de temas finales únicos, mygroup y start_time

    return mygroup, start_time, final_track_URIs_unique



#############################################
# CREATE PLAYLIST ON SPOTIFY
#############################################

# Teniendo ya el listado ordenado de URIs de los temas finales, creo la playlist en Spotify

def create_playlist(mygroup, start_time, final_track_URIs_unique):
    
# Para crear una playlist necesito un token especial.

    token = util.prompt_for_user_token(host,
                               "playlist-modify-public",
                               client_id = "{}".format(client_ID),
                               client_secret = "{}".format(client_secret),
                               redirect_uri = "https://example.com/callback/")
    

# Con la autorización del nuevo token, creo la nueva playlist en el perfil del perfil de 
# la aplicación.

    sp = spotipy.Spotify(auth = token)
    final_playlist = sp.user_playlist_create(host, mygroup["new_playlist_name"])
    
# Añado los temas a la nueva playlist:

    sp.user_playlist_add_tracks(host, final_playlist["uri"][17:], final_track_URIs_unique)
    
# Obtengo su URL, y la comparto con los usuarios:

    final_playlist_url = final_playlist["external_urls"]["spotify"]
    
    print("""
          ·················································
          ·················································
          ·················································
          
          Here's your new combined playlist: 
          
          {}
          
          ENJOY!
          """.format(final_playlist["external_urls"]["spotify"])
          )
    
    elapsed_time = time.time() - start_time
    print("Elapsed time:", elapsed_time)


#############################################
# FINAL PIPELINE
#############################################

if __name__ == '__main__':
    
    users_URIs = receive_users()
    
    users_URIs, users_playlists_names_URIs, mygroup = get_user_playlists(users_URIs)
    
    users_URIs, mygroup, start_time, user_playlists_tracks = save_playlists_tracks(users_URIs, users_playlists_names_URIs, mygroup)
    
    users_URIs, mygroup, start_time, final_tracks, final_track_URIs_pop, final_track_URIs_unique, user_playlists_tracks, final_track_URIs_unique_repeated = get_final_tracks(users_URIs, mygroup, start_time, user_playlists_tracks)
    
    mygroup, start_time, final_track_URIs_unique = create_dataframe(users_URIs, mygroup, start_time, final_tracks, final_track_URIs_pop, final_track_URIs_unique, user_playlists_tracks, final_track_URIs_unique_repeated)
    
    create_playlist(mygroup, start_time, final_track_URIs_unique)