"""
ITrack Menu
Log:
11/30/2021 - Design bare menu window and tracker window. No functionality yet.
12/01/2021 - Get QtCharts to work and be able to load multiple layouts in one window.
12/02/2021 - Add tracker button, display tracker button, and delete tracker button are implemented.
12/03/2021 - Implement table in tabular window. Began implementing the add new row button.
12/05/2021 - Finish implementing add new row button.
12/06/2021 - Add confirmation when deleting a tracker. Implement edit button. Weird bug where the back_up_data changed when the original data was edited was fixed.
12/07/2021 - Add feature that keeps the data stored in files when the application is closed. Add feature to change name of tracker.
12/08/2021 - Implement graphical view for trackers. Implement edit x and y axis titles. Fix error that allows user to create titleless or repeated name tracker.
12/09/2021 - Add Doctests to methods that can be tested automatically. Decorate application.
12/13/2021 - Update documentation. Fix bug that makes the program crash when the user enters a name with a \ or / character. Fix bug that allows user to enter a repeated x value in edit window.
"""
from PySide2.QtGui import QFont, QPainter
from PySide2.QtWidgets import (
    QAbstractItemView, QHeaderView, QTableWidgetItem, QWidget, QApplication, QLabel,
    QPushButton, QMainWindow, QGridLayout, QTableWidget, QMessageBox,
    QDialog, QLineEdit)
from PySide2.QtCore import QSize, Qt
from PySide2.QtCharts import QtCharts
import doctest
from os import getcwd, walk, mkdir, path, remove

