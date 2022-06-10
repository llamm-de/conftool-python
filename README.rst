ConfToolAPI
=======================

.. image:: https://img.shields.io/pypi/pyversions/ConfToolAPI
   :target: https://pypi.org/project/ConfToolAPI/

.. image:: https://img.shields.io/pypi/v/ConfToolAPI
   :target: https://pypi.org/project/ConfToolAPI/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://img.shields.io/github/last-commit/llamm-de/conftool-python
   :target: https://github.com/llamm-de/conftool-python

.. image:: https://img.shields.io/pypi/l/ConfToolAPI
   :target: https://pypi.org/project/ConfToolAPI/

This package provides you with convenient methods to call the 
`ConfTool API <https://www.conftool.net/ctforum/index.php/topic,280.0.html>`_
and easily retrieve data from it.

First steps
------------
After installing the ConfToolAPI package,
::

   python3 -m pip install ConfToolAPI

you can retrieve data from the official ConfTool API, e.g. 
::

   from ConfToolAPI import APIHandler
    
   api = APIHandler("your_endpoint_name", "your_api_key")
   users = api.get_users()

This will deliver you the data of all users registered in ConfTool for 
conference.

If you want to get detailed information about a particular user, you 
can use the following call 
::

   user_data = api.get_user_details("username_or_email")

To check for the validity of a users credentials, you can use 
::

   result = api.check_login("username_or_email", "password")

If you want to access other data from ConfTool, please use the
``admin_export(datafield, include_deleted=False, custom_query=None)`` function 
of the ``APIHandler`` class. The datafields you may query can be one of the 
following:

* papers
* invitations
* authors
* subsumed_authors
* topics
* reviews
* reviewers
* sessions
* participants
* nametags
* identities
* event_participants
* payments
* identities 

To refine the query, a custom extension of the query can be added using the ``custom_query``
argument. For further details on the structure of such queries, please see the 
documentation of `ConfTool <https://www.conftool.net/ctforum/index.php/topic,280.0.html>`_.

License
-------
This project is licensed under the MIT license. For more details, 
please see `LICENSE.rst <LICENSE.rst>`_ file.