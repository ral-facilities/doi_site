import socket
import urllib.request

from test.system import AUTH_STRING, DOI, HOST, TIME_OUT


def _get(url, headers):
    _set_timeout()
    opener = urllib.request.build_opener()
    req = urllib.request.Request(url, None, headers)
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
    auth_header = {"Authorization": "Basic " + AUTH_STRING}

    # GET metadata
    matadata_headers = {"Accept": "application/xml"}
    matadata_headers.update(auth_header)
    response = _get(HOST + "/metadata/" + DOI, matadata_headers)
    print(f"get metadata/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")

    # GET all dois
    response = _get(HOST + "/doi", auth_header)
    print(f"get doi\nreturn code:{response.code}\n{response.readlines()}\n")

    # GET one doi
    response = _get(HOST + "/doi/" + DOI, auth_header)
    print(f"get doi/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")

    # GET media
    response = _get(HOST + "/media/" + DOI, auth_header)
    print(f"get media/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")


if __name__ == "__main__":
    test()
