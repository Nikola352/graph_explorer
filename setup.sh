#!/bin/bash

# External requirements (for app and plugins)
pip install -r ./requirements.txt

# Core platform (mandatory)
pip install ./api
pip install ./core

# Plugins (optional)
pip install ./plugins/visualizer/simple_visualizer
pip install ./plugins/visualizer/block_visualizer
pip install ./plugins/datasource/rdf_datasource
pip install ./plugins/datasource/spotify_datasource
pip install ./plugins/datasource/postgresql_datasource

# Default environment setup
cp ./core/src/core/.example.env ./core/src/core/.env

# Check for port argument and run server
if [ "$#" -ge 1 ]; then
    if [[ $1 =~ ^[0-9]+$ ]]; then
        python ./graph_explorer/manage.py runserver 0.0.0.0:$1
    else
        echo "Warning: First argument should be a port number. Using default port (8000)."
        python ./graph_explorer/manage.py runserver 0.0.0.0:8000
    fi
else
    python ./graph_explorer/manage.py runserver 0.0.0.0:8000  # Default port 8000
fi
