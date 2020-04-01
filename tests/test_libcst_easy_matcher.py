import libcst
import libcst.matchers as m
import pytest

from libcst_easy_matcher import create_matcher


@pytest.mark.parametrize(
    "query, matches",
    [
        ("b = 4", False),
        ("b = __", False),
        ("a = 3", False),
        ("a = '4'", False),
        ("a = 4", True),
        ("a = __", True),
        ("__ = 4", True),
        ("__ = __", True),
    ],
)
def test_create_matcher_assignment(query, matches):
    node = libcst.parse_statement("a = 4").body[0]
    assert m.matches(node, create_matcher(query)) == matches


@pytest.mark.parametrize(
    "query, matches",
    [
        ("bar()", False),
        ("foo()", True),
        ("__()", True),
    ],
)
def test_create_matcher_function_call(query, matches):
    node = libcst.parse_statement("foo()").body[0]
    assert m.matches(node, create_matcher(query)) == matches


@pytest.mark.parametrize(
    "query, matches",
    [
        ("bar(x=3)", False),
        ("foo(x=4)", False),
        ("foo(y=3)", False),
        ("foo(x=3)", True),
        ("foo(x=__)", True),
        ("foo(__=3)", True),
        ("foo(__=__)", True),
        ("foo(__)", True),
    ],
)
def test_create_matcher_function_call_arguments(query, matches):
    node = libcst.parse_statement("foo(x=3)").body[0]
    assert m.matches(node, create_matcher(query)) == matches