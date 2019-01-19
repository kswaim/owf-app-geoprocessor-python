# AbstractCommandEditor - parent class for all command editors
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

from PyQt5 import QtCore, QtGui, QtWidgets
import geoprocessor.util.app_util as app_util
import geoprocessor.ui.util.qt_util as qt_util
import functools
import logging
import webbrowser

try:
    _fromUtf8 = lambda s: s
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class AbstractCommandEditor(QtWidgets.QDialog):
    """
    Abstract command editor used as parent of command editor dialog implementations.
    This class maintains core layout information and provides functions to add components.
    """

    def __init__(self, command):
        """
        Initialize the Abstract Dialog instance.

        Args:
            command (derived from AbstractCommand): the GeoProcessor command to edit
        """
        # Call the parent class
        super().__init__()

        # Command being edited
        self.command = command

        # "input_edit_objects" is a dictionary that relates each command parameter with its associated Qt Widget
        # input field
        # KEY (str): the command parameter name
        # VALUE (obj): the associated Qt Widget input field
        # self.input_edit_objects = {}

        # "command_parameter_current_values" is a dictionary that holds the command parameters and their current values
        # KEY (str): the name of the command parameter
        # VALUE (str): the entered value of the command parameter
        # self.command_parameter_current_values = current_values

        # Initialize components that will be used
        self.CommandDisplay_View_TextBrowser = None

        # Layout used for the main editor
        # - other layouts may be added as needed to organize components
        self.grid_layout = None

        # Position in the layout for components as they are added, 0=row at top, 1 is next down, etc.
        # - each addition should increment before adding a component
        self.grid_layout_row = -1

        # Set initial size of window
        self.resize(500, 300)
        # Set the maximum width of a command editor
        self.setMaximumWidth(800)

    def add_ui_horizontal_separator(self):
        # Create a line (frame object with special specifications). Add the line to the Dialog window.
        # Set the size policy, the shape, the shadow, and the name of the frame object to create the line separator.
        # The frame object, Separator, separates the command description from the input form section of the Dialog box.
        self.Separator = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Separator.sizePolicy().hasHeightForWidth())
        self.Separator.setSizePolicy(sizePolicy)
        self.Separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.Separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Separator.setObjectName(_fromUtf8("Separator"))
        self.grid_layout_row = self.grid_layout_row + 1
        self.grid_layout.addWidget(self.Separator, self.grid_layout_row, 0, 1, 8)

    # def add_text_field(self, label, parameter_name, tooltip=None):
    #     """
    #     Add a text input field as  a QtGui.QLineEdit object that meets the standards of the
    #     GeoProceossor's command dialog window.
    #
    #     Args:
    #         label (str): label to display for text field.
    #         parameter_name (str): the name of the command parameter that is using the line edit field
    #         tooltip (str): optional. The text that will display in a pop-up when the user mouses over the
    #             QtGui.QLineEdit object. This is a good place to expand description of the parameter/parameter values.
    #
    #     Return: None
    #     """
    #
    #     # Set the line edit's object name (XXX_LineEdit where XXX is the name of the command parameter).
    #     line_edit.setObjectName(_fromUtf8("{}_LineEdit".format(parameter_name)))
    #
    #     # Get the dialog box row index that is used to display the command parameter objects
    #     # This is a dynamic index that takes into consideration the order of the command's parameters.
    #     row_index = self.parameters_list.index(parameter_name) + 2
    #
    #     # Add the line edit field to the Dialog box in the correct row. Command line edit fields will always start in
    #     # the second column (1) and will occupy 1 row.
    #     # If the field is set to long, the line edit field will occupy 6 columns.
    #     if long:
    #         self.gridLayout.addWidget(line_edit, row_index, 1, 1, 6)
    #
    #     # If not set to long, the line edit field will occupy 3 columns.
    #     else:
    #         self.gridLayout.addWidget(line_edit, row_index, 1, 1, 3)
    #
    #     # If placeholder text has been specified, add the desired text as placeholder text.
    #     if placeholder_text:
    #         line_edit.setPlaceholderText(_translate("Dialog", placeholder_text, None))
    #
    #     # If tool tip text has been specified, add the desired text as tool tip text.
    #     if tooltip:
    #         line_edit.setToolTip(_translate("Dialog", tooltip, None))
    #
    #     # Create a listener that reacts if the line edit field has been changed. If so, run the
    #     # update_command_display function.
    #     line_edit.textChanged.connect(self.update_command_display)
    #
    #     # Add the QtGui.QLineEdit object to the dictionary of input edit objects. Use the parameter name as the key
    #     # and the QtGui.QLineEdit object as the value.
    #     self.input_edit_objects[parameter_name] = line_edit

    def check_command_parameters(self):
        """
        Check to confirm that the command parameters are valid.

        Returns:
        """
        param_dict = self.get_parameter_dict_from_ui()
        self.command.check_command_parameters(param_dict)

    def setup_ui(self):
        """
        Set up the user interface.
        It should be implemented in a child class, although helper functions are defined in this abstract class.

        Returns: None
        """
        # This should not normally happen but will be the case if a child editor has not implemented the function
        print("In AbstractCommandEditor.setup_ui")

    def setup_ui_core(self):
        # Set up the editor core elements, which apply to any command.
        self.setup_ui_core_top()
        # Set up the editor specific to the command.
        # - this code should be implemented in child class
        self.setup_ui()
        # Set up the core components at the bottom
        self.setup_ui_core_bottom()

        # This will wire up the signals and slots depending on names.
        # REF: http://joat-programmer.blogspot.com/2012/02/pyqt-signal-and-slots-to-capture-events.html
        # - don't do this because not using QtDesigner
        # QtCore.QMetaObject.connectSlotsByName(self)

    def setup_ui_core_bottom(self):
        """
        Setup core UI components at the bottom of the dialog.

        Returns:  None
        """
        self.setup_ui_core_command_area()
        self.setup_ui_core_command_buttons()

    def setup_ui_core_top(self):
        """
        Setup core UI components at the top of the dialog.

        Returns:  None
        """
        # Set the window title to the command name
        self.setObjectName(_fromUtf8(self.command.command_name))
        self.setWindowTitle("Edit " + self.command.command_name + " command")
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        icon_path = app_util.get_property("ProgramIconPath").replace('\\', '/')
        self.setWindowIcon(QtGui.QIcon(icon_path))

        # Because components are added to the UI the dialog will have a size.
        # - don't set the size unless a dialog misbehaves, perhaps a maximum size
        # self.resize(684, 404)

        # Add a grid layout for components to be added
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setObjectName(_fromUtf8("gridLayout"))

        self.setup_ui_core_command_description()
        self.add_ui_horizontal_separator()

    def setup_ui_core_command_area(self):
        # Create a label object to the Dialog window.
        # Set the alignment, the name, and the text of the label.
        # The label, Command Display_Label, labels the CommandDisplay_View_TextBrowser text edit object.
        commandArea_Frame = QtWidgets.QFrame(self)
        commandArea_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        commandArea_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        commandArea_Frame.setObjectName("Command_Parameters")
        self.grid_layout_row = self.grid_layout_row + 1
        self.grid_layout.addWidget(commandArea_Frame, self.grid_layout_row, 0, 1, -1)

        # Create a grid layout object. Apply to the Command_Parameters frame object.
        # Set the name of the grid layout object.
        commandArea_GridLayout = QtWidgets.QGridLayout(commandArea_Frame)
        commandArea_GridLayout.setObjectName("Command_Parameters_Layout")

        self.grid_layout_row = self.grid_layout_row + 1
        self.CommandDisplay_Label = QtWidgets.QLabel(self)
        self.CommandDisplay_Label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.CommandDisplay_Label.setObjectName(_fromUtf8("CommandDisplay_Label"))
        self.CommandDisplay_Label.setText(_translate("Dialog", "Command: ", None))
        commandArea_GridLayout.addWidget(self.CommandDisplay_Label, self.grid_layout_row, 0, 1, 1)
        # Create a text edit object. Add the text edit object to the Dialog window.
        # Set the size, the name and the html of the text edit object.
        # The text edit object, CommandDisplay_View_TextBrowser, displays a dynamic view of the command string.
        self.CommandDisplay_View_TextBrowser = QtWidgets.QTextEdit(self)
        self.CommandDisplay_View_TextBrowser.setObjectName("CommandDisplay_View_TextBrowser")
        self.CommandDisplay_View_TextBrowser.setReadOnly(True)
        self.CommandDisplay_View_TextBrowser.setMaximumHeight(60)
        # self.CommandDisplay_View_TextBrowser.setMinimumSize(QtCore.QSize(0, 100))
        # self.CommandDisplay_View_TextBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
        # #html = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">" \
        # #       "\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { " \
        # #       "white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\';" \
        # #       " font-size:8.25pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px;" \
        # #       " margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">" \
        # #       "<span style=\" font-size:8pt;\">ReadGeoLayerFromGeoJSON()</span></p></body></html>"
        # #self.CommandDisplay_View_TextBrowser.setHtml(_translate("Dialog", html, None))
        commandArea_GridLayout.addWidget(self.CommandDisplay_View_TextBrowser, self.grid_layout_row, 1, 1, -1)

    def setup_ui_core_command_buttons(self):

        buttons_Frame = QtWidgets.QFrame(self)
        buttons_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        buttons_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        buttons_Frame.setObjectName("Command_Parameters")
        self.grid_layout_row = self.grid_layout_row + 1
        self.grid_layout.addWidget(buttons_Frame, self.grid_layout_row, 0, 1, -1)

        # Create a grid layout object. Apply to the Command_Parameters frame object.
        # Set the name of the grid layout object.
        buttons_GridLayout = QtWidgets.QGridLayout(buttons_Frame)
        buttons_GridLayout.setObjectName("Command_Parameters_Layout")

        # Create a button box object. Add the button box object to the Dialog window.
        # Set the orientation, the standard buttons, the name and the connections of the button box object.
        # The button box object, OK_Cancel_Buttons, allow the user to accept or reject the changes made in the dialog.
        self.dialog_ButtonBox = QtWidgets.QDialogButtonBox(self)
        self.dialog_ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_ButtonBox.setObjectName(_fromUtf8("dialog_ButtonBox"))
        self.grid_layout_row = self.grid_layout_row + 1
        use_builtin_buttons = False  # True will cause standard Cancel and Ok buttons to be added
        if use_builtin_buttons:
            self.dialog_ButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
            self.dialog_ButtonBox.button(QtWidgets.QDialogButtonBox.Cancel).setToolTip(
                "Cancel command edit and ignore changes.")
            self.dialog_ButtonBox.button(QtWidgets.QDialogButtonBox.Ok).setToolTip("Save edits to command.")
            self.dialog_ButtonBox.accepted.connect(self.accept)
            self.dialog_ButtonBox.rejected.connect(self.reject)
        else:
            # New design where buttons are added to enable event handling
            # OK button
            # ---------
            self.ok_button = QtWidgets.QPushButton("OK")
            # Object name has parameter at front, which can be parsed out in event-handling code
            self.ok_button.setObjectName(_fromUtf8("OK"))
            self.ok_button.setToolTip("Save edits to command.")
            # self.ok_button.clicked.connect(
                # lambda clicked, f.y_parameter: self.ui_action_open_file(self.load_file_button))
            # Use action role because action is handled in the dialog
            self.dialog_ButtonBox.addButton(self.ok_button, QtWidgets.QDialogButtonBox.ButtonRole.ActionRole)
            self.ok_button.clicked.connect(self.ui_action_ok_clicked)
            # Cancel button
            # ---------
            self.cancel_button = QtWidgets.QPushButton("Cancel")
            # Object name has parameter at front, which can be parsed out in event-handling code
            self.cancel_button.setObjectName(_fromUtf8("Cancel"))
            self.cancel_button.setToolTip("Cancel without saving edits to command.")
            # self.cancel_button.clicked.connect(
            # lambda clicked, f.y_parameter: self.ui_action_open_file(self.load_file_button))
            # Use action role because action is handled in the dialog
            self.dialog_ButtonBox.addButton(self.cancel_button, QtWidgets.QDialogButtonBox.ButtonRole.ActionRole)
            self.cancel_button.clicked.connect(self.ui_action_cancel_clicked)
        # Button box is added regardless of how buttons are defined
        buttons_GridLayout.addWidget(self.dialog_ButtonBox, self.grid_layout_row, 6, 1, 2)

    def setup_ui_core_command_description(self):
        """
        Setup the description component at the top of the dialog.
        """
        # Create a frame object. Add the frame object to the Dialog window.
        # Set the shape, the shadow, and the name of the frame object.
        # The frame object, Command_Description, holds the command description and the view documentation button.
        description_Frame = QtWidgets.QFrame(self)
        description_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        description_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        description_Frame.setObjectName(_fromUtf8("Command_Description"))
        self.grid_layout_row = self.grid_layout_row + 1
        self.grid_layout.addWidget(description_Frame, self.grid_layout_row, 0, 1, 8)

        # Create a grid layout object. Apply to the Command_Description frame object.
        # Set the name of the grid layout object.
        self.gridLayout_2 = QtWidgets.QGridLayout(description_Frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))

        # Create a spacer. Add the spacer to the Command_Description frame object.
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)

        # Create a push button. Add the button to the Command_Description frame object.
        # Set the name, the button text and the connection of the push button.
        # The push button, View_Documentation_Button, displays the command's online user documentation when clicked.
        self.View_Documentation_Button = QtWidgets.QPushButton(description_Frame)
        self.View_Documentation_Button.setObjectName(_fromUtf8("View_Documentation_Button"))
        self.View_Documentation_Button.setText(_translate("Dialog", "  View Documentation  ", None))
        self.View_Documentation_Button.setToolTip("View command documentation in web browser.")
        self.View_Documentation_Button.clicked.connect(self.view_documentation)
        self.gridLayout_2.addWidget(self.View_Documentation_Button, 2, 1, 1, 1)

        # Create a label. Add the label to the Command_Description frame object.
        # Set the name and the text of the label.
        # The label, Command_Description_Label, briefly describes the command.
        self.Command_Description_Label = QtWidgets.QLabel(description_Frame)
        self.Command_Description_Label.setObjectName(_fromUtf8("Command_Description_Label"))
        self.Command_Description_Label.setText(self.command.command_metadata['Description'])
        self.gridLayout_2.addWidget(self.Command_Description_Label, 0, 0, 1, 2)

    # def setupUi_Abstract(self, Dialog):
    #     """
    #     Sets up a Dialog object with the features that are common across all GeoProcessor command dialog windows.
    #
    #     Arg:
    #         Dialog: a QDialog window instance (QtGui.QDialog())
    #
    #     Return: None
    #     """
    #
    #     # Set the name, the initial size and the window title (the name of the command) of the Dialog window object.
    #     # The Dialog window object, Dialog, represents the entire dialog window.
    #     Dialog.setObjectName(_fromUtf8("Dialog"))
    #     Dialog.resize(684, 404)
    #     Dialog.setWindowTitle(_translate("Dialog", self.command_name, None))
    #
    #     # Create a grid layout object. Apply the grid layout to the Dialog window object.
    #     # Set the name of the grid layout object.
    #     self.gridLayout = QtWidgets.QGridLayout(Dialog)
    #     self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    #
    #     # Create a frame object. Add the frame object to the Dialog window.
    #     # Set the shape, the shadow, and the name of the frame object.
    #     # The frame object, Command_Description, holds the command description and the view documentation button.
    #     self.Command_Description = QtWidgets.QFrame(Dialog)
    #     self.Command_Description.setFrameShape(QtWidgets.QFrame.StyledPanel)
    #     self.Command_Description.setFrameShadow(QtWidgets.QFrame.Raised)
    #     self.Command_Description.setObjectName(_fromUtf8("Command_Description"))
    #     self.gridLayout.addWidget(self.Command_Description, 0, 0, 1, 8)
    #
    #     # Create a grid layout object. Apply to the Command_Description frame object.
    #     # Set the name of the grid layout object.
    #     self.gridLayout_2 = QtWidgets.QGridLayout(self.Command_Description)
    #     self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    #
    #     # Create a spacer. Add the spacer to the Command_Description frame object.
    #     spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    #     self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
    #
    #     # Create a push button. Add the button to the Command_Description frame object.
    #     # Set the name, the button text and the connection of the push button.
    #     # The push button, View_Documentation_Button, displays the command's online user documentation when clicked.
    #     self.View_Documentation_Button = QtWidgets.QPushButton(self.Command_Description)
    #     self.View_Documentation_Button.setObjectName(_fromUtf8("View_Documentation_Button"))
    #     self.View_Documentation_Button.setText(_translate("Dialog", "  View Documentation  ", None))
    #     self.View_Documentation_Button.clicked.connect(self.view_documentation)
    #     self.gridLayout_2.addWidget(self.View_Documentation_Button, 2, 1, 1, 1)
    #
    #     # Create a label. Add the label to the Command_Description frame object.
    #     # Set the name and the text of the label.
    #     # The label, Command_Description_Label, briefly describes the command.
    #     self.Command_Description_Label = QtWidgets.QLabel(self.Command_Description)
    #     self.Command_Description_Label.setObjectName(_fromUtf8("Command_Description_Label"))
    #     self.Command_Description_Label.setText(_translate("Dialog", self.command_description, None))
    #     self.gridLayout_2.addWidget(self.Command_Description_Label, 0, 0, 1, 2)
    #
    #     # Create a line (frame object with special specifications). Add the line to the Dialog window.
    #     # Set the size policy, the shape, the shadow, and the name of the frame object to create the line separator.
    #     # The frame object, Separator, separates the command description from the input form section of
    #     # the Dialog box.
    #     self.Separator = QtWidgets.QFrame(Dialog)
    #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(self.Separator.sizePolicy().hasHeightForWidth())
    #     self.Separator.setSizePolicy(sizePolicy)
    #     self.Separator.setFrameShape(QtWidgets.QFrame.HLine)
    #     self.Separator.setFrameShadow(QtWidgets.QFrame.Sunken)
    #     self.Separator.setObjectName(_fromUtf8("Separator"))
    #     self.gridLayout.addWidget(self.Separator, 1, 0, 1, 8)
    #
    #     # Create a button box object. Add the button box object to the Dialog window.
    #     # Set the orientation, the standard buttons, the name and the connections of the button box object.
    #     # The button box object, OK_Cancel_Buttons, allow the user to accept or reject the changes made in the dialog.
    #     self.OK_Cancel_Buttons = QtWidgets.QDialogButtonBox(Dialog)
    #     self.OK_Cancel_Buttons.setOrientation(QtCore.Qt.Horizontal)
    #     self.OK_Cancel_Buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    #     self.OK_Cancel_Buttons.setObjectName(_fromUtf8("OK_Cancel_Buttons"))
    #     self.OK_Cancel_Buttons.accepted.connect(Dialog.accept)
    #     self.OK_Cancel_Buttons.rejected.connect(Dialog.reject)
    #     self.gridLayout.addWidget(self.OK_Cancel_Buttons, self.parameter_count + 4, 6, 1, 2)
    #
    #     # Create a text edit object. Add the text edit object to the Dialog window.
    #     # Set the size, the name and the html of the text edit object.
    #     # The text edit object, CommandDisplay_View_TextBrowser, displays a dynamic view of the command string.
    #     self.CommandDisplay_View_TextBrowser = QtWidgets.QTextEdit(Dialog)
    #     self.CommandDisplay_View_TextBrowser.setMinimumSize(QtCore.QSize(0, 100))
    #     self.CommandDisplay_View_TextBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
    #     self.CommandDisplay_View_TextBrowser.setObjectName(_fromUtf8("CommandDisplay_View_TextBrowser"))
    #     html = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">" \
    #            "\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { " \
    #            "white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\';" \
    #            " font-size:8.25pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px;" \
    #            " margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">" \
    #            "<span style=\" font-size:8pt;\">ReadGeoLayerFromGeoJSON()</span></p></body></html>"
    #     self.CommandDisplay_View_TextBrowser.setHtml(_translate("Dialog", html, None))
    #     self.gridLayout.addWidget(self.CommandDisplay_View_TextBrowser, self.parameter_count + 3, 1, 1, -1)
    #
    #     # Create a label object to the Dialog window.
    #     # Set the alignment, the name, and the text of the label.
    #     # The label, Command Display_Label, labels the CommandDisplay_View_TextBrowser text edit object.
    #     self.CommandDisplay_Label = QtWidgets.QLabel(Dialog)
    #     self.CommandDisplay_Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    #     self.CommandDisplay_Label.setObjectName(_fromUtf8("CommandDisplay_Label"))
    #     self.CommandDisplay_Label.setText(_translate("Dialog", "Command: ", None))
    #     self.gridLayout.addWidget(self.CommandDisplay_Label, self.parameter_count + 3, 0, 1, 1)
    #
    #     # Create a spacer. Add the spacer to the Dialog window.
    #     # The spacer separates the input parameter value fields from the Command Display text browser.
    #     spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    #     self.gridLayout.addItem(spacerItem2, self.parameter_count + 2, 3, 1, -1)
    #
    #     # This will wire up the signals and slots depending on names.
    #     # REF: http://joat-programmer.blogspot.com/2012/02/pyqt-signal-and-slots-to-capture-events.html
    #     QtCore.QMetaObject.connectSlotsByName(Dialog)

    def update_command_display(self):
        """
        Each command dialog box has a command display that shows the string representation of the command with the
        user-specified input parameters. It is updated dynamically as the user enters/selects values for the different
        command parameter fields (this function is called when any text is changed in the input field Qt widgets). The
        function is responsible for reading the inputs, creating the updated string representation of the command and
        updating the CommandDisplay widget.

        Return: None
        """

        # Iterate over the command parameters.
        for command_parameter in self.parameters_list:

            # Get the Qt Widget associated with the command parameter.
            ui_obj = self.input_edit_objects[command_parameter]

            # Get the user-specified value entered in the command parameter Qt Widget input field.
            value = self.get_current_value(ui_obj)

            # Update the current values dictionary with the new user-specified value.
            self.command_parameter_current_values[command_parameter] = value

        # If all of the command parameter values are set to "" (not set), continue.
        if list(self.command_parameter_current_values.values()).count("") == len(self.command_parameter_current_values):

            # The Command Display field should print the command name followed by an empty parenthesis.
            # Ex: ReadGeoLayerFromGeoJSON()
            display = "{}()".format(self.command_name)

        # If AT LEAST ONE command parameter value has been set by the user, continue.
        else:

            # The parameter string text is a string that holds the user-specified parameter values for the
            # command's parameters in a "CommandParameterName=CommandParameterValue" format.
            parameter_string_text = ""

            # Iterate over the command parameters.
            for command_parameter in self.parameters_list:

                # Get the current user-specified value.
                value = self.command_parameter_current_values[command_parameter]

                # If there is a value, add the parameter name and parameter value to the parameter_string_text in a
                # "CommandParameterName=CommandParameterValue" format. A comma is added at the end in order to set up
                # for the next command parameter.
                if value != "":
                    text = '{}="{}", '.format(command_parameter, value)
                    parameter_string_text += text

            # After all of the command parameters with user-specified values have been added to the
            # parameter_string_text, remove the final comma.
            updated_parameter_string_text = parameter_string_text.rsplit(", ", 1)[0]

            # The Command Display field should print the command name followed by a parenthesis filled with the
            # command parameters and associated values.
            # Ex: ReadGeoLayerFromGeoJSON(SpatialDataFile="C:/example/path.geojson", GeoLayerID="Example")
            display = "{}({})".format(self.command_name, updated_parameter_string_text)

        # Update the Command Display Qt Widget to display the dynamic command display text.
        self.CommandDisplay_View_TextBrowser.setText(display)

    def view_documentation(self):
        """
        Opens the command's user documentation in the default browser.

        Return: None
        """

        # The url of the command's user documentation.
        logger = logging.getLogger(__name__)
        command_doc_url = None
        print('Showing documentation')
        try:
            command_doc_url = app_util.get_property('ProgramUserDocumentationUrl')
            # Append more information for the specific command
            command_doc_url = "{}/command-ref/{}/{}/".format(command_doc_url,
                                                             self.command.command_name, self.command.command_name)
            message = "Displaying documentation for command using URL: " + command_doc_url
            print(message)
            logger.info(message)
            # Open the command's user documentation in the default browser.
            # - open in a new tab or if this fails open a new window
            webbrowser.open_new_tab(command_doc_url)
        except Exception as e:
            message = 'Error opening command documentation using  URL "' + command_doc_url + '"'
            logger.error(message, e, exc_info=True)
            qt_util.warning_message_box(message)

    @staticmethod
    def select_file(qt_widget):
        """
        Opens a file browser to allow a user to select a file through a Qt predefined user interface. The path of the
        selected file is added to the qt_widget Qt Widget input field.

        Args:
            qt_widget (obj): the Qt Widget that will display the full path of the selected file

        Return: None
        """

        # Open the browser for file selection. Save the full path of the selected file as a string.
        file_name_text = QtWidgets.QFileDialog.getOpenFileName()[0]

        # Add the full path of the selected file string to the specified input Qt Widget.
        qt_widget.setText(file_name_text)

    def are_required_parameters_specified(self, ui_command_parameter_list):
        """
        Checks if the required parameters of a command are specified by the user in the command dialog window.

        ui_command_parameter_list (list of objects):  a list of the CommandParameter objects (UI-specific class)

        Returns:
            Boolean. If TRUE, all required parameters have been met. If FALSE, one or more of the required parameters
            are not specified.
        """

        # Specified is set to True until proven False.
        specified = True

        # Iterate over the UI CommandParameter objects.
        for ui_parameter in ui_command_parameter_list:

            # If the command parameter is set as "REQUIRED", continue.
            if ui_parameter.optional is False:

                # If the value of the required command parameter has not been specified by the user, set specified
                # to False.
                if self.command_parameter_values[ui_parameter.name] is "":
                    specified = False

        # Return the specified Boolean.
        return specified

    def configureLabel(self, label, parameter_name):
        """
        Configure a QtGui.QLabel object (parameter name label) that meets the standards of the GeoProceossor's
        command dialog window.

        Args:
            label (obj): a QtGui.QLabel object
            parameter_name (str): the name of the command parameter that is using the label

        Return: None
        """

        # Set the label to align right so that it butts up next to the input field.
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Set the label's object name (XXX_Label where XXX is the name of the command parameter).
        label.setObjectName(_fromUtf8("{}_Label".format(parameter_name)))

        # Get the dialog box row index that is used to display the command parameter objects
        # This is a dynamic index that takes into consideration the order of the command's parameters.
        row_index = self.parameters_list.index(parameter_name) + 2

        # Add the label to the Dialog box in the correct row. Command labels will always be in the first column (0),
        # and will occupy 1 column and 1 row.
        self.gridLayout.addWidget(label, row_index, 0, 1, 1)

        # Set the text of the label to be the name of the command parameter.
        label.setText(_translate("Dialog", "{}: ".format(parameter_name), None))

    def configureLineEdit(self, line_edit, parameter_name, long=False, placeholder_text=None, tooltip=None):
        """
        Configure a QtGui.QLineEdit object that meets the standards of the GeoProceossor's command dialog window.

        Args:
            line_edit (obj): a QtGui.QLineEdit object
            parameter_name (str): the name of the command parameter that is using the line edit field
            long (bool): if TRUE, the QtGui.QLineEdit object spans the majority of the dialog window. This is good
                for parameter values that will be an absolute file path. if FALSE, the QtGui.QLineEdit object spans a
                subset of the dialog window. This is good gor parameter value that one require a one/few word value.
            placeholder_text (str): optional. The text that will display within the QtGui.QLineEdit object before the
                user enters a value. This is helpful to supply a parameter description when `long` is set to `True`.
            tooltip (str): optional. The text that will display in a pop-up when the user mouses over the
                QtGui.QLineEdit object. This is a good place to expand description of the parameter/parameter values.

        Return: None
        """

        # Set the line edit's object name (XXX_LineEdit where XXX is the name of the command parameter).
        line_edit.setObjectName(_fromUtf8("{}_LineEdit".format(parameter_name)))

        # Get the dialog box row index that is used to display the command parameter objects
        # This is a dynamic index that takes into consideration the order of the command's parameters.
        row_index = self.parameters_list.index(parameter_name) + 2

        # Add the line edit field to the Dialog box in the correct row. Command line edit fields will always start in
        # the second column (1) and will occupy 1 row.
        # If the field is set to long, the line edit field will occupy 6 columns.
        if long:
            self.gridLayout.addWidget(line_edit, row_index, 1, 1, 6)

        # If not set to long, the line edit field will occupy 3 columns.
        else:
            self.gridLayout.addWidget(line_edit, row_index, 1, 1, 3)

        # If placeholder text has been specified, add the desired text as placeholder text.
        if placeholder_text:
            line_edit.setPlaceholderText(_translate("Dialog", placeholder_text, None))

        # If tool tip text has been specified, add the desired text as tool tip text.
        if tooltip:
            line_edit.setToolTip(_translate("Dialog", tooltip, None))

        # Create a listener that reacts if the line edit field has been changed. If so, run the
        # update_command_display function.
        line_edit.textChanged.connect(self.update_command_display)

        # Add the QtGui.QLineEdit object to the dictionary of input edit objects. Use the parameter name as the key
        # and the QtGui.QLineEdit object as the value.
        self.input_edit_objects[parameter_name] = line_edit

    def configureToolButton(self, tool_button, parameter_name, line_edit_obj_affected):
        """
        Configures a QtGui.QToolButton object that meets the standards of the GeoProceossor's command dialog window.

        Args:
            tool_button (obj): a QtGui.QToolButton object
            parameter_name (str): the name of the command parameter that is using the tool button
            line_edit_obj_affected (obj): a QtGui.QLineEdit object that will be populated with the filepath text of
                the selected file selected with the tool button

        Returns: the path to the selected file
        """

        # Set the tool buttons's object name (XXX_ToolButton where XXX is the name of the command parameter).
        tool_button.setObjectName(_fromUtf8("{}_ToolButton".format(parameter_name)))

        # Set the tool button's text. (Default value is `...` but this can be pulled out into a function argument if
        # needed.)
        tool_button.setText(_translate("Dialog", "...", None))

        # Get the dialog box row index that is used to display the command parameter objects
        # This is a dynamic index that takes into consideration the order of the command's parameters.
        row_index = self.parameters_list.index(parameter_name) + 2

        # Add the tool button to the Dialog box in the correct row. Command tool buttons will always be in the
        # last column (7), and will occupy 1 row and 1 column.
        self.gridLayout.addWidget(tool_button, row_index, 7, 1, 1)

        # Create a listener that reacts if the tool button is clicked. If so, run the select_file function to allow
        # the user to browse to a local file.
        tool_button.clicked.connect(functools.partial(self.select_file, line_edit_obj_affected))

    def configureDescriptionLabel(self, label, parameter_name, text):
        """
        Configure a QtGui.QLabel object (parameter description label) that meets the standards of the GeoProcessor's
        command dialog window.

        Args:
            label (obj): a QtGui.QLabel object
            parameter_name (str): the name of the command parameter that is using the label
            text (str): the parameter description to use as the label text

        Return: None
        """

        # Get the dialog box row index that is used to display the command parameter objects
        # This is a dynamic index that takes into consideration the order of the command's parameters.
        row_index = self.parameters_list.index(parameter_name) + 2

        # Set the label's object name (XXX_Description_Label where XXX is the name of the command parameter).
        label.setObjectName(_fromUtf8("{}_Description_Label".format(parameter_name)))

        # Add the label to the Dialog box in the correct row. Command description labels will always be in the
        # third-to-last column (5), and will occupy 1 column and 3 rows.
        self.gridLayout.addWidget(label, row_index, 5, 1, 3)

        # Set the text of the label to be the command parameter description.
        label.setText(_translate("Dialog", text, None))

    def configureComboBox(self, combobox, parameter_name, choice_list, tooltip=None):
        """
        Configure a QtGui.QComboBox object that meets the standards of the GeoProceossor's command dialog window.

        Args:
            combobox(obj): a QtGui.QComboBox object
            parameter_name (str): the name of the command parameter that is using the combobox field
            choice_list (list): a list of available values for the command parameter
            tooltip (str): optional. The text that will display in a pop-up when the user mouses over the
                QtGui.QComboBox object. This is a good place to expand description of the parameter/parameter values.

        Return: None
        """

        # Get the dialog box row index that is used to display the command parameter objects
        # This is a dynamic index that takes into consideration the order of the command's parameters.
        row_index = self.parameters_list.index(parameter_name) + 2

        # Set the combo box's object name (XXX_ComboBox where XXX is the name of the command parameter).
        combobox.setObjectName(_fromUtf8("{}_ComboBox".format(parameter_name)))

        # Add "spaces" to the ComboBox for each of the available options including a blank option to display that an
        # option has not been selected.
        for i in range(len(choice_list) + 1):
            combobox.addItem(_fromUtf8(""))

        # Add the combo box field to the Dialog box in the correct row. Command combo box fields will always start in
        # the second column (1) and will occupy 1 column and 2 rows.
        self.gridLayout.addWidget(combobox, row_index, 1, 1, 2)

        # Set the combo box default option to the blank option - the first (0) in the list of choices.
        combobox.setItemText(0, _fromUtf8(""))

        # Add the text associated with each parameter option to the appropriate ComboBox "space".
        for i in range(len(choice_list)):
            combobox.setItemText(i+1, _translate("Dialog", choice_list[i], None))

        # If tool tip text has been specified, add the desired text as tool tip text.
        if tooltip:
            combobox.setToolTip(_translate("Dialog", tooltip, None))

        # Add the QtGui.QComboBox object to the dictionary of input edit objects. Use the parameter name as the key
        # and the QtGui.QComboBox object as the value.
        self.input_edit_objects[parameter_name] = combobox

        # Create a listener that reacts if the ComboBox field has been changed. If so, run the
        # update_command_display function.
        combobox.currentIndexChanged.connect(self.update_command_display)

    def get_current_value(self, obj):
        """
        Get the value within a QtGui.Widget object.

        Arg:
            obj (obj): the a QtGui.Widget object to read the value from

        Return: the value within the QtGui.Widget object
        """

        # Different QtGui widgets have different ways of reading their input data. Try both versions and assign the
        # value when one works.
        # Reads LineEdit widgets.
        try:
            value = obj.text()

        # Reads ComboBox widgets.
        except:
            value = obj.currentText()

        # Return the value within the input QtGui.Widget object.
        return value

