import os
from dataclasses import dataclass
from pathlib import Path

import appdirs
from dotenv import load_dotenv


@dataclass
class ApplicationConfig:
    """
    Configuration parameters for the core platform.
    """

    workspace_db_path: Path

    graph_db_uri: str
    graph_db_user: str
    graph_db_password: str


def load_app_config() -> ApplicationConfig:
    """
    Loads default application config.

    Uses user data directory for workspaces db and environment variables for graph db config.

    :return: Loaded application config.
    :rtype: ApplicationConfig
    """

    load_dotenv()

    return ApplicationConfig(
        workspace_db_path=Path(appdirs.user_data_dir(
            "graph_explorer")) / "workspaces.json",
        graph_db_uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
        graph_db_user=os.getenv('NEO4J_USER', 'neo4j'),
        graph_db_password=os.getenv('NEO4J_PASSWORD', 'neo4j')
    )
