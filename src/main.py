import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FunctionPlotter(QMainWindow):
    """
    A class representing the main window for the function plotter application.

    This class handles the GUI elements, user inputs, and plotting of mathematical functions
    using PySide2 for the GUI and Matplotlib for plotting.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")

        # Initialize the central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Initialize input fields for the function and range values
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter function of x, e.g., 5*x^3 + 2*x")
        self.input_layout.addWidget(self.function_input)

        self.min_input = QLineEdit()
        self.min_input.setPlaceholderText("Enter min value of x")
        self.input_layout.addWidget(self.min_input)

        self.max_input = QLineEdit()
        self.max_input.setPlaceholderText("Enter max value of x")
        self.input_layout.addWidget(self.max_input)

        self.layout.addLayout(self.input_layout)

        # Initialize the plot button
        self.plot_button = QPushButton("Plot Function")
        self.plot_button.clicked.connect(self.plot_function)
        self.layout.addWidget(self.plot_button)

        # Initialize the Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def plot_function(self):
        """
        Handles the plotting of the function based on user inputs.
        """
        function = self.function_input.text().replace(" ", "")
        min_x = self.min_input.text()
        max_x = self.max_input.text()

        # Validate inputs
        if not self.validate_inputs(function, min_x, max_x):
            return

        try:
            min_x = float(min_x)
            # Make range from -1e20 to 1e20 whatever the input
            min_x = max(min(1e20, min_x), -1e20)
            max_x = float(max_x)
            # Make range from -1e20 to 1e20 whatever the input
            max_x = max(min(1e20, max_x), -1e20)

        except ValueError:
            self.show_error_message("Min and Max values must be numbers.")
            return

        if min_x >= max_x:
            self.show_error_message("Min value must be less than Max value.")
            return

        if ("log10" in function or "sqrt" in function) and min_x < 0:
            self.show_error_message(
                "Min value must be non-negative for functions with log10 or sqrt."
            )
            return

        x = np.linspace(min_x, max_x, 400)
        try:
            y = eval(self.prepare_function(function, x))
        except Exception as e:
            self.show_error_message(f"Error in function evaluation: {e}")
            return

        # Clear previous plot and plot new function
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title(f"Plot of {function}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.canvas.draw()

    def validate_inputs(self, function, min_x, max_x):
        """
        Validates the user inputs for the function and range values.

        Parameters:
        - function (str): The mathematical function entered by the user.
        - min_x (str): The minimum value of x entered by the user.
        - max_x (str): The maximum value of x entered by the user.

        Returns:
        - bool: True if inputs are valid, False otherwise.
        """
        if not function:
            self.show_error_message("Function cannot be empty.")
            return False

        if not re.match(r"^[\d\.\+\-\*/\^x\(\)log10sqrt]*$", function):
            self.show_error_message("Function contains invalid characters.")
            return False

        if not min_x or not max_x:
            self.show_error_message("Min and Max values cannot be empty.")
            return False

        return True

    def prepare_function(self, function, x):
        """
        Prepares the function for evaluation by replacing operators with their numpy equivalents.

        Parameters:
        - function (str): The mathematical function entered by the user.
        - x (np.ndarray): The array of x values.

        Returns:
        - str: The prepared function.
        """
        function = function.replace("^", "**")
        function = function.replace("log10", "np.log10")
        function = function.replace("sqrt", "np.sqrt")
        # if function is a constant (e.g. y=5)
        if "x" not in function:
            function = f"{function}*np.ones_like(x)"
        return function

    def show_error_message(self, message):
        """
        Displays an error message dialog.

        Parameters:
        - message (str): The error message to display.
        """
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())
