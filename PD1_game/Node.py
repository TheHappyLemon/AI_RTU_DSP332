class Node:
    # just to see if there are not duplicates in tree graph
    id = 0

    def __init__(self, number, depth) -> None:
        self.number = number
        self.depth = depth
        self.children = []
        self.id = Node.id
        Node.id = Node.id + 1

    def getChildren(self) -> list:
        variants = []
        for i in range(2,self.number):
            square = (i * i)
            if square > self.number:
                break
            node = Node(self.number - square, self.depth + 1)
            
            variants.append(node)
        return variants

    def toString(self) -> str:
        children = self.children
        return f"num {self.number} depth: {self.depth}"

    def toStringSmooth(self) -> str:
        s = f"{self.number}" + ":{"
        for child in self.children:
            s = s + f"{child.number} "
        s = s.strip() + "}"
        return s
    
    def copy(self):
        return Node(self.number, self.depth)
