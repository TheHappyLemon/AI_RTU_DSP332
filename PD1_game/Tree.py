from Node import Node

class Tree:
    def __init__(self, root) -> None:
        self.nodes = []
        self.root = root
        self.addNode(self.root)
    
    def addNode(self, node : Node) -> None:
        self.nodes.append(node)
        
    def createTree(self, node : Node):            
        variants = node.getChildren()
        # Check if such child already exists. If not - add to children
        # and generate tree for new child
        for variant in variants:
            node_existing = self.findNode(variant.number, variant.depth)
            if node_existing == None: 
                self.addNode(variant)
                node.children.append(variant)
            else:
                node.children.append(node_existing)
            self.createTree(variant)

    def evaluate(self) -> None:
        self.root.evaluate()

    def printAll(self):
        # Proof that there are no duplicates in the tree!
        sorted_list = sorted(self.nodes, key=lambda x: x.number)
        for node in sorted_list:
            s = f"{node.number}({node.id}):["
            for child in node.children:
                s = s + f"{child.number}({child.id}),"
            s = s.strip(",") + "]"
            print(s)

    def printTree(self, indent):
        print(self.root.toStringSmooth())
        self.__getTree(indent, self.root)

    def __getTree(self, indent : int, node : Node):
        # prints out a tree
        for child in node.children:
            print("-" * indent + child.toStringSmooth())
            self.__getTree(indent + 3, child)

    def findNode(self, number : int, depth : int) -> bool:
        # check if on a given depth there already is such node
        for node in self.nodes:
            if node.number == number and node.depth == depth:
                return node
        return None
    
    def findOptimal(self, number : int, depth : int, maximize : bool) -> bool:
        # Find best variant between node children (max or min)
        node = self.findNode(number, depth)
        if maximize:
            optimal = float('-inf')
        else:
            optimal = float('inf')
        result = None
        for child in node.children:
            if maximize:
                if child.value > optimal:
                    result = child
                    optimal = max(optimal, child.value)
            else:
                if child.value < optimal:
                    result = child
                    optimal = min(optimal, child.value)
        #print(f"optimal value when maximizin = {maximize} for {number} on lvl {depth} is {result.number}")
        return result
