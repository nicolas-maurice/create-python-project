"""
    create_python_project.scripts.content
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement base content class

    Content instance stores the scripts content and enable to reconstruct a script from it

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from .info import BaseInfo, RSTScriptInfo, PyInfo, PySetupInfo, PyDocstringInfo, PyInitInfo


class BaseContent:
    """Base content class starting inheritance tree"""

    info_class = BaseInfo

    def __init__(self, info=None):
        if info is not None:
            assert isinstance(info, self.info_class), \
                '{0} info must be an instance of {1}'.format(type(self), self.info_class)
            self.info = info
        else:
            self.info = self.info_class()


class ScriptContent(BaseContent):
    """Base content class for every script"""

    def __init__(self, info=None, lines=None):
        super().__init__(info)
        self.lines = lines

    def set_lines(self, lines=None):
        self.lines = lines

    def output(self):
        return '\n'.join(self.lines)

    def transform(self, new_info):
        self.info.update(new_info, self.lines)


class RSTContent(ScriptContent):
    """Base content class for .rst script"""

    info_class = RSTScriptInfo


class PyContent(ScriptContent):
    """Base content class for .py script"""

    info_class = PyInfo

    def __init__(self, info=None, lines=None):
        super().__init__(info, lines)
        self.docstring = None
        self.code = ScriptContent(self.info.code)

    def init_docstring(self, docstring_lineno):
        self.info.docstring = PyDocstringInfo()
        self.docstring = RSTContent(info=self.info.docstring)
        self.info.docstring_lineno = docstring_lineno

    def set_lines(self, lines=None):
        lines = lines or self.lines
        super().set_lines(lines)
        self.code.set_lines(lines[self.info.docstring_lineno:])

    def output(self):
        if self.docstring is not None and self.docstring.lines:
            docstring = '\n'.join(['"""'] + [' ' * 4 + line for line in self.docstring.lines] + ['"""\n'])
        else:
            docstring = ''
        return docstring + '\n'.join(self.code.lines)

    def transform(self, new_info):
        if self.docstring:
            self.docstring.transform(new_info.docstring)
        self.code.transform(new_info.code)


class PySetupContent(PyContent):
    """Base content for setup.py script"""

    info_class = PySetupInfo


class PyInitContent(PyContent):
    """Base content for __init__.py script"""

    info_class = PyInitInfo
