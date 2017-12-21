"""
    create_python_project.scripts.ini
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for .ini (.cfg, .coverage) script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import configparser

from .base import BaseScript, BaseReader, BaseWriter, BaseParser
from .content import IniContent


class IniParser(BaseParser):
    """Base class for parsing .ini"""

    def setup_parse(self, input_string):
        super().setup_parse(input_string)
        self.config = configparser.ConfigParser()

    def parse(self, input_string, content):
        super().parse(input_string, content)
        self.config.read_string(input_string)
        content.config = self.config


class IniReader(BaseReader):
    """Base reader class for .ini"""

    content_class = IniContent


class IniWriter(BaseWriter):
    """Base reader class for .ini"""


class IniScript(BaseScript):
    """Base class for manipulating .ini scripts"""

    supported_format = (
        '*.ini',
        'setup.cfg',
        '.coveragerc',
    )

    parser_class = IniParser
    reader_class = IniReader
    writer_class = IniWriter
