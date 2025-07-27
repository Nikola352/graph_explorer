# Graph Explorer

A modular graph visualization tool built with Django and D3.js that enables exploration of complex data relationships through interactive graph visualizations.

## Overview

Graph Explorer uses a plugin-based architecture to support multiple data sources and visualization methods. The application loads graph data from various sources, stores it in Neo4j, and renders interactive visualizations using D3.js.

### Key Features

- **Workspace Management**: Create and manage multiple workspaces, each with its own graph data and configuration
- **Plugin-Based Data Sources**: Extensible system for connecting to various data sources (Spotify, RDF, PostgreSQL, etc.)
- **Multiple Visualization Modes**: Switch between different visualizers and view modes in real-time
- **Interactive Graph Exploration**: Pan, zoom, drag nodes, and explore relationships with mouse controls
- **Advanced Search & Filtering**: Search nodes by any field and apply complex filters to focus on specific data
- **Real-Time Data Refresh**: Reload graph data from sources with a single click
- **Built-in CLI**: Command-line interface for programmatic graph manipulation and automation
- **Responsive UI**: Modern web interface with multiple view modes for different exploration needs

### Architecture

The project is organized into several modular components:

- **`api`** - Core data models and plugin interfaces (pip package)
- **`core`** - Application logic and graph processing (pip package)  
- **`graph_explorer`** - Django web application that serves the UI
- **`plugins`** - Extensible data source and visualizer implementations (pip packages)

All components communicate through the `api` package, which defines the standard interfaces and data models.

### Built-in Plugins

**Data Sources:**
- **Spotify** - Builds graphs of artists and their related/similar artists
- **RDF** - Imports graphs from Turtle RDF format
- **PostgreSQL** - Creates graphs from database schemas with tables as nodes and relationships as edges

**Visualizers:**
- **Simple Visualizer** - Basic node-link diagram, displaying minimal node information
- **Block Visualizer** - Displays all data for each node, allowing full insight into all the details

## Requirements

- Python 3.10+
- Neo4j database instance
- Docker and Docker Compose (for containerized setup)

## Quick Start

### Option 1: Docker Compose (Recommended)

The fastest way to get started:

```bash
docker compose up -d --build
```

This will:
- Start a Neo4j container with default credentials
- Build and run the Django application
- Make the app available at `http://localhost:8000`

### Option 2: Quick Setup Script

For local development without Docker:

0. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

1. **Start Neo4j**:
    You can use the provided docker-compose or set the connection parameters as environtment variables.
   ```bash
   cd neo4j
   docker compose up -d
   ```

2. **Run the setup script**:
   ```bash
   # Linux/macOS
   ./setup.sh

   # Windows
   setup.bat

   # Or specify a custom port
   ./setup.sh 3000
   ```

