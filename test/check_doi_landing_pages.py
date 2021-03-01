"""
This script will contact DataCite and retrieve a list of all minted DOIs.
It will then check that all the landing pages exist.

"""
import base64
from getpass import getpass
import socket
import sys
import urllib.error
from urllib.parse import urljoin
import urllib.request


TIME_OUT = 60
HOST = "https://doi.stfc.ac.uk"


def _get(url_, auth_string=None):
    socket.setdefaulttimeout(TIME_OUT)
    opener = urllib.request.build_opener()
    headers = {}

    if auth_string is not None:
        headers = {"Authorization": "Basic " + auth_string}
    req = urllib.request.Request(url_, None, headers)

    try:
        response = opener.open(req)
    finally:
        _close(opener)

    return response


def _close(opener):
    try:
        opener.close()
    # pylint: disable=bare-except
    except:
        pass


def _get_dois(auth_string):
    """
    Get a list of all of the DOIs.

    """
    url_ = urljoin(HOST, "doi")

    try:
        response = _get(url_, auth_string)
    except urllib.error.URLError as ex:
        print(f"URLError trying to get list of DOIs from {url_}\n{ex}")
        sys.exit(1)

    dois = []

    for line in response:
        if line != "":
            dois.append(line.strip().decode("ISO-8859-1"))

    return dois


def _check_doi(auth_string, doi):
    """
    Check the landing page for the DOI.

    """
    query_uri = urljoin(HOST, "doi/" + doi)

    try:
        response = _get(query_uri, auth_string)
    except urllib.error.URLError as ex:
        print(f"URLError from {query_uri} for doi {doi}\n{ex}")
        return

    for line in response:
        url_ = line.decode("utf-8")
        landing_page = None

        try:
            landing_page = _get(url_)

        except urllib.error.HTTPError as ex:
            if ex.code == 404:
                print(f"Landing page {url_} for doi {doi} not found\n")
            else:
                print(f"HTTPError error from landing page {url_} for doi {doi}\n{ex}")
            continue

        except urllib.error.URLError as ex:
            print(f"URLError from landing page {url_} for doi {doi}\n{ex}")
            continue
        # pylint: disable=broad-except

        except Exception as ex:
            print(f"Unexpected error from landing page {url_} for doi {doi}\n{ex}")
            continue

        if landing_page is not None and landing_page.code != 200:
            print(
                f"Unexpected return code {landing_page.code}, from landing page {url_} "
                "for doi {doi}\n"
            )


def main(username, password):
    auth_string = (
        (base64.encodebytes(f"{username}:{password}".encode())).rstrip().decode("utf-8")
    )
    dois = _get_dois(auth_string)

    for doi in dois:
        _check_doi(auth_string, doi)

    print("\nDOI check finished\n")


if __name__ == "__main__":
    print("Enter credentials")
    USERNAME = input("Username: ")
    PASSWORD = getpass()
    main(USERNAME, PASSWORD)
