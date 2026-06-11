import json
import random
import string
import time
import xml.dom.minidom as DOM
import xml.etree.ElementTree as ET
import pymysql
import os
import yaml
import requests
import csv

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: time.sleep(time_s))
        return self


class BasePage(object):

    def __init__(self, driver, base_url=None):
        self.driver = driver
        self.base_url = base_url
        self.timeout = 20
        self.implicit_wait = 20

    # -- String Functions --

    @staticmethod
    def generate_unique_id(chars_number):
        """Generate N-char random alphanumeric string (mixed case)."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=chars_number))

    @staticmethod
    def generate_unique_lowercase_id(chars_number):
        """Generate N-char random alphanumeric string (lowercase)."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=chars_number))

    @staticmethod
    def generate_unique_uppercase_id(chars_number):
        """Generate N-char random alphanumeric string (uppercase)."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=chars_number))

    @staticmethod
    def generate_unique_email(username, id, domain_list):
        """Combine username, id and a random domain from domain_list into an email address."""
        return username + '.' + id + random.choice(domain_list)

    @staticmethod
    def split_string_between(string_value, slice_a, slice_b):
        """Return the substring between the first occurrence of slice_a and the last of slice_b."""
        pos_a = string_value.find(slice_a)
        if pos_a == -1:
            return ""
        pos_b = string_value.rfind(slice_b)
        if pos_b == -1:
            return ""
        adjusted_pos_a = pos_a + len(slice_a)
        if adjusted_pos_a >= pos_b:
            return ""
        return string_value[adjusted_pos_a:pos_b]

    @staticmethod
    def split_string_before(string_value, slice_a):
        """Return the substring before the first occurrence of slice_a."""
        pos_a = string_value.find(slice_a)
        if pos_a == -1:
            return ""
        return string_value[0:pos_a]

    @staticmethod
    def split_string_after(string_value, slice_a):
        """Return the substring after the last occurrence of slice_a."""
        pos_a = string_value.rfind(slice_a)
        if pos_a == -1:
            return ""
        adjusted_pos_a = pos_a + len(slice_a)
        if adjusted_pos_a >= len(string_value):
            return ""
        return string_value[adjusted_pos_a:]

    @staticmethod
    def remove_chars_from_string(string_value, char_list):
        """Remove every character in char_list from string_value."""
        new_string = string_value
        for char in char_list:
            new_string = new_string.replace(char, "")
        return new_string

    @staticmethod
    def replace_string_with(string_value, old_string, new_string):
        return string_value.replace(old_string, new_string)

    @staticmethod
    def empty_string_to_none_string(string_value):
        if string_value == '':
            return None
        return string_value

    @staticmethod
    def get_string_around(string_value, slice_a, slice_b):
        string_a = BasePage.split_string_before(string_value, slice_a)
        string_b = BasePage.split_string_after(string_value, slice_b)
        return string_a.rstrip() + string_b.rstrip()

    # -- Database Functions --

    @staticmethod
    def open_connection_with_database(host, port, username, password, database):
        try:
            return pymysql.connect(
                host=host, port=port, user=username, passwd=password, db=database,
                cursorclass=pymysql.cursors.DictCursor, autocommit=True
            )
        except Exception:
            print(f"Error connecting to MySQL database '{database}'.")

    @staticmethod
    def execute_query(db_connection, sql_query):
        try:
            with db_connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                db_connection.commit()
        finally:
            db_connection.close()
        return result

    @staticmethod
    def get_entire_result_from_executed_query(host, port, username, password, database, sql_query):
        connection = BasePage.open_connection_with_database(host, port, username, password, database)
        return BasePage.execute_query(connection, sql_query)

    @staticmethod
    def execute_query_from_db(host, port, username, password, database, sql_query):
        connection = BasePage.open_connection_with_database(host, port, username, password, database)
        return BasePage.execute_query(connection, sql_query)

    @staticmethod
    def select_all_from_table(db_connection, table):
        sql_query = f"SELECT * FROM {table}"
        db_connection.execute(sql_query)
        return db_connection.fetchall()

    @staticmethod
    def close_connection_database(db_connection):
        db_connection.close()

    # -- DataPool Functions --

    @staticmethod
    def get_columns_from_dict(source, args_key):
        """Return a comma-separated string of column names from a dict entry in source."""
        data_args = source.get(args_key.replace(' ', '_'))
        if data_args is None:
            raise Exception(f"No matching results for parameter data = '{args_key}' in DataPool.")
        return ', '.join(data_args[0].keys())

    @staticmethod
    def datapool_read(source, data, key):
        """Return the value at 'key' from the 'data' collection in 'source'."""
        data_args = source.get(data.replace(' ', '_'))
        dt_key = key.replace(' ', '_')
        if data_args is None:
            raise Exception(f"No matching results for data = '{data}', key = '{key}' in DataPool.")
        value = data_args.get(dt_key)
        if value is None:
            raise Exception(f"No matching results for data = '{data}', key = '{key}' in DataPool.")
        return value

    @staticmethod
    def read_yml_file(yml_path):
        with open(yml_path) as file:
            return yaml.full_load(file)

    @staticmethod
    def select_the_keys_from_yml(yml_path, parent_reference):
        environments = BasePage.read_yml_file(yml_path)
        if parent_reference == "environment":
            return sorted(environments.keys())
        params = set()
        for key in environments.keys():
            params.update(environments[key])
        return sorted(params)

    # -- List Functions --

    @staticmethod
    def union_list_without_duplicate_item(list_a, list_b):
        result_list = list(list_a)
        result_list.extend(x for x in list_b if x not in result_list)
        return result_list

    @staticmethod
    def intersection_list(list_a, list_b):
        return [list(filter(lambda x: x in list_a, sublist)) for sublist in list_b]

    @staticmethod
    def remove_item_from_list(lst, item):
        return [x for x in lst if x != item]

    @staticmethod
    def get_random_item_from_list(lst):
        return random.choice(lst)

    @staticmethod
    def get_different_random_item_from_list(lst, item):
        result_list = [x for x in lst if x != item]
        return random.choice(result_list)

    @staticmethod
    def get_list_from_source(source, data):
        """Return the list named 'data' from 'source'."""
        data_args = source.get(data.replace(' ', '_'))
        if data_args is None:
            raise Exception(f"No matching results for parameter data = '{data}' in DataPool.")
        return data_args[0]

    @staticmethod
    def get_data_from_dict(dict_args, key):
        """Return the value at 'key' from dict_args."""
        if dict_args is None:
            raise Exception(f"No matching results for key = '{key}' in Dictionary.")
        value = dict_args.get(key)
        if value is None:
            raise Exception(f"No matching results for key = '{key}' in Dictionary.")
        return value

    # -- UI Functions --

    @staticmethod
    def page_has_loaded(driver):
        page_state = driver.execute_script('return document.readyState;')
        if page_state != 'complete':
            raise Exception("Page didn't finish loading or took too long.")

    @staticmethod
    def element_exists(driver, timeout, selector_type, element):
        """Return True if element is present within timeout, False otherwise."""
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((selector_type, element))
            )
        except (TimeoutException, NoSuchElementException):
            return False
        return True

    @staticmethod
    def fast_element_exists(driver, selector_type, element):
        """Return True if element is immediately present, False otherwise."""
        try:
            driver.find_element(selector_type, element)
        except NoSuchElementException:
            return False
        return True

    @staticmethod
    def locate_element(driver, timeout, selector_type, element):
        """Wait up to timeout seconds and return the element, raising Exception if not found."""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((selector_type, element))
            )
        except TimeoutException:
            raise Exception(
                f"Element '{element}' with selector type '{selector_type}' not found on screen."
            )

    @staticmethod
    def get_the_ancestor_element(element, parent_xpath):
        try:
            return element.find_element(By.XPATH, f"ancestor::{parent_xpath}")
        except (TimeoutException, NoSuchElementException):
            raise Exception("Ancestor element not found on screen.")

    @staticmethod
    def wait_until_disappears(driver, timeout_to_be_visible, timeout_to_be_invisible, selector_type, element):
        """Wait for element to appear then disappear. Returns True on success, False on timeout."""
        try:
            if BasePage.element_exists(driver, timeout_to_be_visible, selector_type, element):
                WebDriverWait(driver, timeout_to_be_invisible).until_not(
                    EC.presence_of_element_located((selector_type, element))
                )
            else:
                raise Exception(
                    f"Element '{element}' with type '{selector_type}' not found on screen."
                )
        except TimeoutException:
            return False
        return True

    @staticmethod
    def wait_for_element(driver, timeout_to_be_visible, selector_type, element):
        """Wait until element is visible. Returns True on success, False on timeout."""
        try:
            WebDriverWait(driver, timeout_to_be_visible).until(
                EC.visibility_of_element_located((selector_type, element))
            )
        except TimeoutException:
            return False
        return True

    @staticmethod
    def verify_element_list(driver, timeout, element_list):
        """Assert every element in element_list is present and optionally matches expected text."""
        fail_results = []
        for key in element_list:
            element = BasePage.get_data_from_dict(key, "element")
            selector_type = BasePage.get_data_from_dict(key, "type")
            text_expected = BasePage.get_data_from_dict(key, "text_expected")
            if not BasePage.element_exists(driver, timeout, selector_type, element):
                fail_results.append(f"Element '{element}' not found on screen.")
            elif text_expected:
                text_obtained = BasePage.locate_element(driver, timeout, selector_type, element).text
                if text_obtained != text_expected:
                    fail_results.append(
                        f"Expected '{text_expected}' on '{element}', got '{text_obtained}'."
                    )
        if fail_results:
            raise Exception(fail_results)

    @staticmethod
    def get_element_from_list(driver, selector_type, element_list, attribute, expected_attribute_content):
        elements = driver.find_elements(selector_type, element_list)
        for element in elements:
            if element.get_attribute(attribute) == expected_attribute_content:
                return element

    @staticmethod
    def get_list_without_an_element(driver, selector_type, element_list, attribute, expected_attribute_content):
        elements = driver.find_elements(selector_type, element_list)
        result_list = [e for e in elements if e.get_attribute(attribute) != expected_attribute_content]
        if not result_list:
            raise Exception("The provided list is empty or no matching elements were found.")
        return result_list

    @staticmethod
    def select_option_from_dropdown_list(driver, selector_type, dropdown_element, attribute,
                                         expected_attribute_content):
        element_found = BasePage.locate_element(driver, 10, selector_type, dropdown_element)
        options_list = element_found.find_elements(By.TAG_NAME, 'option')
        for option in options_list:
            if option.get_attribute(attribute) == expected_attribute_content:
                option.click()

    # -- XML Functions --

    @staticmethod
    def read_xml_file(xml_file):
        """Open and return the raw content of an XML file."""
        with open(xml_file, 'r', encoding='utf8') as xml:
            return xml.read()

    @staticmethod
    def beautify_xml(element):
        """Return a pretty-printed XML string."""
        element_content = element
        if not isinstance(element_content, (bytes, str)):
            element_content = element.content.decode("utf-8")
        reparsed = DOM.parseString(element_content)
        return '\n'.join(
            line for line in reparsed.toprettyxml(indent=' ' * 2).split('\n') if line.strip()
        )

    @staticmethod
    def verify_responses_status(response, request):
        if str(response) != '<Response [500]>':
            return True
        print("Request used:\n", request)
        print("Obtained Response:\n", BasePage.beautify_xml(response.content))
        raise Exception(
            f"Status {response}. System disabled, suspended, or request badly formatted."
        )

    @staticmethod
    def get_xml_root(response, endpoint):
        """Parse response or string as XML and return the root Element."""
        response_content = response
        if not isinstance(response_content, (bytes, str)):
            response_content = response.content.decode("utf-8")
        try:
            return ET.fromstring(response_content)
        except ET.ParseError as err:
            error = BasePage.split_string_before(str(err), ": line ")
            if error == 'not well-formed (invalid token)':
                raise Exception(f"XML parse error. Check the endpoint: {endpoint}")
            raise

    @staticmethod
    def count_blocks_by_id_tag_on_xml(response, tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        return sum(1 for _ in response_root.findall('.//' + tag))

    @staticmethod
    def find_value_on_xml(response, tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        for element in response_root.iterfind('.//' + tag):
            return element.text

    @staticmethod
    def find_values_inside_blocks_on_xml(response, tag, endpoint):
        values_list = []
        position = 1
        response_root = BasePage.get_xml_root(response, endpoint)
        for data_block in response_root.findall('.//' + tag):
            for element in data_block.iter():
                values_list.append([position, element.tag, element.text])
            position += 1
        return values_list

    @staticmethod
    def get_data_from_tag_parent_list(tag_parent_list, tag_name, tag_value):
        """Return all tag/value pairs from the block matching tag_name == tag_value."""
        index = None
        for elem in tag_parent_list:
            if tag_name == elem[1] and tag_value == elem[2]:
                index = elem[0]
        if index is None:
            return []
        return [[e[1], e[2]] for e in tag_parent_list if e[0] == index]

    @staticmethod
    def remove_tag_from_xml_response(response, parent_tag, child_tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        for child in response_root.findall(parent_tag):
            for element in child.findall(child_tag):
                child.remove(element)
        return response_root

    @staticmethod
    def remove_closed_tag_from_xml_response(response, closed_tag, closed_child_tag, parent_tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        for child in response_root.findall(closed_tag):
            for _ in child.findall(closed_child_tag):
                return response_root
        return BasePage.remove_tag_from_xml_response(response, parent_tag, closed_tag, endpoint)

    @staticmethod
    def tag_exists_on_xml(response, tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        for _ in response_root.iterfind('.//' + tag):
            return True
        return False

    @staticmethod
    def tag_list_exists_on_xml(response, tag_list, endpoint):
        for tag in tag_list.values():
            if not BasePage.tag_exists_on_xml(response, tag, endpoint):
                return False
        return True

    @staticmethod
    def tag_list_is_on_xml(response, tag_list, namespace, endpoint):
        for tag in tag_list.values():
            if not BasePage.tag_exists_on_xml(response, tag, endpoint):
                raise Exception(
                    f"Tag <{tag.replace(namespace, '')}> was not found in the XML response."
                )

    @staticmethod
    def verify_hit(response, tag_list, endpoint):
        for tag in tag_list.values():
            if BasePage.tag_exists_on_xml(response, tag, endpoint):
                return True
        return False

    @staticmethod
    def confirm_persistence_of_response_in_different_sources(
        source_a, source_b, args, namespace_a, namespace_b,
        source_name_a, source_name_b, endpoint_a, endpoint_b
    ):
        fail_list = []
        for key in args.items():
            item_a = BasePage.find_value_on_xml(source_a, key[1], endpoint_a)
            item_b = BasePage.find_value_on_xml(source_b, key[1], endpoint_b)
            if item_a != item_b:
                fail_list.append(
                    f"{source_name_a} {key[1].replace(namespace_a, '')} = {item_a} "
                    f"vs {source_name_b} {key[1].replace(namespace_b, '')} = {item_b} — mismatch."
                )
        if fail_list:
            print(*fail_list, sep="\n")
            raise Exception("End of Fail List")

    @staticmethod
    def compare_values_from_two_xml(
        xml_a, xml_b, args_a, args_b, namespace_a, namespace_b,
        source_name_a, source_name_b, endpoint_a, endpoint_b
    ):
        fail_list = []
        while True:
            key_a = args_a.popitem()
            key_b = args_b.popitem()
            item_a = BasePage.find_value_on_xml(xml_a, key_a[1], endpoint_a)
            item_b = BasePage.find_value_on_xml(xml_b, key_b[1], endpoint_b)
            if item_a != item_b:
                fail_list.append(
                    f"{source_name_a} {key_a[1].replace(namespace_a, '')} = {item_a} "
                    f"vs {source_name_b} {key_b[1].replace(namespace_b, '')} = {item_b} — mismatch."
                )
            if not args_a or not args_b:
                break
        if fail_list:
            print(*fail_list, sep="\n")
            raise Exception("End of Fail List")

    @staticmethod
    def list_all_paths_on_xml_starting_from_node(path_list, response_root, start_path, namespace, node_name):
        for element in response_root:
            element_name = ET.QName(element.tag)
            parent = element_name.text.strip().lstrip(namespace)
            new_path = start_path + "/" + parent
            if list(element):
                BasePage.list_all_paths_on_xml_starting_from_node(
                    path_list, element, new_path, namespace, node_name
                )
            path = BasePage.split_string_after(new_path, node_name)
            if path:
                path_list.append(path)
        return path_list

    @staticmethod
    def list_all_full_paths_on_xml(path_list, response_root, start_path, namespace):
        for element in response_root:
            element_name = ET.QName(element.tag)
            parent = element_name.text.strip().lstrip(namespace)
            new_path = start_path + "/" + parent
            if list(element):
                BasePage.list_all_full_paths_on_xml(path_list, element, new_path, namespace)
            path_list.append(new_path)
        return path_list

    @staticmethod
    def compare_pathlist_from_two_xml_responses(
        context, system_name_a, system_name_b, response_a, response_b,
        namespace_a, namespace_b, node_name_a, node_name_b, endpoint_a, endpoint_b
    ):
        xml_root_a = BasePage.get_xml_root(response_a, endpoint_a)
        xml_root_b = BasePage.get_xml_root(response_b, endpoint_b)
        path_list_a = BasePage.list_all_paths_on_xml_starting_from_node(
            [], xml_root_a, "", namespace_a, node_name_a
        )
        path_list_b = BasePage.list_all_paths_on_xml_starting_from_node(
            [], xml_root_b, "", namespace_b, node_name_b
        )
        print(f"\nPath count — {system_name_a}: {len(path_list_a)}, {system_name_b}: {len(path_list_b)}")

        divergent_paths = sorted(set(path_list_a).symmetric_difference(set(path_list_b)))
        if not divergent_paths:
            return

        result_a = [p for p in path_list_a if p not in path_list_b]
        result_b = [p for p in path_list_b if p not in path_list_a]
        print(f"Total divergent: {len(divergent_paths)}", *divergent_paths, sep="\n")
        print(f"\n{system_name_a} only ({len(result_a)}):", *result_a, sep="\n")
        print(f"\n{system_name_b} only ({len(result_b)}):", *result_b, sep="\n")
        raise Exception("End of Divergent Paths Report")

    # -- JSON Functions --

    @staticmethod
    def load_json(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def load_json_as_string(json_file_path):
        with open(json_file_path, 'r') as file:
            return file.read()

    @staticmethod
    def load_json_as_dict(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def get_json_keys(json_file_path):
        return BasePage.load_json_as_dict(json_file_path).keys()

    @staticmethod
    def get_json_values(json_file_path):
        return BasePage.load_json_as_dict(json_file_path).values()

    @staticmethod
    def write_json_as_string(json_data):
        return json.dumps(json_data, sort_keys=True)

    @staticmethod
    def write_json_as_dict(json_data):
        return json.dumps(json_data, sort_keys=True)

    @staticmethod
    def key_exists(context, key):
        return BasePage.find_key_on_json(context.json, key) == key

    @staticmethod
    def value_is_correct(context, key, value):
        if value == 'null':
            value = None
        if not BasePage.key_exists(context, key):
            return False
        return context.json.get(key) == value

    @staticmethod
    def find_value_json(obj, key):
        if isinstance(obj, dict):
            if key in obj:
                return obj[key]
            for v in obj.values():
                result = BasePage.find_value_json(v, key)
                if result is not None:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = BasePage.find_value_json(item, key)
                if result is not None:
                    return result

    @staticmethod
    def find_key_on_json(obj, key):
        if not isinstance(obj, dict):
            return None
        if key in obj:
            return key
        for v in obj.values():
            if isinstance(v, dict):
                item = BasePage.find_key_on_json(v, key)
                if item is not None:
                    return item

    @staticmethod
    def find_key_and_replace_value_json(obj, key, value):
        if isinstance(obj, dict):
            if key in obj:
                obj[key] = value
                return json.dumps(obj, indent=2, sort_keys=True)
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    item = BasePage.find_key_and_replace_value_json(v, key, value)
                    if item is not None:
                        return json.dumps(obj, indent=2, sort_keys=True)
        elif isinstance(obj, list):
            for v in obj:
                item = BasePage.find_key_and_replace_value_json(v, key, value)
                if item is not None:
                    return json.dumps(obj, indent=2, sort_keys=True)

    @staticmethod
    def simple_edit_json(json_file_path, args_data):
        args = dict(args_data[0]) if isinstance(args_data, list) else args_data
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            json_data = dict(data[0]) if isinstance(data, list) else data
            for args_key, args_value in args.items():
                BasePage.find_key_and_replace_value_json(json_data, args_key, args_value)
        return json.dumps(json_data, indent=2, sort_keys=True)

    @staticmethod
    def edit_json(json_file_path, args_data):
        """Edit a JSON file by replacing values for matching keys in args_data."""
        new_json = []
        if isinstance(args_data, list):
            for item in args_data:
                args = json.loads(item) if isinstance(item, str) else item
                with open(json_file_path, 'r') as file:
                    data = json.load(file)
                    json_data = dict(data[0]) if isinstance(data, list) else data
                    for args_key, args_value in args.items():
                        BasePage.find_key_and_replace_value_json(json_data, args_key, args_value)
                new_json.append(json.dumps(json_data, sort_keys=True))
        elif isinstance(args_data, dict):
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                json_data = data[0] if isinstance(data, list) else data
                for args_key, args_value in args_data.items():
                    BasePage.find_key_and_replace_value_json(json_data, args_key, args_value)
            new_json.append(json.dumps(json_data, sort_keys=True))
        return new_json

    @staticmethod
    def load_csv(csv_file_path):
        result = []
        with open(csv_file_path, mode='r') as csv_file:
            for row in csv.DictReader(csv_file):
                result.append(json.dumps(row, sort_keys=True))
        return result
