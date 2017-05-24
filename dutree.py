#coding:utf-8
import os
import sys

TREEIMAGE = { 'LEFT':'|', 'MID':'  |', 'RIGHT':'--'}

class Node:
    def __init__(self, name, level, size=0, isfile=True):
        self.name = name
        self.level = level
        self.size = size
        self.isfile = isfile

    def _format_size(self, bytesize):
        units = ((10 ** 15, 'PB'), (10 ** 12, 'TB'), (10 ** 9, 'GB'), (10 ** 6, 'MB'), (10 ** 3, 'KB'), (1, 'B'))
        if bytesize == 1 or bytesize == 0:
            return '{0}B'.format(bytesize)
        for measure, suffix in units:
            if bytesize >= measure:
                return '{0}{1}'.format(float(bytesize) / measure, suffix)

    def format(self):
        node_name = self.name
        if not self.isfile:
            node_name = ' ' + self.name + '/' if not self.name == '/' else '/'
        else:
            node_name = '{0} {1}'.format(self.name, '\033[94m'+self._format_size(self.size)+'\033[0m')
        if self.level == -1:
            return node_name
        return TREEIMAGE['LEFT'] + TREEIMAGE['MID']*self.level + TREEIMAGE['RIGHT'] + node_name

class Tree:
    def __init__(self, directory):
        self.directory = directory
        self.tree_result = ''

    def _build(self, directory, level):
        for root, dirs, files in os.walk(directory):
            node = Node(os.path.basename(root), level, isfile=False)
            self.tree_result += node.format() + '\n'
            level += 1
            for f in files:
                size = os.path.getsize(os.path.join(root, f))
                node = Node(f, level, size=size)
                self.tree_result += node.format() + '\n'
            for d in dirs:
                self._build(os.path.join(root, d), level)
            break
    def build(self):
        self._build(self.directory, -1)
        return self.tree_result

'''
    def _folder_size(self, directory):
        total = 0
        for root, dirs, files in os.walk(directory):
            total += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return total
'''

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()
    t = Tree(directory)
    print t.build()
