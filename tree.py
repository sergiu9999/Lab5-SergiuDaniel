from collections import defaultdict


class LabeledTree:
    def __init__(self):
        self._sons = defaultdict(list)
        self._label = {}
        self._right_sibling = {}
        self._father = {}

    def add_son(self, node, son):
        if self._sons[node]:
            self._right_sibling[self._sons[node][-1]] = son
        self._sons[node].append(son)
        self._father[son] = node

    def add_label(self, node, node_label):
        self._label[node] = node_label

    def get_table(self):
        table = []
        for node, label in self._label.items():
            table.append((node, label, self._father.get(node),self._right_sibling.get(node)))
        return table
