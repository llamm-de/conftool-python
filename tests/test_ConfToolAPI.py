import pytest
import time

from ConfToolAPI.APIHandler import APIHandler

API_KEY_DUMMY = "aOig7Nm3B"
INITIAL_NONCE_DUMMY = 1
ENDPOINT_DUMMY = "test2022"

@pytest.fixture(scope="session")
def env_file_nonce(tmp_path_factory):
    f = tmp_path_factory.mktemp("data") / ".env_nonce"
    f.write_text(f"ENDPOINT_NAME = {ENDPOINT_DUMMY} \n API_KEY = {API_KEY_DUMMY} \n INITIAL_NONCE = {INITIAL_NONCE_DUMMY}")
    return f

@pytest.fixture(scope="session")
def env_file(tmp_path_factory):
    f = tmp_path_factory.mktemp("data") / ".env"
    f.write_text(f"ENDPOINT_NAME = {ENDPOINT_DUMMY} \n API_KEY = {API_KEY_DUMMY}")
    return f

def test_initialize_nonce():
    api = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY)
    api_initial_nonce = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY, initial_nonce=INITIAL_NONCE_DUMMY)

    assert api.last_nonce <= int(time.time() * 10000)
    assert api_initial_nonce.last_nonce == INITIAL_NONCE_DUMMY

def test_object_from_env_file_nonce(env_file_nonce):
    api = APIHandler.from_dotenv(env_file_nonce)
    assert api.api_key == API_KEY_DUMMY
    assert api.last_nonce == INITIAL_NONCE_DUMMY
    assert api.base_url == f"https://www.conftool.org/{ENDPOINT_DUMMY}/rest.php"

def test_object_from_env_file(env_file):
    api = APIHandler.from_dotenv(env_file)
    assert api.api_key == API_KEY_DUMMY
    assert api.last_nonce <= int(time.time() * 10000)
    assert api.base_url == f"https://www.conftool.org/{ENDPOINT_DUMMY}/rest.php"

# def test_api_call_except_for_non_xml_response():
#     assert False

# def test_api_call_except_for_error_response():
#     assert False

def test_passhash():
    api = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY, initial_nonce=INITIAL_NONCE_DUMMY)    
    hash = api._create_passhash()

    assert hash == '775d4968b4aca5a8a9ac2f3d55393f05fb4968cb79424bb199d26e23c45c2df6'

def test_repr():
    api = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY) 
    assert repr(api) == f"<ConfToolAPI object: https://www.conftool.org/{ENDPOINT_DUMMY}/rest.php>"