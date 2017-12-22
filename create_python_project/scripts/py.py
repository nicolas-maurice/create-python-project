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


class PyCodeVisitor(ast.NodeVisitor):
    def __init__(self, content):
        self.content = content


class TransformImportVisitor(PyCodeVisitor):

    def __init__(self, content, old_import=None, new_import=None):
        super().__init__(content)
        self.old_import = old_import
        self.new_import = new_import
        self.should_rename_import = False

    def visit_Import(self, node):
        for name in node.names:
            if name.name == self.old_import:
                self.content.update_line(node.lineno - 1, self.old_import, self.new_import)
                self.should_rename_import = name.asname is None

            elif name.asname == self.old_import:  # pragma: no branch
                self.should_rename_import = False

    def visit_ImportFrom(self, node):
        old_module, new_module = node.module, self.content.update_value(node.module,
                                                                        self.old_import,
                                                                        self.new_import)
        self.content.update_line(node.lineno - 1, old_module, new_module)

        for name in node.names:
            if name.name == self.old_import:
                self.should_rename_import = False

    def visit_Name(self, node):
        if self.should_rename_import:
            if node.id == self.old_import:
                self.content.update_line(node.lineno - 1, self.old_import, self.new_import)

    def visit_arg(self, node):
        if self.should_rename_import:
            if node.arg == self.old_import:
                self.content.update_line(node.lineno - 1, self.old_import, self.new_import)


class PyCodeContent(ContentWithInfo):

    def __init__(self, info=None, lines=None):
        super().__init__(info, lines)
        self.ast = None

    def transform(self, old_import=None, new_import=None, new_info=None):
        super().transform(new_info=new_info)
        self.prepare_transform()
        if isinstance(old_import, str) and isinstance(new_import, str):
            TransformImportVisitor(self, old_import=old_import, new_import=new_import).visit(self.ast)

    def prepare_transform(self):
        self.ast = ast.parse(self.output())


class PyContent(ContentWithInfo):
    """Base content class for .py script"""

    info_class = PyInfo

    def __init__(self, info=None, lines=None):
        super().__init__(info, lines)
        self.docstring = None
        self.code = PyCodeContent(self.info.code)

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

    def transform(self, old_value=None, new_value=None,
                  old_import=None, new_import=None,
                  new_info=None):
        if isinstance(new_info, self.info_class):
            if self.docstring:
                self.docstring.transform(old_value=old_value,
                                         new_value=new_value,
                                         new_info=new_info.docstring)
            self.code.transform(old_import=old_import,
                                new_import=new_import,
                                new_info=new_info.code)
        else:
            self.code.transform(old_import=old_import,
                                new_import=new_import)


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
        content.ast = self.ast

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
