from itertools import combinations

class Torch:
    def __init__(self, time) -> None:
        self.time = time

    def burn(self, time) -> bool:
        self.time = self.time -time
        if self.time < 1:
            self.time = 0    
            return False
        return True

class Node:
    def __init__(self, P1:dict, P2:dict, time) -> None:
        self.P1 = P1.copy()
        self.P2 = P2.copy()
        self.torch = Torch(time)
        self.winnable = False
        self.children = []
       
    def goForward(self, names:list) -> str:
        if len(self.P1) < 2:
            raise Exception("Noone to go forward with")
        t = 0
        for name in names:
            tmp = self.P1.get(name)
            if tmp == None:
                raise Exception("tried to move traveller that is not on P1")
            if tmp > t:
                t = tmp
        if not self.torch.burn(t):
            return "LOST: Torch has burnt down"
        # Move traveleers to P2
        for name in names:
            self.P2[name] = self.P1[name]     
        self.P2 = dict(sorted(self.P2.items()))       
        for name in names:
            del self.P1[name] 
        return ""

    def goBack(self, name) -> str:
        if len(self.P2) == 0:
            raise Exception("Noone to return")
        t = self.P2.get(name)
        if t == None:
            raise Exception("tried to move traveller that is not on P2")
        if not self.torch.burn(t):
            return "LOST: Torch has burnt down"
        # Move traveller to P1
        self.P1[name] = self.P2[name]
        self.P1 = dict(sorted(self.P1.items()))  
        del self.P2[name]
        return ""

    def getVariants(self, count, p) -> list:
        answ = []
        if p == "P1":
            for combination in combinations(self.P1, count):
                answ.append(combination)
        else:
            for combination in combinations(self.P2, count):
                answ.append(combination)
        return answ

    def toString(self):
        return "P1= " + str(self.P1) + " P2= " + str(self.P2) + " t = " + str(self.torch.time)

    def toStringSmooth(self):
        s = "P1 = {"
        for traveller in self.P1.keys():
            s = s + traveller + " "
        s = s.rstrip() + "} P2 = {"
        for traveller in self.P2.keys():
            s = s + traveller + " "
        return s.rstrip() + "}"

    def isEnd(self):
        return self.P1 == END.P1 and self.P2 == END.P2

    def copy(self):
        return Node(self.P1, self.P2, self.torch.time)

    def getTree(self, indent):
        for child in self.children:
            print("-" * indent + child.toStringSmooth(), (("WON" if child.winnable else "LOST") if len(child.children) == 0 else ""), "t =",child.torch.time)
            child.getTree(indent + 3)

END = Node({}, {'A':1, 'B':3, 'C':5}, 0)

def play(node:Node):
    variants_f = node.getVariants(2, "P1")
    i = 0
    for variant_f in variants_f:
        node_f = node.copy()
        answ = node_f.goForward(variant_f)
        if answ.startswith("LOST"):
            #print(answ)
            return
        node.children.append(node_f)
        # print(i, node_f.toString())
        if node_f.isEnd():
            # print(i, "WON")
            node_f.winnable = True
        else:
            variants_b = node_f.getVariants(1, "P2")
            j = 0
            for variant_b in variants_b:
                node_b = node_f.copy()
                answ = node_b.goBack(variant_b[0])
                if answ.startswith("LOST"):
                    # print(answ)
                    return
                node_f.children.append(node_b)
                # print(i, j, node_b.toString())
                play(node_b)
            j = j + 1
        i = i + 1


if __name__ == "__main__":
    node = Node({'A':1, 'B':3, 'C':5}, {}, 12)
    a = node.copy()
    try:
        play(node)
        print("*" * 30)
        print(node.toStringSmooth())
        node.getTree(3)
        pass
    except Exception as e:
        print(str(e))