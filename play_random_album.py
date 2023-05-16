from init_spotipy import spotipy_init
import get_all_albums
import random


def play_random_album():
    sp = spotipy_init()

    # dict[str, album_metadata.AlbumMetadata]:
    my_albums = get_all_albums.get_all_albums_from_spotify()
    random_key = random.choice(list(my_albums.keys()))
    random_album = my_albums[random_key]
    print(f"Random album:\n\n\t{random_album.album_name}\n\t{random_album.artist}\n\n")
    answer = input("Play this album?\n(y/n)>")
    if answer.lower() == "y":
        print(f"Playing {random_album.album_name}...")
        album_details = sp.album(random_album.album_id)
        sp.start_playback(context_uri=album_details["uri"])


if __name__ == "__main__":
    play_random_album()
