import requests.api
from requests.auth import HTTPBasicAuth

from amqpstorm.compatibility import urlparse
from amqpstorm.management.exception import ApiConnectionError
from amqpstorm.management.exception import ApiError


class HTTPClient(object):
    def __init__(self, api_url, username, password, timeout):
        self._auth = HTTPBasicAuth(username, password)
        self._timeout = timeout
        self._base_url = api_url

    def get(self, path, payload=None, headers=None):
        """HTTP GET operation.

        :param path: URI Path
        :param payload: HTTP Body
        :param headers: HTTP Headers

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :return: Response
        """
        return self._request('get', path, payload, headers)

    def post(self, path, payload=None, headers=None):
        """HTTP POST operation.

        :param path: URI Path
        :param payload: HTTP Body
        :param headers: HTTP Headers

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :return: Response
        """
        return self._request('post', path, payload, headers)

    def delete(self, path, payload=None, headers=None):
        """HTTP DELETE operation.

        :param path: URI Path
        :param payload: HTTP Body
        :param headers: HTTP Headers

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :return: Response
        """
        return self._request('delete', path, payload, headers)

    def put(self, path, payload=None, headers=None):
        """HTTP PUT operation.

        :param path: URI Path
        :param payload: HTTP Body
        :param headers: HTTP Headers

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :return: Response
        """
        return self._request('put', path, payload, headers)

    def _request(self, method, path, payload=None, headers=None):
        """HTTP operation.

        :param method: Operation type (e.g. post)
        :param path: URI Path
        :param payload: HTTP Body
        :param headers: HTTP Headers

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :return: Response
        """
        url = urlparse.urljoin(self._base_url, 'api/%s' % path)
        headers = headers or {}
        headers['content-type'] = 'application/json'
        try:
            response = requests.request(method, url,
                                        auth=self._auth, data=payload,
                                        headers=headers,
                                        timeout=self._timeout)
        except requests.RequestException as why:
            raise ApiConnectionError(str(why))

        json_response = self._get_json_output(response)
        self._check_for_errors(response, json_response)
        return json_response

    @staticmethod
    def _get_json_output(response):
        """Get JSON output from the HTTP response.

        :param requests.Response response:

        :return: Json payload
        """
        try:
            content = response.json()
        except ValueError:
            content = None
        return content

    @staticmethod
    def _check_for_errors(response, json_response):
        """Check payload for errors.

        :param response: HTTP response
        :param json_response: Json response

        :raises ApiError: Raises if the remote server encountered an error.

        :return:
        """
        status_code = response.status_code
        try:
            response.raise_for_status()
        except requests.HTTPError as why:
            raise ApiError(str(why), reply_code=status_code)
        if isinstance(json_response, dict) and 'error' in json_response:
            raise ApiError(json_response['error'], reply_code=status_code)
