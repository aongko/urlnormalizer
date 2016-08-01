from urlparser import parse_string, MalformatUrlException

supported_schemes = ['http', 'https']

def _validate_url(url):
	if url.get_scheme().lower() not in supported_schemes:
		raise InvalidUrlException('Unsupported scheme.')

def normalize_url(input_url):
	url = parse_string(input_url)
	try:
		_validate_url(url)
	except MalformatUrlException as ex:
		raise ex
	builder = url.builder()
	builder.set_scheme(url.get_scheme().lower())
	host = url.get_host().lower()
	if host.endswith("."):
		host = host[:-1]
	builder.set_host(host)
	builder.set_fragment(None)
	return builder.build().get()

class InvalidUrlException(Exception):
	pass
