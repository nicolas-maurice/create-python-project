"""
    create_python_project.scripts.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for python script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import ast

from .base import ContentWithInfo, BaseScript, BaseReader, BaseParser, BaseWriter
from .rst import RSTContent, RSTScript, RSTVisitor, RSTParser
from ..info import PyInfo, PyDocstringInfo, SingleLineTextInfo


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


class PyDocstringVisitor(RSTVisitor):
    """Base class for visiting Python script docstring"""

    def visit_field(self, node):
        field_name, field_body = node.children[0].astext(), node.children[1].children[0].astext()
        if field_name in self.content.info._fields:
            setattr(self.content.info, field_name, SingleLineTextInfo(text=field_body, lineno=node.line - 1))


class PyDocstringParser(RSTParser):
    """Base class for parsing Python Script Docstrings"""

    _rst_visitor_class = PyDocstringVisitor


class PyDocstringScript(RSTScript):
    """Base class for parser python docstring"""

    parser_class = PyDocstringParser


class PyReader(BaseReader):
    """Base class for reading python scripts"""

    content_class = PyContent


class PyParser(BaseParser):
    """Base class for parsing py scripts"""

    def setup_parse(self, input_string):
        super().setup_parse(input_string)
        self.docstring_parser = PyDocstringParser()

        self.ast = ast.parse(input_string)
        self.docstring = ast.get_docstring(self.ast)

    def parse(self, input_string, content):
        super().parse(input_string, content)

        self.parse_docstring(content)
        self.parse_code(content)

        content.set_lines()

    def parse_docstring(self, content):
        if self.docstring is not None:
            content.init_docstring(self.ast.body[0].lineno)
            self.docstring_parser.parse(self.docstring, content.docstring)

    def parse_code(self, content):
        pass


class PyWriter(BaseWriter):
    """Base writer for Python Scripts"""


class PyScript(BaseScript):
    """Base class for manipulating py scripts"""

    supported = (
        '*.py',
    )

    parser_class = PyParser
    reader_class = PyReader
    writer_class = PyWriter
