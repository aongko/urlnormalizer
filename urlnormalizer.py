import argparse

class _UrlBuilder:
	def __init__(self):
		self.protocol = ''
		self.tld = ''
		self.paths = []

	def set_protocol(self, protocol):
		self.protocol = protocol

	def set_tld(self, tld):
		self.tld = tld

	def add_path(self, path):
		self.paths.append(path)

	def set_paths(self, paths):
		self.paths = paths

	def build(self):
		url = self.protocol + self.tld + '/'
		url += '/'.join(self.paths)
		return url

class InvalidUrlException(Exception):
	pass

def normalize_url(input_url):
	if not input_url.startswith('https://') and not input_url.startswith('http://'):
		raise InvalidUrlException('Missing protocol.')

	builder = _UrlBuilder()

	tld_start_idx = input_url.find('://') + 3
	tld_end_idx = len(input_url) - 1
	have_paths = input_url[tld_start_idx:].find('/') != -1
	if have_paths:
		tld_end_idx = tld_start_idx + input_url[tld_start_idx:].find('/') - 1
	tld = input_url[tld_start_idx:tld_end_idx + 1]
	builder.set_tld(tld)

	protocol = input_url[:tld_start_idx]
	builder.set_protocol(protocol)

	paths = []
	if have_paths:
		paths_start_idx = input_url.find(builder.build()) + len(builder.build())
		paths_section = input_url[paths_start_idx:]
		paths = paths_section.split('/')
		paths = [path for path in paths if len(path) > 0]
	builder.set_paths(paths)

	return builder.build()
