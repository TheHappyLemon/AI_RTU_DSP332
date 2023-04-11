from Node import Node

class Tree:
    def __init__(self, root) -> None:
        self.nodes = []
        self.root = root
        self.addNode(self.root)
    
    def addNode(self, node : Node) -> None:
        #print("adding", node.toString())
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
        #print(f"looking for num {number} depth {depth}")
        for node in self.nodes:
            #print(node.toString(), "same?->", node.number == number and node.depth == depth)
            #input()
            if node.number == number and node.depth == depth:
                return node
        return None
