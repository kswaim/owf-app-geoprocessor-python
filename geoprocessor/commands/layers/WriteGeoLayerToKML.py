# WriteGeoLayerToKML - write a GeoLayer to a KML file
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

from geoprocessor.commands.abstract.AbstractCommand import AbstractCommand

from geoprocessor.core.CommandLogRecord import CommandLogRecord
from geoprocessor.core.CommandParameterMetadata import CommandParameterMetadata
from geoprocessor.core.CommandPhaseType import CommandPhaseType
from geoprocessor.core.CommandStatusType import CommandStatusType

import geoprocessor.util.command_util as command_util
import geoprocessor.util.io_util as io_util
import geoprocessor.util.qgis_util as qgis_util
import geoprocessor.util.validator_util as validators

import logging


class WriteGeoLayerToKML(AbstractCommand):
    """
    Writes a GeoLayer to a spatial data file in KML format.

    This command writes a GeoLayer registered within the geoprocessor to a KML spatial data file. The KML
    spatial data file can then be viewed within Google Earth, moved within folders on the local computer, packaged for
    delivery, etc.

    Registered GeoLayers are stored as GeoLayer objects within the geoprocessor's GeoLayers list. Each GeoLayer has one
    feature type (point, line, polygon, etc.) and other data (an identifier, a coordinate reference system, etc). This
    function only writes one single GeoLayer to a single spatial data file in GeoJSON format.

    Command Parameters
    * GeoLayerID (str, required): the identifier of the GeoLayer to be written to a spatial data file in GeoJSON format.
    * OutputFile (str, required): the relative pathname of the output spatial data file.
    * PlacemarkNameAttribute (str, optional): Allows you to specify the field to use for the KML <name> element.
        Default: Name
    * PlacemarkDescriptionAttribute (str, optional): Allows you to specify the field to use for the KML <description>
        element. Default: Description
    """

    # Define the command parameters.
    __command_parameter_metadata = [
        CommandParameterMetadata("GeoLayerID", type("")),
        CommandParameterMetadata("OutputFile", type("")),
        CommandParameterMetadata("PlacemarkNameAttribute", type("")),
        CommandParameterMetadata("PlacemarkDescriptionAttribute", type(""))]

    def __init__(self):
        """
        Initialize the command.
        """

        # AbstractCommand data
        super().__init__()
        self.command_name = "WriteGeoLayerToKML"
        self.command_parameter_metadata = self.__command_parameter_metadata

        # Command metadata for command editor display
        self.command_metadata = dict()
        self.command_metadata['Description'] = "Write a GeoLayer to a file in KML format."
        self.command_metadata['EditorType'] = "Simple"

        # Command Parameter Metadata
        self.parameter_input_metadata = dict()
        # GeoLayerID
        self.parameter_input_metadata['GeoLayerID.Description'] = "identifier of the GeoLayer to write"
        self.parameter_input_metadata['GeoLayerID.Label'] = "GeoLayerID"
        self.parameter_input_metadata['GeoLayerID.Required'] = True
        self.parameter_input_metadata['GeoLayerID.Tooltip'] = "The GeoLayer identifier, can use ${Property}."
        # OutputFile
        self.parameter_input_metadata['OutputFile.Description'] = "property file to write"
        self.parameter_input_metadata['OutputFile.Label'] = "Output file"
        self.parameter_input_metadata['OutputFile.Required'] = True
        self.parameter_input_metadata['OutputFile.Tooltip'] = \
            "The output KML file (relative or absolute path). ${Property} syntax is recognized."
        self.parameter_input_metadata['OutputFile.FileSelector.Type'] = "Write"
        self.parameter_input_metadata['OutputFile.FileSelector.Title'] = "Select file to write output"
        # PlacemarkNameAttribute
        self.parameter_input_metadata['PlacemarkNameAttribute.Description'] =\
            "geolayer attribute for the KML's placemark name"
        self.parameter_input_metadata['PlacemarkNameAttribute.Label'] = "Placemark name attribute"
        self.parameter_input_metadata['PlacemarkNameAttribute.Tooltip'] = (
            "The GeoLayer attribute to populate the output KML's placemark <name> elements.\n"
            "Each GeoLayer feature is coverted into a KML placemark. Each placemark can have a <name> element.\n"
            "The attribute values within the PlacemarkNameAttribute will populate each placemark's name.\n"
            "For further explanation, look at the example KML document under the Structure section of the Keyhole "
            "Markup Language Wikipedia page.")
        self.parameter_input_metadata['PlacemarkNameAttribute.Value.Default.Description'] =\
            "The output KML placemarks will not have a <name> element."
        # PlacemarkDescriptionAttribute
        self.parameter_input_metadata['PlacemarkDescriptionAttribute.Description'] =\
            "GeoLayer attribute for KML's placemark description"
        self.parameter_input_metadata['PlacemarkDescriptionAttribute.Label'] = "Placemark description attribute"
        self.parameter_input_metadata['PlacemarkDescriptionAttribute.Tooltip'] = (
            "The GeoLayer attribute to populate the output KML's placemark <description> elements.\n"
            "Each GeoLayer feature is coverted into a KML placemark. Each placemark can have a <description> element.\n"
            "The attribute values within the PlacemarkDescriptionAttribute will populate each"
            "placemark's description.\n"
            "For further explanation, look at the example KML document under the Structure section of the "
            "Keyhole Markup Language Wikipedia page.")
        self.parameter_input_metadata['PlacemarkDescriptionAttribute.Value.Default'] = \
            "The output KML placemarks will not have a <description> element."

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

        # Check that parameter GeoLayerID is a non-empty, non-None string.
        # - existence of the GeoLayer will also be checked in run_command().
        pv_GeoLayerID = self.get_parameter_value(parameter_name='GeoLayerID', command_parameters=command_parameters)

        if not validators.validate_string(pv_GeoLayerID, False, False):
            message = "GeoLayerID parameter has no value."
            recommendation = "Specify the GeoLayerID parameter to indicate the GeoLayer to write."
            warning += "\n" + message
            self.command_status.add_to_log(
                CommandPhaseType.INITIALIZATION,
                CommandLogRecord(CommandStatusType.FAILURE, message, recommendation))

        # Check that parameter OutputFile is a non-empty, non-None string.
        # - existence of the folder will also be checked in run_command().
        pv_OutputFile = self.get_parameter_value(parameter_name='OutputFile', command_parameters=command_parameters)

        if not validators.validate_string(pv_OutputFile, False, False):
            message = "OutputFile parameter has no value."
            recommendation = "Specify the OutputFile parameter (relative or absolute pathname) to indicate the " \
                             "location and name of the output spatial data file in GeoJSON format."
            warning += "\n" + message
            self.command_status.add_to_log(
                CommandPhaseType.INITIALIZATION,
                CommandLogRecord(CommandStatusType.FAILURE, message, recommendation))

        # Check for unrecognized parameters.
        # This returns a message that can be appended to the warning, which if non-empty triggers an exception below.
        warning = command_util.validate_command_parameter_names(self, warning)

        # If any warnings were generated, throw an exception.
        if len(warning) > 0:
            self.logger.warning(warning)
            raise ValueError(warning)

        # Refresh the phase severity
        self.command_status.refresh_phase_severity(CommandPhaseType.INITIALIZATION, CommandStatusType.SUCCESS)

    def __should_write_geolayer(self, geolayer_id, output_file_abs):
        """
       Checks the following:
       * the ID of the GeoLayer is an existing GeoLayer ID
       * the output folder is a valid folder

       Args:
           geolayer_id: the ID of the GeoLayer to be written
           output_file_abs: the full pathname to the output file

       Returns:
             Boolean. If TRUE, the GeoLayer should be written. If FALSE, at least one check failed and the GeoLayer
                should not be written.
       """

        # List of Boolean values. The Boolean values correspond to the results of the following tests. If TRUE, the
        # test confirms that the command should be run.
        should_run_command = []

        # If the GeoLayer ID is not an existing GeoLayer ID, raise a FAILURE.
        should_run_command.append(validators.run_check(self, "IsGeoLayerIdExisting", "GeoLayerID", geolayer_id, "FAIL"))

        # If the folder of the OutputFile file path is not a valid folder, raise a FAILURE.
        should_run_command.append(validators.run_check(self, "DoesFilePathHaveAValidFolder", "OutputFile",
                                                       output_file_abs, "FAIL"))

        # Return the Boolean to determine if the process should be run.
        if False in should_run_command:
            return False
        else:
            return True

    def run_command(self):
        """
        Run the command. Write the GeoLayer to a spatial data file in KML format.

        Returns: None.

        Raises:
            RuntimeError if any warnings occurred during run_command method.
        """

        # Obtain the parameter values.
        pv_GeoLayerID = self.get_parameter_value("GeoLayerID")
        pv_OutputFile = self.get_parameter_value("OutputFile")
        pv_PlacemarkNameAttribute = self.get_parameter_value("PlacemarkNameAttribute")
        pv_PlacemarkDescriptionAttribute = self.get_parameter_value("PlacemarkDescriptionAttribute")

        # Convert the OutputFile parameter value relative path to an absolute path and expand for ${Property} syntax
        output_file_absolute = io_util.verify_path_for_os(
            io_util.to_absolute_path(self.command_processor.get_property('WorkingDir'),
                                     self.command_processor.expand_parameter_value(pv_OutputFile, self)))

        # Run the checks on the parameter values. Only continue if the checks passed.
        if self.__should_write_geolayer(pv_GeoLayerID, output_file_absolute):

            try:
                # Get the GeoLayer
                geolayer = self.command_processor.get_geolayer(pv_GeoLayerID)

                # Write the GeoLayer to a spatial data file in KML format
                # "Note that KML by specification uses only a single projection, EPSG:4326. All OGR KML output will be
                # presented in EPSG:4326. As such OGR will create layers in the correct coordinate system and transform
                # any geometries." - www.gdal.org/drv_kml.html
                qgis_util.write_qgsvectorlayer_to_kml(geolayer.qgs_vector_layer,
                                                      output_file_absolute,
                                                      "EPSG:4326",
                                                      pv_PlacemarkNameAttribute,
                                                      pv_PlacemarkDescriptionAttribute,
                                                      "clampToGround")

            # Raise an exception if an unexpected error occurs during the process
            except Exception as e:
                self.warning_count += 1
                message = "Unexpected error writing GeoLayer {} to GeoJSON format.".format(pv_GeoLayerID)
                recommendation = "Check the log file for details."
                self.logger.error(message, exc_info=True)
                self.command_status.add_to_log(CommandPhaseType.RUN,
                                               CommandLogRecord(CommandStatusType.FAILURE, message, recommendation))

        # Determine success of command processing. Raise Runtime Error if any errors occurred
        if self.warning_count > 0:
            message = "There were {} warnings proceeding this command.".format(self.warning_count)
            raise RuntimeError(message)

        # Set command status type as SUCCESS if there are no errors.
        else:
            self.command_status.refresh_phase_severity(CommandPhaseType.RUN, CommandStatusType.SUCCESS)
