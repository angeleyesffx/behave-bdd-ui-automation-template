import json
from jsondiff import diff
from behave import *
from features.datapool import DATA_ACCESS
from features.pages.basepage import BasePage
import requests


@given(u'I get the endpoint from TokenAPI')
def get_token_endpoint(context):
    context.endpoint_token_api = f"{context.base_url}/authentication"


@given(u'I get the endpoint from HomeAPI')
@when(u'I get the endpoint from HomeAPI')
def get_home_endpoint(context):
    context.endpoint_home_api = f"{context.base_url}/home"


@when(u'the request sends POST to the TokenAPI')
def send_post_token_api_request(context):
    headers = {
        'x-os': 'android',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({"user": context.user, "password": context.password})
    context.response = requests.post(context.endpoint_token_api, data=payload, headers=headers)
    context.data = context.response.json()


@when(u'the request sends POST to the TokenAPI with invalid credentials')
def send_post_token_api_invalid_request(context):
    headers = {
        'x-os': 'android',
        'Content-Type': 'application/json',
    }
    email = BasePage.datapool_read(DATA_ACCESS, 'invalid_user', 'email')
    password = BasePage.datapool_read(DATA_ACCESS, 'invalid_user', 'password')
    payload = json.dumps({"user": email, "password": password})
    context.response = requests.post(context.endpoint_token_api, data=payload, headers=headers)


@when(u'the request sends GET to the HomeAPI')
def send_get_home_request(context):
    token = BasePage.find_value_json(context.data, "token")
    headers = {
        'x-token': f"{{{token}}}",
        'x-token-type': 'jwt',
        'x-os': 'android',
        'x-poc-id': '0000100002',
    }
    context.response = requests.get(context.endpoint_home_api, headers=headers)
    context.page = context.response.json()


@then(u'I should see the response')
def verify_api_response(context):
    with open('features/pages/api_example.json') as f:
        expected = json.load(f)
    result = diff(expected, context.page)
    assert not result, \
        f"Response from '{context.endpoint_home_api}' differs from expected fixture: {result}"
