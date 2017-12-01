"""
    scripts.base
    ~~~~~~~~~~~~

    Base class for script manipulation

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os


class BaseScript:
    """Base class for manipulating a script

    :param path: Path of the script
    :type path: str
    :param content: Optional content of the script
                    (if not provided, it will try to load the script from the given path)
    :type content: str
    """

    def __init__(self, path=None, content=None):
        self.path = None
        self.content = None

        if path is not None:
            assert os.path.exists(path), 'The path {path} is not a valid file path'.format(path=path)
            self.path = os.path.abspath(path)

        if isinstance(content, str):
            self.content = content
        else:
            if self.path is not None:
                self.content = self.load(self.path)

    def set_path(self, path):
        """Set the script path

        :param path: New path
        :type path: str
        """
        # Validate that the file in an existing file
        assert os.path.exists(path) or os.path.exists(os.path.dirname(path)), \
            'The path {path} is not a valid file path'.format(path=path)
        self.path = os.path.abspath(path)

    @property
    def basename(self):
        """Basename of the script"""
        if self.path is not None:
            return os.path.basename(self.path)

    @property
    def dirname(self):
        """Basename of the script"""
        if self.path is not None:
            return os.path.dirname(self.path)

    @property
    def abspath(self):
        """Abspath of the script"""
        if self.path is not None:
            return os.path.abspath(self.path)

    def relpath(self, start=None):
        """Relative path of the script

        :param start: Optional path against which to compute the relative path (default to current directory)
        :type start: str
        """
        if self.path is not None:
            return os.path.relpath(self.abspath, start)

    @staticmethod
    def load(path):
        """Load a script"""
        with open(path, 'r') as f:
            return f.read()

    def save(self, path=None, content=None):
        """Save script"""
        path = path or self.path
        content = content or self.content
        with open(path, 'w') as f:
            f.write(content)

    def format(self, *args, **kwargs):
        """Format script content

        This method just terminates the super() chain
        """

# class PyScript(BaseScript):
#    """Base class for manipulating Python script"""
#
#    header_parser = re.compile(
#        r'^"""\n'
#       r'(?:{}\t*)(?P<import_name>)'
#    )
