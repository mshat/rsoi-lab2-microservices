import requests


class UriPart:
    EXTRA_SUBSTRINGS = ('://', '/', ':', '?')

    def __init__(self, part, extra_substrings=EXTRA_SUBSTRINGS, left_service_substring='', right_service_substring=''):
        self.part = part
        self.clear_part(extra_substrings)
        if part and left_service_substring:
            self.left_add_substring(left_service_substring)
        if part and right_service_substring:
            self.right_add_substring(right_service_substring)

    def clear_part(self, extra_substrings):
        self.part = self.part.strip()
        if not extra_substrings:
            return
        for substring in extra_substrings:
            self.my_strip(substring)

    def left_add_substring(self, substring):
        self.part = substring + self.part

    def right_add_substring(self, substring):
        self.part += substring

    def my_strip(self, extra_substring):
        if self.part.startswith(extra_substring):
            self.part = self.part.replace(extra_substring, '', 1)
        if self.part.endswith(extra_substring):
            self.part = self.part[:-(len(extra_substring))]

    def __str__(self):
        return self.part


class Scheme(UriPart):
    def __init__(self, part, right_service_substring='://', **kwargs):
        super().__init__(part, right_service_substring=right_service_substring, **kwargs)


class Host(UriPart):
    def __init__(self, part, **kwargs):
        super().__init__(part, **kwargs)


class Port(UriPart):
    def __init__(self, part, left_service_substring=':', **kwargs):
        super().__init__(part, left_service_substring=left_service_substring, **kwargs)


class Path(UriPart):
    def __init__(self, part, left_service_substring='/', **kwargs):
        super().__init__(part, left_service_substring=left_service_substring, **kwargs)


class Query(UriPart):
    def __init__(self, part, left_service_substring='?', **kwargs):
        super().__init__(part, left_service_substring=left_service_substring, **kwargs)


class Uri:
    def __init__(self, scheme='http', host='127.0.0.1', port='8080', path='', query=''):
        self._scheme = Scheme(scheme)
        self._host = Host(host)
        self._port = Port(port)
        self._path = Path(path)
        self._query = Query(query)

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, val):
        self._scheme = Scheme(val)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, val):
        self._host = Host(val)

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val):
        self._port = Port(val)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        self._path = Path(val)

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, val):
        self._query = Query(val)

    def __str__(self):
        return f'{self.scheme}{self._host}{self._path}{self._query}'
        #return f'{self.scheme}{self._host}{self._port}{self._path}{self._query}'


class RequestsAdapter:
    def __init__(self, uri=None, scheme='http', host='127.0.0.1', port='', path='', query='', headers=None, data=None):
        if uri:
            self.uri = uri
        else:
            self._uri = Uri(scheme, host, port, path, query)
        self._headers = headers
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val: dict):
        self._data = val

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, val: dict):
        self._headers = val

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, val):
        if isinstance(val, Uri):
            self._uri = val
        else:
            raise Exception('Val is not Uri instance')

    def get(self):
        response = requests.get(str(self._uri), headers=self.headers, data=self.data)
        return response

    def post(self):
        response = requests.post(str(self._uri), headers=self.headers, data=self.data)
        return response

    def patch(self):
        response = requests.patch(str(self._uri), headers=self.headers, data=self.data)
        return response

    def delete(self):
        response = requests.delete(str(self._uri), headers=self.headers, data=self.data)
        return response
