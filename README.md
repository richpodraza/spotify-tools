I wrote these tools because of a few problems that still exist with being a Spotify (or any other popular music streaming service) customer, relative to the days of owning CDs, tapes, records, even mp3s.

- I lost most of the details about my music library when going to Spotify, i.e. what albums and artists did I like? Spotify does let you "follow" artists and albums, but it's a big effort to go through and do that.
- No streaming service has native support for one of the most common ways I want to listen to music: by random album. This means listen to the album from the start to finish, but choose it randomly. And when it is over, pick another random album.

So this small set of rough Python scripts solves those problems for me. Hopefully they are useful for you too, and please feel free to make requests or send PRs.

# spotify_tools
This is just a menu for choosing among 4 other tools listed here: sync_with_spotify, make_10_random_album_playlist, play_random_album, and artists_and_albums_from_playlists.

# sync_with_spotify
If you have a large library of followed albums, it takes a good while (10+ seconds) to read them all from the Spotify API. This function will read them and write them to a local json file. The json file is then where make_10_random_album_playlist reads from when choosing albums.

# make_10_random_album_playlist
This function will read from your local json file of album metadata, randomly choose 10 albums (that haven't been chosen lately), update the metadata to indicate they have been chosen, create a dedicated playlist for this function, and update it. The playlist is dedicated in the sense that re-running this tool with overwrite that playlist instead of creating a new one. That is just my personal preference, I consider the results of this function to be temporary.

# play_random_album
This will read all your albums from Spotify API (not the local json file) and pick a random one to play. 

# artists_and_albums_from_playlists
This will read all the playlists that you have created in your Spotify library, and from those playlists follow all the artists with tracks that appear more than 5 times and albums whose tracks that appear more than 3 times. Apart from more properly giving your Spotify library its character (which will help with recommendations), this helps make_10_random_album_playlist and play_random_album do what they do.