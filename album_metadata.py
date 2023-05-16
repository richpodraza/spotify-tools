import json


class AlbumMetadata:
    def __init__(self, album_id: str, album_name: str, artist: str, selected_count: int):
        self.album_id = album_id
        self.album_name = album_name
        self.artist = artist
        self.selected_count = selected_count

    def __eq__(self, other: 'AlbumMetadata'):
        if not isinstance(other, AlbumMetadata):
            return False
        return self.album_id == other.album_id and \
            self.album_name == other.album_name and \
            self.artist == other.artist and \
            self.selected_count == other.selected_count

    @staticmethod
    def read_from_file(file_path: str) -> dict[str, 'AlbumMetadata']:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        albums = {}
        for album_id, album_data in data.items():
            album_name = album_data["album_name"]
            artist = album_data["artist"]
            selected_count = album_data["selected_count"]
            albums[album_id] = AlbumMetadata(
                album_id, album_name, artist, selected_count)

        return albums

    @staticmethod
    def write_to_file(albums: dict[str, 'AlbumMetadata'], file_path: str):
        data = {}
        for album_id, album in albums.items():
            data[album_id] = {"album_name": album.album_name,
                              "artist": album.artist, "selected_count": album.selected_count}

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
