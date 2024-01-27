from utils import create_short_code, get_short_code


def test_create_short_link():
    short_code = create_short_code()
    assert len(short_code) == 6
    assert type(short_code) == str


def test_get_short_code():
    short_code = get_short_code({"short_link": "http://127.0.0.1:8000/go/BmQrQC"})
    assert len(short_code) == 6
    assert type(short_code) == str
    assert short_code == "BmQrQC"
