"""
    create_python_project.scripts.content
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement base content class

    Content instance stores the scripts content and enable to reconstruct a script from it

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""
import re

from .info import BaseInfo, RSTScriptInfo, PyInfo, PySetupInfo, PyDocstringInfo, PyInitInfo


class ScriptContent:
    """Base content class for every script"""

    def __init__(self, lines=None):
        self.lines = lines

    def set_lines(self, lines=None):
        self.lines = lines

    def output(self):
        return '\n'.join(self.lines)

    def update_value(self, value, old, new):
        return value.replace(old, new)

    def transform(self, old_value=None, new_value=None):
        if isinstance(old_value, str) and isinstance(new_value, str):  # pragma: no branch
            for i, line in enumerate(self.lines):
                self.lines[i] = self.update_value(line, old_value, new_value)


class ContentWithInfo(ScriptContent):
    info_class = BaseInfo

    def __init__(self, info=None, lines=None):
        super().__init__(lines)
        if info is not None:
            assert isinstance(info, self.info_class), \
                '{0} info must be an instance of {1}'.format(type(self), self.info_class)
            self.info = info
        else:
            self.info = self.info_class()

    def transform(self, old_value=None, new_value=None, new_info=None):
        if isinstance(new_info, self.info_class):  # pragma: no branch
            self.info.update(new_info, self.lines)
        super().transform(old_value=old_value,
                          new_value=new_value)


class RSTContent(ContentWithInfo):
    """Base content class for .rst script"""

    info_class = RSTScriptInfo


class PyContent(ContentWithInfo):
    """Base content class for .py script"""

    info_class = PyInfo

    def __init__(self, info=None, lines=None):
        super().__init__(info, lines)
        self.docstring = None
        self.code = ContentWithInfo(self.info.code)

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

    def transform(self, old_value=None, new_value=None, new_info=None):
        if isinstance(new_info, self.info_class):
            if self.docstring:
                self.docstring.transform(old_value=old_value,
                                         new_value=new_value,
                                         new_info=new_info.docstring)
            self.code.transform(new_info=new_info.code)


class PySetupContent(PyContent):
    """Base content for setup.py script"""

    info_class = PySetupInfo


class PyInitContent(PyContent):
    """Base content for __init__.py script"""

    info_class = PyInitInfo


class IniContent(ScriptContent):
    """Base content for .ini scripts"""

    _section_pattern = re.compile('\[(?P<header>[^]]+)\]')
    _comment_pattern = re.compile('\s*#.*')
    _item_pattern = re.compile('((?P<option>.*?)(?P<delim>[=:]))?(?P<space>\s*)(?P<value>.*)')

    def transform(self, old_value=None, new_value=None):
        if isinstance(old_value, str) and isinstance(new_value, str):
            for i, line in enumerate(self.lines):
                if self._section_pattern.match(line) or self._comment_pattern.match(line):
                    continue
                elif self._item_pattern.match(line):  # pragma: no branch
                    match = self._item_pattern.match(line)

                    updated_value = self.update_value(match.group('value'), old_value, new_value)
                    self.lines[i] = self._item_pattern.sub('\g<option>\g<delim>\g<space>{value}'
                                                           .format(value=updated_value),
                                                           line)
