.. image:: https://travis-ci.org/nicolas-maurice/create-python-project.svg?branch=master
    :target: https://travis-ci.org/nicolas-maurice/create-python-project#

.. image:: https://codecov.io/gh/nicolas-maurice/create-python-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nicolas-maurice/create-python-project

Create-Python-Project
=====================

This project is inspired from excellent `Create-React-App`_.
It implements a Command Line Interface to enable straightforward manipulation of Python projects.
It allows to easily create a new Python project from an existing Python project by contextualizing it to your new project.
Multiple context information can be updated such

- Project's name
- Author's information (name and email)
- Hyperlinks to specific resources (such as badges)
- etc.

When creating the new project Create-Python-Project

#. clones the original project
#. applies commits for contextualization
#. changes remote origin to the new project remote
#. creates remote upstream to the original project

This way it is straightforward to retrieve updates from the original project.

.. _Create-React-App: https://github.com/facebookincubator/create-react-app

Requirements
------------

Distribution
~~~~~~~~~~~~

It is highly recommended to use this project on Unix distribution.

Git
~~~

Having the latest version of ``git`` installed locally.

Docker
~~~~~~

Having ``docker`` and ``docker-compose`` installed locally.

Python
~~~~~~

Having Python 3.5 and 3.6 installed locally.

It is also recommended having ``virtualenv`` installed locally.