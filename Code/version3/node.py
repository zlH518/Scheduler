import glob
import config


class Node:
    NodeId = 0
    Nodes = []

    def __init__(self, cards_per_node: int):
        self.node_id = Node.NodeId  # 唯一标识NodeID
        self.cards = cards_per_node  # 每个node的cards数量
        self.tasks = []  # 存储当前节点中正在处理的任务
        self.emptyCards = cards_per_node  # 存储当前节点中剩余的卡
        Node.Nodes.append(self)
        Node.NodeId += 1

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False

    def __bool__(self):
        return self.emptyCards != 0

    def __repr__(self):
        return f"Node(node_id={self.node_id}, cards={self.cards})"

    @classmethod
    def reset(cls):
        cls.Nodes.clear()
        cls.NodeId = 0
        cls.create_Nodes()

    @classmethod
    def create_Nodes(cls):
        for _ in range(config.node_num):
            Node(config.cards_per_node)
        return True


if __name__ == '__main__':
    print("\nResetting Nodes...")
    Node.reset()

    print("Nodes after re-creation:")
    for node in Node.Nodes:
        print(node)