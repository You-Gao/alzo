import threading
import tkinter as tk

def make_message_box(message):
    def show_box():
        root = tk.Tk()
        root.title("alzo")
        root.attributes("-topmost", True)
        root.resizable(False, False)

        label = tk.Label(root, text=message, padx=20, pady=20, justify="left", wraplength=1000, anchor="center") #wrap is kind of magic, but max-width of your monitor
        label.pack()
        
        x,y = get_middle(root)
        root.geometry(f"+{x}+{y}")

        root.overrideredirect(False)
        root.mainloop()

    threading.Thread(target=show_box, daemon=True).start()
    
def get_middle(root: tk):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2) + 1350 # Magic number, but meant to move if you have multiple monitors
    y = (screen_height // 2) - (height // 2) + 350 # Same as above, X,Y starts at 0,0 top-left of screen
    return x,y
 
# Helps place root.geometry to where you want it    
def get_mouse_position():
    root = tk.Tk()
    root.withdraw()
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    root.destroy()
    return x, y
    
if __name__ == "__main__":
    make_message_box("THIS IS A REALLY LONG MESSAGE THAT WILL TAKE A LOT MORE SPACE THIS IS A REALLY LONG MESSAGE THAT WILL TAKE A LOT MORE SPACETHIS IS A REALLY LONG MESSAGE THAT WILL TAKE A LOT MORE SPACETHIS IS A REALLY LONG MESSAGE THAT WILL TAKE A LOT MORE SPACE")
    while True:
        import time
        time.sleep(.5)
        print(get_mouse_position())