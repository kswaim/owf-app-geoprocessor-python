# # - command for single line comment starting with #
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

from geoprocessor.core.CommandPhaseType import CommandPhaseType
from geoprocessor.core.CommandStatusType import CommandStatusType


class ExpectedStatusFailure(AbstractCommand):
    """
    # comment.
    """
    def __init__(self):
        """
        Initialize a new instance of the command.
        """
        # The AbstractCommand.command_string will be used to output the full string:
        super().__init__()
        # Set the command status to success so that testing reports look better
        self.command_status.initialization_status = CommandStatusType.SUCCESS
        self.command_status.discovery_status = CommandStatusType.SUCCESS
        self.command_status.run_status = CommandStatusType.SUCCESS

        # Use hash for the command name for menu and window title
        self.command_name = "#@expectedStatus Failure"
        # Description for menu "Command()... <description>"
        self.command_description = "Used to test commands"

        # Command metadata for command editor display
        self.command_metadata = {}
        self.command_metadata['Description'] = ('Enter one of more comments (leading # will be added automatically '
                                                'if not shown). \n'
                                                'See also the /* and */ commands for multi-line comments, '
                                                'which are useful for commenting out multiple commands.')
        self.command_metadata['EditorType'] = 'InsertLineRulerEditor'

    def initialize_command(self, command_string, processor, full_initialization):
        """
        Initialize the command.  This overrides the AbstractCommand.initialize_command function
        because a comment is treated as simple text.

        Args:
            command_string: Full command string, which may include indentation.
            processor: The GeoProcessor instance, which the command will use to interact with the processor.
            full_initialization: Ignored.  A value of False is passed to AbstractCommand.initialize_command().

        Returns:
            None.
        """

        # Set data in the parent class, but do not attempt to parse the command since unknown syntax
        full_initialization = False
        super(ExpectedStatusFailure, self).initialize_command(command_string, processor, full_initialization)

    def run_command(self):
        """
        Run the command.  Does nothing since comments cause no action.

        Returns:
            None.
        """
        self.command_status.refresh_phase_severity(CommandPhaseType.RUN, CommandStatusType.SUCCESS)
