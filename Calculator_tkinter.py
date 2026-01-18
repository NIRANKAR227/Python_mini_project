from tkinter import *
import ast

root = Tk()
root.title("Calculator")

# Display
display = Entry(root, font=("Arial", 14))
display.grid(row=1, columnspan=6, pady=5)

# Insert numbers
def get_number(num):
    display.insert(END, num)

# Insert operations
def get_operation(operator):
    display.insert(END, operator)

# Clear
def clear_all():
    display.delete(0, END)

# Undo
def undo():
    text = display.get()
    display.delete(0, END)
    display.insert(0, text[:-1])

# Calculate safely
def calculate():
    expression = display.get()
    try:
        node = ast.parse(expression, mode="eval")
        result = eval(compile(node, "<string>", "eval"))
        clear_all()
        display.insert(0, result)
    except Exception:
        clear_all()
        display.insert(0, "Error")

# ---------- Buttons ----------

# Numbers
numbers = [1,2,3,4,5,6,7,8,9]
counter = 0

for x in range(2,5):
    for y in range(3):
        text = numbers[counter]
        Button(root, text=text, width=4, height=2,
               command=lambda t=text: get_number(t)).grid(row=x, column=y)
        counter += 1

Button(root, text="0", width=4, height=2,
       command=lambda: get_number(0)).grid(row=5, column=1)

# Operations
operations = ['+','-','*','/','*3.14','%','(',"**",')',"**2"]
count = 0

for x in range(4):
    for y in range(3):
        if count < len(operations):
            op = operations[count]
            Button(root, text=op, width=4, height=2,
                   command=lambda t=op: get_operation(t)).grid(row=x+2, column=y+3)
            count += 1

# Control Buttons
Button(root, text="AC", width=4, height=2, command=clear_all).grid(row=5, column=5)
Button(root, text="=", width=4, height=2, command=calculate).grid(row=5, column=2)
Button(root, text="Del", width=4, height=2, command=undo).grid(row=5, column=4)

root.mainloop()

