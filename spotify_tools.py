import make_10_random_album_playlist
import sync_with_spotify
import play_random_album
import artists_and_albums_from_playlists


def main_menu():
    print("Please choose an option:")
    print("[1] Sync albums with Spotify")
    print("[2] Make a random 10 album playlist")
    print("[3] Play a random album")
    print("[4] Follow albums and artists from playlists")
    print("[Q] Quit")

    while True:
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            sync_with_spotify.sync_with_spotify()
            break
        elif choice == '2':
            make_10_random_album_playlist.make_playlist()
            break
        elif choice == '3':
            play_random_album.play_random_album()
            break
        elif choice == '4':
            artists_and_albums_from_playlists.follow_artists_and_albums_from_playlists()
            break
        elif choice == 'Q' or choice == 'q':
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or Q/q to quit.")


if __name__ == "__main__":
    main_menu()
