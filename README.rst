ConfTool API for Python
=======================

This package provides you with convenient methods to call the 
`ConfTool API <https://www.conftool.net/ctforum/index.php/topic,280.0.html>`_
to easily retrieve data from it.


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black


First steps
------------
After installing the conftool package, you can retrieve data 
from the official ConfTool API, e.g. 
::

    from ConfToolAPI import APIHandler
    
    api = APIHandler("your_endpoint_name", "your_api_key")

    users = api.get_users()

This will deliver you the data of all users registered in ConfTool for 
conference.

License
-------
This project is licensed under the MIT license. For more details, 
please see `LICENSE.rst <LICENSE.rst>`_ file.