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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Function input
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter function of x, e.g., 5*x^3 + 2*x")
        self.input_layout.addWidget(self.function_input)

        # Min and max inputs
        self.min_input = QLineEdit()
        self.min_input.setPlaceholderText("Enter min value of x")
        self.input_layout.addWidget(self.min_input)

        self.max_input = QLineEdit()
        self.max_input.setPlaceholderText("Enter max value of x")
        self.input_layout.addWidget(self.max_input)

        self.layout.addLayout(self.input_layout)

        # Plot button
        self.plot_button = QPushButton("Plot Function")
        self.plot_button.clicked.connect(self.plot_function)
        self.layout.addWidget(self.plot_button)

        # Matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def plot_function(self):
        function = self.function_input.text()
        function = function.replace(" ", "")
        min_x = self.min_input.text()
        max_x = self.max_input.text()

        # Validate inputs
        if not self.validate_inputs(function, min_x, max_x):
            return

        try:
            min_x = float(min_x)
            max_x = float(max_x)
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

        # Clear previous plot
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title(f"Plot of {function}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.canvas.draw()

    def validate_inputs(self, function, min_x, max_x):
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
        function = function.replace("^", "**")
        function = function.replace("log10", "np.log10")
        function = function.replace("sqrt", "np.sqrt")
        return function

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec_())
