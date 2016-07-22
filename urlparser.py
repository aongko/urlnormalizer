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
		self._queries = queries

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

	if url_string.find(':') == -1:
		raise MalformatUrlException('Missing scheme.')

	scheme = url_string[:url_string.find(':')]
	builder.set_scheme(scheme)

	host_section = url_string[len(scheme+'://'):]
	if url_string[len(scheme+'://'):].find('/') != -1:
		host_end = url_string[len(scheme+'://'):].find('/') + len(scheme+'://')
		host_section = url_string[len(scheme+'://'):host_end]
	host = host_section
	if host_section.find('@') != -1:
		host = host_section[host_section.find('@')+1:]
		user_section = host_section[:host_section.find('@')]
		user = user_section
		if user_section.find(':') != -1:
			user = user_section[:user_section.find(':')]
			password = user_section[user_section.find(':')+1:]
			builder.set_password(password)
		builder.set_user(user)
	if host.find(':') != -1:
		try:
			port = int(host[host.find(':')+1:])
		except ValueError:
			raise MalformatUrlException('Port must be a number.')
		builder.set_port(port)
	builder.set_host(host)

	path_section = url_string[url_string.find(host)+len(host):]
	if path_section.find('?') != -1:
		path_section = path_section[:path_section.find('?')]
	elif path_section.find('#') != -1 :
		path_section = path_section[:path_section.find('#')]
	paths = path_section.split('/')
	paths = [path for path in paths if len(path) > 0]
	builder.set_paths(paths)

	if url_string.find('?') != -1:
		query_section = url_string[url_string.find('?')+1:]
		if query_section.find('#') != -1:
			query_section = query_section[:query_section.find('#')]
		queries = query_section.split('&')
		parsed_queries = []
		for query in queries:
			parsed_query = query.split('=')
			parsed_queries.append(tuple(parsed_query))
		builder.set_queries(parsed_queries)

	fragment_section = url_string[url_string.find('#'):]
	fragment = fragment_section[1:]
	builder.set_fragment(fragment)

	return builder.build()

class MalformatUrlException(Exception):
	pass
