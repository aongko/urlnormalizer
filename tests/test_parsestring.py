from pytest import raises

from urlparser import parse_string, MalformatUrlException

def test_malformat_url():
	with raises(MalformatUrlException) as ex:
		parse_string('example.com')
	assert str(ex.value) == 'Missing scheme.'

def test_simple_url():
	url = parse_string('http://example.com/')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get() == 'http://example.com/'

def test_host_is_ip():
	url = parse_string('http://203.0.113.1/')
	assert url.get_scheme() == 'http'
	assert url.get_host() == '203.0.113.1'
	assert url.get() == 'http://203.0.113.1/'

def test_simple_url_without_trailing_slash():
	url = parse_string('http://example.com')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get() == 'http://example.com/'

def test_url_with_user():
	url = parse_string('http://user@example.com/')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_user() == 'user'
	assert url.get() == 'http://user@example.com/'

def test_url_with_user_and_password():
	url = parse_string('http://user:password@example.com/')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_user() == 'user'
	assert url.get_password() == 'password'
	assert url.get() == 'http://user:password@example.com/'

def test_url_with_port():
	url = parse_string('http://example.com:8000/')
	assert url.get_port() == 8000

def test_url_with_nan_port():
	with raises(MalformatUrlException) as ex:
		parse_string('http://example.com:abcd/')
	assert str(ex.value) == 'Port must be a number.'

def test_url_with_path():
	url = parse_string('http://example.com/path')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_paths() == ['path']
	assert url.get() == 'http://example.com/path'

def test_url_with_path_and_trailing_slash():
	url = parse_string('http://example.com/path/')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_paths() == ['path']
	assert url.get() == 'http://example.com/path'

def test_url_with_paths():
	url = parse_string('http://example.com/path1/path2')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_paths() == ['path1', 'path2']
	assert url.get() == 'http://example.com/path1/path2'

def test_url_with_paths_and_trailing_slash():
	url = parse_string('http://example.com/path1/path2/')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_paths() == ['path1', 'path2']
	assert url.get() == 'http://example.com/path1/path2'

def test_url_with_query():
	url = parse_string('http://example.com/?q=query')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_queries() == [('q', 'query')]
	assert url.get() == 'http://example.com/?q=query'

def test_url_with_query_no_value():
	url = parse_string('http://example.com/?query')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_queries() == [('query',)]
	assert url.get() == 'http://example.com/?query'

def test_url_with_query_and_equal_sign_no_value():
	url = parse_string("http://example.com/?query=")
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_queries() == [('query', '')]
	assert url.get() == 'http://example.com/?query='

def test_url_with_queries():
	url = parse_string('http://example.com/?q=query&query')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_queries() == [('q', 'query'), ('query',)]
	assert url.get() == 'http://example.com/?q=query&query'

def test_url_with_fragment():
	url = parse_string('http://example.com/#fragment')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_fragment() == 'fragment'
	assert url.get() == 'http://example.com/#fragment'

def test_url_with_empty_fragment():
	url = parse_string('http://example.com/#')
	assert url.get_scheme() == 'http'
	assert url.get_host() == 'example.com'
	assert url.get_fragment() == ''
	assert url.get() == 'http://example.com/'

def test_url():
	url = parse_string('http://user:password@example.com/path1/path2?q=query&query#fragment')
	assert url.get_scheme() == 'http'
	assert url.get_user() == 'user'
	assert url.get_password() == 'password'
	assert url.get_host() == 'example.com'
	assert url.get_paths() == ['path1', 'path2']
	assert url.get_queries() == [('q', 'query'), ('query',)]
	assert url.get_fragment() == 'fragment'
	assert url.get() == 'http://user:password@example.com/path1/path2?q=query&query#fragment'
