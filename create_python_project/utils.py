"""
    create_python_project.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements utilities functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import fnmatch
import re

from .scripts import get_script_class


def get_script(blob):
    """Get a script object from a blob

    :param blob: Blob to get a script from
    :type blob:
    """
    return get_script_class(blob.path)(source=blob.abspath)


def read(blob):
    """Read a blob

    :param blob: Blob to read
    :type blob:
    """
    script = get_script(blob)
    script.read()
    return script


def get_info(blob):
    """Get script info

    :param blob: Blob to get a info from
    :type blob:
    """
    return read(blob).content.info


def publish(blob, *args, **kwargs):
    """Publish a blob

    :param blob: Blob to publish
    :type blob:
    """
    script = read(blob)
    script.set_destination(destination=kwargs.pop('destination', blob.abspath))
    publication = script.publish(*args, **kwargs)
    return publication


def is_matching(patterns, blob):
    """Tests if a blob's path and a str path are the same

    It is also possible to provide a list of str paths then it tests if the blob's path is in the list

    :param path: Path or list of path
    :type path: str or list
    :param blob: Blob to test
    :type blob:
    :rtype: bool
    """
    for pattern in patterns:
        if re.match(fnmatch.translate(pattern), blob.path):
            return True
    return False


def format_package_name(name):
    return name.lower().replace('-', '_')


def format_project_name(name):
    return '-'.join([word.capitalize() for word in name.split('-')])


def format_py_script_title(path):
    parts = path.split('/')
    return '.'.join(parts[:-1] + ([] if parts[1] == '__init__.py' else [parts[-1].split('.')[0]]))
