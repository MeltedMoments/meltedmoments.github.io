from dotenv import load_dotenv
import os
from label_studio_sdk import LabelStudio
import portfolio.logging_utils as logging_utils

log = logging_utils.log

# load api key from .env file
load_dotenv()
API_KEY = os.getenv("LABEL_STUDIO_API_KEY")
if API_KEY is None:
    raise ValueError("LABEL_STUDIO_API_KEY environment variable not set. Please set it in your .env file.")

# Connect to Label Studio
label_studio = LabelStudio(api_key=API_KEY)

# Create a project with the specified title and labeling configuration
def create_project(title:str, label_config_file:str):
    """
    Create a new project in Label Studio.

    Args:
        title (str): The title of the project.
        label_config_file (str): The file path of the labelling configuration XML file.

    Returns:
        Project: The created project object.
    """
    # Read the XML file
    with open(label_config_file, 'r', encoding='utf-8') as f:
        label_config = f.read()

    # Create a new project
    project = label_studio.projects.create(
        title=title,
        label_config=label_config,
    )
    return project


def list_projects():
    """
    List all projects in Label Studio.

    Returns:
        list: A list of project objects.
    """
    # List all projects
    projects = label_studio.projects.list()
    print(f"   ID   Title")
    print(f"===================")
    for project in projects:
        print(f" {project.id:3}    {project.title}")
    return projects


def delete_project(project_id:int):
    """
    Delete a project in Label Studio.

    Args:
        project_id (int): The ID of the project to delete.

    Returns:
        None
    """
    # Delete the project
    label_studio.projects.delete(id=project_id)
