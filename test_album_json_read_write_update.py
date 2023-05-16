import get_all_albums
import album_metadata
import random


def assertDictionariesEqual(dict1, dict2):
    assert len(dict1) == len(dict2)
    assert dict1.keys() == dict2.keys()
    for key, value in dict1.items():
        dict2Val = dict2[key]
        assert value == dict2Val


def randomize_selected_count_values_between_x_and_y(albums: dict[str, album_metadata.AlbumMetadata], x: int, y: int) -> dict[str, album_metadata.AlbumMetadata]:
    for album in albums.values():
        album.selected_count = random.randint(x, y)
    return albums


def test_reading_and_writing_album_metadata():
    print('Testing reading and writing albums json...')
    print('Getting albums from Spotify...')
    albums = get_all_albums.get_all_albums_from_spotify()
    print('Writing albums to file...')
    get_all_albums.write_all_albums_to_file(albums, "albums_test_1.json")
    print('Reading albums from file...')
    albums_read_from_file_1 = get_all_albums.read_all_albums_from_file(
        "albums_test_1.json")
    print('Writing albums to another file...')
    get_all_albums.write_all_albums_to_file(
        albums_read_from_file_1, "albums_test_2.json")
    print('Reading albums from another file...')
    albums_read_from_file_2 = get_all_albums.read_all_albums_from_file(
        "albums_test_2.json")

    assertDictionariesEqual(albums, albums_read_from_file_1)
    assertDictionariesEqual(albums, albums_read_from_file_2)
    assertDictionariesEqual(albums_read_from_file_1, albums_read_from_file_2)

    print('Writing albums to existing file...')
    get_all_albums.write_all_albums_to_file(
        albums_read_from_file_1, "albums_test_2.json")
    print('Reading albums from existing file...')
    re_read_albums = get_all_albums.read_all_albums_from_file(
        "albums_test_2.json")
    assertDictionariesEqual(re_read_albums, albums_read_from_file_1)

    print('Reading albums from non-existent file...')
    non_existant_albums = get_all_albums.read_all_albums_from_file(
        "does_not_exist.json")
    assert len(non_existant_albums) == 0


def test_selecting_10_random_albums():
    print('Testing selecting 10 random albums...')
    print('Getting albums from Spotify...')
    albums = get_all_albums.get_all_albums_from_spotify()

    print('Setting all selected counts to 0...')
    albums = randomize_selected_count_values_between_x_and_y(albums, 0, 0)
    random_albums = get_all_albums.select_10_random_albums(albums)
    assert len(random_albums) == 10
    for album in random_albums.values():
        assert album.selected_count == 0

    print('Setting all selected counts to 5...')
    albums = randomize_selected_count_values_between_x_and_y(albums, 5, 5)
    random_albums = get_all_albums.select_10_random_albums(albums)
    assert len(random_albums) == 10
    for album in random_albums.values():
        assert album.selected_count == 5

    print('Randomizing selected counts between 0 and 1...')
    albums = randomize_selected_count_values_between_x_and_y(albums, 0, 1)
    random_albums = get_all_albums.select_10_random_albums(albums)

    assert len(random_albums) == 10
    # print the selected_Count of each random album
    print("Selected counts:")
    for album in random_albums.values():
        print(album.selected_count)
        assert album.selected_count >= 0
        assert album.selected_count <= 10

    print('Randomizing selected counts between 0 and 10...')
    albums = randomize_selected_count_values_between_x_and_y(albums, 0, 10)
    random_albums = get_all_albums.select_10_random_albums(albums)

    assert len(random_albums) == 10
    # print the selected_Count of each random album
    print("Selected counts:")
    for album in random_albums.values():
        print(album.selected_count)
        assert album.selected_count >= 0
        assert album.selected_count <= 10


def test_updating_album_metadata():
    print('Testing updating album metadata...')
    print('Getting albums from Spotify...')
    albums = get_all_albums.get_all_albums_from_spotify()

    print('Writing albums to file...')
    get_all_albums.write_all_albums_to_file(albums, "albums_test_1.json")

    print('Selecting random albums...')
    random_albums = get_all_albums.select_10_random_albums(albums)

    print('Updating selected albums...')
    get_all_albums.update_albums_selected_counts_in_file(
        random_albums, "albums_test_1.json")

    print('Reading albums from file...')
    albums_read_from_file = get_all_albums.read_all_albums_from_file(
        "albums_test_1.json")

    print('Asserting that selected counts are correct...')
    for album_id, album in random_albums.items():
        assert albums_read_from_file[album_id].selected_count == album.selected_count+1


def run_tests():
    # test_reading_and_writing_album_metadata()
    # test_selecting_10_random_albums()
    test_updating_album_metadata()


if __name__ == "__main__":
    run_tests()
