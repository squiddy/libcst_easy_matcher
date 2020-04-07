import dataclasses
from collections.abc import Iterable

import libcst
import libcst.matchers as m


__version__ = '0.1.0'


class Transformer:
    """
    Transform a concrete node from LibCST to an equivalent node of matchers.

    For the most part, this just passes arguments from e.g. libcst.Call to
    libcst.matchers.Call, but maps the placeholders (`__`) to m.DoNotCare.
    """

    def on_visit(self, node):
        name = type(node).__name__

        if name == 'Name' and node.value == '__':
            return m.DoNotCare()

        kwargs = {}
        for field in dataclasses.fields(node):
            if field.name in ['semicolon', 'comma', 'equal']:
                continue
            if 'whitespace' in field.name:
                continue

            value = getattr(node, field.name)
            if value is None:
                continue

            if isinstance(value, str):
                pass
            elif isinstance(value, Iterable):
                value = [self.on_visit(e) for e in value]
            else:
                value = self.on_visit(value)

            kwargs[field.name] = value
        
        return getattr(m, name)(**kwargs)


def create_matcher(code):
    """
    Returns a LibCST matcher derived from the python code.
    """
    node = libcst.parse_statement(code)
    assert len(node.body) == 1, 'Only one statement support at this time.'
    return Transformer().on_visit(node.body[0])
