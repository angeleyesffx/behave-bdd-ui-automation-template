import json
import os

from behave import *
from features.steps.data_source.other_datasource import new_information
from features.pages.basepage import BasePage
from requests.auth import HTTPBasicAuth
import requests
import xml.etree.ElementTree as ET


@given(u'a request to the Some API')
def get_some_endpoint(context):
    context.endpoint_some_api = f"{context.some_api_url}/Some_path"


@given(u'a request to the Whatever API')
def get_whatever_endpoint(context):
    context.endpoint_whatever = f"{context.whatever_api}/Whatever_path"


@when(u'the request sends POST to the Whatever API')
def send_post_whatever_request(context):
    payload_whatever = BasePage.read_xml_file(
        os.path.join(os.path.dirname(__file__), 'data_source', 'whatever.xml')
    )
    context.response_whatever = requests.post(
        context.endpoint_whatever,
        auth=HTTPBasicAuth(context.username_whatever_api, context.password_whatever_api),
        data=payload_whatever,
        headers={'Content-Type': 'text/xml'},
        verify=False,
    )


@when(u'the request sends POST to the Some API')
def send_post_some_request(context):
    payload_some = BasePage.read_xml_file(
        os.path.join(os.path.dirname(__file__), 'data_source', 'some.xml')
    )
    context.response = requests.post(
        context.endpoint_some_api,
        auth=HTTPBasicAuth(context.username_some_api, context.password_some_api),
        data=payload_some,
        headers={'Content-Type': 'text/xml'},
        verify=False,
    )


@when(u'the request sends POST to the Other API')
def send_post_other_request(context):
    json_path = os.path.join(os.path.dirname(__file__), 'data_source', 'other_payloads.json')
    new_information.update({'other_id': context.other_id, 'another_id': context.another_id})
    json_file = BasePage.edit_json(json_path, new_information)
    payload = json.loads(json_file[0])
    context.response = requests.post(context.endpoint_whatever, json=payload)
    context.json = context.response.json()


@then(u'the response form Some API should be equal on API Whatever')
def compare_some_and_whatever_responses(context):
    some_value = BasePage.find_value_on_xml(context.response, 'some_tag_key_xml', context.endpoint_some_api)
    whatever_value = BasePage.find_value_on_xml(context.response_whatever, 'some_tag_key_xml', context.endpoint_whatever)
    assert some_value == whatever_value


@then(u'the wrong password message should be received')
def wrong_password_auth_message(context):
    assert context.json['status']['message'].rsplit(' ', 1)[0] == 'Wrong Password for Login ID:'


@then(u'the wrong user message should be received')
def wrong_user_auth_message(context):
    message = context.json['status']['message']
    assert message.startswith('Login ') and message.endswith(' not in system')
