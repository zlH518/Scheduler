# from typing import Iterable
#
# class Node:
#     def __init__(self, cards):
#         self.cards = cards
#
# class Package:
#     def __init__(self, cardsPerPackage: int, nodeId: int):
#         self.cards = cardsPerPackage
#         self.nodeId = nodeId
#         self.task = None
#
#     def __repr__(self):
#         return f"Package(cards={self.cards}, nodeId={self.nodeId})"
#
#
# class Group:
#     def __init__(self, cardsPerPackage: int, nodes: Iterable[Node], theta: float):
#         self.cardsPerPackage = cardsPerPackage
#         self.emptyPackage = []
#         self.usedPackage = []
#         self.theta = theta
#         self.completedTask = []
#         self.durationTime = []
#         self.create_packages(nodes)
#
#     def create_packages(self, nodes):
#         for index, node in enumerate(nodes):
#             remaining_cards = node.cards
#             while remaining_cards >= self.cardsPerPackage:
#                 self.emptyPackage.append(Package(self.cardsPerPackage, index))
#                 remaining_cards -= self.cardsPerPackage
#                 node.cards = remaining_cards  # 修改节点的卡片数量
#
#     def __repr__(self):
#         return f"Group(emptyPackage={self.emptyPackage}, usedPackage={self.usedPackage}, theta={self.theta})"
#
#
# # 示例使用
# nodes = [Node(8) for _ in range(6)]  # 创建3个节点，每个节点有8张卡
# group = Group(6, nodes, 0.5)  # 假设每个包打包4张卡
#
# # 打印生成的包和节点的卡片数量
# for package in group.emptyPackage:
#     print(package)
#
# # 打印每个节点的卡片数量，验证是否被修改
# for node in nodes:
#     print(f"Node cards: {node.cards}")


class a:
    def __init__(self,arg1):
        self.arg=arg1

    def __repr__(self):
        return str(self.arg)

class b:
    def __init__(self,num):
        self.somea=[a(2) for _ in range(num)]

    def __getitem__(self, item):
        return self.somea[item]

    def __repr__(self):
        return str([repr(x) for x in self.somea])

B=b(10)
a=B[2]
a.arg=10
print(repr(B))