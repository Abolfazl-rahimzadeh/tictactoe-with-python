import tkinter as tk
from tkinter import messagebox

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, color, text, command=None):
        super().__init__(parent, background=color, width=width, height=height, highlightthickness=0)
        self.corner_radius = corner_radius
        self.command = command
        self.text_str = text

        self.create_round_rectangle(0, 0, width, height, radius=self.corner_radius, fill=color, tags="button")
        self.text_id = self.create_text(width/2, height/2, text=text, fill="black", font=("Arial", 12), tags="button")
        self.tag_bind("button", "<ButtonPress-1>", self._on_click) #Bind click event

    def create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]

        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event=None):
        if self.command is not None:
            self.command()

    def setText(self, text): #setter to update text
       self.itemconfig(self.text_id, text=text) # Updates the text on the item

    def bindClick(self):
        self.tag_bind("button", "<ButtonPress-1>", self._on_click) # rebind the button

    def unbindClick(self):
        self.tag_unbind("button", "<ButtonPress-1>") #unbind so you can't click more

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        self.turn = 0  # Counter for turns
        self.H = 0  # Current player (0 for O, 1 for X)
        self.buttons = []  # List to hold button objects

        # Create buttons
        for i in range(3):
            for j in range(3):
                button = RoundedButton(
                    master,
                    width=80,
                    height=50,
                    corner_radius=15,
                    color="gray",
                    text="",
                    command=lambda row=i, col=j: self.btn_click(row, col),
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

        # Create reset button
        self.reset_button = RoundedButton(
            master,
            width=100,
            height=30,
            corner_radius=10,
            color="white",  # Changed reset button color to white
            text="Reset Game",
            command=self.reset_game,
        )
        self.reset_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Styling
        master.configure(bg='lightgray')


    def btn_click(self, row, col):
        """Handles button clicks."""
        button_index = row * 3 + col
        button = self.buttons[button_index] #button is of type RoundedButton now

        items = button.find_withtag("button") #Gets all items with tag 'button'
        if items:
           text_id = items[1]  #Text will always be the second item.
           current_text = button.itemcget(text_id, "text") #get's text from the item

           if current_text == "":  # check if the button is empty
               self.turn += 1
               self.H = self.turn % 2  # Determine current player

               # Set button text based on the current player
               text = "O" if self.H == 0 else "X"  # set button text based on H
               button.setText(text) #updates the button text using the setText method

                # Check for a winner
               if self.check_for_winner():
                  winner = "O" if self.H == 0 else "X"
                  messagebox.showinfo("Game Over", f"{winner} won!")
                  self.disable_all_buttons()  # Disable all buttons after a win
               elif self.turn == 9:  # Check for a draw
                   messagebox.showinfo("Game Over", "It's a draw!")
                   self.disable_all_buttons()



    def check_for_winner(self):
        """Checks for a winner."""
        b = [self.buttons[i].itemcget(self.buttons[i].find_withtag("button")[1], "text")  for i in range(9)]  # list of text on the buttons
        return (
            (b[0] == b[1] == b[2] != "")
            or (b[3] == b[4] == b[5] != "")
            or (b[6] == b[7] == b[8] != "")
            or (b[0] == b[3] == b[6] != "")
            or (b[1] == b[4] == b[7] != "")
            or (b[2] == b[5] == b[8] != "")
            or (b[0] == b[4] == b[8] != "")
            or (b[2] == b[4] == b[6] != "")
        )

    def disable_all_buttons(self):
        """Disables all buttons after the game is over."""
        for button in self.buttons:
            button.unbindClick() #call our new unbind

    def reset_game(self):
        """Resets the game state."""
        self.turn = 0  # Reset turn counter
        for button in self.buttons:
           button.setText("")  # Clear the text using setter method
           button.bindClick()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
