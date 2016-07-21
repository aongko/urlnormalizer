from pytest import raises

from urlnormalizer import normalize_url, InvalidUrlException

def test_missing_protocol():
	url = 'blog.jetbrains.com'
	with raises(InvalidUrlException) as ex:
		normalize_url(url)
	assert str(ex.value) == 'Missing protocol.'

def test_url_without_path_should_have_trailing_slash():
	url_without_trailing_slash = 'http://blog.jetbrains.com'
	result_without_trailing_slash = normalize_url(url_without_trailing_slash)
	assert result_without_trailing_slash == 'http://blog.jetbrains.com/'

	url_with_trailing_slash = 'http://blog.jetbrains.com/'
	result_with_trailing_slash = normalize_url(url_with_trailing_slash)
	assert result_with_trailing_slash == 'http://blog.jetbrains.com/'

def test_url_with_path_should_not_have_trailing_slash():
	url = 'http://blog.jetbrains.com/kotlin/feed/'
	result = normalize_url(url)
	assert result == 'http://blog.jetbrains.com/kotlin/feed'

def test_safely_handle_params():
	url = 'http://blog.jetbrains.com/kotlin/feed?utm_campaign=twitter'
	result = normalize_url(url)
	assert result == 'http://blog.jetbrains.com/kotlin/feed?utm_campaign=twitter'
