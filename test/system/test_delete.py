import socket
import urllib.request

from test.system import AUTH_STRING, DOI, HOST, TIME_OUT


def _delete(url, headers):
    _set_timeout()
    opener = urllib.request.build_opener()
    req = urllib.request.Request(url, data=None, headers=headers)
    req.get_method = lambda: "DELETE"
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

    # DELETE metadata
    response = _delete(HOST + "/metadata/" + DOI, auth_header)
    print(
        f"delete metadata/{DOI}\nreturn code:{response.code}\n{response.readlines()}\n"
    )


if __name__ == "__main__":
    test()
