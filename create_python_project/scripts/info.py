"""
    create_python_project.scripts.info
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement base info class

    Info instance are element used to keep track of information contained in scripts

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""
import re

from collections import OrderedDict


class FieldDescriptor:
    """Base Field Descriptor from which every Info inherit from"""

    def __init__(self, name=None, default=None):
        self._name = name
        if callable(default):
            self.default = default()
        else:
            self.default = default

    def __set__(self, instance, value):
        value = value if value is not None else self.default
        if value is not None:
            self.validate(instance, value)
        instance.__dict__[self._name] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)

    def set_name(self, name):
        self._name = name

    def attr_name(self, instance):
        return '{class_name}.{name}'.format(class_name=instance.__class__.__name__,
                                            name=self._name)

    def validate(self, instance, value):
        for klass in reversed(type(self).__mro__):
            if hasattr(klass, 'is_valid') and not klass.is_valid(self, value):
                klass.raise_error(klass.error_message(self, attr=self.attr_name(instance), value=value))

    def error_message(self, attr, value):
        raise NotImplementedError

    @staticmethod
    def raise_error(message):
        raise NotImplementedError

    def is_valid(self, value):
        return True


class InfoMeta(type):
    """Meta class for Info"""

    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, dict(ns))

        fields = sum([list(base._fields) for base in bases if hasattr(base, '_fields')], [])

        for field, info in ns.items():
            if isinstance(info, FieldDescriptor):
                info.set_name(field)
                fields.append(field)
        cls._fields = tuple(set(fields))

        return cls


class BaseInfo(FieldDescriptor, metaclass=InfoMeta):
    """BaseInfo class"""

    def __init__(self, _name=None, default=None, **kwargs):
        super().__init__(name=_name, default=default)
        for field in self._fields:
            setattr(self, field, kwargs.get(field, None))

    def validate_info(self, info):
        if info is not None:
            assert isinstance(info, type(self)), '{0} must be updated to {0} but you passed {1}'.format(type(self), info)

    def transform_lines(self, new_info, lines):
        pass

    def update_info(self, new_info):
        """Update the current info with the new info"""
        for field in self._fields:
            current, new = getattr(self, field), getattr(new_info, field, None)
            if isinstance(current, BaseInfo) and isinstance(new, BaseInfo):
                current.update_info(new)
            setattr(self, field, new)

    def update(self, new_info, lines=None):
        """Perform transformation on lines corresponding to the new provided info and update current info with new info"""

        self.validate_info(new_info)

        if lines is not None:
            self.transform_lines(new_info, lines)

        for field in self._fields:
            current, new = getattr(self, field), getattr(new_info, field, None)
            if isinstance(current, BaseInfo) and isinstance(new, BaseInfo):
                current.update(new, lines)
            else:
                try:
                    iterator = iter(current)
                except TypeError:
                    continue
                else:
                    for i, info in enumerate(iterator):
                        if isinstance(info, BaseInfo):
                            info.update(new[i], lines)
        self.update_info(new_info)


class BaseTypeInfo(BaseInfo):
    """Base type info validating against a type"""

    _type = object

    def is_valid(self, value):
        return isinstance(value, self._type)

    def error_message(self, attr, value):
        return '{attr} must be an instance of {_type} but you passed {value}'.format(_type=self._type,
                                                                                     attr=attr,
                                                                                     value=value)

    @staticmethod
    def raise_error(message):
        raise TypeError(message)


class IntInfo(BaseTypeInfo):
    """Base info validating against int"""

    _type = int


class StrInfo(BaseTypeInfo):
    """Base info validating against str"""

    _type = str


class BoolInfo(BaseTypeInfo):
    """Base bool info validating against bool"""

    _type = bool


class TupleInfo(BaseTypeInfo):
    """Base list info validating against list"""

    _type = tuple


class ItemTupleInfo(TupleInfo):
    _item_type = BaseInfo

    def is_valid(self, value):
        for val in value:
            if not isinstance(val, self._item_type):
                return False
        return True

    def error_message(self, attr, value):
        return '{attr} elements must be instance of {type} but you passed {value}'.format(type=self._item_type,
                                                                                          attr=attr,
                                                                                          value=value)


class NonNullStrInfo(StrInfo):
    """Non Null Str Info"""

    def is_valid(self, value):
        return len(value) > 0

    def error_message(self, attr, value):
        return '{attr} must be a non null string'.format(attr=attr)

    @staticmethod
    def raise_error(message):
        raise AssertionError(message)


class SingleLineStrInfo(StrInfo):
    """Single Line Str Info"""

    def is_valid(self, value):
        return len(value.split('\n')) == 1

    def error_message(self, attr, value):
        return '{attr} must be a one line string'.format(attr=attr)


class NonNullSingleLineStrInfo(NonNullStrInfo, SingleLineStrInfo):
    """Non Null Single Line Str info"""


class RSTSymbolInfo(NonNullStrInfo):
    """.rst underline symbol info"""

    _symbols = '=-`:\'"~^_*+#<>'

    def is_valid(self, value):
        return len(value) == 1 and value in self._symbols

    def error_message(self, attr, value):
        return '{attr} must be one of {symbols} but you passed {value}'.format(symbols=self._symbols,
                                                                               attr=attr,
                                                                               value=value)


class ComplexInfo(BaseInfo):
    """Info validating against its class"""

    def is_valid(self, value):
        return isinstance(value, type(self))

    def error_message(self, attr, value):
        return '{attr} must be an instance of {type} but you passed {value}'.format(type=type(self),
                                                                                    attr=attr,
                                                                                    value=value)

    @staticmethod
    def raise_error(message):
        raise TypeError(message)


class TextInfo(ComplexInfo):
    """Text Info"""

    text = StrInfo()
    lineno = IntInfo()

    def transform_lines(self, new_info, lines):
        lines[self.lineno] = lines[self.lineno].replace(self.text, new_info.text.strip())
        super().transform_lines(new_info, lines)


class NonNullTextInfo(TextInfo):
    """Text Info"""

    text = NonNullStrInfo()


class RSTTitleInfo(TextInfo):
    """Info for an .rst section title"""

    text = NonNullSingleLineStrInfo(default='<title>')
    symbol = RSTSymbolInfo(default='=')
    has_overline = BoolInfo(default=False)

    def transform_lines(self, new_info, lines):
        lines[self.lineno + 1] = len(new_info.text) * new_info.symbol
        if self.has_overline:
            lines[self.lineno - 1] = len(new_info.text) * new_info.symbol
        super().transform_lines(new_info, lines)


class RSTScriptInfo(ComplexInfo):
    """Info of an .rst script"""

    title = RSTTitleInfo()


class SingleLineTextInfo(TextInfo):
    text = NonNullSingleLineStrInfo()


class PyDocstringInfo(RSTScriptInfo):
    """Info of a python docstring"""

    copyright = SingleLineTextInfo()
    license = SingleLineTextInfo()


class CodeInfo(BaseInfo):
    """Info for python script code"""


class PyInfo(ComplexInfo):
    """Info of a python script"""

    docstring = PyDocstringInfo()
    code = CodeInfo(default=CodeInfo)
    docstring_lineno = IntInfo(default=0)


class KwargInfo(ComplexInfo):
    """Info for kwarg argument of a python function"""

    arg = NonNullSingleLineStrInfo()
    value = SingleLineStrInfo()
    lineno = IntInfo()

    def transform_lines(self, new_info, lines):
        pattern = re.compile('(?P<arg>{arg}\s?=\s?)?(?P<quote>[\'"])(?P<value>{value})[\'"]'.format(arg=self.arg, value=self.value))
        lines[self.lineno] = pattern.sub('\g<arg>\g<quote>{value}\g<quote>'.format(value=new_info.value), lines[self.lineno])
        super().transform_lines(new_info, lines)


class KwargTupleInfo(ItemTupleInfo):
    """Info for setup packages"""

    _item_type = KwargInfo


class SetupKwargsInfo(ComplexInfo):
    """Info contained in a setuptools setup call"""

    name = KwargInfo()
    version = KwargInfo()
    url = KwargInfo()
    author = KwargInfo()
    author_email = KwargInfo()
    description = KwargInfo()
    packages = KwargTupleInfo()


class SetupInfo(CodeInfo):
    setup = SetupKwargsInfo()


class PySetupInfo(PyInfo):
    code = SetupInfo(default=SetupInfo)
