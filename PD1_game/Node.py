class Node:
    # just to see if there are not duplicates in tree graph
    id = 0

    def __init__(self, number, depth) -> None:
        self.number = number
        self.depth = depth
        self.children = []
        self.id = Node.id
        self.value = None
        self.evaluated = False
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

    def evaluate(self):
        if self.evaluated:
            # saves some time
            return
        #print(f"evaluating {self.number}")
        # if it is a leaf
        if len(self.children) == 0:
            if self.number == 0:
                # Draw
                self.value = 0
            elif self.number % 2 == 1:
                # First player win
                self.value = -1
            else:
                # Second player win
                self.value = 1
            #print(f"set {self.number} to {self.value}")
            self.evaluated = True
        else:
            # Not a leaf
            if self.depth % 2 == 1:
                # First player's (maximizator) turn
                #print("maximizin")
                max_val = float('-inf')
                for child in self.children:
                    child.evaluate()
                    #print(f"max({max_val}, {child.value}) = {max(max_val, child.value)}")
                    max_val = max(max_val, child.value)
                #print(f"setting {self.number} to {max_val}")
                self.value = max_val
                self.evaluated = True
            else:
                # Second player's (minimizator) turn
                #print("minimizin")
                min_val = float('inf')
                for child in self.children:
                    child.evaluate()
                    #print(f"min({min_val}, {child.value}) = {min(min_val, child.value)}")
                    min_val = min(min_val, child.value)
                #print(f"setting {self.number} to {min_val}")
                #input()
                self.value = min_val
                self.evaluated = True

    def toString(self) -> str:
        children = self.children
        return f"num {self.number} depth: {self.depth}"

    def toStringSmooth(self) -> str:
        s = f"{self.number} val({self.value})" + ":{"
        for child in self.children:
            s = s + f"{child.number} "
        s = s.strip() + "}"
        return s
    
    def copy(self):
        return Node(self.number, self.depth)
