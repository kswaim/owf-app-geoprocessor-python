@echo off
rem gp2.bat
rem
rem Windows batch file to run the Open Water Foundation GeoProcessor application
rem - This script is for Python2/QGIS2
rem - This script should work on a normal Windows 7/10 computer.
rem - The geoprocessor package must be installed in a normal location, such as
rem   Python site-packages folder.
rem - This script should be installed in the QGIS bin folder or other location
rem   that is in the PATH or otherwise can be executed.

rem Set the Python environment to find the correct run-time libraries
rem - The GEOPROCESSOR_ENV_SETUP environment variable is set to YES
rem   to indicate that setup has been done.
rem - This causes setup to occur only once if rerunning this batch file.

if "%GEOPROCESSOR_ENV_SETUP%"=="YES" GOTO run
rem ===================================================================================
rem ========== START COPY FROM run*pycharm*.bat SCRIPT WITHOUT PYCHARM ================
rem
echo Start defining QGIS/OWF GeoProcessor environment...

rem Where QGIS is installed
rem - TODO Need to figure out what to do if not in this location, multiple QGIS installs, etc.
SET QGIS_INSTALL_HOME=C:\OSGeo4W64
if not exist %QGIS_INSTALL_HOME% GOTO noqgis

SET OSGEO4W_ROOT=%QGIS_INSTALL_HOME%
rem Set the QGIS environment by calling the setup script that is distributed with QGIS
rem - the following will reset the PATH and then add QGIS folders to path
rem - therefore other programs that were found before may not be found
CALL %OSGEO4W_ROOT%\bin\o4w_env.bat

rem Name of QGIS version to run (**for running OWF GeoProcessor don't run QGIS
rem rem but need to use correct QGIS components**).
rem rem Run the latest release of the OSGeo4W QGIS by setting value to `qgis`.
rem rem Run the long term release of the OSGeo4W QGIS by setting value to `qgis-ltr`.
rem rem The QGIS OSGeo4W64 installer as of February 23, 2018 installs QGIS version 3 as `qgis`, which still has issues.
rem rem Therefore, this script defaults to using the long-term-release version if it exists.
rem rem If someone is still using an older version (pre version 3), then gp-ltr.bat will not be available,
rem rem and `qgis` should be used.
rem rem The main issue will be if someone installs the new version (post February 23, 2018) and does not do the
rem rem advanced install to select the LTR for install, then they only get QGIS version 3,
rem rem which is not currently available.
rem rem This batch file could be updated to print an intelligent message for that case.
rem rem Old default:
rem rem SET QGISNAME=qgis
rem rem New default:
rem rem SET QGISNAME=qgis-ltr
set _qgisLTR=%OSGEO4W_ROOT%\bin\qgis-ltr.bat

rem Run LTR version if it is available.
if exist %_qgisLtr% set QGISNAME=qgis-ltr
rem rem Else run base/latest version if it is available.
if not exist %_qgisLtr% set QGISNAME=qgis
echo QGISNAME is %QGISNAME%

rem Absolute path to QGIS software, used to find version-specific executables.
SET QGIS=%OSGEO4W_ROOT%\apps\%QGISNAME%
rem Not sure what the following is used for but include in case PyCharm or QGIS uses
SET QGIS_PREFIX_PATH=%QGIS%

rem Add QGIS to the PATH environmental variable so that all QGIS, GDAL, OGR, etc. programs are found
SET PATH=%PATH%;%QGIS%\bin

rem Add pyQGIS libraries to the PYTHONPATH so that they are found by Python
rem - Currently only QGIS 2.X with Python 2.X is supported
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\%QGISNAME%\python
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\%QGISNAME%\python\plugins
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\Python27\Lib\site-packages

rem ========== END COPY FROM run*pycharm*.bat SCRIPT ==================================

rem Indicate that the setup has been completed
rem - this will ensure that the script when run again does not repeat setup
rem   and keep appending to environment variables
set GEOPROCESSOR_ENV_SETUP=YES
echo ...done defining QGIS/OWF GeoProcessor environment
rem ========== START GeoProcessor Setup Steps to be done once =========================
rem QGIS Python
set QGIS_PYTHON_EXE=%OSGEO4W_ROOT%\bin\python.exe

rem Normal Python (should be Python 2.7)
set PYTHON_EXE=python

rem  Set the PYTHONPATH to include the geoprocessor module
rem  - Folder for libraries must contain "geoprocessor" since modules being searched for will start with that.
rem  - The following commented examples are for development environment but should not be needed
rem    if the geoprocessor has been installed in site-packages.
rem GEOPROCESSOR_HOME="/cygdrive/C/Users/${USERNAME}/owf-dev/GeoProcessor/git-repos/owf-app-geoprocessor-python/geoprocessor"
rem set GEOPROCESSOR_HOME=C:\Users\%USERNAME%\owf-dev\GeoProcessor\git-repos\owf-app-geoprocessor-python
rem set PYTHONPATH=%GEOPROCESSOR_HOME%;%PYTHONPATH%

echo PYTHONPATH=%PYTHONPATH%

rem ========== END GeoProcessor Setup Steps to be done once ===========================
rem ========== END setup steps to be done once ========================================
rem ===================================================================================

rem Below here assumes that the above environment has been setup by running in the window previously

:run

rem  Run Python on the code
rem  - must use Python 2.7 compatible with QGIS

echo Running OWF GeoProcessor application gp, for legacy Python2/QGIS2...

rem Run QGIS Python with the geoprocessor module found using PYTHONPATH set above.
rem - Must use Python 2.7 compatible with QGIS
rem - The --version run works (use for testing basic setup)
rem - Pass command line arguments that were passed tot he gp.bat file.
rem %QGIS_PYTHON_EXE% --version
%QGIS_PYTHON_EXE% -m geoprocessor.app.gp %*

rem Normal (non-QGIS) Python
rem - this is not used and can likely be removed once QGIS Python use is confirmed.
rem %PYTHON_EXE% -m geoprocessor.app.gp %*

rem Exit with the error level of the Python command
exit /b %ERRORLEVEL%

:noqgis
rem QGIS install folder was not found
echo QGIS standard installation folder was not found:  %QGIS_INSTALL_HOME%
exit /b 1
