# WriteTableToExcel

from geoprocessor.commands.abstract.AbstractCommand import AbstractCommand

from geoprocessor.core.CommandLogRecord import CommandLogRecord
from geoprocessor.core.CommandParameterMetadata import CommandParameterMetadata
import geoprocessor.core.command_phase_type as command_phase_type
import geoprocessor.core.command_status_type as command_status_type

import geoprocessor.util.command_util as command_util
import geoprocessor.util.io_util as io_util
import geoprocessor.util.pandas_util as pandas_util
import geoprocessor.util.string_util as string_util
import geoprocessor.util.validator_util as validators

import logging
import os


class WriteTableToExcel(AbstractCommand):
    """
    Writes a Table to an Excel file.

    Command Parameters
    * TableID (str, required): the identifier of the Table to be written to the Excel file 
    * OutputFile (str, required): the relative pathname of the output Excel file.
    * OutputWorksheet (str, required): the name of the worksheet that the Table will be written
     * WriteHeaderRow (bool, optional): If TRUE, the column names are written. If FALSE, the column names are excluded.
        Default: True
    * WriteIndexColumn (bool, optional): If TRUE, the index column is written, If FALSE, the index column is excluded.
        Default: True
    * FileFormat (str, optional): This parameter determines which version of an Excel file to write.
        Available options are: `xlsx`, `xls` and `xlsm`. Default: `xlsx`. If the Excel file already exists, this
        parameter is ignored and the file format of the original excel file is used.
    """

    # Define the command parameters/
    __command_parameter_metadata = [
        CommandParameterMetadata("TableID", type("")),
        CommandParameterMetadata("OutputFile", type("")),
        CommandParameterMetadata("OutputWorksheet", type("")),
        CommandParameterMetadata("WriteHeaderRow", type("")),
        CommandParameterMetadata("WriteIndexColumn", type("")),
        CommandParameterMetadata("FileFormat", type(""))]

    def __init__(self):
        """
        Initialize the command.
        """

        # AbstractCommand data
        super(WriteTableToExcel, self).__init__()
        self.command_name = "WriteTableToExcel"
        self.command_parameter_metadata = self.__command_parameter_metadata

        # Class data
        self.warning_count = 0
        self.logger = logging.getLogger(__name__)

    def check_command_parameters(self, command_parameters):
        """
        Check the command parameters for validity.

        Args:
            command_parameters: the dictionary of command parameters to check (key:string_value)

        Returns: None.

        Raises:
            ValueError if any parameters are invalid or do not have a valid value.
            The command status messages for initialization are populated with validation messages.
        """

        warning = ""

        # Check that parameter TableID is a non-empty, non-None string.
        pv_TableID = self.get_parameter_value(parameter_name='TableID', command_parameters=command_parameters)

        if not validators.validate_string(pv_TableID, False, False):
            message = "TableID parameter has no value."
            recommendation = "Specify the TableID parameter to indicate the Table to write."
            warning += "\n" + message
            self.command_status.add_to_log(
                command_phase_type.INITIALIZATION,
                CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Check that parameter OutputFile is a non-empty, non-None string.
        pv_OutputFile = self.get_parameter_value(parameter_name='OutputFile', command_parameters=command_parameters)

        if not validators.validate_string(pv_OutputFile, False, False):
            message = "OutputFile parameter has no value."
            recommendation = "Specify the OutputFile parameter (relative or absolute pathname) to indicate the " \
                             "location and name of the output Excel file."
            warning += "\n" + message
            self.command_status.add_to_log(
                command_phase_type.INITIALIZATION,
                CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Check that parameter WriteHeaderRow is a valid Boolean value or None.
        pv_WriteHeaderRow = self.get_parameter_value(parameter_name='WriteHeaderRow',
                                                     command_parameters=command_parameters)

        if not validators.validate_bool(pv_WriteHeaderRow, True, False):
            message = "WriteHeaderRow parameter is not a valid Boolean value."
            recommendation = "Specify a valid Boolean value for the WriteHeaderRow parameter."
            warning += "\n" + message
            self.command_status.add_to_log(
                command_phase_type.INITIALIZATION,
                CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Check that parameter WriteIndexColumn is a valid Boolean value or None.
        pv_WriteIndexColumn = self.get_parameter_value(parameter_name='WriteIndexColumn',
                                                       command_parameters=command_parameters)

        if not validators.validate_bool(pv_WriteIndexColumn, True, False):
            message = "WriteIndexColumn parameter is not a valid Boolean value."
            recommendation = "Specify a valid Boolean value for the WriteIndexColumn parameter."
            warning += "\n" + message
            self.command_status.add_to_log(
                command_phase_type.INITIALIZATION,
                CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Check that optional parameter FileFormat is either `xls`, `xlsx`, `xlsm` or None.
        pv_FileFormat = self.get_parameter_value(parameter_name="FileFormat", command_parameters=command_parameters)
        acceptable_values = ["xls", "xlsx", "xlsm"]
        if not validators.validate_string_in_list(pv_FileFormat, acceptable_values, none_allowed=True,
                                                  empty_string_allowed=False, ignore_case=True):
            message = "FileFormat parameter value ({}) is not recognized.".format(pv_FileFormat)
            recommendation = "Specify one of the acceptable values ({}) for the FileFormat parameter.".format(
                acceptable_values)
            warning += "\n" + message
            self.command_status.add_to_log(
                command_phase_type.INITIALIZATION,
                CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Check for unrecognized parameters.
        # This returns a message that can be appended to the warning, which if non-empty triggers an exception below.
        warning = command_util.validate_command_parameter_names(self, warning)

        # If any warnings were generated, throw an exception.
        if len(warning) > 0:
            self.logger.warning(warning)
            raise ValueError(warning)

        # Refresh the phase severity
        self.command_status.refresh_phase_severity(command_phase_type.INITIALIZATION, command_status_type.SUCCESS)

    def __should_write_table(self, table_id, output_file_abs):
        """
       Checks the following:
       * the ID of the Table is an existing Table ID
       * the output folder is a valid folder

       Args:
           table_id: the ID of the Table to be written
           output_file_abs: the full pathname to the output file

       Returns:
           run_write: Boolean. If TRUE, the writing process should be run. If FALSE, it should not be run.
       """

        # List of Boolean values. The Boolean values correspond to the results of the following tests. If TRUE, the
        # test confirms that the command should be run.
        should_run_command = []

        # If the Table ID is not an existing Table ID, raise a FAILURE.
        should_run_command.append(validators.run_check(self, "IsTableIdExisting", "TableID", table_id, "FAIL"))

        # Get the full path to the output folder
        output_folder_abs = io_util.get_path(output_file_abs)

        # If the output folder is not an existing folder, raise a FAILURE.
        should_run_command.append(validators.run_check(self, "IsFolderPathValid", "OutputFile", output_folder_abs,
                                                       "FAIL"))

        # Return the Boolean to determine if the process should be run.
        if False in should_run_command:
            return False
        else:
            return True

    def run_command(self):
        """
        Run the command. Write the Table to an excel file.

        Returns: None.

        Raises:
            RuntimeError if any warnings occurred during run_command method.
        """

        # Obtain the parameter values except for the OutputCRS
        pv_TableID = self.get_parameter_value("TableID")
        pv_OutputFile = self.get_parameter_value("OutputFile")
        pv_OutputWorksheet = self.get_parameter_value("OutputWorksheet")
        pv_WriteHeaderRow = self.get_parameter_value("WriteHeaderRow", default_value="True")
        pv_WriteIndexColumn = self.get_parameter_value("WriteIndexColumn", default_value="True")
        pv_FileFormat = self.get_parameter_value("FileFormat")

        # Convert the Boolean parameters from string to valid Boolean values.
        pv_WriteHeaderRow = string_util.str_to_bool(pv_WriteHeaderRow)
        pv_WriteIndexColumn = string_util.str_to_bool(pv_WriteIndexColumn)

        # Convert the OutputFile parameter value relative path to an absolute path and expand for ${Property} syntax
        output_file_absolute = io_util.verify_path_for_os(
            io_util.to_absolute_path(self.command_processor.get_property('WorkingDir'),
                                     self.command_processor.expand_parameter_value(pv_OutputFile, self)))

        # If the excel file already exists, ignore the pv_FileFormat parameter (set it to None).
        if os.path.exists(output_file_absolute):
            pv_FileFormat = None

        # Run the checks on the parameter values. Only continue if the checks passed.
        if self.__should_write_table(pv_TableID, output_file_absolute):

            try:

                # Get the Table object
                table = self.command_processor.get_table(pv_TableID)

                # Write the tables to an Excel file.
                pandas_util.write_df_to_excel(table.df, output_file_absolute, pv_OutputWorksheet, pv_WriteHeaderRow,
                                              pv_WriteIndexColumn)

            # Raise an exception if an unexpected error occurs during the process
            except Exception as e:
                self.warning_count += 1
                message = "Unexpected error writing Table {} to Excel workbook file {}.".format(pv_TableID,
                                                                                                pv_OutputFile)
                recommendation = "Check the log file for details."
                self.logger.error(message, exc_info=True)
                self.command_status.add_to_log(command_phase_type.RUN,
                                               CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Determine success of command processing. Raise Runtime Error if any errors occurred
        if self.warning_count > 0:
            message = "There were {} warnings proceeding this command.".format(self.warning_count)
            raise RuntimeError(message)

        # Set command status type as SUCCESS if there are no errors.
        else:
            self.command_status.refresh_phase_severity(command_phase_type.RUN, command_status_type.SUCCESS)
