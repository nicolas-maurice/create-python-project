"""
    create_python_project.scripts.init
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for python __init__.py script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""
import _ast
import ast

from .content import PyInitContent
from .info import VarInfo
from .py import PyScript, PyParser, PyReader


class PyInitVisitor(ast.NodeVisitor):
    def __init__(self, content, line_offset=None):
        self.content = content
        self.info = content.info.code
        self.line_offset = line_offset or content.info.docstring_lineno

    def visit(self, node):
        print(node)
        super().visit(node)

    def visit_Assign(self, node):
        target, value = node.targets[0], node.value
        if isinstance(target, _ast.Name) and isinstance(value, _ast.Str):
            if target.id == '__version__':
                version = VarInfo(var=target.id, value=value.s, lineno=value.lineno - self.line_offset - 1)
                self.info.version = version


"""
class SetupKwargsVisitor(PyCodeVisitor):
    def __init__(self, content, line_offset=None):
        super().__init__(content, line_offset)
        self.info = self.content.info.code.setup

    def visit_keyword(self, node):
        if node.arg in self.info._fields:

            if isinstance(node.value, _ast.Str):
                setattr(self.info, node.arg, KwargInfo(arg=node.arg,
                                                       value=node.value.s,
                                                       lineno=node.value.lineno - self.line_offset - 1))
            elif isinstance(node.value, _ast.List):
                setattr(self.info,
                        node.arg,
                        tuple([KwargInfo(arg=node.arg, value=elt.s, lineno=elt.lineno - self.line_offset - 1)
                               for elt in node.value.elts]))


class SetupVisitor(PyCodeVisitor):
    def __init__(self, content):
        super().__init__(content)
        self.setup_alias = None
        self.setup_visited = False

    def visit_ImportFrom(self, node):
        if node.module == 'setuptools':
            for name in node.names:
                if name.name == 'setup':
                    self.setup_alias = name.asname or name.name

    def visit_Call(self, node):
        if not self.setup_visited and isinstance(node.func, _ast.Name) and node.func.id == self.setup_alias:
            self.content.info.code.setup = SetupKwargsInfo()
            SetupKwargsVisitor(self.content,
                               self.line_offset).visit(node)
            self.setup_visited = True
"""


class PyInitReader(PyReader):
    """Base class for reader setup.py script"""

    content_class = PyInitContent


class PyInitParser(PyParser):
    """Base class for parsing setup.py script"""

    def parse_code(self, content):
        PyInitVisitor(content).visit(self.ast)


class PyInitScript(PyScript):
    """Base class for manipulating setup.py script"""

    supported_format = ('__init__.py',)

    parser_class = PyInitParser
    reader_class = PyInitReader
