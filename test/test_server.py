
import sys, os
from fastapi.testclient import TestClient
sys.path.append(f"{os.pardir}/MediaRouter/")
import config

path_data = config.PATH_DATA
name_video = 'test_video.mp4'
name_image = 'test_image.jpg'
name_zip = 'test_zip.zip'
name_image_wrong = 'test_image.jp'

from server import app
testclient = TestClient(app)

def test_read_main():
    res = testclient.get('')
    assert res.status_code == 200
    assert type(res.json()) == dict

def test_video():

    with open(f"{path_data}/{name_video}", "rb") as _file:
        res = testclient.post("/video?test=1", files={"file": (f"_{name_video}", _file, "video/mp4")})
    print(res)
    assert res.status_code == 200
    assert type(res.json()) == dict

    # with open(f"{path_data}/{name_image}", "rb") as _file:
    #     res = testclient.post("/video/?test=1", files={"file": (name_image_wrong, _file, "image/jpeg")})
    # assert res.status_code == 400


def test_image():

    with open(f"{path_data}/{name_image}", "rb") as _file:
        res = testclient.post("/image?test=1", files={"file": (f"_{name_image}", _file, "image/png")})
    print(res.status_code)
    assert res.status_code == 200
    # assert type(res.json()) == dict

    # with open(f"{path_data}/{name_zip}", "rb") as _file:
    #     res = testclient.post("/image/?test=1", files={"file": (name_zip, _file, "image/png")})
    # print(res)
    # assert res.status_code == 400

    pass


def test_zip():

    with open(f"{path_data}/{name_zip}", "rb") as _file:
        res = testclient.post("/zip?test=1", files={"file": (f"{name_zip}", _file, "application/zip")})
    print(res.status_code)
    assert res.status_code == 200
    assert type(res.json()) == dict

def test_files():

    with open(f"{path_data}/{name_zip}", "rb") as file_zip, \
         open(f"{path_data}/{name_image}", "rb") as file_image, \
         open(f"{path_data}/{name_video}", "rb") as file_video:

        files = [
            ('files', file_zip), \
            ('files', file_image), \
            ('files', file_video)
        ]
        res = testclient.post("/files?test=1", files=files)
        print(res.status_code)
        assert res.status_code == 200
        assert type(res.json()) == dict

if __name__ == "__main__":

    test_read_main()

    test_files()

    test_image()
    
    test_video()

    test_zip()
