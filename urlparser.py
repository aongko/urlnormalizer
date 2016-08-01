import sys
if sys.version_info >= (3, 0):
	from urllib.parse import urlparse, parse_qsl
else:
	from urlparse import urlparse, parse_qsl


class Url(object):

	def __init__(self, builder):
		self._scheme = builder._scheme
		self._user = builder._user
		self._password = builder._password
		self._host = builder._host
		self._port = builder._port
		self._paths = builder._paths
		self._queries = builder._queries
		self._fragment = builder._fragment

	def get_scheme(self):
		return self._scheme

	def get_user(self):
		return self._user

	def get_password(self):
		return self._password

	def get_host(self):
		return self._host

	def get_port(self):
		return self._port

	def get_paths(self):
		return self._paths

	def get_queries(self):
		return self._queries

	def get_fragment(self):
		return self._fragment

	def get(self):
		url = self._scheme + '://'
		if self._user:
			url += self._user
			if self._password:
				url += ':' + self._password
			url += '@'
		url += self._host
		if self._port:
			url += ':' + str(self._port)
		url += '/'
		url += '/'.join(self._paths)
		if len(self._queries) > 0:
			url += '?'
			queries = []
			for query in self._queries:
				if len(query) == 1:
					queries.append('%s' % query)
				else:
					queries.append('%s=%s' % query)
			url += '&'.join(queries)
		if self._fragment:
			url += '#' + self._fragment
		return url

	def builder(self):
		return UrlBuilder(self)

class UrlBuilder(object):

	def __init__(self, url=None):
		self._scheme = None
		self._user = None
		self._password = None
		self._host = None
		self._port = None
		self._paths = []
		self._queries = []
		self._fragment = None

		if url:
			self._scheme = url.get_scheme()
			self._user = url.get_user()
			self._password = url.get_password()
			self._host = url.get_host()
			self._port = url.get_port()
			self._paths = url.get_paths()
			self._queries = url.get_queries()
			self._fragment = url.get_fragment()

	def set_scheme(self, scheme):
		self._scheme = scheme

	def set_user(self, user):
		self._user = user

	def set_password(self, password):
		self._password = password

	def set_host(self, host):
		self._host = host

	def set_port(self, port):
		self._port = port

	def set_paths(self, paths):
		self._paths = paths

	def set_queries(self, queries):
		self._queries = sorted(queries)

	def set_fragment(self, fragment):
		self._fragment = fragment

	def _validate(self):
		if self._scheme is None:
			return 'Missing scheme.'
		if self._host is None:
			return 'Missing host.'

	def build(self):
		err = self._validate()
		if err is not None:
			raise Exception(err)
		return Url(self)

def parse_string(url_string):
	builder = UrlBuilder()

	u = urlparse(url_string)
	scheme = u.scheme

	if not scheme:
		raise MalformatUrlException('Missing scheme.')
	builder.set_scheme(scheme)

	port = None
	try:
		port = u.port
	except ValueError:
		raise MalformatUrlException("Port must be a number.")

	builder.set_host(u.hostname)
	builder.set_port(port)
	builder.set_user(u.username)
	builder.set_password(u.password)

	path_section = u.path
	paths = [path for path in path_section.split('/') if path]
	builder.set_paths(paths)

	parsed_queries = []
	if u.query:
		queries = u.query.split('&')
		for query in queries:
			parsed_query = query.split('=')
			parsed_queries.append(tuple(parsed_query))

	builder.set_queries(parsed_queries)

	builder.set_fragment(u.fragment)

	return builder.build()

class MalformatUrlException(Exception):
	pass
