# Function Plotter

## Overview

This project is a simple function plotter application built using PySide2 for the GUI and Matplotlib for plotting. The application allows users to input a mathematical function and plot its graph over a specified range.

## Features

- Input a function of `x`, e.g., `5*x^3 + 2*x`.
- Specify minimum and maximum values for `x`.
- Supports operators: `+`, `-`, `/`, `*`, `^`, `log10()`, `sqrt()`.
- Input validation with user-friendly error messages.
- GUI built using PySide2.
- Plotting powered by Matplotlib.


## Compatibility

This project is developed and tested using Python 3.9. Due to compatibility issues with PySide2 in newer Python versions, it is highly recommended to use Python 3.9 for running this application.

Download Python 3.9.6 from the official Python website:
   [Python 3.9.6](https://www.python.org/downloads/release/python-396/)

> The version used in this project is python3.9.6 that is mentioned above.  


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/HalemoGPA/master_micro_task.git
    cd master_micro_task
    ```

2. Create a virtual environment:
    ```bash
    python -m venv master_micro
    master_micro\Scripts\activate   # On macOS and Linux, use `source master_micro/bin/activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the application, execute the following command:
```bash
python src/main.py
```

## Running the Tests

To run the tests, use the following command:
```bash
pytest
```

## Examples

### Basic Function Input
- **Function:** `5*x^3 + 2*x`
- **Range:** `0` to `10`
- **Expected Output:** Parabolic curve.   <br>   
![Basic Function](screenshots/ex1.JPG)


### Invalid Character in Function
- **Function:** `5*x^3 + 2*x + !`
- **Range:** `0` to `10`
- **Expected Output:** Error message: "Function contains invalid characters."   <br>   
![Invalid Character](screenshots/ex2.JPG)


### Complex Formula Function
- **Function:** `5*x^3 + 2*x -4/x + 7`
- **Range:** `-10` to `10`
- **Expected Output:** Combined plot of Cubic and rational functions.   <br>   
![Complex Formula](screenshots/ex3.JPG)


### Using Sqrt & log10 in Function
- **Function:** `2*x^4 - log10(x) + sqrt(x)`
- **Range:** `0` to `50`
- **Expected Output:** Combined plot of square root, logarithm, and quadratic function.   <br>   
![Complex Formula](screenshots/ex4.JPG)


### Negative Input to sqrt or log10
- **Function:** `2*x^4 - log10(x) + sqrt(x)`
- **Range:** `-50` to `500`
- **Expected Output:** Error message: "Min value must be non-negative for functions with log10 or sqrt."   <br>  
![Negative Input](screenshots/ex5.JPG)


### Wrong Input for Min and Max Values
- **Function:** `x`
- **Range:** `a` to `2`
- **Expected Output:** Error message: "Min and Max values must be numbers."    <br>  
![Wrong Input](screenshots/ex7.JPG)



### Using -inf and +inf for min and max values
- **Function:** `x`
- **Range:** `-inf` to `inf`
- **Expected Output:** Straight 45deg line from -inf to +inf    <br>  
![-inf to inf range](screenshots/ex8.JPG)

### Constant Function Formula
- **Function:** `5`
- **Range:** `-10` to `10`
- **Expected Output:** Straight horizontal line from -inf to +inf    <br>  
![constant function](screenshots/ex9.JPG)


### Empty Function
- **Function:** ` `
- **Range:** ` ` to ` `
- **Expected Output:** Error message: "Function cannot be empty."       <br>  
![constant function](screenshots/ex11.JPG)

### Min value is larger than Max value
- **Function:** `x`
- **Range:** `10` to `5`
- **Expected Output:** Error message: "Min value must be less than Max value."       <br>  
![constant function](screenshots/ex12.JPG)


### Empty Min value
- **Function:** `x`
- **Range:** ` ` to `5`
- **Expected Output:** Error message: "Min and Max values cannot be empty."       <br>  
![constant function](screenshots/ex13.JPG)

## Screenshot of running the automated tests
![automated tests](screenshots/ex14.JPG)