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
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if not visit_func:
            raise NotImplementedError(
                f"Implementation for '{type(node).__name__}' missing."
            )
        return visit_func(node)

    def visit_Assign(self, node):
        return m.Assign(
            targets=[self.on_visit(t) for t in node.targets],
            value=self.on_visit(node.value),
        )

    def visit_AssignTarget(self, node):
        return m.AssignTarget(target=self.on_visit(node.target))

    def visit_Name(self, node):
        if node.value == "__":
            return m.DoNotCare()
        else:
            return m.Name(value=node.value)

    def visit_SimpleString(self, node):
        return m.SimpleString(value=node.value)

    def visit_Integer(self, node):
        return m.Integer(value=node.value)

    def visit_Call(self, node):
        return m.Call(
            func=self.on_visit(node.func), args=[self.on_visit(a) for a in node.args]
        )

    def visit_Expr(self, node):
        return m.Expr(value=self.on_visit(node.value))
    
    def visit_Arg(self, node):
        if node.keyword is None:
            return m.DoNotCare()
        else:
            return m.Arg(
                value=self.on_visit(node.value),
                keyword=self.on_visit(node.keyword)
            )


def create_matcher(code):
    """
    Returns a LibCST matcher derived from the python code.
    """
    node = libcst.parse_statement(code)
    assert len(node.body) == 1, 'Only one statement support at this time.'
    return Transformer().on_visit(node.body[0])
