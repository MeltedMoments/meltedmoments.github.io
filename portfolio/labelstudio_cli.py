# label-studio-cli.py
# Command line interface for Label Studio project management.
# This script provides commands to list, create, delete projects and tasks in Label Studio.
# It uses the Label Studio API to perform these operations.
# The script is designed to be run from the command line and uses the Typer library for argument parsing.
# The script is part of the portfolio package and uses the logging_utils module for logging.


import typer
from typing_extensions import Annotated
import portfolio.common.labelstudio_helper as labelstudio
import portfolio.logging_utils as logging_utils

log = logging_utils.log

app = typer.Typer(no_args_is_help=True)
project_app = typer.Typer(no_args_is_help=True, help="Project management commands")
app.add_typer(project_app, name="project")


@project_app.command("list-all")
def list_projects():
    """
    List all projects in Label Studio.
    """
    labelstudio.list_projects()


@project_app.command("create")
def create_project(name: 
                   Annotated[str, typer.Argument(help="The project title", 
                                                 show_default=False)],
                   config: 
                   Annotated[str, typer.Argument(help="The label configuration XML file",
                                                 show_default=False)]):
    """
    Create a new project in Label Studio.
    """
    project = labelstudio.create_project(title=name, label_config_file=config)
    log.info(f"Project created: {project.title} ID: {project.id})")


@project_app.command("delete-project")
def delete_project(project_id: Annotated[int, typer.Argument(help="The ID of the project to delete")]):
    """
    Delete a project in Label Studio.
    """
    labelstudio.delete_project(project_id)
    log.info(f"Project deleted ID: {project_id}")
    labelstudio.list_projects()


@project_app.command("delete-all-tasks")
def delete_all_tasks(project_id: Annotated[int, typer.Argument(help="The ID of the project")]):
    """
    Delete all tasks in a project in Label Studio.
    """
    labelstudio.delete_all_tasks(project_id)


if __name__ == '__main__':
    app()
