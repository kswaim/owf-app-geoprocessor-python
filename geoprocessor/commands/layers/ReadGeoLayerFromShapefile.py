# ReadGeoLayerFromShapefile

from geoprocessor.commands.abstract.AbstractCommand import AbstractCommand

from geoprocessor.core.CommandLogRecord import CommandLogRecord
from geoprocessor.core.CommandParameterMetadata import CommandParameterMetadata
import geoprocessor.core.command_phase_type as command_phase_type
import geoprocessor.core.command_status_type as command_status_type
from geoprocessor.core.GeoLayer import GeoLayer

import geoprocessor.util.commandUtil as command_util
import geoprocessor.util.qgisUtil as qgis_util
import geoprocessor.util.ioUtil as io_util
import geoprocessor.util.validatorsUtil as validators

import os
import logging


class ReadGeoLayerFromShapefile(AbstractCommand):

    """
    Reads a GeoLayer from a Shapefile spatial data file.

    This command reads a GeoLayer from a Shapefile file and creates a GeoLayer object within the
    geoprocessor. The GeoLayer can then be accessed in the geoprocessor by its identifier and further processed.

    GeoLayers are stored on a computer or are available for download as a spatial data file (GeoJSON, shapefile,
    feature class in a file geodatabase, etc.). Each GeoLayer has one feature type (point, line, polygon, etc.) and
    other data (an identifier, a coordinate reference system, etc). Note that this function only reads a single
    GeoLayer from a single file in Shapefile format.

    In order for the geoprocessor to use and manipulate spatial data files, GeoLayers are instantiated as
    `QgsVectorLayer <https://qgis.org/api/classQgsVectorLayer.html>`_ objects.

    Command Parameters
    * SpatialDataFile (str, required): the relative pathname to the spatial data file (GeoJSON format)
    * GeoLayerID (str, optional): the GeoLayer identifier. If None, the spatial data filename (without the .geojson
        extension) will be used as the GeoLayer identifier. For example: If GeoLayerID is None and the absolute
        pathname to the spatial data file is C:/Desktop/Example/example_file.geojson, then the GeoLayerID will be
        `example_file`.
    * IfGeoLayerIDExists (str, optional): This parameter determines the action that occurs if the CopiedGeoLayerID
        already exists within the GeoProcessor. Available options are: `Replace`, `ReplaceAndWarn`, `Warn` and `Fail`
        (Refer to user documentation for detailed description.) Default value is `Replace`.
    """

    # Define the command parameters.
    __command_parameter_metadata = [
        CommandParameterMetadata("SpatialDataFile", type("")),
        CommandParameterMetadata("GeoLayerID", type("")),
        CommandParameterMetadata("IfGeoLayerIDExists", type(""))]

    def __init__(self):
        """
        Initialize the command
        """

        # AbstractCommand data
        super(ReadGeoLayerFromShapefile, self).__init__()
        self.command_name = "ReadGeoLayerFromShapefile"
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

        # Check that parameter SpatialDataFile is a non-empty, non-None string.
        # - existence of the file will also be checked in run_command().
        pv_SpatialDataFile = self.get_parameter_value(parameter_name='SpatialDataFile',
                                                      command_parameters=command_parameters)

        if not validators.validate_string(pv_SpatialDataFile, False, False):

            message = "SpatialDataFile parameter has no value."
            recommendation = "Specify the SpatialDataFile parameter to indicate the spatial data layer file."
            warning += "\n" + message
            self.command_status.add_to_log(
                command_phase_type.INITIALIZATION,
                CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Check that optional parameter IfGeoLayerIDExists is either `Replace`, `ReplaceAndWarn`, `Warn`, `Fail`, None.
        pv_IfGeoLayerIDExists = self.get_parameter_value(parameter_name="IfGeoLayerIDExists",
                                                         command_parameters=command_parameters)
        acceptable_values = ["Replace", "ReplaceAndWarn", "Warn", "Fail"]
        if not validators.validate_string_in_list(pv_IfGeoLayerIDExists, acceptable_values, none_allowed=True,
                                                  empty_string_allowed=True, ignore_case=True):
            message = "IfGeoLayerIDExists parameter value ({}) is not recognized.".format(pv_IfGeoLayerIDExists)
            recommendation = "Specify one of the acceptable values ({}) for the IfGeoLayerIDExists parameter.".format(
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

        else:
            # Refresh the phase severity
            self.command_status.refresh_phase_severity(command_phase_type.INITIALIZATION, command_status_type.SUCCESS)

    def __should_read_geolayer(self, spatial_data_file_abs, geolayer_id):

        """
        Checks the following:
        * the SpatialDataFile (absolute) is a valid file
        * the SpatialDataFile (absolute) ends in .SHP (warning, not error)
        * the ID of the output GeoLayer is unique (not an existing GeoLayerList ID)
        * the ID of the output GeoLayer is unique (not an existing GeoLayer ID)

        Args:
            spatial_data_file_abs: the full pathname to the input spatial data file
            geolayer_id: the ID of the output GeoLayer

        Returns:
            run_read: Boolean. If TRUE, the read process should be run. If FALSE, the read process should not be run.
        """

        # Boolean to determine if the read process should be run. Set to true until an error occurs.
        run_read = True

        # If the input spatial data file is not a valid file path, raise a FAILURE.
        if not os.path.isfile(spatial_data_file_abs):

            run_read = False
            self.warning_count += 1
            message = "The SpatialDataFile ({}) is not a valid file.".format(spatial_data_file_abs)
            recommendation = "Specify a valid file."
            self.logger.error(message)
            self.command_status.add_to_log(command_phase_type.RUN,
                                           CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # If the input spatial data file does not end in .geojson, raise a WARNING.
        if not spatial_data_file_abs.upper().endswith(".SHP"):
            self.warning_count += 1
            message = 'The SpatialDataFile ({}) does not end with the .shp extension.'.format(spatial_data_file_abs)
            recommendation = "No recommendation logged."
            self.logger.warning(message)
            self.command_status.add_to_log(command_phase_type.RUN,
                                           CommandLogRecord(command_status_type.WARNING, message, recommendation))

        # If the GeoLayer ID is the same as as already-existing GeoLayerListID, raise a FAILURE.
        if self.command_processor.get_geolayerlist(geolayer_id):

            run_read = False
            self.warning_count += 1
            message = 'The GeoLayerID ({}) value is already in use as a GeoLayerList ID.'.format(geolayer_id)
            recommendation = 'Specify a new GeoLayerID.'
            self.logger.error(message)
            self.command_status.add_to_log(command_phase_type.RUN,
                                           CommandLogRecord(command_status_type.FAILURE,
                                                            message, recommendation))

        # If the GeoLayerID is the same as an already-registered GeoLayerID, react according to the
        # pv_IfGeoLayerIDExists value.
        elif self.command_processor.get_geolayer(geolayer_id):

            # Get the IfGeoLayerIDExists parameter value.
            pv_IfGeoLayerIDExists = self.get_parameter_value("IfGeoLayerIDExists", default_value="Replace")

            # Warnings/recommendations if the GeolayerID is the same as a registered GeoLayerID.
            message = 'The GeoLayerID ({}) value is already in use as a GeoLayer ID.'.format(geolayer_id)
            recommendation = 'Specify a new GeoLayerID.'

            # The registered GeoLayer should be replaced with the new GeoLayer (with warnings).
            if pv_IfGeoLayerIDExists.upper() == "REPLACEANDWARN":
                self.warning_count += 1
                self.logger.warning(message)
                self.command_status.add_to_log(command_phase_type.RUN,
                                               CommandLogRecord(command_status_type.WARNING,
                                                                message, recommendation))

            # The registered GeoLayer should not be replaced. A warning should be logged.
            if pv_IfGeoLayerIDExists.upper() == "WARN":

                run_read = False
                self.warning_count += 1
                self.logger.warning(message)
                self.command_status.add_to_log(command_phase_type.RUN,
                                               CommandLogRecord(command_status_type.WARNING,
                                                                message, recommendation))

            # The matching IDs should cause a FAILURE.
            elif pv_IfGeoLayerIDExists.upper() == "FAIL":

                run_read = False
                self.warning_count += 1
                self.logger.error(message)
                self.command_status.add_to_log(command_phase_type.RUN,
                                               CommandLogRecord(command_status_type.FAILURE,
                                                                message, recommendation))

        # Return the Boolean to determine if the read process should be run. If TRUE, all checks passed. If FALSE,
        # one or many checks failed.
        return run_read

    def run_command(self):
        """
        Run the command. Read the layer file from a Shapefile, create a GeoLayer object, and add to the
        GeoProcessor's geolayer list.

        Returns: None.

        Raises:
            RuntimeError if any warnings occurred during run_command method.
        """

        # Obtain the parameter values.
        pv_SpatialDataFile = self.get_parameter_value("SpatialDataFile")
        pv_GeoLayerID = self.get_parameter_value("GeoLayerID", default_value='%f')

        # Convert the SpatialDataFile parameter value relative path to an absolute path and expand for ${Property}
        # syntax
        spatial_data_file_absolute = io_util.verify_path_for_os(
            io_util.to_absolute_path(self.command_processor.get_property('WorkingDir'),
                                     self.command_processor.expand_parameter_value(pv_SpatialDataFile, self)))

        # If the pv_GeoLayerID is a valid %-formatter, assign the pv_GeoLayerID the corresponding value.
        if pv_GeoLayerID in ['%f', '%F', '%E', '%P', '%p']:
            pv_GeoLayerID = io_util.expand_formatter(spatial_data_file_absolute, pv_GeoLayerID)

        # Run the checks on the parameter values. Only continue if the checks passed.
        if self.__should_read_geolayer(spatial_data_file_absolute, pv_GeoLayerID):

            try:

                # Create a QGSVectorLayer object with the SpatialDataFile in Shapefile format
                qgs_vector_layer = qgis_util.read_qgsvectorlayer_from_file(spatial_data_file_absolute)

                # Create a GeoLayer and add it to the geoprocessor's GeoLayers list
                geolayer_obj = GeoLayer(geolayer_id=pv_GeoLayerID,
                                        geolayer_qgs_vector_layer=qgs_vector_layer,
                                        geolayer_source_path=spatial_data_file_absolute)
                self.command_processor.add_geolayer(geolayer_obj)

            # Raise an exception if an unexpected error occurs during the process
            except Exception as e:

                self.warning_count += 1
                message = "Unexpected error reading GeoLayer {} from Shapefile {}.".format(pv_GeoLayerID,
                                                                                           pv_SpatialDataFile)
                recommendation = "Check the log file for details."
                self.logger.exception(message, e)
                self.command_status.add_to_log(command_phase_type.RUN,
                                               CommandLogRecord(command_status_type.FAILURE, message, recommendation))

        # Determine success of command processing. Raise Runtime Error if any errors occurred
        if self.warning_count > 0:
            message = "There were {} warnings proceeding this command.".format(self.warning_count)
            raise RuntimeError(message)

        # Set command status type as SUCCESS if there are no errors.
        else:
            self.command_status.refresh_phase_severity(command_phase_type.RUN, command_status_type.SUCCESS)
