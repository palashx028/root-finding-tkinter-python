import tkinter as tk
from tkinter import messagebox, filedialog
from sympy import symbols, sympify, lambdify
import matplotlib.pyplot as plt
import numpy as np

def preprocess_function_input(user_input):
    expr = user_input.replace('^', '**')
    expr = expr.replace('X', 'x')
    return expr

def bisection_method(func_str, error_tol=1e-4):
    x = symbols('x')
    expr = sympify(func_str)
    f = lambdify(x, expr, modules=['math'])

    found = False
    for i in range(-100, 100):
        a = i
        b = i + 1
        try:
            if f(a) * f(b) < 0:
                found = True
                break
        except:
            continue
    if not found:
        raise ValueError("No valid interval found in [-100,100]. Try a different function.")

    iterations = []
    iteration = 1

    while True:
        c = (a + b) / 2
        fc = f(c)
        iterations.append((iteration, a, b, c, fc))

        if abs(fc) < error_tol or iteration > 1000:
            break

        if f(a) * fc < 0:
            b = c
        else:
            a = c

        iteration += 1

    return expr, iterations, c, fc

def save_iterations(iterations, filepath):
    with open(filepath, 'w') as f:
        f.write("| Iter |     a     |     b     |     c     |    f(c)    |\n")
        f.write("-----------------------------------------------------------\n")
        for it in iterations:
            f.write(f"| {it[0]:>4} | {it[1]:9.5f} | {it[2]:9.5f} | {it[3]:9.5f} | {it[4]:10.6f} |\n")

def plot_function(expr, root):
    x = symbols('x')
    f = lambdify(x, expr, modules=['numpy'])
    x_vals = np.linspace(root - 10, root + 10, 400)
    y_vals = f(x_vals)

    plt.figure(figsize=(8,5))
    plt.plot(x_vals, y_vals, label='f(x)')
    plt.axhline(0, color='black', lw=0.8)
    plt.plot(root, f(root), 'ro', label=f'Root ≈ {root:.6f}')
    plt.title('Function Plot with Root (Bisection Method)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()

def run_bisection():
    user_input = entry_func.get()
    func_str = preprocess_function_input(user_input)

    error_str = entry_error.get()

    if not func_str.strip():
        messagebox.showerror("Input Error", "Please enter a function.")
        return

    try:
        error_tol = float(error_str)
        if error_tol <= 0:
            raise ValueError()
    except:
        messagebox.showerror("Input Error", "Enter a positive numeric error tolerance.")
        return

    try:
        expr, iterations, root, froot = bisection_method(func_str, error_tol)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Function: f(x) = {expr}\n")
    output_text.insert(tk.END, f"Approximate root: {root:.6f}\n")
    output_text.insert(tk.END, f"f(root) = {froot:.6f}\n")
    output_text.insert(tk.END, f"Total iterations: {len(iterations)}\n\n")
    output_text.insert(tk.END, "| Iter |     a     |     b     |     c     |    f(c)    |\n")
    output_text.insert(tk.END, "-----------------------------------------------------------\n")
    for it in iterations:
        output_text.insert(tk.END, f"| {it[0]:>4} | {it[1]:9.5f} | {it[2]:9.5f} | {it[3]:9.5f} | {it[4]:10.6f} |\n")

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files","*.txt"),("All Files","*.*")],
        title="Save iteration table as..."
    )
    if save_path:
        save_iterations(iterations, save_path)
        messagebox.showinfo("Saved", f"Iteration table saved to:\n{save_path}")

    plot_function(expr, root)

root = tk.Tk()
root.title("Bisection Method Solver")

tk.Label(root, text="Enter function f(x):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_func = tk.Entry(root, width=40)
entry_func.grid(row=0, column=1, padx=5, pady=5)
entry_func.insert(0, "x^3 - 2*x^2 - 1")  # default example with ^

tk.Label(root, text="Error tolerance:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_error = tk.Entry(root, width=20)
entry_error.grid(row=1, column=1, padx=5, pady=5)
entry_error.insert(0, "0.0001")

btn_run = tk.Button(root, text="Run Bisection Method", command=run_bisection)
btn_run.grid(row=2, column=0, columnspan=2, pady=10)

output_text = tk.Text(root, width=70, height=20)
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
# This code implements a GUI for the Bisection Method to find roots of functions.
# It allows users to input a function and an error tolerance, runs the method.                          
