import hashlib
import time
import requests
import xmltodict
from dotenv import dotenv_values
from urllib.request import urlretrieve as shitty_wget

class APIHandler:
    """
    A simple class for handling API requests to conftool.org API.
    """

    def __init__(self, endpoint_name: str, api_key: str, initial_nonce: int = None) -> None:
        """
        Constructor for APIHandler
        """
        self.api_key = api_key
        self.base_url = f"https://www.conftool.org/{endpoint_name}/rest.php"
        
        if initial_nonce:
            self.last_nonce = initial_nonce
        else:
            self.last_nonce = int(time.time() * 10000)

    @classmethod
    def from_dotenv(cls, env_file_name: str) -> 'APIHandler':
        """
        Overloading of constructor for using .env files to create new object
        """
        config = dotenv_values(env_file_name)
        if "INITIAL_NONCE" in config:
            return cls(config["ENDPOINT_NAME"], config["API_KEY"], initial_nonce=int(config["INITIAL_NONCE"]))
        else: 
            return cls(config["ENDPOINT_NAME"], config["API_KEY"])

    def _create_passhash(self) -> str:
        """
        Create API passhash according to the documentation at https://www.conftool.net/ctforum/index.php/topic,280.0.html
        """
        self.last_nonce += 1
        to_hash = f"{self.last_nonce}{self.api_key}"
        passhash = hashlib.sha256(to_hash.encode("utf-8")).hexdigest()

        return passhash

    def admin_export(self, datafield: str, include_deleted: bool = False, custom_query: str =None) -> dict:
        """
        Retrieve data from adminExport endpoint of ConfTool API
        """

        # Assemble queries in url
        if include_deleted:
            deleted_flag = 1
        else:
            deleted_flag = 0
        
        url = (f"{self.base_url}?page=adminExport&export_select={datafield}"
               f"&form_include_deleted={deleted_flag}&form_export_format=xml"
               f"&form_export_header=default&cmd_create_export=true")

        if custom_query:
            url += custom_query

        # call api
        data = self._call_api(url)

        return data

    def download_paper(self, form_id: int, filename: str) -> bool:
        """
        Download a file
        """
        
        url = self.base_url
        url += f"?page=downloadPaper"
        url += f"&form_id={form_id}"
        url += f"&passhash={self._create_passhash()}"  # this sets self.last_nonce to the right nonce
        url += f"&nonce={self.last_nonce}"

        try:
            shitty_wget( url, filename )
        except:
            return False
        
        return True

    def get_users(self, include_deleted: bool = False, custom_query: str = None) -> dict:
        """
        Convenience wrapper for get list of users
        """
        return self.admin_export("users", include_deleted, custom_query)

    def get_user_details(self, identifier: str) -> dict:
        """
        Get data of a single user identified by username or email
        """
        url = (f"{self.base_url}?page=remoteLogin&user={identifier}&command=request")

        # call api
        data = self._call_api(url)

        return data

    def check_login(self, identifier: str, password: str) -> dict:
        """
        Check if a user identified by username or mail can log in with given password
        """
        url = (f"{self.base_url}?page=remoteLogin&user={identifier}"
               f"&command=login&password={password}")

        # call api
        data = self._call_api(url)

        return data

    def _call_api(self, url: str) -> dict:
        """
        Call the API, check response and return data
        """

        passhash = self._create_passhash()
        url += f"&nonce={self.last_nonce}&passhash={passhash}"
        
        response = requests.get(url)

        # Convert xml response into OrderedDictionary
        try:
            data = xmltodict.parse(response.text)
        except:
            raise RuntimeError(f'File Download is not yet implemented for ConfTool API.')

        # Check response status. 
        # Since the ConfTool API always returns status code 200 within the header, 
        # we have to manually check the error message.
        if "rest" in data:
            raise RuntimeError(f'Fetching API did not work: {data["rest"]["message"]}')

        return data

    def __repr__(self) -> str:
       return f"<ConfToolAPI object: {self.base_url}>"
