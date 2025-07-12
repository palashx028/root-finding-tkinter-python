# Root Finding Tkinter Python

This project implements two numerical root-finding methods — **Bisection Method** and **False Position Method (Regula Falsi)** — using Python Tkinter GUI.

## Features
- User inputs function as a string, e.g. `x^3 - 2x^2 - 1`
- Automatically finds suitable interval for root search
- Displays iteration tables with root approximation
- Allows saving iteration data to `.txt` file
- Plots the function and marks the root on the graph

## Requirements

- Python 3.x
- Packages: `sympy`, `matplotlib`, `numpy`

Install required packages:

```bash
pip install -r requirements.txt
