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


def test_invalid_function_input(function_plotter, qtbot):
    function_plotter.function_input.setText("5*x^3 + 2*x + !")
    function_plotter.min_input.setText("0")
    function_plotter.max_input.setText("10")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert (
        "Function contains invalid characters."
        in function_plotter.centralWidget().findChildren(QMessageBox)[0].text()
    )


def test_invalid_min_max_values(function_plotter, qtbot):
    function_plotter.function_input.setText("5*x^3 + 2*x")
    function_plotter.min_input.setText("10")
    function_plotter.max_input.setText("0")
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    assert (
        "Min value must be less than Max value."
        in function_plotter.centralWidget().findChildren(QMessageBox)[0].text()
    )
