from pytest import raises

from urlnormalizer import normalize_url, InvalidUrlException, MalformatUrlException

def test_missing_scheme():
	with raises(MalformatUrlException) as ex:
		normalize_url('example.com')
	assert str(ex.value) == 'Missing scheme.'

def test_unsupported_scheme():
	with raises(InvalidUrlException) as ex:
		normalize_url('ftp://example.com')
	assert str(ex.value) == 'Unsupported scheme.'

def test_accept_http():
	assert normalize_url('http://example.com/') == 'http://example.com/'
	assert normalize_url('HTTP://example.com/') == 'http://example.com/'
	assert normalize_url('http://EXAMPLE.COM/') == 'http://example.com/'

def test_accept_https():
	assert normalize_url('https://example.com/') == 'https://example.com/'
	assert normalize_url('HTTPS://example.com/') == 'https://example.com/'
	assert normalize_url('https://EXAMPLE.COM/') == 'https://example.com/'

def test_url_without_path_should_have_trailing_slash():
	assert normalize_url('http://example.com') == 'http://example.com/'

def test_url_with_path_should_not_have_trailing_slash():
	assert normalize_url('http://example.com/part1/part2/') == \
		'http://example.com/part1/part2'

def test_safely_handle_params():
	assert normalize_url('http://example.com/part1/part2?q=query') == \
		'http://example.com/part1/part2?q=query'

def test_fragment_removed():
	assert normalize_url('http://example.com/#fragment') == \
		'http://example.com/'
