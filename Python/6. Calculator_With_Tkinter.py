import tkinter as tk  # Import the tkinter module for creating GUI applications

calculation = ""  # Initialize an empty string to store the ongoing calculation

def append_to_calculation(symbol):
    # Function to append a symbol to the calculation
    global calculation  # Use the global calculation variable
    calculation += str(symbol)  # Append the symbol to the calculation string
    result.delete(1.0, "end")  # Clear the result Text widget
    result.insert(1.0, calculation)  # Insert the updated calculation string into the Text widget

def evaluate_calculation():
    # Function to evaluate the current calculation
    global calculation  # Use the global calculation variable
    try:
        result_val = str(eval(calculation))  # Evaluate the calculation and convert the result to a string
        calculation = result_val  # Update the calculation string to the result
        result.delete(1.0, "end")  # Clear the result Text widget
        result.insert(1.0, result_val)  # Insert the result into the Text widget
    except:  # If there's an error during evaluation
        clear()  # Clear the calculation
        result.insert(1.0, "Error")  # Display an error message

def clear():
    # Function to clear the current calculation
    global calculation  # Use the global calculation variable
    calculation = ""  # Reset the calculation string to empty
    result.delete(1.0, "end")  # Clear the result Text widget

root = tk.Tk()  # Create the main application window
root.geometry("300x305")  # Set the window size

result = tk.Text(root, height=2, width=16, font=("Arial", 24))  # Create a Text widget for displaying the calculation/result
result.grid(columnspan=5)  # Position the Text widget, spanning 5 columns

# Define the buttons with their text, row, and column positions
buttons = [
    ('1', 2, 1), ('2', 2, 2), ('3', 2, 3),
    ('4', 3, 1), ('5', 3, 2), ('6', 3, 3),
    ('7', 4, 1), ('8', 4, 2), ('9', 4, 3),
    ('0', 5, 2), ('+', 2, 4), ('-', 3, 4),
    ('*', 4, 4), ('/', 5, 4), ('(', 5, 1),
    (')', 5, 3)
]

for (text, row, col) in buttons:
    # Create a button for each entry in the buttons list
    button = tk.Button(root, text=text, command=lambda t=text: append_to_calculation(t), width=5, font=("Arial", 14), bd=5)
    button.grid(row=row, column=col)  # Position the button in the grid

button_clear = tk.Button(root, text="C", command=clear, width=10, font=("Arial", 14), bd=5)  # Create the clear button
button_clear.grid(row=6, column=1, columnspan=2)  # Position the clear button

button_equal = tk.Button(root, text="=", command=evaluate_calculation, width=10, font=("Arial", 14), bd=5, background='orange', fg='white')  # Create the equal button
button_equal.grid(row=6, column=3, columnspan=2)  # Position the equal button

root.mainloop()  # Start the main event loop of the application
