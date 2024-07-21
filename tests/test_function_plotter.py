import sys
import os
import pytest
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget
from PySide2.QtCore import Qt
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

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


# test functions



def test_basic_function_input(function_plotter, qtbot):
    """
    Test plotting a basic function.
    """
    function_plotter.function_input.setText("5*x^3 + 2*x")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_invalid_character_in_function(function_plotter, qtbot):
    with qtbot.wait_signal(
        function_plotter.error_message_signal, timeout=5000
    ) as blocker:
        function_plotter.function_input.setText("5*x^3 + 2*x + !")
        function_plotter.min_input.setText("0")
        function_plotter.max_input.setText("10")
        qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert blocker.args[0] == "Function contains invalid characters."


def test_complex_formula_function(function_plotter, qtbot):
    """
    Test plotting a complex formula function.
    """
    function_plotter.function_input.setText("5*x^3 + 2*x - 4/x + 7")
    function_plotter.min_input.setText("-10")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_using_sqrt_and_log10_in_function(function_plotter, qtbot):
    """
    Test plotting a function using sqrt and log10.
    """
    function_plotter.function_input.setText("2*x^4 - log10(x) + sqrt(x)")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("50")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_negative_input_to_sqrt_or_log10(function_plotter, qtbot):
    with qtbot.wait_signal(
        function_plotter.error_message_signal, timeout=5000
    ) as blocker:
        function_plotter.function_input.setText("2*x^4 - log10(x) + sqrt(x)")
        function_plotter.min_input.setText("-50")
        function_plotter.max_input.setText("500")
        qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert blocker.args[0] == "Min value must be non-negative for functions with log10 or sqrt."


def test_wrong_input_for_min_and_max_values(function_plotter, qtbot):
    with qtbot.wait_signal(
        function_plotter.error_message_signal, timeout=5000
    ) as blocker:
        function_plotter.function_input.setText("x")
        function_plotter.min_input.setText("a")
        function_plotter.max_input.setText("2")
        qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert blocker.args[0] == "Min and Max values must be numbers."


def test_using_infinity_for_min_and_max_values(function_plotter, qtbot):
    """
    Test plotting a function with -inf and +inf for min and max values.
    """
    function_plotter.function_input.setText("x")
    function_plotter.min_input.setText("-inf")
    function_plotter.max_input.setText("inf")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()


def test_constant_function_formula(function_plotter, qtbot):
    """
    Test plotting a constant function.
    """
    function_plotter.function_input.setText("5")
    function_plotter.min_input.setText("-10")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert function_plotter.ax.has_data()