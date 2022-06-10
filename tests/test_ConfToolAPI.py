import pytest
import time

from ConfToolAPI.APIHandler import APIHandler

API_KEY_DUMMY = "aOig7Nm3B"
INITIAL_NONE_DUMMY = 1
ENDPOINT_DUMMY = "test2022"

def test_initialize_nonce():
    api = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY)
    api_initial_nonce = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY, initial_nonce=INITIAL_NONE_DUMMY)

    assert api.last_nonce <= int(time.time() * 10000)
    assert api_initial_nonce.last_nonce == INITIAL_NONE_DUMMY

def test_passhash():
    api = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY, initial_nonce=INITIAL_NONE_DUMMY)    
    hash = api._create_passhash()

    assert hash == '775d4968b4aca5a8a9ac2f3d55393f05fb4968cb79424bb199d26e23c45c2df6'

def test_repr():
    api = APIHandler(ENDPOINT_DUMMY, API_KEY_DUMMY) 
    assert repr(api) == f"<ConfToolAPI object: https://www.conftool.org/{ENDPOINT_DUMMY}/rest.php>"