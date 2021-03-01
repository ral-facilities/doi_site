import socket
import urllib.request

from test.system import AUTH_STRING, DOI, HOST, TIME_OUT


def _head(url, headers):
    _set_timeout()
    opener = urllib.request.build_opener()
    req = urllib.request.Request(url, None, headers)
    req.get_method = lambda: "HEAD"
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
    response = _head(HOST + "/metadata/" + DOI, matadata_headers)
    print(f"head metadata/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")

    # GET all dois
    response = _head(HOST + "/doi", auth_header)
    print(f"head doi\nreturn code:{response.code}\n{response.readlines()}\n")

    # GET one doi
    response = _head(HOST + "/doi/" + DOI, auth_header)
    print(f"head doi/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")

    # GET media
    response = _head(HOST + "/media/" + DOI, auth_header)
    print(f"head media/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n")


if __name__ == "__main__":
    test()