class Tracker:
    """Class Tracker is a class that has a list
    where all the data is stored and a string that represents 
    the name given to the tracker. It also has a field that
    stores the same values of self.data independently in
    case the data needs to be restored (this field should not be accessed).
    The titles of the x and y axis are also stored, and a back up is also stored
    in case the values need to be restored.
    """
    def __init__(self):
        """Initializes a Tracker class.
        >>> obj = Tracker()
        >>> obj.name
        ''
        >>> obj.data
        []
        >>> obj.back_up_data
        ()
        >>> obj.x_axis_title
        'X-Axis'
        >>> obj.y_axis_title
        'Y-Axis'
        >>> obj.back_up_axis_titles
        ()
        """
        self.name = ""
        self.data = []
        self.back_up_data = ()
        self.x_axis_title = "X-Axis"
        self.y_axis_title = "Y-Axis"
        self.back_up_axis_titles = ()

    def __str__(self):
        """Returns a human readable string
        representing Tracker class.
        >>> obj = Tracker()
        >>> print(obj)
        : []
        >>> obj.name = 'Hi'
        >>> obj.data = [1, 2, 3]
        >>> print(obj)
        Hi: [1, 2, 3]
        """
        return f"{self.name}: {self.data}"
    
    def get_name(self):
        """Returns the name of the tracker saved
        by the user.
        >>> obj = Tracker()
        >>> obj.get_name()
        ''
        >>> obj.name = 'Hi'
        >>> obj.get_name()
        'Hi'
        """
        return self.name
    
    def get_data(self):
        """Returns the data stored in the tracker object.
        >>> obj = Tracker()
        >>> obj.get_data()
        []
        >>> obj.data = [[1, 2]]
        >>> obj.get_data()
        [[1, 2]]
        """
        return self.data
    
    def set_name(self, new_name):
        """Changes name of field self.name to new_name
        >>> obj = Tracker()
        >>> obj.set_name('Hi')
        >>> obj.get_name()
        'Hi'
        >>> obj.set_name('')
        >>> obj.get_name()
        ''
        """
        self.name = new_name
    
    def set_data(self, new_data):
        """Changes data stored in the tracker object
        with new_data
        >>> obj = Tracker()
        >>> obj.set_data([[]])
        >>> obj.get_data()
        [[]]
        >>> obj.set_data([[1, 2], [1, 3]])
        >>> obj.get_data()
        [[1, 2], [1, 3]]
        """
        self.data = new_data
    
    def set_x_axis_title(self, new_title):
        """Sets self.x_axis_title with given new_title
        >>> obj = Tracker()
        >>> previous_title = obj.get_x_axis_title()
        >>> obj.set_x_axis_title('X')
        >>> previous_title != obj.get_x_axis_title()
        True
        >>> obj.get_x_axis_title()
        'X'
        >>> obj.set_x_axis_title('')
        >>> obj.get_x_axis_title()
        ''
        """
        self.x_axis_title = new_title
    
    def set_y_axis_title(self, new_title):
        """Sets self.y_axis_title with given new_title
        >>> obj = Tracker()
        >>> previous_title = obj.get_y_axis_title()
        >>> obj.set_y_axis_title('Y')
        >>> previous_title != obj.get_y_axis_title()
        True
        >>> obj.get_y_axis_title()
        'Y'
        >>> obj.set_y_axis_title('')
        >>> obj.get_y_axis_title()
        ''
        """
        self.y_axis_title = new_title
    
    def get_x_axis_title(self):
        """Returns the title stored in
        self.x_axis_title
        >>> obj = Tracker()
        >>> obj.get_x_axis_title()
        'X-Axis'
        >>> obj.set_y_axis_title('X')
        >>> obj.get_y_axis_title()
        'X'
        """
        return self.x_axis_title
    
    def get_y_axis_title(self):
        """Returns the title stored in
        self.y_axis_title.
        >>> obj = Tracker()
        >>> obj.get_y_axis_title()
        'Y-Axis'
        >>> obj.set_y_axis_title('Y')
        >>> obj.get_y_axis_title()
        'Y'
        """
        return self.y_axis_title
    
    def set_back_up_data(self):
        """Copies the values stored in self.data and the x, y axis titles
        and stores them in the field self.back_up_data and self.back_up_axis_titles
        >>> obj = Tracker()
        >>> obj.set_data([[1, 4], [6, 10]])
        >>> obj.set_back_up_data()
        >>> len(obj.back_up_data) > 0
        True
        >>> len(obj.back_up_axis_titles) > 0
        True
        >>> obj.back_up_axis_titles[0] == obj.get_x_axis_title()
        True
        >>> obj.back_up_axis_titles[1] == obj.get_y_axis_title()
        True
        >>> obj.set_data([[1, 4], [6, 10]])
        >>> obj.back_up_data is obj.get_data()
        False
        """
        self.back_up_data = tuple(tuple(elem) for elem in self.data)
        self.back_up_axis_titles = str(self.get_x_axis_title()), str(self.get_y_axis_title())
    
    def restore_data(self):
        """Restores the values of self.data before
        it was edited.
        >>> obj = Tracker()
        >>> obj.set_data([[2, 0], [10, 2]])
        >>> previous_data = obj.get_data()
        >>> previous_x_title = obj.get_x_axis_title()
        >>> previous_y_title = obj.get_y_axis_title()
        >>> obj.set_back_up_data()
        >>> obj.set_data([[1, 0], [2, 10]])
        >>> obj.set_x_axis_title('X')
        >>> obj.set_y_axis_title('y')
        >>> obj.restore_data()
        >>> obj.get_data() == previous_data
        True
        >>> obj.get_x_axis_title() == previous_x_title
        True
        >>> obj.get_y_axis_title() == previous_y_title
        True
        >>> previous_data is obj.get_data()
        False
        """
        self.data = list(list(elem) for elem in self.back_up_data)
        self.x_axis_title = self.back_up_axis_titles[0]
        self.y_axis_title = self.back_up_axis_titles[1]
        self.back_up_data = ()
        self.back_up_axis_titles = ()
    
    def check_for_x_repeats(self, value_to_search):
        """Finds if there is any repeats with the x value
        that the user is trying to add to the list.
        >>> obj = Tracker()
        >>> obj.set_data([[2, 5], [3, 1], [6, 5]])
        >>> obj.check_for_x_repeats(2)
        True
        >>> obj.set_data([[0, 1], [5, 3], [2, 8]])
        >>> obj.check_for_x_repeats(10)
        False
        >>> obj.set_data([[]])
        >>> obj.check_for_x_repeats(0)
        False
        """
        for graph_point in self.get_data():
            if len(graph_point) > 0 and graph_point[0] == value_to_search:      #index 0 of the nested list 'data' is where the x value is stored.
                return True
        else:
            return False
    
    def replace_y_value(self, x_value, y_value):
        """Replaces y value using the x value as a
        key.
        >>> obj = Tracker()
        >>> obj.set_data([[2, 6], [5, 10], [6, 20]])
        >>> obj.replace_y_value(5, 2)
        >>> obj.get_data()
        [[2, 6], [5, 2], [6, 20]]
        >>> obj.set_data([[4, 10], [19, 1], [10, 9]])
        >>> obj.replace_y_value(10, 9)
        >>> obj.get_data()
        [[4, 10], [19, 1], [10, 9]]
        >>> previous_data = obj.get_data()
        >>> obj.replace_y_value(4, 10)
        >>> new_data = obj.get_data()
        >>> previous_data is new_data
        False
        >>> previous_data[0] is new_data[0]
        False
        >>> obj.set_data([[]])
        >>> obj.replace_y_value(9, 10)
        >>> obj.get_data()
        [[]]
        """
        copy_data = list([list(elem) for elem in self.get_data()])
        for graph_point in copy_data:
            if len(graph_point) > 0 and graph_point[0] == x_value:
                graph_point[1] = y_value
        self.set_data(copy_data)
    
    def sort_tracker_data(self):
        """Sorts tracker data according to its x value
        by selection sort algorithm.
        >>> obj = Tracker()
        >>> obj.set_data([[45, 10], [10, 20], [20, 100]])
        >>> obj.sort_tracker_data()
        >>> obj.get_data()
        [[10, 20], [20, 100], [45, 10]]
        >>> obj.set_data([[]])
        >>> obj.sort_tracker_data()
        >>> obj.get_data()
        [[]]
        >>> obj.set_data([[-10, 90], [-5, 10], [-15, 20]])
        >>> obj.sort_tracker_data()
        >>> obj.get_data()
        [[-15, 20], [-10, 90], [-5, 10]]
        >>> previous_list = obj.get_data()
        >>> obj.sort_tracker_data()
        >>> new_list = obj.get_data()
        >>> previous_list is new_list
        False
        >>> previous_list[0] is new_list[0]
        False
        """
        copy_data = list([list(elem) for elem in self.get_data()])

        for index in range(len(copy_data) - 1):
            smallest_index = index
            for remaining_index in range(index + 1, len(copy_data)):
                if copy_data[remaining_index][0] < copy_data[smallest_index][0]:
                    smallest_index = remaining_index
            temp_value = copy_data[index]
            copy_data[index] = copy_data[smallest_index]
            copy_data[smallest_index] = temp_value
        self.set_data(copy_data)

