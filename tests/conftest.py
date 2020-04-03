import libcst
import libcst.matchers as m
import pytest

from libcst_easy_matcher import create_matcher


def pytest_collect_file(parent, path):
    if path.ext == ".txt" and path.basename.startswith("test"):
        return File.from_parent(parent, fspath=path)


class File(pytest.File):
    def collect(self):
        with self.fspath.open() as f:
            lines = f.read().split('===')
            code = lines[0].strip()

            non_matches = [l.strip() for l in lines[1].strip().split('---')]
            matches = [l.strip() for l in lines[2].strip().split('---')]

            for i, query in enumerate(non_matches):
                spec = (code, query, False)
                yield Item.from_parent(self, name=f'non match {i}', spec=spec)

            for i, query in enumerate(matches):
                spec = (code, query, True)
                yield Item.from_parent(self, name=f'match {i}', spec=spec)


class Item(pytest.Item):
    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec

    def runtest(self):
        code, query, expected = self.spec
        node = libcst.parse_statement(code).body[0]
        assert m.matches(node, create_matcher(query)) == expected

    def repr_failure(self, excinfo):
        code, query, expected = self.spec
        if expected:
            return f'{query} did not match {code}'
        else:
            return f'{query} did match {code}'

    def reportinfo(self):
        return self.fspath, 0, self.name