from tkinter import *
from constants import *
from Node import Node
from Tree import Tree

class NumGame:
    def __init__(self):
        self.root = Tk()
        self.root.title("PR1: Artjoms Kučerjavijs")
        self.root.resizable(False, False)
        self.create_widgets()
        self.tree = None

    def start(self):
        self.root.mainloop()

    def create_widgets(self):
        # create all user interface to play the game
        self.label_player_1 = Label(self.root, text = "Player 1")
        self.label_player_2 = Label(self.root, text = "Player 2")
        self.label_result_txt = Label(self.root, text = "Number:")
        self.label_result_num = Label(self.root, text = "")
        self.label_msg      = Label(self.root, text = "", fg="red")
        self.entry_player_1 = Entry(self.root)
        self.entry_player_2 = Entry(self.root)
        self.button_player_1 = Button(self.root, text="Subtract", command=self.subtract_1)
        self.button_player_2 = Button(self.root, text="Subtract", command=self.subtract_2)
        self.button_reset    = Button(self.root, text="Restart" , command=self.restart_game)
        # position all user interface very simply :)
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
        self.label_result_num.config(text=number_begin)
        self.set_total_number(number_begin)
    
    def set_total_number(self, data : int):
        data = str(data)
        self.label_result_num.config(text=data)

    def subtract_1(self):
        player1_input = self.entry_player_1.get()
        self.__handle_input__(player1_input)

    def subtract_2(self):
        player2_input = self.entry_player_2.get()
        self.__handle_input__(player2_input)

    def __handle_input__(self, number : str):
        # check if number was provided
        try:
            number = int(number)
        except ValueError:
            self.label_msg.config(text="Invalid input! Enter an integer")
            return
        # check if not 0 or 1 was provided
        if number in restricted_input:
            self.label_msg.config(text="Invalid input! 0 and 1 are not allowed")
            return
        # check if provided number is not larger that total atm
        total = int(self.label_result_num.cget("text"))
        number_2 = number * number
        if number_2 > total:
            self.label_msg.config(text=f"Invalid input! {number}^2 is {number_2} it is too much. Input can not be larger than Number at the moment")
            return
        self.label_msg.config(text="")
        number = total - number_2
        self.set_total_number(number)
    
    def getTree(self):
        root_node = Node(int(self.label_result_num.cget("text")), 0) 
        self.tree = Tree(root_node)
        self.tree.createTree(root_node)

    def printTree(self):
        # Outputs tree in UNIX-style
        print("Generated tree:")
        self.tree.printTree(3)
        
    def printProof(self):
        # Proof that there are no duplicates in generated tree!
        self.tree.printAll()
        

    def restart_game(self):
        print("Game restarted...")
        


if __name__ == "__main__":
    my_game = NumGame()
    my_game.getTree()
    my_game.printTree()
    my_game.start()