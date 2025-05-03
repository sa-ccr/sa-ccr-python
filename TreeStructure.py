import json

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.parent = None
        self.data = {}  # Arbitrary metadata
        self.trade = None
        self.trade_details = None

    def AddChild(self, name):
        if name not in self.children:
            child = TreeNode(name)
            child.parent = self
            self.children[name] = child
        return self.children[name]

    def __getitem__(self, name):
        return self.children[name]

    def __contains__(self, name):
        return name in self.children

    def __repr__(self, level=0):
        indent = "    " * level
        rep = f"{indent}- {self.name}"
        if self.data:
            rep += f" (data: {self.data})"
        if self.trade:
            rep += f" (trade_id: {self.trade.get('external_id', 'N/A')})"
        rep += "\n"
        for child in self.children.values():
            rep += child.__repr__(level + 1)
        return rep

    def print_tree(self):
        print(self.__repr__())

    def find_node(self, name):
        """Recursively find node by name"""
        if self.name == name:
            return self
        for child in self.children.values():
            result = child.find_node(name)
            if result:
                return result
        return None

    def to_dict(self):
        """Export tree to a nested dictionary"""
        result = {
            "name": self.name,
            "data": self.data,
            "trade": self.trade,
            "trade_details": self.trade_details,
            "children": [child.to_dict() for child in self.children.values()]
        }
        return result

    def to_json(self):
        """Export tree to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
