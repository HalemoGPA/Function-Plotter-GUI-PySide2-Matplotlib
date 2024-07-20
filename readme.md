# Function Plotter

## Overview

This project is a simple function plotter application built using PySide2 for the GUI and Matplotlib for plotting. The application allows users to input a mathematical function and plot its graph over a specified range.

## Features

- Input a mathematical function of `x` (e.g., `5*x^3 + 2*x`).
- Specify the range for `x` (min and max values).
- Validate inputs to ensure correct function syntax and valid range.
- Plot the function using Matplotlib.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/FunctionPlotterProject.git
    cd FunctionPlotterProject
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the application, execute the following command:
```bash
python src/main.py
