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
    """Fixture for creating a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def function_plotter(app_instance, qtbot):
    """Fixture for creating a FunctionPlotter instance."""
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    return plotter


def test_valid_function_input(function_plotter, qtbot):
    function_plotter.function_input.setText("5*x^3 + 2*x")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_logarithm(function_plotter, qtbot):
    function_plotter.function_input.setText("log10(x)")
    function_plotter.min_input.setText("1")
    function_plotter.max_input.setText("100")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_square_root(function_plotter, qtbot):
    function_plotter.function_input.setText("sqrt(x)")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("25")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_function_with_combined_operators(function_plotter, qtbot):
    function_plotter.function_input.setText("sqrt(x) + log10(x) + x^2")
    function_plotter.min_input.setText("1")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_large_range_of_x(function_plotter, qtbot):
    function_plotter.function_input.setText("x^2")
    function_plotter.min_input.setText("-1000")
    function_plotter.max_input.setText("1000")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_small_range_of_x(function_plotter, qtbot):
    function_plotter.function_input.setText("x^2")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("1")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_negative_x_values(function_plotter, qtbot):
    function_plotter.function_input.setText("x^3")
    function_plotter.min_input.setText("-10")
    function_plotter.max_input.setText("0")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_high_degree_polynomial(function_plotter, qtbot):
    function_plotter.function_input.setText("x^6 - 2*x^4 + x^2")
    function_plotter.min_input.setText("-10")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_floating_point_coefficients(function_plotter, qtbot):
    function_plotter.function_input.setText("0.5*x^2 + 2.5*x")
    function_plotter.min_input.setText("-5")
    function_plotter.max_input.setText("5")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()




def test_function_with_spaces(function_plotter, qtbot):
    function_plotter.function_input.setText("  x ^ 2  +  3 * x ")
    function_plotter.min_input.setText("-5")
    function_plotter.max_input.setText("5")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()
