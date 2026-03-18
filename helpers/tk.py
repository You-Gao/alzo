import threading
import tkinter as tk

def make_message_box(message):
    def show_box():
        root = tk.Tk()
        root.title("alzo")
        root.attributes("-topmost", True)
        root.resizable(False, False)
        root.geometry("+2280+860")  # Position on screen

        label = tk.Label(root, text=message, padx=20, pady=20)
        label.pack()

        root.overrideredirect(False)
        root.mainloop()

    threading.Thread(target=show_box, daemon=True).start()
 
# Helps place root.geometry to where you want it    
def get_mouse_position():
    root = tk.Tk()
    root.withdraw()
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    root.destroy()
    return x, y
    
if __name__ == "__main__":
    make_message_box("TEST")
    while True:
        import time
        time.sleep(.5)
        print(get_mouse_position())