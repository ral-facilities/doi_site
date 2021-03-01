import codecs
from os.path import join
import socket
import urllib.request

from test.system import AUTH_STRING, DATA_DIR, DOI, HOST, TIME_OUT


def _post(url, body, content_type):
    _set_timeout()
    opener = urllib.request.build_opener()
    headers = {"Content-Type": content_type, "Authorization": "Basic " + AUTH_STRING}

    body_encoded = body.encode("utf-8").strip()
    req = urllib.request.Request(url, data=body_encoded, headers=headers)
    try:
        response = opener.open(req)
    finally:
        _close(opener)
    return response


def _set_timeout():
    """
    Set the time out used by urllib.
    """
    socket.setdefaulttimeout(TIME_OUT)


def _close(opener):
    try:
        opener.close()
    # pylint: disable=bare-except
    except:
        pass


def test():

    # POST metadata
    # read in metadata
    body_unicade = codecs.open(
        join(DATA_DIR, "meta_body.xml"),
        "r",
        encoding="utf-8",
    ).read()
    response = _post(HOST + "/metadata", body_unicade, "application/xml;charset=UTF-8")
    print(f"post metadata\nreturn code:{response.code}\n{response.readlines()}\n")

    # POST DOI
    # read in doi
    body_unicade = (
        codecs.open(
            join(DATA_DIR, "doi_body"),
            "r",
            encoding="utf-8",
        )
        .read()
        .strip()
    )
    response = _post(HOST + "/doi", body_unicade, "text/plain;charset=UTF-8")
    print(f"post doi\nreturn code:{response.code}\n{response.readlines()}\n")

    # POST media
    # read in media
    body_unicade = codecs.open(
        join(DATA_DIR, "media_body"),
        "r",
        encoding="utf-8",
    ).read()
    response = _post(HOST + "/media/" + DOI, body_unicade, "text/plain;charset=UTF-8")
    print(f"post media/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")


if __name__ == "__main__":
    test()
