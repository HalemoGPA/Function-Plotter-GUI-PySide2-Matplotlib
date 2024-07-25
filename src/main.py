import sys
import os
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
from PySide2.QtCore import Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Suppress font warnings
os.environ["QT_LOGGING_RULES"] = "qt.qpa.fonts.warning=false"


class FunctionPlotter(QMainWindow):
    """
    Main window for the function plotter application.

    This class handles the GUI elements, user inputs, and plotting of mathematical functions
    using PySide2 for the GUI and Matplotlib for plotting.
    """

    error_message_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface elements."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_layout = QHBoxLayout()
        self.function_input = self.create_line_edit(
            "Enter function of x, e.g., 5*x^3 + 2*x"
        )
        self.min_input = self.create_line_edit("Enter min value of x")
        self.max_input = self.create_line_edit("Enter max value of x")

        self.input_layout.addWidget(self.function_input)
        self.input_layout.addWidget(self.min_input)
        self.input_layout.addWidget(self.max_input)
        self.layout.addLayout(self.input_layout)

        self.plot_button = QPushButton("Plot Function")
        self.plot_button.clicked.connect(self.plot_function)
        self.layout.addWidget(self.plot_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def create_line_edit(self, placeholder):
        """
        Create a QLineEdit with a placeholder text.

        Parameters:
        - placeholder (str): The placeholder text for the QLineEdit.

        Returns:
        - QLineEdit: The created QLineEdit object.
        """
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        return line_edit

    def plot_function(self):
        """Handle the plotting of the function based on user inputs."""
        function = self.function_input.text().replace(" ", "")
        min_x, max_x = self.min_input.text(), self.max_input.text()

        if not self.validate_inputs(function, min_x, max_x):
            return

        min_x, max_x = self.parse_range(min_x, max_x)
        x = np.linspace(min_x, max_x, 400)
        if "log10" in function:
            x = np.where(
                x == 0, 1e-15, x
            )  # Add a small value to x where x is 0 if log10 is in the function

        try:
            y = eval(self.prepare_function(function, x))
        except Exception as e:
            self.show_error_message(f"Error in function evaluation: {e}")
            return

        self.update_plot(x, y, function)

    def validate_inputs(self, function, min_x, max_x):
        """
        Validate the user inputs for the function and range values.

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

        try:
            min_x = float(min_x)
            max_x = float(max_x)
        except ValueError:
            self.show_error_message("Min and Max values must be numbers.")
            return False

        if min_x >= max_x:
            self.show_error_message("Min value must be less than Max value.")
            return False

        if ("log10" or "sqrt") in function and min_x < 0:
            self.show_error_message(
                "Min value must be non-negative for functions with log10 or sqrt."
            )
            return False

        if "/0" in function:
            self.show_error_message("Division by zero is not allowed.")
            return False

        return True

    def parse_range(self, min_x, max_x):
        """
        Parse and limit the range values to a valid range.

        Parameters:
        - min_x (str): The minimum value of x entered by the user.
        - max_x (str): The maximum value of x entered by the user.

        Returns:
        - tuple: The parsed and limited range values.
        """
        min_x = max(min(1e20, float(min_x)), -1e20)
        max_x = max(min(1e20, float(max_x)), -1e20)
        return min_x, max_x

    def prepare_function(self, function, x):
        """
        Prepare the function for evaluation by replacing operators with their numpy equivalents.

        Parameters:
        - function (str): The mathematical function entered by the user.
        - x (np.ndarray): The array of x values.

        Returns:
        - str: The prepared function.
        """
        function = function.replace("^", "**")
        function = function.replace("log10", "np.log10")
        function = function.replace("sqrt", "np.sqrt")

        if "x" not in function:
            function = f"{function}*np.ones_like(x)"
        return function

    def update_plot(self, x, y, function):
        """
        Update the plot with the new function.

        Parameters:
        - x (np.ndarray): The array of x values.
        - y (np.ndarray): The array of y values.
        - function (str): The mathematical function entered by the user.
        """
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title(f"Plot of {function}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.canvas.draw()

    def show_error_message(self, message):
        """
        Display an error message dialog.

        Parameters:
        - message (str): The error message to display.
        """
        QMessageBox.critical(self, "Error", message)
        self.error_message_signal.emit(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())
