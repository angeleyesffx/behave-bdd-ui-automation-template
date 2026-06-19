from behave import *
from features.pages.basepage import BasePage
import requests


@given(u'a request to the API')
def _endpoint(context):
    pass


@then(u'the response status is {code_status}')
def response_status(context, code_status):
    expected = int(code_status)
    actual = context.response.status_code
    assert actual == expected, \
        f"Expected HTTP {expected} but received HTTP {actual}"


@then(u'the response should content the key {key}')
def response_content_key(context, key):
    found = BasePage.key_exists(context, key)
    assert found is True, \
        f"Expected key '{key}' in response but it was not found"


@then(u'the response should content a key {key} with the value {value}')
def response_content_key_with_value(context, key, value):
    result = BasePage.value_is_correct(context, key, value)
    assert result is True, \
        f"Expected key '{key}' to have value '{value}' but value was different or key was not found"


@then(u'the response should content a key {key} with some value different the null')
def response_content_key_different_null(context, key):
    value = context.json[key]
    assert value is not None, \
        f"Expected key '{key}' to have a non-null value but got None"