class MainWindow(QMainWindow):
    """Class MenuWindow is a QMainWindow class that is in charge
    of displaying the application for user interaction.
    """
    def __init__(self):
        """Initializes window for menu of ITrack.
        >>> obj = MainWindow()
        >>> dir_address = obj.TRACKER_INFO_DIR
        >>> obj.tracker_list
        []
        >>> some_table = obj.menu_table
        >>> obj.tracker_selected
        >>> obj.add_row_window
        >>> obj.new_x_value_input
        >>> obj.new_y_value_input
        >>> obj.new_x_value
        0
        >>> obj.new_y_value
        0
        >>> obj.warning_window
        >>> obj.edit_table
        >>> obj.edit_tracker_name_button
        >>> obj.go_to_button
        >>> obj.tracker_name
        ''
        >>> obj.delete_button
        >>> obj.edit_tracker_name_window
        >>> obj.new_tracker_user_input
        >>> obj.axis_title_user_input
        >>> obj.edit_axis_window
        >>> some_layout = obj.main_layout
        """
        super().__init__()
        
        self.setWindowTitle("ITrack")
        self.setMinimumSize(QSize(685, 685))

        self.TRACKER_INFO_DIR = path.join(getcwd(), "tracker_info")
        self.tracker_list = []
        self.menu_table = None
        self.tracker_selected = None
        self.add_row_window = None
        self.new_x_value_input = None
        self.new_y_value_input = None
        self.new_x_value = 0
        self.new_y_value = 0
        self.warning_window = None
        self.edit_table = None
        self.main_layout = None
        self.edit_tracker_name_button = None
        self.go_to_button = None
        self.tracker_name = ""
        self.delete_button = None
        self.edit_tracker_name_window = None
        self.new_tracker_user_input = None
        self.axis_title_user_input = None
        self.edit_axis_window = None

        self.main_layout = self.get_menu_layout()

    def check_for_valid_tracker_name(self, user_input):
        """Checks the input of user for new tracker name.
        Always returns true unless the input is an empty string,
        the name already exists, or the name has a \, /, or : character.
        >>> obj = MainWindow()
        >>> tracker = Tracker()
        >>> tracker.set_name("SomeTracker")
        >>> obj.tracker_list.append(tracker)
        >>> obj.check_for_valid_tracker_name('')
        False
        >>> obj.check_for_valid_tracker_name('AnotherTracker')
        True
        >>> obj.check_for_valid_tracker_name('SomeTracker')
        False
        >>> obj.check_for_valid_tracker_name('\\Something')
        False
        >>> obj.check_for_valid_tracker_name('/Something')
        False
        >>> obj.check_for_valid_tracker_name(':something')
        False
        """
        all_trackers = self.tracker_list

        if len(user_input) == 0:
            return False
        elif '\\' in user_input or '/' in user_input or ':' in user_input:
            return False
        else:
            for tracker in all_trackers:
                if tracker.get_name() == user_input:
                    return False
            else:
                return True
    
    def execute_invalid_name_window(self):
        """Pops up a QMessageBox warning
        when the user enters an invalid name
        for a tracker.
        """
        self.warning_window = QMessageBox()
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setText("Invalid tracker name, check if this name already exists, the input is empty, or the new name has a \, /, or : character.")
        self.warning_window.setStandardButtons(QMessageBox.Ok)
        self.warning_window.setWindowTitle("Error")

        self.warning_window.exec()

    def add_tracker_confirmed(self):
        """Creates a new Tracker() object
        when the add Tracker button is confirmed
        and is added to the field self.tracker_list.
        Window that prompts user to enter new name for
        new tracker is closed.
        """
        if self.check_for_valid_tracker_name(self.new_tracker_user_input.text()):
            new_tracker = Tracker()

            new_tracker.set_name(self.new_tracker_user_input.text())
            self.tracker_list.append(new_tracker)

            self.render_menu_window()

            self.add_window.accept()
        else:
            self.execute_invalid_name_window()
        
    def invalid_input_entered_in_edit_table(self):
        """Pops up a QMessageBox when the
        value entered is not a number.
        """
        self.warning_window = QMessageBox()
        self.warning_window.setWindowTitle("Error")
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setStandardButtons(QMessageBox.Ok)
        self.warning_window.setText("Value entered must be a number!")

        self.warning_window.exec()
    
    def x_value_repeat_entered_in_edit_table(self):
        self.warning_window = QMessageBox()
        self.warning_window.setWindowTitle("Error")
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setStandardButtons(QMessageBox.Ok)
        self.warning_window.setText("X value must be unique!")

        self.warning_window.exec()
    
    def edit_tracker_data(self, row, col):
        """This signal is triggered when the user edits
        a value in the edit table. Given row and column
        given by the signal, this method changes the data
        in the tracker object with the new data if valid, that is
        if the number returned by the user is a number. Otherwise,
        it pops up a warning window stating that the value entered
        is invalid.
        """
        tracker_data = self.tracker_selected.get_data()
        try:
            new_data = float(self.edit_table.item(row, col).text())
            if col == 0:    #checks if value changed is a x value.
                if not self.tracker_selected.check_for_x_repeats(new_data):
                    tracker_data[row][col] = new_data
                else:
                    self.x_value_repeat_entered_in_edit_table()
                    self.edit_table.blockSignals(True)
                    self.edit_table.setItem(row, col, QTableWidgetItem(str(tracker_data[row][col])))
                    self.edit_table.blockSignals(False)
            else:   #Gets executed if value changed is a y value.
                tracker_data[row][col] = new_data
        except ValueError:
            self.invalid_input_entered_in_edit_table()
            self.edit_table.blockSignals(True)
            self.edit_table.setItem(row, col, QTableWidgetItem(str(tracker_data[row][col])))   #Replaces the value entered with previous value.
            self.edit_table.blockSignals(False)

    def edit_tracker_canceled(self):
        """This method is called when the user clicks
        the cancel button in the edit window. This method will
        restore the values of data before it was edited and will 
        render the table window again. This method will ask the user if
        he is sure to discard all changes made.
        """
        self.warning_window = QMessageBox()

        self.warning_window.setWindowTitle("Warning")
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.warning_window.setText("Are you sure that you want to discard all changes made?")
        
        if self.warning_window.exec() == QMessageBox.Yes:
            self.tracker_selected.restore_data()
            self.render_tabular_window()
    
    def edit_tracker_confirmed(self):
        """This method is called when the user clicks
        the confirm button in the edit window. This method 
        will first ask for confirmation. If the user accepts, the
        tabular window will be rendered again with the changes made to the
        data.
        """
        self.warning_window = QMessageBox()

        self.warning_window.setWindowTitle("Warning")
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.warning_window.setText("Are you sure you want to apply all changes made to the data?")

        if self.warning_window.exec() == QMessageBox.Yes:
            self.tracker_selected.sort_tracker_data()
            self.render_tabular_window()

    def add_tracker_canceled(self):
        """Closes window that prompts user
        to enter new name for new tracker.
        """
        self.add_window.reject()

    def add_tracker(self):
        """Pops up a QDialog prompting the user to
        enter a new name for the tracker.
        """
        self.add_window = QDialog()
        self.new_tracker_user_input = QLineEdit()
        instructions = QLabel("Enter name for new tracker.")
        layout = QGridLayout()
        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        confirm_button.clicked.connect(self.add_tracker_confirmed)
        cancel_button.clicked.connect(self.add_tracker_canceled)

        layout.addWidget(instructions, 0, 0, 1, 2)
        layout.addWidget(self.new_tracker_user_input, 1, 0, 1, 2)
        layout.addWidget(confirm_button, 2, 0)
        layout.addWidget(cancel_button, 2, 1)

        self.add_window.setWindowTitle("Add Tracker")
        self.add_window.setFixedSize(QSize(400, 120))
        self.add_window.setLayout(layout)
        
        self.add_window.exec_()

    def delete_tracker_selected(self):
        """This method first asks for confirmation. If user confirms,
        this method searches for self.tracker_selected in
        self.tracker_list and deletes it from the list.
        """
        self.warning_window = QMessageBox()
        self.warning_window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.warning_window.setText("Are you sure you want to delete this tracker?")
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setWindowTitle("Warning")

        if self.warning_window.exec() == QMessageBox.Yes:
            self.tracker_list.remove(self.tracker_selected)
    
    def remove_data_row(self):
        """This method asks confirmation first in order to delete
        a row from the data. If user confirms, this method finds
        the clicked delete button and uses its location to remove
        the row from the tracker data.
        """
        self.warning_window = QMessageBox()
        self.warning_window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.warning_window.setText("Are you sure you want to delete this row?")
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setWindowTitle("Warning")

        if self.warning_window.exec() == QMessageBox.Yes:
            tracker_data = self.tracker_selected.get_data()
            row = 0
            widget_found = False
            while True:
                for col in range(self.edit_table.columnCount()):
                    if self.edit_table.cellWidget(row, col) == self.sender():
                        widget_found = True
                        break
                if widget_found:
                    break
                else:
                    row += 1
            tracker_data.pop(row)

    def edit_tracker_name_confirmed(self):
        """This method gets executed when the user
        confirms that he wants to change the name
        of the tracker selected. It checks whether the new
        name is valid. This means that the new name is not
        found in another tracker.
        """
        tracker = self.tracker_selected

        if self.check_for_valid_tracker_name(self.new_tracker_user_input.text()):
            tracker.set_name(self.new_tracker_user_input.text())

            self.render_menu_window()
            self.edit_tracker_name_window.accept()
        else:
            self.execute_invalid_name_window()
    
    def edit_tracker_name_canceled(self):
        """This method closes the window
        that asks user for confirmation
        to change the name of the tracker.
        """
        self.edit_tracker_name_window.reject()

    def edit_tracker_name(self):
        """This method gets called when the edit tracker
        name button gets clicked.
        """
        self.edit_tracker_name_window = QDialog()
        self.new_tracker_user_input = QLineEdit()
        window_layout = QGridLayout()
        instructions = QLabel("Enter new name for tracker.")
        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        self.edit_tracker_name_window.setWindowTitle("Edit Tracker Name")
        confirm_button.clicked.connect(self.edit_tracker_name_confirmed)
        cancel_button.clicked.connect(self.edit_tracker_name_canceled)

        window_layout.addWidget(instructions, 0, 0, 1, 2)
        window_layout.addWidget(self.new_tracker_user_input, 1, 0, 1, 2)
        window_layout.addWidget(confirm_button, 2, 0)
        window_layout.addWidget(cancel_button, 2, 1)

        self.edit_tracker_name_window.setLayout(window_layout)
        self.edit_tracker_name_window.show()

    def set_tracker_selected(self):
        """Searches for the row of the button clicked
        and uses that number as an index for tracker_list.
        This way, the program will be able to save in a
        field (self.tracker_selected) the tracker
        that needs to be displayed.
        """
        row = 0
        widget_found = False
        while True:
            for col in range(self.menu_table.columnCount()):
                if self.menu_table.cellWidget(row, col) == self.sender():
                    widget_found = True
                    break
            if widget_found:
                break
            else:
                row += 1
        self.tracker_selected = self.tracker_list[row]
    
    def create_back_up_for_tracker_data(self):
        """When the edit button in the table window is clicked, 
        this method will be called to create a copy of the data
        stored in tracker in case the user does not want to confirm
        the changes done in the data.
        """
        self.tracker_selected.set_back_up_data()
    
    def check_for_valid_input(self, new_x_value, new_y_value):
        """Checks whether new x and y values are numbers. If so,
        self.new_x_value and self.new_y_value are updated.
        >>> obj = MainWindow()
        >>> obj.check_for_valid_input('20.0', '40.0')
        True
        >>> obj.new_x_value
        20.0
        >>> obj.new_y_value
        40.0
        >>> obj.check_for_valid_input('34..0', '37.0')
        False
        >>> obj.new_x_value
        20.0
        >>> obj.new_y_value
        40.0
        >>> obj.check_for_valid_input('abc', 'ytu')
        False
        >>> obj.check_for_valid_input('1', '2')
        True
        >>> obj.new_x_value
        1.0
        >>> obj.new_y_value
        2.0
        >>> obj.check_for_valid_input('0', '0')
        True
        >>> obj.new_x_value
        0.0
        >>> obj.new_y_value
        0.0
        >>> obj.check_for_valid_input('-2.0', '-1.0')
        True
        >>> obj.new_x_value
        -2.0
        >>> obj.new_y_value
        -1.0
        """
        try:
            new_x_value = float(new_x_value)
            new_y_value = float(new_y_value)
            self.new_x_value = new_x_value
            self.new_y_value = new_y_value
            return True
        except ValueError:
            return False

    def add_new_row_confirmed(self):
        """Adds the new values entered in the
        add new row window in the data of tracker
        object if the new values are valid. Otherwise
        it pops up a window displaying potential
        errors in the input. If the x value is repeated,
        it will ask the user whether he wants to replace
        its y value with the new y value, otherwise
        it does not change the data.
        """
        valid_input = self.check_for_valid_input(self.new_x_value_input.text().strip(), self.new_y_value_input.text().strip())

        if valid_input:
            x_repeats = self.tracker_selected.check_for_x_repeats(self.new_x_value)
        else:
            x_repeats = False

        if valid_input and not x_repeats:
            tracker_data = self.tracker_selected.get_data()
            new_graph_point = []
            
            new_graph_point.append(self.new_x_value)
            new_graph_point.append(self.new_y_value)

            tracker_data.append(new_graph_point)

            self.tracker_selected.sort_tracker_data()

            self.render_tabular_window()
            self.add_row_window.accept()

        else:
            text_to_display = ""
            self.warning_window = QMessageBox()
            self.warning_window.setWindowTitle("Warning")
            text_to_display = "Warning: x value already exists, clicking save will replace the old x and y values with the new ones." if x_repeats else \
                "Warning: x or y value entered is not a number, please check again."
            self.warning_window.setText(text_to_display)
            self.warning_window.setIcon(QMessageBox.Warning)
            if not valid_input:
                self.warning_window.setStandardButtons(QMessageBox.Ok)
            else: #Else branch executes when there is a repeat in an x value.
                self.warning_window.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)

            if self.warning_window.exec() == QMessageBox.Save:
                self.tracker_selected.replace_y_value(self.new_x_value, self.new_y_value)
                self.render_tabular_window()
                self.add_row_window.accept()

    def add_new_row_canceled(self):
        """Closes QDialog window for
        adding new row.
        """
        self.add_row_window.reject()

    def add_row_button_clicked(self):
        """Pops up a QDialog window that will prompt
        the user to enter a x value and y value to add
        them to the tracker table.
        """
        self.add_row_window = QDialog()
        window_layout = QGridLayout()
        instruction_text = QLabel("Please enter an x and y value to add them to the table.")
        new_x_value_label = QLabel("X Value: ")
        new_y_value_label = QLabel("Y Value: ")
        self.new_x_value_input = QLineEdit()
        self.new_y_value_input = QLineEdit()
        confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")

        self.add_row_window.setWindowTitle("Add New Row")
        confirm_button.clicked.connect(self.add_new_row_confirmed)
        cancel_button.clicked.connect(self.add_new_row_canceled)

        window_layout.addWidget(instruction_text, 0, 0, 1, 2)
        window_layout.addWidget(new_x_value_label, 1, 0)
        window_layout.addWidget(self.new_x_value_input, 1, 1)
        window_layout.addWidget(new_y_value_label, 2, 0)
        window_layout.addWidget(self.new_y_value_input, 2, 1)
        window_layout.addWidget(confirm_button, 3, 0)
        window_layout.addWidget(cancel_button, 3, 1)

        self.add_row_window.setLayout(window_layout)
        
        self.add_row_window.exec_()
    
    def invalid_axis_title_name(self):
        """Pops up a window with an error stating that the
        user cannot enter an empty input for the graph axis names.
        """
        self.warning_window = QMessageBox()
        self.warning_window.setIcon(QMessageBox.Warning)
        self.warning_window.setText("Input cannot be empty nor have a \ character.")
        self.warning_window.setStandardButtons(QMessageBox.Ok)
        self.warning_window.setWindowTitle("Error")

        self.warning_window.exec()
    
    def edit_x_axis_title_confirmed(self):
        """If the user entered a valid input (any input except empty or \ character),
        the method will change the name of the x axis of the tracker selected and
        will close the window that prompts user for input. Otherwise it will
        pop up a window with an error message.
        """
        if len(self.axis_title_user_input.text()) > 0 and '\\' not in self.axis_title_user_input.text():
            self.tracker_selected.set_x_axis_title(self.axis_title_user_input.text())
            self.render_edit_window()
            self.edit_axis_window.accept()
        else:
            self.invalid_axis_title_name()

    def edit_y_axis_title_confirmed(self):
        """If the user entered a valid input (any input except empty or \ character),
        the method will change the name of the y axis of the tracker selected
        and will close the window that prompts user for input. Otherwise it will
        pop up a window with an error message.
        """
        if len(self.axis_title_user_input.text()) > 0 and '\\' not in self.axis_title_user_input.text():
            self.tracker_selected.set_y_axis_title(self.axis_title_user_input.text())
            self.render_edit_window()
            self.edit_axis_window.accept()
        else:
            self.invalid_axis_title_name()

    def edit_axis_title_canceled(self):
        """Closes window that prompts user for new x or y axis title.
        """
        self.edit_axis_window.reject()

    def edit_x_axis_title(self):
        """Pops up a QDialog window that asks
        user for new name of x axis title.
        """
        self.edit_axis_window = QDialog()
        self.axis_title_user_input = QLineEdit()
        confirm_button = QPushButton("Confirm")
        instructions = QLabel("Please enter a new name for the x-axis title.")
        cancel_button = QPushButton("Cancel")
        window_layout = QGridLayout()

        self.edit_axis_window.setWindowTitle("X-Axis Title Change")

        confirm_button.clicked.connect(self.edit_x_axis_title_confirmed)
        cancel_button.clicked.connect(self.edit_axis_title_canceled)

        window_layout.addWidget(instructions, 0, 0, 1, 2)
        window_layout.addWidget(self.axis_title_user_input, 1, 0, 1, 2)
        window_layout.addWidget(confirm_button, 2, 0)
        window_layout.addWidget(cancel_button, 2, 1)

        self.edit_axis_window.setLayout(window_layout)
        self.edit_axis_window.show()

    def edit_y_axis_title(self):
        """Pops up a QDialog window that asks user
        for new name of y axis title.
        """
        self.edit_axis_window = QDialog()
        self.axis_title_user_input = QLineEdit()
        confirm_button = QPushButton("Confirm")
        instructions = QLabel("Please enter a new name for the y-axis title.")
        cancel_button = QPushButton("Cancel")
        window_layout = QGridLayout()

        self.edit_axis_window.setWindowTitle("Y-Axis Title Change")

        confirm_button.clicked.connect(self.edit_y_axis_title_confirmed)
        cancel_button.clicked.connect(self.edit_axis_title_canceled)

        window_layout.addWidget(instructions, 0, 0, 1, 2)
        window_layout.addWidget(self.axis_title_user_input, 1, 0, 1, 2)
        window_layout.addWidget(confirm_button, 2, 0)
        window_layout.addWidget(cancel_button, 2, 1)

        self.edit_axis_window.setLayout(window_layout)
        self.edit_axis_window.show()
    
    def get_tracker_table(self):
        """Returns a QTableWidget that contains the information stored
        in the tracker selected.
        """
        tracker_data = self.tracker_selected.get_data()
        tracker_table = QTableWidget(len(tracker_data), 2)

        tracker_table.setFont(QFont("Comic Sans MS", 11))
        tracker_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tracker_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tracker_table.setSelectionMode(QAbstractItemView.NoSelection)
        tracker_table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tracker_selected.get_x_axis_title()))
        tracker_table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tracker_selected.get_y_axis_title()))
        tracker_table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        tracker_table.horizontalHeader().setFont(QFont("Comic Sans MS", 12, italic=True))
        tracker_table.verticalHeader().hide()

        for index in range(len(tracker_data)):
            x_value = tracker_data[index][0]
            y_value = tracker_data[index][1]
            tracker_table.setItem(index, 0, QTableWidgetItem(str(x_value)))
            tracker_table.setItem(index, 1, QTableWidgetItem(str(y_value)))
        
        return tracker_table

    def get_menu_table(self):
        """Returns a QTableWidget that contains all the trackers.
        """
        trackers_table = QTableWidget(len(self.tracker_list), 4)
        trackers_table.setFont(QFont("Comic Sans MS", 11))
        trackers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        trackers_table.setSelectionMode(QAbstractItemView.NoSelection)
        trackers_table.setShowGrid(False)
        trackers_table.setHorizontalHeaderItem(0, QTableWidgetItem("Tracker Name"))
        trackers_table.setHorizontalHeaderItem(1, QTableWidgetItem("Display Data"))
        trackers_table.setHorizontalHeaderItem(2, QTableWidgetItem("Delete Tracker"))
        trackers_table.setHorizontalHeaderItem(3, QTableWidgetItem("Edit Name"))
        trackers_table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        trackers_table.horizontalHeader().setFont(QFont("Comic Sans MS", 12, italic=True))
        trackers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for index in range(len(self.tracker_list)):
            self.delete_button = QPushButton("X")
            self.go_to_button = QPushButton("Go")
            self.tracker_name = self.tracker_list[index].get_name()
            self.edit_tracker_name_button = QPushButton("Edit")

            self.go_to_button.clicked.connect(self.set_tracker_selected)
            self.go_to_button.clicked.connect(self.render_tabular_window)
            self.delete_button.clicked.connect(self.set_tracker_selected)
            self.delete_button.clicked.connect(self.delete_tracker_selected)
            self.delete_button.clicked.connect(self.render_menu_window)
            self.edit_tracker_name_button.clicked.connect(self.set_tracker_selected)
            self.edit_tracker_name_button.clicked.connect(self.edit_tracker_name)

            trackers_table.setCellWidget(index, 0, QLabel(self.tracker_name))
            trackers_table.setCellWidget(index, 1, self.go_to_button)
            trackers_table.setCellWidget(index, 2, self.delete_button)
            trackers_table.setCellWidget(index, 3, self.edit_tracker_name_button)

        return trackers_table
    
    def get_graph_view(self):
        """Returns a QChartView object representing the graph
        that needs to be shown.
        """
        graph = QtCharts.QChart()
        graph_view = QtCharts.QChartView()
        data_line = QtCharts.QLineSeries()
        x_axis = QtCharts.QValueAxis()
        y_axis = QtCharts.QValueAxis()

        graph.legend().hide()
        graph.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        x_axis.setTitleText(self.tracker_selected.get_x_axis_title())
        y_axis.setTitleText(self.tracker_selected.get_y_axis_title())
        x_axis.setLabelsFont(QFont("Comic Sans MS", 12))
        y_axis.setLabelsFont(QFont("Comic Sans MS", 12))

        graph.addAxis(x_axis, Qt.AlignBottom)
        graph.addAxis(y_axis, Qt.AlignLeft)

        for graph_point in self.tracker_selected.get_data():
            data_line.append(graph_point[0], graph_point[1])

        graph.addSeries(data_line)

        data_line.attachAxis(x_axis)
        data_line.attachAxis(y_axis)
        data_line.setPointsVisible(True)

        graph_view.setChart(graph)
        graph_view.setRenderHint(QPainter.Antialiasing)

        return graph_view

    def get_menu_layout(self):
        """Sets layout to include all the trackers
        currently saved. Returns layout to render.
        """
        self.menu_table = self.get_menu_table()
        menu_layout = QGridLayout()
        add_button = QPushButton("Add New Tracker")
        menu_header = QLabel("ITrack Menu")

        add_button.setFont(QFont("Comic Sans MS", 9))
        add_button.clicked.connect(self.add_tracker)
        menu_header.setFont(QFont("Comic Sans MS", 15))
        
        menu_layout.addWidget(menu_header, 0, 0)
        menu_layout.addWidget(self.menu_table, 1, 0)
        menu_layout.addWidget(add_button, 2, 0)

        return menu_layout
    
    def get_table_layout(self):
        """Returns layout of table values of tracker selected to
        render
        """
        table_layout = QGridLayout()
        back_to_menu_button = QPushButton("Back to Menu")
        change_to_graph_button = QPushButton("Set to Graphical Form")
        add_new_row_button = QPushButton("Add New Row")
        edit_button = QPushButton("Edit tracker")
        tracker_header = QLabel(self.tracker_selected.get_name())

        if len(self.tracker_selected.get_data()) <= 1:
            change_to_graph_button.setDisabled(True)

        tracker_header.setFont(QFont("Comic Sans MS", 14))
        back_to_menu_button.setFont(QFont("Comic Sans MS", 9))
        back_to_menu_button.clicked.connect(self.render_menu_window)
        change_to_graph_button.clicked.connect(self.render_graph_window)
        change_to_graph_button.setFont(QFont("Comic Sans MS", 9))
        add_new_row_button.clicked.connect(self.add_row_button_clicked)
        add_new_row_button.setFont(QFont("Comic Sans MS", 10))
        edit_button.clicked.connect(self.create_back_up_for_tracker_data)
        edit_button.clicked.connect(self.render_edit_window)
        edit_button.setFont(QFont("Comic Sans MS", 9))

        table_layout.addWidget(tracker_header, 0, 0, 1, 2)
        table_layout.addWidget(add_new_row_button, 0, 2)
        table_layout.addWidget(self.get_tracker_table(), 1, 0, 1, 3)
        table_layout.addWidget(back_to_menu_button, 2, 0)
        table_layout.addWidget(edit_button, 2, 1)
        table_layout.addWidget(change_to_graph_button, 2, 2)

        return table_layout

    def get_graph_layout(self):
        """Returns layout of graphical representation of tracker selected
        to render.
        """
        graph_window_layout = QGridLayout()
        tabular_form_button = QPushButton("Return to Tabular Form")
        back_to_trackers_menu = QPushButton("Return to Menu")
        graph_frame = self.get_graph_view()
        tracker_header = QLabel(self.tracker_selected.get_name())

        tabular_form_button.clicked.connect(self.render_tabular_window)
        back_to_trackers_menu.clicked.connect(self.render_menu_window)
        tracker_header.setFont(QFont("Comic Sans MS", 14))
        back_to_trackers_menu.setFont(QFont("Comic Sans MS", 9))
        tabular_form_button.setFont(QFont("Comic Sans MS", 9))

        graph_window_layout.addWidget(tracker_header, 0, 0, 1, 2)
        graph_window_layout.addWidget(graph_frame, 1, 0, 1, 2)
        graph_window_layout.addWidget(back_to_trackers_menu, 2, 0)
        graph_window_layout.addWidget(tabular_form_button, 2, 1)

        return graph_window_layout
    
    def get_edit_table(self):
        """Returns a QTableWidget containing all the values of the
        tracker. This table is allowed to be edited.
        """
        table_data = self.tracker_selected.get_data()
        self.edit_table = QTableWidget(len(table_data), 3)

        self.edit_table.blockSignals(True)
        self.edit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.edit_table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tracker_selected.get_x_axis_title()))
        self.edit_table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tracker_selected.get_y_axis_title()))
        self.edit_table.setHorizontalHeaderItem(2, QTableWidgetItem("Delete Row"))
        self.edit_table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.edit_table.verticalHeader().hide()

        self.edit_table.cellChanged.connect(self.edit_tracker_data)

        for index in range(len(table_data)):
            x_value = table_data[index][0]
            y_value = table_data[index][1]
            remove_row_button = QPushButton("X")

            remove_row_button.clicked.connect(self.remove_data_row)
            remove_row_button.clicked.connect(self.render_edit_window)

            self.edit_table.setItem(index, 0, QTableWidgetItem(str(x_value)))
            self.edit_table.setItem(index, 1, QTableWidgetItem(str(y_value)))
            self.edit_table.setCellWidget(index, 2, remove_row_button)
        self.edit_table.blockSignals(False)
        
        return self.edit_table
    
    def get_edit_layout(self):
        """Returns layout of edit window to render.
        """
        edit_window_layout = QGridLayout()
        confirm_edit_button = QPushButton("Confirm")
        edit_table_widget = self.get_edit_table()
        cancel_edit_button = QPushButton("Cancel")
        edit_x_axis_button = QPushButton("Edit X-Axis Title")
        edit_y_axis_button = QPushButton("Edit Y-Axis Title")
        tracker_title = QLabel(self.tracker_selected.get_name() + ": Edit Window")

        tracker_title.setFont(QFont("Comic Sans MS", 14, italic=True))
        edit_x_axis_button.clicked.connect(self.edit_x_axis_title)
        edit_y_axis_button.clicked.connect(self.edit_y_axis_title)
        edit_x_axis_button.setFont(QFont("Comic Sans MS", 9))
        edit_y_axis_button.setFont(QFont("Comic Sans MS", 9))
        cancel_edit_button.clicked.connect(self.edit_tracker_canceled)
        cancel_edit_button.setFont(QFont("Comic Sans MS", 9))
        confirm_edit_button.clicked.connect(self.edit_tracker_confirmed)
        confirm_edit_button.setFont(QFont("Comic Sans MS", 9))

        edit_window_layout.addWidget(tracker_title, 0, 0, 1, 2)
        edit_window_layout.addWidget(edit_table_widget, 1, 0, 1, 2)
        edit_window_layout.addWidget(edit_x_axis_button, 2, 0)
        edit_window_layout.addWidget(edit_y_axis_button, 2, 1)
        edit_window_layout.addWidget(confirm_edit_button, 3, 0)
        edit_window_layout.addWidget(cancel_edit_button, 3, 1)

        return edit_window_layout

    def delete_widgets_in_layout(self):
        """Deletes current widgets in window in order
        to substitute them with different widgets.
        """
        while True:
            widget_to_remove = self.main_layout.takeAt(0)
            if widget_to_remove == None:
                break
            else:
                widget_to_remove.widget().deleteLater()
    
    def render_tabular_window(self):
        """Renders main_layout obtained from method get_table_layout.
        """
        self.delete_widgets_in_layout()
        self.main_layout = self.get_table_layout()
        layout_container = QWidget()

        layout_container.setLayout(self.main_layout)
        self.setCentralWidget(layout_container)
    
    def render_menu_window(self):
        """Renders main_layout obtained from method get_menu_layout.
        """
        self.delete_widgets_in_layout()
        self.main_layout = self.get_menu_layout()
        layout_container = QWidget()

        layout_container.setLayout(self.main_layout)
        self.setCentralWidget(layout_container)
    
    def render_graph_window(self):
        """Renders main_layout obtained from method get_graph_layout.
        """
        self.delete_widgets_in_layout()
        self.main_layout = self.get_graph_layout()
        layout_container = QWidget()

        layout_container.setLayout(self.main_layout)
        self.setCentralWidget(layout_container)
    
    def render_edit_window(self):
        """Renders main_layout obtained from the method
        get_edit_layout.
        """
        self.delete_widgets_in_layout()
        self.main_layout = self.get_edit_layout()
        layout_container = QWidget()

        layout_container.setLayout(self.main_layout)
        self.setCentralWidget(layout_container)
    
    def check_for_trash_files(self):
        """Deletes any file that is not found in self.tracker_list
        """
        for dir_name, sub_name, files in walk(self.TRACKER_INFO_DIR):
            tracker_names = [tracker.get_name() for tracker in self.tracker_list]
            for file in files:
                if path.basename(file) not in tracker_names:
                    remove(path.join(dir_name, file))

    def save_data_in_files(self):
        """When the application closes, this method will
        be in charge of saving all the data from all the trackers
        stored in self.tracker_list in their respective files.
        """
        self.check_for_trash_files()
        self.generate_tracker_data_directory()

        all_trackers = self.tracker_list

        for tracker in all_trackers:
            tracker_obj = tracker
            tracker_data = tracker_obj.get_data()
            tracker_name = tracker_obj.get_name()
            tracker_x_axis = tracker_obj.get_x_axis_title()
            tracker_y_axis = tracker_obj.get_y_axis_title()
            file_name = tracker_name
            file_path = path.join(self.TRACKER_INFO_DIR, file_name)

            with open(file_path, 'w') as file:
                file.write(f"{tracker_x_axis}\n")
                file.write(f"{tracker_y_axis}\n")
                for graph_point in tracker_data:
                    file.write(f"{graph_point[0]} {graph_point[1]}\n")
    
    def generate_tracker_data_directory(self):
        """Checks if directory tracker_info
        exists. If not, the directory is created.
        """
        for dir_name, sub_name, files in walk(getcwd()):
            if dir_name == self.TRACKER_INFO_DIR:
                break
        else:
            mkdir(self.TRACKER_INFO_DIR)
    
    def load_tracker_data(self):
        """Loads all the data inside the
        directory tracker_info. Stores the data
        in its trackers respectively and assembles everything together
        in self.tracker_list.
        """
        self.generate_tracker_data_directory()

        for dir_name, sub_name, files in walk(self.TRACKER_INFO_DIR):
            for file in files:
                with open(path.join(dir_name, file), 'r') as file_obj:
                    new_tracker = Tracker()
                    tracker_data = []

                    new_tracker.set_name(path.basename(file))

                    x_axis_title = file_obj.readline().replace('\n', '')
                    y_axis_title = file_obj.readline().replace('\n', '')

                    new_tracker.set_x_axis_title(x_axis_title)
                    new_tracker.set_y_axis_title(y_axis_title)
                    while True:
                        file_line = file_obj.readline()
                        if not file_line:
                            break
                        else:
                            x_value, y_value = file_line.split()
                            graph_point = [float(x_value), float(y_value)]
                            tracker_data.append(graph_point)
                    new_tracker.set_data(tracker_data)
                    self.tracker_list.append(new_tracker)
        self.render_menu_window()

app = QApplication()
app_window = MainWindow()

app_window.load_tracker_data()

app_window.show()
app.exec_()

app_window.save_data_in_files()

if __name__ == '__main__':
    doctest.testmod()