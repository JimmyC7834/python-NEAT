import tkinter as tk

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


# Create a frame for the canvas with non-zero row&column weights
# frame_canvas = tk.Frame(frame_main)
# frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
# frame_canvas.grid_rowconfigure(0, weight=1)
# frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
#frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(root, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# Add 9-by-5 buttons to the frame
rows = 9
columns = 5
buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
for i in range(0, rows):
    for j in range(0, columns):
        buttons[i][j] = tk.Canvas(frame_buttons,bg='blue', width = 50, height=50)
        buttons[i][j].grid(row=i, column=j, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

# Launch the GUI
root.mainloop()