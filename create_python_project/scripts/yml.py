import re
from functools import partial

import yaml
from yaml.tokens import ScalarToken, ValueToken, BlockEntryToken, FlowEntryToken, FlowSequenceStartToken

from .base import BaseScript, BaseReader, BaseWriter, BaseParser
from .content import ScriptContent


class YmlContent(ScriptContent):
    _comment_pattern = re.compile('(?P<start>[^#]*)(?P<comment>#.*)')

    def __init__(self, lines=None):
        super().__init__(lines)
        self.scan_yml = None

    def prepare_transform(self):
        self.yml_tokens = self.scan_yml(self.output())

    def transform(self, old_value=None, new_value=None):
        if isinstance(old_value, str) and isinstance(new_value, str):
            self.prepare_transform()
            for token in self.yml_tokens:
                print(token)
                if isinstance(token, ValueToken) or isinstance(token, BlockEntryToken) or \
                        isinstance(token, FlowEntryToken) or isinstance(token, FlowSequenceStartToken):
                    token = next(self.yml_tokens)
                    if isinstance(token, ScalarToken):
                        start_mark, end_mark = token.start_mark, token.end_mark
                        updated_value = self.update_value(token.value, old_value, new_value)
                        self.lines[start_mark.line] = '{start}{value}{end}'. \
                            format(start=self.lines[start_mark.line][:start_mark.column],
                                   value=updated_value,
                                   end=self.lines[start_mark.line][end_mark.column:])

            # comment are not parsed by PYyaml so we need to transform it manually
            self.transform_comment(old_value=old_value, new_value=new_value)

    def transform_comment(self, old_value=None, new_value=None):
        for i, line in enumerate(self.lines):
            self.lines[i] = self._comment_pattern.sub(partial(self.replace_comment, old_value, new_value), line)

    def replace_comment(self, old_value, new_value, match):
        return (match.group('start') or '') + self.update_value(match.group('comment'),
                                                                old_value,
                                                                new_value)


class YmlParser(BaseParser):
    """Base class for parsing .ini"""

    def parse(self, input_string, content):
        super().parse(input_string, content)
        content.scan_yml = yaml.scan


class YmlReader(BaseReader):
    """Base reader class for .ini"""

    content_class = YmlContent


class YmlWriter(BaseWriter):
    """Base reader class for .ini"""


class YmlScript(BaseScript):
    """Base class for manipulating .ini scripts"""

    supported_format = (
        '*.yml',
        '*.yaml',
    )

    parser_class = YmlParser
    reader_class = YmlReader
    writer_class = YmlWriter
