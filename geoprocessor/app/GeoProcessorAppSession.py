# GeoProcessorAppSession - class to manage GeoProcessor session
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

import getpass
import logging
import os


class GeoProcessorAppSession(object):
    """
    Manage the session, such as saving the application state.
    This is a port of the Java TSToolSession class.

    The $HOME/.owf-gp/command-file-history.txt file contains a list of recently opened or saved command files,
    with format shown below (paths will be consistent with the operating system, in the case below for Cygwin):

    # GeoProcessor command file history, most recent at top, shared between GeoProcessor instances
    /cygdrive/c/Users/sam/owf-dev/GeoProcessor/git-repos/owf-app-geoprocessor-python-test/test/commands/RunProgram/test-RunProgram-echo-env.gp
    /cygdrive/c/Users/sam/owf-dev/GeoProcessor/git-repos/owf-app-geoprocessor-python-test/test/commands/RunProgram/test-wlgetquery-datadisp.gp

    And on Windows 10:

    # GeoProcessor command file history, most recent at top, shared between GeoProcessor instances
    C:/Users/sam/owf-dev/GeoProcessor/git-repos/owf-app-geoprocessor-python-test/test/commands/0-Warning/test-warning-and-failure.gp
    C:/Users/sam/owf-dev/GeoProcessor/git-repos/owf-app-geoprocessor-python-test/test/commands/MergeGeoLayers/test-MergeGeoLayers-Lines-AttributeMap.gp
    """
    def __init__(self):
        pass

    def create_log_folder(self):
        """
        Create the folder where the application log file lives.

        Returns:
            True if the creation is successful, False if not.
        """
        log_folder = self.get_log_folder()
        # Do not allow log file to be created under Linux root but allow the application to run
        if log_folder == "/":
            return False

        if not os.path.exists(log_folder):
            try:
                os.makedirs(log_folder)
            except OSError as e:
                return False
        else:
            # Make sure it is writeable
            if not os.access(log_folder, os.W_OK):
                return False
        return True

    def get_app_folder(self):
        """
        Get the name of the application folder for the user.

        Returns:
            The name of the folder for user geoprocessor application files.
        """
        app_folder = os.path.join(self.get_user_folder(), ".owf-gp")
        logging.info('Application folder is "' + app_folder + '"')
        return app_folder

    def get_history_file(self):
        """
        Get the name of the command history file for the user.

        Returns:
            The name of the history file.
        """
        history_file = os.path.join(self.get_app_folder(), "command-file-history.txt")
        logging.info('Command file history is"' + history_file + '"')
        return history_file

    def get_log_file(self):
        """
        Get the name of the log file for the user.

        Returns:
            The name of the log file.
        """
        log_file = os.path.join(self.get_log_folder(), "gp_" + getpass.getuser() + ".log")
        logging.info('Log file is "' + log_file + '"')
        return log_file

    def get_log_folder(self):
        """
        Get the name of the log file folder for the user.
        
        Returns:
            The name of the folder for user log files.
        """
        log_folder = os.path.join(self.get_app_folder(), "log")
        logging.info('Log folder is "' + log_folder + '"')
        return log_folder

    def get_user_folder(self):
        """
        Return the name of the user folder for the operating system, for example:
            Windows:  C:\\Users\\UserName\\.owfgp
            Linux: /home/UserName/.owfgp

        Returns:
            The name of the user folder.
        """
        user_folder = os.path.expanduser("~")
        logging.info('User folder is "' + user_folder + '"')
        return user_folder

    def push_history(self, command_file):
        """
        Push a new command file onto history. This reads the history, updates it, and writes it.
        The new file is added at the top, corresponding to the most recent file.
        This is done because if multiple GeoProcessor sessions are running, they will share history.

        Args:
            command_file:
                 Full path to command file that has been opened.

        Returns:
            None
        """

        # Read the history file from the .geoprocessor file
        history = self.read_history()
        # Add in the first position so it will show up first in the File... Open... menu
        history.insert(0, command_file)

        # print("Command File: " + command_file)

        # Process from back so that old duplicates are removed and recent access is always at the top of the list
        # print("History before loop: " +  str(history))
        max_files = 100
        for i in reversed(list(range(0, len(history)))):
            if i >= 1:
                old = history[i]
                if i >= max_files:
                    # Trim the history to the maximum
                    del history[i]
                elif old == command_file or old == '' or old.startswith("#"):
                    # Ignore comments, blank lines and duplicate to most recent access
                    del history[i]
                    i -= 1
        self.write_history(history)

    def read_history(self):
        """
        Read the history of command files that have been opened.

        Returns:
            The list of command files recently opened, newest first, with comments removed.
        """

        # history_list = list(history.splitlines())

        # for line in history_list:
        #    if(line.startswith("#")):
        #        history_list.remove(line)

        # print(history_list)

        try:
            with open(self.get_history_file()) as f:
                history = f.read().splitlines()
                for line in history:
                    if line.startswith("#"):
                        # Remove comments
                        history.remove(line)
                return history
        except Exception as e:
            # For now just swallow exception - may be because the history folder does not exist
            # message = 'Exception opening command file history'
            # print(message)
            # logging.exception(message, e, exc_info=True)
            return []

    def write_history(self, history_list):
        """
        Write the history of command files that have been opened

        :param history_list: a list of strings representing the history of command files
        """

        # Don't allow files to be created under root on Linux(?)

        # History being written (?)

        string_builder =\
            "# GeoProcessor command file history, most recent at top, shared between GeoProcessor instances\n"

        try:
            for s in history_list:
                string_builder += s + "\n"
            # Create the history folder if necessary
            f = open(self.get_history_file(), "w")
            folder = os.path.abspath(os.path.join(self.get_history_file(), '..'))
            if not os.path.exists(folder):
                if not os.makedirs(folder):
                    # Unable to make folder
                    return
            try:
                f.write(string_builder)
            except Exception as e:
                # Absorb exception for now
                pass
        except Exception as e:
            message = 'Exception writing command file history'
            print(message)
            logging.exception(message, e, exc_info=True)
