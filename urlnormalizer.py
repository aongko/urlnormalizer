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

	# remove utm parameters
	# https://support.google.com/analytics/answer/1033867
	blacklist = ['utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_campaign']
	queries = filter(lambda x: x[0] not in blacklist, url.get_queries())
	builder.set_queries(queries)

	return builder.build().get()

class InvalidUrlException(Exception):
	pass
