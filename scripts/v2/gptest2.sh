#!/bin/sh

# Script to run the Open Water Foundation GeoProcessor application
# - This is for Python2/QGIS2
# - This script should eventually work for Cygwin, Git Bash (MinGW), and Linux
# - This requires a Python 2.7 interpreter but does not require QGIS.
# - The geoprocessor package is expected to be found in the chosen Python 2.7

# Might need to handle different operating systems
# cygwinUname=`uname -a | grep -i cygwin`

# Save all the arguments so they can be used as a global argument in the function
# - might be a way to pass to the runProcessor function
allArgs=$@

# Function to run Python version 2.7
runProcessor () {
	# python or python2 can be used for Python 2.
        # Version is printed to stderr or stdout so a bit tricker to redirect
	pythonExe="python2"
        # First try the general Python launcher
        pythonVersion=`${pythonExe} --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1`
        if [ "${pythonVersion}" = "2" ]
		then
		# Python 2 version was found
		# - run geoprocessor/app/gp.py
		# - Expect that the geoprocessor folder is found under site-packages
		#export PYTHONPATH="$PYTHONPATH:$OSGEO4W_ROOT/apps/qgis/python"
		#export PYTHONPATH="$PYTHONPATH:$OSGEO4W_ROOT/apps/qgis/python/plugins"
		#export PYTHONPATH="$PYTHONPATH:$OSGEO4W_ROOT/apps/Python27/Lib/site-packages"
		echo ""
		echo "Running the geoprocessor for legacy Python2/QGIS2..."
		${pythonExe} -m geoprocessor.app.gp ${allArgs}
	else
		# Python 2 version was not found
                echo ""
                echo "Cannot determine available python 2 available to run processor."
                exit 1
        fi
}

# Main entry point into script

# Run the processor
runProcessor
exit 0
