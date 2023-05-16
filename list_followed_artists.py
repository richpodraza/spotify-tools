from init_spotipy import spotipy_init


def list_followed_artists():
    sp = spotipy_init()

    def add_artists(my_artists, items):
        my_artists.extend(items)

    def get_all_artists(my_artists, result):
        add_artists(my_artists, result["artists"]["items"])
        while result["artists"]["next"]:
            result = sp.next(result["artists"])
            add_artists(my_artists, result["artists"]["items"])

    my_artists = []
    result = sp.current_user_followed_artists()
    get_all_artists(my_artists, result)

    print("Number of artists", len(my_artists))
    for artist in my_artists:
        print(artist["name"])


if __name__ == "__main__":
    list_followed_artists()
