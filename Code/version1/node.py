
class BaseNode:
    NODEID = 0

    def __init__(self, cards_per_node: int):
        self.node_id = BaseNode.NODEID          #唯一标识NodeID
        self.cards = cards_per_node             #每个node的cards数量
        self.tasks = []                         #存储当前节点中正在处理的任务
        self.remainCards = cards_per_node       #存储当前节点中剩余的卡


    def __repr__(self):
        return self.cards
