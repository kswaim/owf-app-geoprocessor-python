# qt_util - Qt utility functions
# ________________________________________________________________NoticeStart_
# GeoProcessor
# Copyright (C) 2017-2019 Open Water Foundation
# 
# GeoProcessor is free software:  you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     GeoProcessor is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with GeoProcessor.  If not, see <https://www.gnu.org/licenses/>.
# ________________________________________________________________NoticeEnd___

from PyQt5 import QtGui, QtWidgets
import geoprocessor.util.app_util as app_util


def from_utf8(s):
    """
    Function to convert strings from UTF8 representation to Python string.
    The following code was autogenerated by Qt Designer:

    try:
        _fromUtf8 = lambda s: s
    except AttributeError:
        def _fromUtf8(s):
            return s

    The above generates warnings in PyCharm and web information indicate to just use a function,
    so this is the function.

    Args:
        s (str): string to convert.

    Returns:
        A string converted from UTF-8.
    """
    return s


def info_message_box(message, app_name=None, title="Information"):
    """
    Display an information message dialog.

    Args:
        app_name (str): Application name to use in dialog title
            (default if None is to get from app_util.get_property("ProgramName")
        message (str): Message string.
        title (str): Title for dialog.

    Returns:
        Which button was selected as QtWidgets.QMessageBox.Ok (only one button is available).
    """
    app_name = app_util.get_property("ProgramName")
    if app_name is not None:
        # Use the application name in the title
        title = app_name + " - " + title
    message_box = new_message_box(QtWidgets.QMessageBox.Information, QtWidgets.QMessageBox.Ok, message, title)
    return message_box


def new_message_box(message_type, standard_buttons_mask, message, title):
    """
    Create and execute a message box, returning an indicator for the button that was selected.
    REF: https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm

    Args:
            message_type (str): the type of message box, for example QtWidgets.QMessageBox.Question
            standard_buttons_mask (str): a bitmask indicating the buttons to include in the message box,
                    for example QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            message (str): a message to display in the message box
            title (str) a title for the message box. Appears in the top window bar.

    Returns:
        The clicked button name. See the button_value_dic for more information.
    """

    # Create the Message Box object.
    message_box = QtWidgets.QMessageBox()

    # Set the Message Box icon.
    message_box.setIcon(message_type)

    # Set the Message Box message text.
    message_box.setText(message)

    # Set the Message Box title text.
    message_box.setWindowTitle(title)

    # Set the Message Box standard buttons.
    message_box.setStandardButtons(standard_buttons_mask)

    # Set the icon
    # - icon path should use Qt / notation
    icon_path = app_util.get_property("ProgramIconPath").replace('\\','/')
    # print("Icon path='" + icon_path + "'")
    # message_box.setWindowIcon(QtGui.Icon(icon_path))
    message_box.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))

    # Execute the Message Box and retrieve the clicked button enumerator.
    btn_value = message_box.exec_()

    # Return the clicked button Qt type
    return btn_value


# TODO smalers 2019-01-19 need to figure out what this really does.
def translate(context, text, disambig):
    """
    Function to translate a string between human languages?
    The following code was autogenerated by Qt Designer:

    try:
        _encoding = QtWidgets.QApplication.UnicodeUTF8
        def _translate(context, text, disambig):
            return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
    except AttributeError:
        def _translate(context, text, disambig):
            return QtWidgets.QApplication.translate(context, text, disambig)

    The above generates warnings in PyCharm and web information indicate to just use a function,
    so this is the function.

    Args:
        context (str):  ? - need to figure out
        text (str):  test to translate
        disambig (str): ? - need to figure out

    Returns:
        A string converted from UTF-8.
    """
    try:
        _encoding = QtWidgets.QApplication.UnicodeUTF8
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
    except AttributeError:
        return QtWidgets.QApplication.translate(context, text, disambig)


def warning_message_box(message, app_name=None, title="Warning"):
    """
    Display a warning message dialog.

    Args:
        app_name (str): Application name to use in dialog title
            (default if None is to get from app_util.get_property("ProgramName")
        message (str): Message string.
        title (str): Title for dialog.

    Returns:
        Which button was selected as QtWidgets.QMessageBox.Ok (only one button is available).
    """
    if app_name is None:
        app_name = app_util.get_property("ProgramName")
    if app_name is not None:
        # Use the application name in the title
        title = app_name + " - " + title
    message_box = new_message_box(QtWidgets.QMessageBox.Warning, QtWidgets.QMessageBox.Ok, message, title)
    return message_box
