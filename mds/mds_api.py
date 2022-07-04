import base64
import mds.http.helper
import requests
import urllib.parse
from doi_site.settings import DATACITE_URL, DATACITE_USER_NAME, DATACITE_PASSWORD, DOI_PREFIX, TIME_OUT


class MdsApiError(Exception):
    pass


class MdsApi:
    """
    This class handles GET, HEAD, PUT, POST and DELETE requests to the
    DataCite MDS API.

    An insance of the class must first be created, passing the DJango request
    to the constructor (the request is needed to check the user's allowed DOI
    sub-domains).

    POST, PUT and DELETE requests are checked to ensure they contain the
    site's DOI prefix and one of the user's DOI sub-domains. The request must
    therefore include the DOI in the URL.

    The arguments to the methods are the same as for the requests library.
    The methods return the response object from the requests libary.

    Example usage:
        from mds.mds_api import MdsApi

        mdsApi = MdsApi(request)
        r = mdsApi.get("/metadata/10.5438/0012")
    """

    def __init__(self, http_request):
        self._http_request = http_request


    def _authorise(self, url):
        parse_result = urllib.parse.urlparse(url)
        path = parse_result.path

        if path.startswith("/doi/"):
            doi = path[len("/doi/"):]
        elif path.startswith("/metadata/"):
            doi = path[len("/metadata/"):]
        elif path.startswith("/media/"):
            doi = path[len("/media/"):]
        else:
            raise MdsApiError("URL path must start with one of ['/doi/', '/metadata/', '/media/']")

        if not doi.startswith(DOI_PREFIX + "/"):
            raise MdsApiError("DOI prefix must be " + DOI_PREFIX + "/")

        doi_suffix = doi[len(DOI_PREFIX + "/"):]

        if not mds.http.helper.is_authorized(self._http_request, doi_suffix):
            raise MdsApiError("DOI not authorised: " + path)


    def _do_request(self, method, url, **kwargs):
        url = urllib.parse.urljoin(DATACITE_URL, url)

        kwargs.setdefault("headers", {})
        kwargs.setdefault("timeout", TIME_OUT)

        auth_string = (
            (base64.encodebytes((DATACITE_USER_NAME + ":" + DATACITE_PASSWORD).encode()))
            .decode("utf-8")
            .rstrip()
        )
        kwargs["headers"].update({"Authorization": "Basic " + auth_string})

        return requests.request(method, url, **kwargs)


    def get(self, url, params=None, **kwargs):
        return self._do_request('get', url, params=params, **kwargs)


    def head(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        return self._do_request('head', url, **kwargs)


    def post(self, url, data=None, json=None, **kwargs):
        self._authorise(url)
        return self._do_request('post', url, data=data, json=json, **kwargs)


    def put(self, url, data=None, **kwargs):
        self._authorise(url)
        return self._do_request('put', url, data=data, **kwargs)


    def delete(self, url, **kwargs):
        self._authorise(url)
        return self._do_request('delete', url, **kwargs)
