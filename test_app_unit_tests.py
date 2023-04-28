import pytest
import app as app


@pytest.fixture
def decodes():
    return app.get_json_data(app.DECODES_FILE_PATH)


@pytest.fixture
def encodes():
    return app.get_csv_data(app.ENCODES_FILE_PATH)


@pytest.fixture
def bitlink_dict(encodes):
    return app.make_bitlink_dict(encodes)


@pytest.fixture
def count_clicks(bitlink_dict, decodes):
    return app.count_clicks(bitlink_dict, decodes, 2021)


def test_get_json_data():
    data = app.get_json_data(app.DECODES_FILE_PATH)
    assert len(data) > 0
    assert isinstance(data[0], dict)


def test_make_bitlink_dict(encodes):
    assert app.make_bitlink_dict(encodes) == {
        "http://bit.ly/31Tt55y": "https://google.com/",
        "http://bit.ly/2kJO0qS": "https://github.com/",
        "http://bit.ly/2kkAHNs": "https://twitter.com/",
        "http://bit.ly/2kJdsg8": "https://reddit.com/",
        "http://bit.ly/2kJej0k": "https://linkedin.com/",
        "http://bit.ly/2lNPjVU": "https://youtube.com/",
    }


def test_count_clicks(encodes, decodes, bitlink_dict):
    count_dict = app.count_clicks(bitlink_dict, decodes, 2021)
    assert count_dict
    assert isinstance(count_dict, dict)
    assert len(count_dict.items()) == len(encodes)


def test_jsonify(count_clicks):
    sorted_dicts = app.sort_and_jsonify(count_clicks)
    assert sorted_dicts
    assert isinstance(sorted_dicts, list)
    assert isinstance(sorted_dicts[0], dict)
