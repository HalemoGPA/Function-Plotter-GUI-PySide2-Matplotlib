import sys
import os
import pytest
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtCore import Qt

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from main import FunctionPlotter


@pytest.fixture(scope="session")
def app_instance():
    """
    Fixture for creating a QApplication instance.

    Returns:
    - QApplication: The QApplication instance.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def function_plotter(app_instance, qtbot):
    """
    Fixture for creating a FunctionPlotter instance.

    Parameters:
    - app_instance (QApplication): The QApplication instance.
    - qtbot (QtBot): The QtBot instance for simulating user interactions.

    Returns:
    - FunctionPlotter: The FunctionPlotter instance.
    """
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    return plotter


# good input tests


def test_valid_function_input(function_plotter, qtbot):
    """
    Test plotting a valid function.
    """
    function_plotter.function_input.setText("5*x^3 + 2*x")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_logarithm(function_plotter, qtbot):
    """
    Test plotting a function with a logarithm.
    """
    function_plotter.function_input.setText("log10(x)")
    function_plotter.min_input.setText("1")
    function_plotter.max_input.setText("100")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_square_root(function_plotter, qtbot):
    """
    Test plotting a function with a square root.
    """
    function_plotter.function_input.setText("sqrt(x)")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("25")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_combined_operators(function_plotter, qtbot):
    """
    Test plotting a function with combined operators.
    """
    function_plotter.function_input.setText("sqrt(x) + log10(x) + x^2")
    function_plotter.min_input.setText("1")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_large_range_of_x(function_plotter, qtbot):
    """
    Test plotting a function over a large range of x values.
    """
    function_plotter.function_input.setText("x^2")
    function_plotter.min_input.setText("-1000")
    function_plotter.max_input.setText("1000")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_small_range_of_x(function_plotter, qtbot):
    """
    Test plotting a function over a small range of x values.
    """
    function_plotter.function_input.setText("x^2")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("1")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_negative_x_values(function_plotter, qtbot):
    """
    Test plotting a function with negative x values.
    """
    function_plotter.function_input.setText("x^3")
    function_plotter.min_input.setText("-10")
    function_plotter.max_input.setText("0")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_high_degree_polynomial(function_plotter, qtbot):
    """
    Test plotting a high-degree polynomial function.
    """
    function_plotter.function_input.setText("x^6 - 2*x^4 + x^2")
    function_plotter.min_input.setText("-10")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_floating_point_coefficients(function_plotter, qtbot):
    """
    Test floating point coefficients function.
    """
    function_plotter.function_input.setText("0.5*x^2 + 2.5*x")
    function_plotter.min_input.setText("-5")
    function_plotter.max_input.setText("5")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_spaces(function_plotter, qtbot):
    """
    Test function with spaces.
    """
    function_plotter.function_input.setText("  x ^ 2  +  3 * x ")
    function_plotter.min_input.setText("-5")
    function_plotter.max_input.setText("5")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


# bad input tests


# def test_invalid_function_input_characters(function_plotter, qtbot):
#     function_plotter.function_input.setText("5*x^3 + 2*x + !")
#     function_plotter.min_input.setText("0")
#     function_plotter.max_input.setText("10")
#     qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
#     qtbot.waitUntil(lambda: function_plotter.centralWidget().findChildren(QMessageBox))
#     message_box = function_plotter.centralWidget().findChildren(QMessageBox)[0]
#     assert "Function contains invalid characters." in message_box.text()


# def test_empty_function_input(function_plotter, qtbot):
#     function_plotter.function_input.setText("")
#     function_plotter.min_input.setText("0")
#     function_plotter.max_input.setText("10")
#     qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
#     qtbot.waitUntil(lambda: function_plotter.centralWidget().findChildren(QMessageBox))
#     message_box = function_plotter.centralWidget().findChildren(QMessageBox)[0]
#     assert "Function cannot be empty." in message_box.text()


# def test_invalid_min_max_values(function_plotter, qtbot):
#     function_plotter.function_input.setText("5*x^3 + 2*x")
#     function_plotter.min_input.setText("10")
#     function_plotter.max_input.setText("0")
#     qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
#     qtbot.waitUntil(lambda: function_plotter.centralWidget().findChildren(QMessageBox))
#     message_box = function_plotter.centralWidget().findChildren(QMessageBox)[0]
#     assert "Min value must be less than Max value." in message_box.text()


# def test_non_numeric_min_max_values(function_plotter, qtbot):
#     function_plotter.function_input.setText("5*x^3 + 2*x")
#     function_plotter.min_input.setText("a")
#     function_plotter.max_input.setText("b")
#     qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
#     qtbot.waitUntil(lambda: function_plotter.centralWidget().findChildren(QMessageBox))
#     message_box = function_plotter.centralWidget().findChildren(QMessageBox)[0]
#     assert "Min and Max values must be numbers." in message_box.text()


# def test_empty_min_max_values(function_plotter, qtbot):
#     function_plotter.function_input.setText("x^2")
#     function_plotter.min_input.setText("")
#     function_plotter.max_input.setText("")
#     qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
#     qtbot.waitUntil(lambda: function_plotter.centralWidget().findChildren(QMessageBox))
#     message_box = function_plotter.centralWidget().findChildren(QMessageBox)[0]
#     assert "Min and Max values cannot be empty." in message_box.text()
