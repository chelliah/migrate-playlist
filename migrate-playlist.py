import requests
import json
import spotipy
import os
import re
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIFY_USER_ID = '1289250171'


SPOTIFY_PLAYLIST_ID = '15CwnfgJblY5jKZZ0t9QWd'
TRACKS_STRING = """
Chkn	5:03	Ashrae Fax	Never Really Been into It	Alternative	0	
Freakalizer	3:50	Sudan Archives	Natural Brown Prom Queen	R&B/Soul	0	1
Πήγαινέ Μέ	3:27	Spivak	Μετά Το Ρέιβ	Electronic	0	
In My Color 	4:49	Jimmy Edgar	XXX	Electronic	2	
Always There	3:42	Daphni	Cherry	Electronic	2	
Puppy (Feel The Beat Mix)	3:36	Doss	Puppy (Feel the Beat Mix) - Single	Electronic	0	
Mona	2:51	Daphni	Cherry	Electronic	2	1
Korty	2:40	D'Arcangelo	D'Arcangelo - EP	Techno	0	1
Pressed	2:10	Alvvays	Blue Rev	Alternative	2	16
The Headmaster Ritual	4:53	The Smiths	Meat Is Murder	Rock	0	5
Drifting	4:15	Growing Pains	Heaven Spots	Alternative	0	1
Wish	3:01	Blood Orange	Four Songs - EP	Alternative	0	1
No Bitterness	3:38	Alex G	God Save the Animals	Alternative	0	2
Pharmacist	2:04	Alvvays	Blue Rev	Alternative	2	23
Memory Foam	3:45	Molly Nilsson	Imaginations	Alternative	0	1
You're Lookin' at My Guy	2:55	The Radio Dept.	You're Lookin' at My Guy - Single	Pop	0	1
Miss Modular	4:29	Stereolab	Dots and Loops	Alternative	0	1
Ever New	7:09	Beverly Glenn-Copeland	Keyboard Fantasies	New Age	0	1
Dog Song	2:48	Warm Human	Hold Music	Downtempo	0	1
Don't Be So Hard on Your Own Beauty	3:12	yeule	Glitch Princess	Pop	0	2
On Retinae (East Version)	5:15	dip in the pool	Retinae	J-Pop	0	
Sorrowful Soil	3:16	Björk	Fossora	Electronic	0	4
Untitled #3 (Samskeyti)	6:33	Sigur Rós	( )	Alternative	0	1
"""

NON_ALPHA_CHAR_REGEX = re.compile(r'[^A-Za-z0-9 ]+')

def client_login():
    scope = "playlist-modify-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    return sp

def get_first_match(items, track, artist):
    match = None
    if len(items) > 0:
        match = items[0]
    else:
        print("Unable to find results for {match_string}")

    return match

def get_tracks_list_from_string():
    split_string = TRACKS_STRING.replace(u'\xa0', u'').split("\n")
    tracks_list = []
    for track in split_string:
        if track == "":
            continue
        track_fields = track.split("\t")
        # Add track and artist as tuple
        tracks_list.append((track_fields[0], track_fields[2]))

    return tracks_list

def add_tracks_to_playlist(playlist_id, tracks):
    sp = client_login()
    track_uris = []
    for track in tracks:
        track_name = track[0]
        track_artist = track[1]
        print(f"Searching for {track_name}: {track_artist}")
        track_search = sp.search(f"{track}", limit=5, type="track")
        matching_track = get_first_match(track_search["tracks"]["items"], track=track_name,  artist=track_artist)
        if matching_track is not None:
            track_uris.append(matching_track["uri"])
    print('Adding tracks to playlist!')
    sp.playlist_add_items(playlist_id,items=track_uris)

if __name__ == "__main__":
    tracks_list = get_tracks_list_from_string()
    add_tracks_to_playlist(SPOTIFY_PLAYLIST_ID, tracks_list)
