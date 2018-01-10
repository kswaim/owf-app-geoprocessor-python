import geoprocessor.util.command as command_util

from geoprocessor.commands.layers.ReadGeoLayerFromShapefile import ReadGeoLayerFromShapefile
from geoprocessor.commands.layers.ReadGeoLayerFromGeoJSON import ReadGeoLayerFromGeoJSON
from geoprocessor.commands.layers.ReadGeoLayersFromFolder import ReadGeoLayersFromFolder
from geoprocessor.commands.layers.ReadGeoLayersFromFGDB import ReadGeoLayersFromFGDB
from geoprocessor.commands.layers.WriteGeoLayerToGeoJSON import WriteGeoLayerToGeoJSON
from geoprocessor.commands.layers.WriteGeoLayerToShapefile import WriteGeoLayerToShapefile

from geoprocessor.commands.logging.Message import Message
from geoprocessor.commands.logging.StartLog import StartLog

from geoprocessor.commands.running.EndFor import EndFor
from geoprocessor.commands.running.EndIf import EndIf
from geoprocessor.commands.running.For import For
from geoprocessor.commands.running.If import If
from geoprocessor.commands.running.SetProperty import SetProperty

from geoprocessor.commands.testing.CompareFiles import CompareFiles
from geoprocessor.commands.testing.CreateRegressionTestCommandFile import CreateRegressionTestCommandFile

from geoprocessor.commands.util.CopyFile import CopyFile
from geoprocessor.commands.util.RemoveFile import RemoveFile
from geoprocessor.commands.util.UnknownCommand import UnknownCommand


class GeoProcessorCommandFactory(object):
    """
    Factory to create command instances by examining command string.
    Only instantiates the command instance but does not parse the command string.
    The command string is parsed within the command class instance."""

    # The dictionary of all available commands, in alphabetical order.
    # key: the name of the command (converted to all UPPERCASE)
    # value: the constructor (__init__) function to create an instance of the command
    # This dictionary serves two purposes:
    # 1) It provides a registry of all commands known to the geoprocessor (via this factory class)
    # 2) It provides the list of constructor functions to call, to simplify logic
    registered_commands = {
        "COMPAREFILES": CompareFiles(),
        "COPYFILE": CopyFile(),
        "CREATEREGRESSIONTESTCOMMANDFILE": CreateRegressionTestCommandFile(),
        "ENDFOR": EndFor(),
        "ENDIF": EndIf(),
        "FOR": For(),
        "IF": If(),
        "MESSAGE": Message(),
        "REMOVEFILE": RemoveFile(),
        "SETPROPERTY": SetProperty(),
        "STARTLOG": StartLog()
    }

    def __init__(self):
        pass

    def __is_command_valid(self, command_name):
        """
        Checks if the command is a valid registered command by examining the command name.
        A valid command can be further processed to create a command instance.

        Args:
            command_name: the name of the command

        Returns:
            True if the command is registered as recognized, False if not.
        """

        registered_command_names = list(self.registered_commands.keys())
        if command_name.upper() in registered_command_names:
            return True
        else:
            return False

    def new_command(self, command_string, create_unknown_command_if_not_recognized=True):
        """
        Creates the object of a command class called from a command line of the command file.

        Args:
            command_string (str): the command string entered by the user in the command file
            create_unknown_command_if_not_recognized (bool) If TRUE, create an UnknownCommand when the input
            command is not recognized, if FALSE, throw an error.

        Returns:
            A command instance of class type that matches the command name.
            The command is not parsed.

        Raises:
            ValueError if the command is not recognized and create_unknown_command_if_not_recognized=False.
        """

        # Get command name from the first part of the command.
        command_string_trimmed = command_string.strip()
        paren_pos = command_string_trimmed.find('(')

        # Blank line so insert a BlankCommand command.
        if len(command_string_trimmed) == 0:
            # return BlankCommand.BlankCommand()
            pass

        # Comment line.
        # elif command_string_trimmed[:1] == '#':
            # return CommentCommand.CommentCommand()
            pass

        # The symbol '(' was found.
        # Assume command of syntax CommandName(Param1="...",Param2="...").
        elif paren_pos != -1:

            # Get command name from command string, command name is before the first open parenthesis.
            command_name = command_util.parse_command_name_from_command_string(command_string_trimmed)

            # Initialize the command class object if it is a valid command.
            command_name_upper = command_name.upper()
            init_from_dictionary_constructor = False
            if init_from_dictionary_constructor:
                # TODO smalers 2017-12-28 Figure out if the dictionary constructor can be called.
                # The following is a clever way to initialize instances using a constructor function
                # from the command dictionary.
                # However, it does not seem to work.  For example, if multiple Message commands
                # are initialized, the AbstractCommand.command_parameters dictionary for all Message
                # command instances will have the values corresponding to the last Message command.
                if self.__is_command_valid(command_name):
                    command = self.registered_commands[command_name_upper]
                    return command
            else:
                # Constructing the following way always seems to work properly
                if command_name_upper == "COMPAREFILES":
                    return CompareFiles()
                elif command_name_upper == "COPYFILE":
                    return CopyFile()
                elif command_name_upper == "READGEOLAYERSFROMFOLDER":
                    return ReadGeoLayersFromFolder()
                elif command_name_upper == "READGEOLAYERFROMGEOJSON":
                    return ReadGeoLayerFromGeoJSON()
                elif command_name_upper == "READGEOLAYERFROMSHAPEFILE":
                    return ReadGeoLayerFromShapefile()
                elif command_name_upper == "READGEOLAYERSFROMFGDB":
                    return ReadGeoLayersFromFGDB()
                elif command_name_upper == "CREATEREGRESSIONTESTCOMMANDFILE":
                    return CreateRegressionTestCommandFile()
                elif command_name_upper == "ENDFOR":
                    return EndFor()
                elif command_name_upper == "ENDIF":
                    return EndIf()
                elif command_name_upper == "FOR":
                    return For()
                elif command_name_upper == "IF":
                    return If()
                elif command_name_upper == "MESSAGE":
                    return Message()
                elif command_name_upper == "REMOVEFILE":
                    return RemoveFile()
                elif command_name_upper == "SETPROPERTY":
                    return SetProperty()
                elif command_name_upper == "STARTLOG":
                    return StartLog()
                elif command_name_upper == "WRITEGEOLAYERTOGEOJSON":
                    return WriteGeoLayerToGeoJSON()
                elif command_name_upper == "WRITEGEOLAYERTOSHAPEFILE":
                    return WriteGeoLayerToShapefile()

            # If here the command name was not matched.
            # Don't know the command so create an UnknownCommand or throw an exception.
            if create_unknown_command_if_not_recognized:
                print("Command line is unknown command. Adding UnknownCommand: " + command_string_trimmed)
                return UnknownCommand()
            else:
                print("Command line is unknown syntax.")
                raise ValueError('Unrecognized command "' + command_string + '"')

        # The syntax is not recognized so create an UnknownCommand or throw an exception.
        else:
            if create_unknown_command_if_not_recognized:
                print("Command line is unknown syntax. Adding UnknownCommand: " + command_string_trimmed)
                return UnknownCommand()
            else:
                print("Command line is unknown syntax.")
                raise ValueError('Unrecognized command "' + command_string + '"')