The setup script will:
- Install all Python dependencies
- Install core packages and plugins
- Set up default environment configuration
- Start the Django development server on [localhost:8000](http://localhost:8000)

### Option 3: Manual Development Setup

For full development control:

0. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install core packages**:
   ```bash
   pip install -e ./api
   pip install -e ./core
   ```

3. **Install plugins** (optional):
   ```bash
   # Visualizers
   pip install -e ./plugins/visualizer/simple_visualizer
   pip install -e ./plugins/visualizer/block_visualizer
   
   # Data sources
   pip install -e ./plugins/datasource/rdf_datasource
   pip install -e ./plugins/datasource/spotify_datasource
   pip install -e ./plugins/datasource/postgresql_datasource
   ```

4. **Configure environment**:
   ```bash
   cp ./core/src/core/.example.env ./core/src/core/.env
   ```

5. **Start Neo4j and run the application**:
   ```bash
   cd neo4j && docker compose up -d
   cd ../graph_explorer
   python manage.py runserver
   ```

## Configuration

### Environment Variables

Configure the application by editing `/core/src/core/.env`:

```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

### Neo4j Setup

**Default credentials:** `neo4j/password`

The included Neo4j configuration enables APOC plugins for advanced graph operations. You can access the Neo4j browser at `http://localhost:7474`.


## Usage

### Getting Started

1. **Access the Application**: Navigate to [`http://localhost:8000`](http://localhost:8000)
2. **Default Workspace**: The application starts with a default workspace that you can modify or use as-is
3. **Create New Workspace**: Optionally create additional workspaces for different projects or data sets

### Workspace Configuration

#### Data Source Setup
1. **Select Data Source**: Choose from installed data source plugins (Spotify, RDF, PostgreSQL, etc.)
2. **Configure Parameters**: Set required parameters for your chosen data source:
   - **Spotify**: Artist names or IDs to explore
   - **RDF**: Upload Turtle files or provide RDF endpoints
   - **PostgreSQL**: Database connection details and schema preferences
3. **Load Data**: Click the save button to import graph data from your configured source
4. **Refresh Data**: Use the refresh button to reload the latest data from your source at any time

#### Visualization Settings
- **Select Visualizer**: Choose from available visualizer plugins using the dropdown menu
- **Switch Anytime**: Visualizers can be changed without reloading data, allowing quick comparison of different rendering styles

### Interface Overview

#### View Modes
The application provides three distinct view modes for exploring your graph:

1. **Main View**: 
   - Primary interactive graph visualization
   - Full-featured node manipulation and exploration
   - Pan, zoom, and drag functionality
   - Hover nodes for detailed information

2. **Bird's Eye View**:
   - Miniature overview of the entire graph
   - Navigate large graphs efficiently
   - Quick jumping to different graph regions
   - Visual indicator of current viewport in main view

3. **Tree View**:
   - Hierarchical, expandable representation
   - Similar to file explorers (like VS Code)
   - Collapse/expand node branches
   - Ideal for exploring nested relationships and hierarchies

#### Search and Filtering
- **Universal Search**: Search for nodes by any field or property
- **Advanced Filtering**: Apply filters based on:
  - Field name (any node property)
  - Operators: `eq` (equal), `neq` (not equal), `gt` (greater than), `gte` (≥), `lt` (less than), `lte` (≤)
  - Custom values for precise data exploration
- **Real-time Results**: Filters and searches update the visualization immediately

### Command Line Interface (CLI)

Graph Explorer includes a powerful CLI for programmatic graph manipulation and automation.

#### Accessing the CLI
- **In-App Console**: Click the console button in the web interface to open an embedded CLI
- **Django Management**: Use Django's management command system:
  ```bash
  python manage.py graph_cli <command> --workspace <workspace_id> [options]
  ```

#### CLI Commands

**Node Management:**
```bash
# Create a new node
create-node --id <node_id> [--data '{json_properties}']
# Example: create-node --id user_123 --data '{"name": "John Doe", "age": 30}'

# Update existing node properties
update-node --id <node_id> [--data '{json_properties}']
# Example: update-node --id user_123 --data '{"age": 31, "city": "New York"}'

# Remove a node and all its connections
delete-node --id <node_id>
# Example: delete-node --id user_123
```

**Edge Management:**
```bash
# Create relationship between nodes
create-edge --src <source_id> --tgt <target_id> [--data '{json_properties}']
# Example: create-edge --src user_123 --tgt company_456 --data '{"role": "employee", "since": "2020"}'

# Update edge properties
update-edge --src <source_id> --tgt <target_id> [--data '{json_properties}']
# Example: update-edge --src user_123 --tgt company_456 --data '{"role": "manager"}'

# Remove relationship
delete-edge --src <source_id> --tgt <target_id>
# Example: delete-edge --src user_123 --tgt company_456
```

**Data Exploration:**
```bash
# Search nodes by text content
search --query <search_term>
# Example: search --query "John"  # Finds nodes containing "John" in any field

# Filter nodes by specific criteria
filter --field <property_name> --operator <op> --value <filter_value>
# Examples:
filter --field age --operator gt --value 25        # Age greater than 25
filter --field name --operator eq --value "John"   # Name exactly equals "John"
filter --field city --operator neq --value "NYC"   # City not equal to "NYC"
```

**Graph Management:**
```bash
# Remove all nodes and edges from current workspace
clear-graph
```

#### CLI Usage Examples

**Web Console Example:**
```bash
# In the web interface console:
create-node --id city_001 --data '{"name": "Novi Sad", "country": "Serbia", "population": 380000}'
create-node --id city_002 --data '{"name": "Belgrade", "country": "Serbia", "population": 1700000}'
create-edge --src city_001 --tgt city_002 --data '{"relationship": "nearby", "distance_km": 80}'
```

**Django Management Example:**
```bash
# From command line:
python manage.py graph_cli create-node --workspace 1 --id my_node --data '{"city": "Novi Sad"}'
python manage.py graph_cli filter --workspace 1 --field population --operator gte --value 500000
```

### Interactive Features

- **Node Interaction**: Click nodes to view properties, drag to reposition
- **Dynamic Updates**: All changes (via UI or CLI) reflect immediately in visualizations
- **Multi-Workspace**: Switch between workspaces without losing data or configuration
- **Multi-session access**: Workspace configurations and graph data are persisted for later use

## Creating Custom Plugins

### Data Source Plugin

Create a new data source by implementing the `DataSourcePlugin` interface:

```python
from api.components.datasource import DataSourcePlugin, DataSourceConfigParam
from api.models.graph import Graph

class MyDataSourcePlugin(DataSourcePlugin):
    def name(self) -> str:
        return "My Data Source"
    
    def identifier(self) -> str:
        return "my_datasource"
    
    def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
        return [
            DataSourceConfigParam(
                name="api_key",
                value_type=DataSourceConfigParam.Type.PASSWORD,
                display_name="API Key",
                required=True
            ),
            DataSourceConfigParam(
                name="endpoint",
                value_type=DataSourceConfigParam.Type.URL,
                display_name="API Endpoint",
                default="https://api.example.com"
            )
        ]
    
    def load(self, **kwargs) -> Graph:
        # Your data loading logic here
        # Return a Graph object
        pass
```

### Visualizer Plugin

Create custom visualizations by implementing the `VisualizerPlugin` interface:

```python
from api.components.visualizer import VisualizerPlugin
from api.models.graph import Graph

class MyVisualizerPlugin(VisualizerPlugin):
    def name(self) -> str:
        return "My Visualizer"
    
    def identifier(self) -> str:
        return "my_visualizer"
    
    def display(self, graph: Graph, **kwargs) -> str:
        # Generate HTML string with D3.js visualization
        # Follow the integration rules for interactivity:
        # - Use enabled="true", drag="true", tooltip="true", zoom="true", click-focus="true"
        # - Nodes: <g class='node'>
        # - Links: <path class='link'>
        return html_string
```

### Plugin Integration

1. **Create a pyproject.toml** for your plugin:
   ```toml
    [build-system]
    requires = ["setuptools >= 61.0"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "my_data_source"
    version = "0.1"
    dependencies = [
        "api==0.1"
    ]
    requires-python = ">= 3.10"

    [tool.setuptools.packages.find]
    where = ["src"]

    [project.entry-points."graph_explorer.datasources"]
    my_data_source = "my_data_source.implementation:MyDataSourcePlugin"
   ```

2. **Install your plugin**:
   ```bash
   pip install -e ./path/to/your/plugin
   ```

3. **Restart the application** to load the new plugin.

## Development

### Project Structure

```
graph_explorer/
├── api/                    # Core interfaces and models
├── core/                   # Application logic
├── graph_explorer/         # Django web application
├── plugins/
│   ├── datasource/         # Data source plugins
│   └── visualizer/         # Visualizer plugins
├── neo4j/                  # Neo4j Docker setup
├── requirements.txt        # Python dependencies
├── setup.sh               # Quick setup script
├── setup.bat              # Windows setup script
└── docker-compose.yml     # Full application stack
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes following the plugin interfaces
4. Test with the provided setup methods
5. Submit a pull request

## Troubleshooting

**Neo4j connection issues:**
- Ensure Neo4j is running: `docker ps`
- Check connection parameters in `.env`
- Verify Neo4j health: `http://localhost:7474`

**Plugin not loading:**
- Verify plugin installation: `pip list`
- Check entry points in `pyptoject.toml`
- Restart the Django application

**Port conflicts:**
- Neo4j: Change ports in `neo4j/docker-compose.yml`
- Django: Use `./setup.sh <port>` or modify `manage.py runserver`

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Nikola352/graph_explorer/blob/main/LICENSE) file for details.

## Screenshots

![Simple Visualizer](https://raw.githubusercontent.com/Nikola352/graph_explorer/assets/screenshots/ss1.png)
![Block Visualizer](https://raw.githubusercontent.com/Nikola352/graph_explorer/assets/screenshots/ss2.png)
![Data Source Configuration](https://raw.githubusercontent.com/Nikola352/graph_explorer/assets/screenshots/ss3.png)
![CLI](https://raw.githubusercontent.com/Nikola352/graph_explorer/assets/screenshots/ss4.png)
