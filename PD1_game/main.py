from tkinter import *
from constants import *
from Node import Node
from Tree import Tree
from math import sqrt

class NumGame:
    def __init__(self):
        self.root = Tk()
        self.root.title("PR1: Artjoms Kučerjavijs")
        self.root.resizable(False, False)
        self.game_loaded = False
        self.tree = None
        self.is_ai_turn = False
        self.is_ai_maximizator = False
        self.game_depth = 1
        self.playing = False
        self.is_ai_first = False
        self.number_begin = "24"
        self.slider_var = IntVar()
        self.slider_var.set(self.number_begin)
        self.create_widgets()

    def start(self):
        self.root.mainloop()

    def create_widgets(self):
        # create settings interface to choose settings
        self.canvas0 = Canvas(self.root)
        self.label_welcome = Label(self.canvas0, text = welcome_text)
        self.label_turn_ord = Label(self.canvas0, text = "Human will go first")
        self.button_turn_ord = Button(self.canvas0, text="Swap order", command=self.swap)
        self.button_start = Button(self.canvas0, text="Start", command=self.load_game)
        self.slider = Scale(self.canvas0, from_=20, to=100, orient=HORIZONTAL, variable=self.slider_var)
        self.label_slider = Label(self.canvas0, text = "Choose starting number:")
        # place settings
        self.canvas0.pack()
        self.label_welcome.grid(row=0, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.label_turn_ord.grid(row=1, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.button_turn_ord.grid(row=2, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.button_start.grid(row=3, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.label_slider.grid(row=4, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.slider.grid(row=5, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        
    def create_game(self):
        # GAME interface
        if not self.game_loaded:
            self.canvas = Canvas(self.root)
            self.label_player_1 = Label(self.canvas, text = "Player 1(AI)")
            self.label_player_2 = Label(self.canvas, text = "Player 2(human)")
            self.label_result_txt = Label(self.canvas, text = "Number:")
            self.label_result_num = Label(self.canvas, text = "")
            self.label_msg      = Label(self.canvas, text = "", fg="red")
            self.entry_player_1 = Entry(self.canvas)
            self.entry_player_2 = Entry(self.canvas)
            self.button_player_1 = Button(self.canvas, text="Subtract", command=self.subtract_1)
            self.button_player_2 = Button(self.canvas, text="Subtract", command=self.subtract_2)
            self.button_reset    = Button(self.canvas, text="Restart" , command=self.restart_game)
            self.game_loaded = True
        # position all user interface very simply :)
        self.canvas.pack()
        self.label_player_1.grid(row=0, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.label_player_2.grid(row=0, column=2 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.label_result_txt.grid(row=0, column=1 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.label_result_num.grid(row=1, column=1 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.label_msg.grid(row=3, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b), columnspan=3)
        self.entry_player_1.grid(row=1, column=0 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.entry_player_2.grid(row=1, column=2 , padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.button_player_1.grid(row=2, column=0, padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.button_player_2.grid(row=2, column=2, padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        self.button_reset.grid(row=2, column=1, padx=(padx_l, padx_r), pady = (pady_t, pady_b))
        # if I dont use this command, width wont be updated and will be equal to 1
        self.root.update_idletasks()
        # set user interface initial properties
        width = self.root.winfo_width()
        self.label_msg.config(wraplength=width)
        self.set_total_number(self.number_begin)
        self.playing = True
        self.label_result_num.config(text=self.number_begin)
        if self.is_ai_turn:
            self.root.after(1000, self.get_ai_move)
    
    def set_total_number(self, data : int):
        data = str(data)
        self.label_result_num.config(text=data)

    def subtract_1(self):
        #AI entruy
        #player1_input = self.entry_player_1.get()
        #self.__handle_input__(player1_input)
        pass

    def subtract_2(self):
        # players etry
        if self.playing:
            if self.is_ai_turn:
                self.label_msg.config(text=f"Wait for AI to make it's turn!")
            else:
                player2_input = self.entry_player_2.get()
                good_move = self.__handle_input__(player2_input, True)
                if good_move:
                    if not self.game_over():
                        self.is_ai_turn = True
                        self.root.after(1000, self.get_ai_move)
                    else:
                        self.playing = False

    def __handle_input__(self, number : str, is_player : bool = False):
        # check if number was provided
        try:
            number = int(number)
        except ValueError:
            self.label_msg.config(text="Invalid input! Enter an integer")
            return False
        # check if not 0 or 1 was provided
        if number in restricted_input:
            self.label_msg.config(text="Invalid input! 0 and 1 are not allowed")
            return False
        # check if provided number is not larger that total atm
        total = int(self.label_result_num.cget("text"))
        number_2 = number * number
        if number_2 > total:
            self.label_msg.config(text=f"Invalid input! {number}^2 is {number_2} it is too much. Input can not be larger than Number at the moment")
            return False
        self.label_msg.config(text="")
        number = total - number_2
        self.set_total_number(number)
        self.game_depth = self.game_depth + 1
        return True
    
    def load_game(self):
        self.game_depth = 1        
        self.number_begin = self.slider_var.get()
        if self.tree is None or self.tree.root.number != self.number_begin:
            print("Please wait, game tree is loading...")
            self.getTree()
            print("Game tree created!\nPlease wait, evaluating game tree...")
            self.evaluateTree()
            print("Game tree Evaluated! Game ready!")
            #self.printTree()
            #self.tree.printAll()
        self.create_game()
        self.canvas0.pack_forget()

    def swap(self):
        data = self.label_turn_ord.cget("text")
        if data.startswith("Human"):
            data = AI_txt
        else:
            data = HMN_txt
        self.label_turn_ord.config(text=data)
        self.is_ai_turn = not self.is_ai_turn
        # here is_ai_turn is check if ai will be first
        # and first player if maximizator, so if ai is first, it has to maximize
        # and if ai is second it has to minimize
        self.is_ai_maximizator = self.is_ai_turn
        self.is_ai_first = self.is_ai_turn

    def getTree(self):
        root_node = Node(int(self.number_begin), 1) 
        self.tree = Tree(root_node)
        self.tree.createTree(root_node)

    def evaluateTree(self):
        self.tree.evaluate()

    def printTree(self):
        # Outputs tree in UNIX-style
        print("Generated tree:")
        self.tree.printTree(3)
        
    def printProof(self):
        # Proof that there are no duplicates in generated tree!
        self.tree.printAll()
        
    def restart_game(self):
        self.canvas.pack_forget()
        self.canvas0.pack()
        self.label_msg.config(text=f"")
        self.is_ai_turn = False
        self.label_turn_ord.config(text=HMN_txt)
        self.is_ai_first = False

    def set_ai_num(self, num : str):
        self.entry_player_1.delete(0, END)
        self.entry_player_1.insert(0, num)

    def get_ai_move(self):
        if self.is_ai_turn:
            #print("ai is moving...")  
            total = int(self.label_result_num.cget("text")) 
            node = self.tree.findOptimal(number=total,depth=self.game_depth, maximize=self.is_ai_maximizator)
            ai_num = int(sqrt(total - node.number))
            self.set_ai_num(str(ai_num))
            #print(f"ai led to {node.number}")
            self.set_total_number(str(node.number))
            self.game_depth = self.game_depth + 1
            if not self.game_over():
                #print("ai moved")
                self.is_ai_turn = False
            else:
                self.playing = False
                

    def game_over(self):
        total = int(self.label_result_num.cget("text")) 
        node = self.tree.findNode(total, self.game_depth)
        if len(node.children) == 0:
            if node.number % 2 == 1:
                if self.is_ai_first:
                    self.label_msg.config(text="Game over! Human won")
                else:
                    self.label_msg.config(text="Game over! AI won")
            else:
                if self.is_ai_first:
                    self.label_msg.config(text="Game over! AI won")
                else:
                    self.label_msg.config(text="Game over! Human won")
            return True
        return False

if __name__ == "__main__":
    my_game = NumGame()
    my_game.start()
    