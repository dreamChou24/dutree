#coding:utf-8
import os
import sys
import platform

#树形图的常量
TREEIMAGE = { 'LEFT':'|', 'MID':'  |', 'RIGHT':'--'}
#度量单位
UNITS = ((10 ** 15, 'PB'), (10 ** 12, 'TB'), (10 ** 9, 'GB'), (10 ** 6, 'MB'), (10 ** 3, 'KB'), (1, 'B'))

'''
节点的类
属性：
name 节点的名称
level 节点级别，最高级-1，每增加1级加1
size 节点大小
isfile True为文件，False为文件夹
方法：
_format_size 用于度量转换，并携带单位
format 用于将对象图像化
'''
class Node:
    def __init__(self, name, level, size=0, isfile=True):
        self.name = name
        self.level = level
        self.size = size
        self.isfile = isfile

    def _format_size(self, bytesize):
        if bytesize == 1 or bytesize == 0:
            return '{0}B'.format(bytesize)
        for unit in UNITS:
            if bytesize >= unit[0]:
                return '{0}{1}'.format(float(bytesize) / unit[0], unit[1])

    def format(self):
        node_size = '\033[94m' + self._format_size(self.size) + '\033[0m' if 'Linux' in platform.system() else self._format_size(self.size)
        if not self.isfile:
            node_name = '{0}{1} {2}'.format(self.name, os.sep, node_size) if not self.name == '/' else '{0} {1}'.format('/', node_size)
        else:
            node_name = '{0} {1}'.format(self.name, node_size)
        if self.level == -1:
            return node_name
        return TREEIMAGE['LEFT'] + TREEIMAGE['MID']*self.level + TREEIMAGE['RIGHT'] + node_name

'''
树类
属性：
directory 要形成树形目录的路径
tree_result 树形目录的最终结果
方法：
_build 根据提供的路径构建树形目录
_folder_size 统计目录大小
build 创建目录树
'''
class Tree:
    def __init__(self, directory):
        self.directory = directory
        self.tree_result = ''

    def _build(self, directory, level):
        for root, dirs, files in os.walk(directory):
            size = self._folder_size(root)
            node = Node(os.path.basename(root), level, size=size, isfile=False)
            self.tree_result += node.format() + '\n'
            level += 1
            for f in files:
                size = os.path.getsize(os.path.join(root, f))
                node = Node(f, level, size=size)
                self.tree_result += node.format() + '\n'
            for d in dirs:
                self._build(os.path.join(root, d), level)
            break

    def _folder_size(self, directory):
        total = 0
        for root, dirs, files in os.walk(directory):
            total += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return total
    
    def build(self):
        self._build(self.directory, -1)
        return self.tree_result

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()
    if os.path.isdir(directory):
        t = Tree(directory)
        print t.build()
    else:
        print 'File can not parse to tree.'
