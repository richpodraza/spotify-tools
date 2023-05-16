from init_spotipy import spotipy_init
from spotipy import Spotify
import get_all_albums
from datetime import date
import json
import album_metadata


def write_playlist_id_to_config(playlist_id):

    try:
        config_file = open('config.json', 'r')
    except FileNotFoundError:
        config_file = open('config.json', 'x')

    try:
        config = json.load(config_file)
    except Exception as e:
        print('Error occurred loading config_file contents as json: ', e)
        config = dict()
    finally:
        config_file.close()

    config.update({'random-album-playlist-id': playlist_id})

    try:
        config_file = open('config.json', 'w')
    except Exception as e:
        print('Error occurred opening the config file to write', e)

    json.dump(config, config_file, indent=2)
    config_file.close()


def read_playlist_id_from_config():
    try:
        config_file = open('config.json', 'r')
        try:
            config = json.load(config_file)
            try:
                return config['random-album-playlist-id']
            except Exception as e:
                print('Exception trying to get the playlist id from config: ', e)
                return None
        except Exception as e:
            print('Error occurred loading config_file contents as json: ', e)
            return None
        finally:
            config_file.close()
    except FileNotFoundError:
        print('Failed to read playlist id from config, config file does not exist (yet)')
        return None


def get_track_ids_from_albums(sp: Spotify, albums: dict[str, album_metadata.AlbumMetadata]) -> list[str]:
    track_ids = list()
    for album_id in albums.keys():
        album_tracks = sp.album_tracks(album_id)
        for track in album_tracks['items']:
            track_ids.append(track['id'])
    return track_ids


def pretty_print_playlist(albums: dict[str, album_metadata.AlbumMetadata]):

    list1 = list()
    list2 = list()
    list3 = list()

    for i, album in enumerate(albums.values()):
        list1.append(i+1)
        list2.append(album.artist)
        list3.append(album.album_name)

    max_len_1 = max(len(str(x)) for x in list1)
    max_len_2 = max(len(str(x)) for x in list2)
    max_len_3 = max(len(str(x)) for x in list3)

    for i in range(max(len(list1), len(list2), len(list3))):
        val1 = str(list1[i]).ljust(max_len_1)
        val2 = str(list2[i]).ljust(max_len_2)
        val3 = str(list3[i]).ljust(max_len_3)
        print(f"\t{val1}  {val2}  {val3}")


def get_playlist_id(sp: Spotify) -> str:
    random_album_playlist_id = read_playlist_id_from_config()
    user = sp.current_user()

    playlist_name = date.today().strftime("%A %b %d")
    playlist_description = 'Ten random albums generated on ' + playlist_name

    if random_album_playlist_id is None:
        print(
            f'No existing random album playlist id found in config, creating playlist "{playlist_name}"...')
        result = sp.user_playlist_create(user=user['id'], name=playlist_name, public=False,
                                         collaborative=False, description=playlist_description)
        random_album_playlist_id = result['id']
        write_playlist_id_to_config(random_album_playlist_id)
    else:
        # Playlist already exists, so update the name
        sp.playlist_change_details(
            random_album_playlist_id, name=playlist_name, description=playlist_description)
    return random_album_playlist_id


def add_tracks_to_playlist(sp: Spotify, playlist_id: str, track_ids: list[str]):
    print(f'Adding {len(track_ids)} tracks to playlist...')
    i = 0
    while i < len(track_ids):
        j = i + 50
        if j > len(track_ids):
            j = len(track_ids)
        # print(f'Adding tracks to playlist between {i} and {j}')
        if i == 0:  # only "replace" the first time, so the playlist is cleared and now we start adding new tracks
            sp.playlist_replace_items(
                playlist_id, track_ids[i:j])
        else:
            sp.playlist_add_items(playlist_id,
                                  track_ids[i:j])
        i = j
    print('Done!')


def make_playlist():
    sp = spotipy_init()
    user = sp.current_user()

    album_metadata_filename = 'album_metadata.json'

    my_albums = get_all_albums.read_all_albums_from_file(
        album_metadata_filename)

    random_albums = get_all_albums.select_10_random_albums(my_albums)

    print('Random albums playlist:\n\n')
    pretty_print_playlist(random_albums)

    answer = input(f'\nCreate this playlist?\n(y/n): ')

    if answer.lower() == 'y':
        print(f'Updating selected album counts...')
        get_all_albums.update_albums_selected_counts_in_file(
            random_albums, album_metadata_filename)

        print(f'Creating list of tracks from albums...')
        random_album_track_ids = get_track_ids_from_albums(sp, random_albums)
        # for i, id in enumerate(random_album_track_ids):
        #     print(i, id)

        # Get the random album playlist id from config
        # We will just replace the contents of this existing playlist instead of creating a new one
        # This reduces playlist clutter, makes this playlist temporary in nature
        random_album_playlist_id = get_playlist_id(sp)

        # Now add the new random albums
        add_tracks_to_playlist(
            sp, random_album_playlist_id, random_album_track_ids)


if __name__ == '__main__':
    make_playlist()
