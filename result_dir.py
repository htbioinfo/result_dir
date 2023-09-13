# -*- coding: utf-8 -*-
from os import makedirs
from os.path import join


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self._parent = parent

    def parent(self, parent):
        self._parent = parent

    def __call__(self):
        if self._parent is None:
            return self.name
        return join(self._parent(), self.name)


class File(Node):
    pass


class Dir(Node):
    def __init__(self, name, parent=None):
        super(Dir, self).__init__(name, parent)
        self.update()

    def nodes(self):
        for name in dir(self):
            if name.startswith('_'):
                continue
            node = getattr(self, name)
            if not isinstance(node, Node):
                continue
            yield node

    def dirs(self):
        for node in self.nodes():
            if isinstance(node, Dir):
                yield node

    def files(self):
        for node in self.nodes():
            if isinstance(node, File):
                yield node

    def update(self):
        for node in self.nodes():
            node.parent(self)
        return self

    def make(self):
        makedirs(self(), exist_ok=True)
        for dir in self.dirs():  # noqa
            dir.make()
        return self
