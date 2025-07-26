@echo off

:: External requirements (for app and plugins)
pip install -r .\requirements.txt

:: Core platform (mandatory)
pip install .\api
pip install .\core

:: Plugins (optional)
pip install .\plugins\visualizer\simple_visualizer
pip install .\plugins\visualizer\block_visualizer
pip install .\plugins\datasource\rdf_datasource
pip install .\plugins\datasource\spotify_datasource
pip install .\plugins\datasource\postgresql_datasource

:: Default environment setup
copy .\core\src\core\.example.env .\core\src\core\.env

:: Check for port argument and run server
if "%~1"=="" (
    python .\graph_explorer\manage.py runserver
) else (
    echo %~1|findstr /r "^[0-9][0-9]*$">nul
    if errorlevel 1 (
        echo Warning: First argument should be a port number. Using default port.
        python .\graph_explorer\manage.py runserver
    ) else (
        python .\graph_explorer\manage.py runserver %~1
    )
)