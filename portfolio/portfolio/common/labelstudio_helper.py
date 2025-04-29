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

###########################################################################
# Project Management Functions
###########################################################################

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
    # print(projects)
    print(f"  ID   Title             Tasks    Description")
    print(f"{'=' * 60}")
    for project in projects:
        tasks = label_studio.tasks.list(project=project.id)
        count = sum(1 for _ in tasks)  # This exhausts the iterable

        # print(f"Tasks: {count}")
        print(f" {project.id:3}    {project.title:15}   {count:5}   {project.description}")
        # print(project)
        # log.info(f"Project tasks: {len(project.tasks)}")
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


def list_project_info(project_id:int):
    """
    Get information about a project.

    Args:
        project_id (int): The ID of the project.

    Returns:
        Project: The project object.
    """
    # Get the project
    try:
        project = label_studio.projects.get(project_id)
        log.info(f"Project ID {project_id} Title: {project.title} Description: {project.description}")
    except Exception as e:
        log.error(f"Project {project_id} does not exist.")
        log.error(f"Error: {e}")
        return None
    # return project


###########################################################################
# Task Management Functions
###########################################################################

def delete_all_tasks(project_id:int):
    """
    Delete all tasks in a project.

    Args:
        project_id (int): The ID of the project.

    Returns:
        None
    """
    try:
        # Get the project
        label_studio.tasks.delete_all_tasks(project_id)
        log.info(f"All tasks deleted from project: {project_id}")
    except Exception as e:
        log.error(f"Project {project_id} does not exist.")
        log.error(f"Error: {e}")
        return None

def import_tasks(project_id:int, tasks_file:str):
    """
    Import tasks from a JSON file into a project.

    Args:
        project_id (int): The ID of the project.
        tasks_file (str): The file path of the JSON file containing the tasks.

    Returns:
        None
    """
    log.info(f"Importing tasks from {tasks_file} to project {project_id}")
    try:
        #Read the JSON file
        with open(tasks_file, 'r', encoding='utf-8') as f:
            tasks = f.read()

        log.info(f"Tasks type {type(tasks)}")
        # Get the project
        project = label_studio.projects.get(project_id)
        label_studio.projects.import_tasks(id=project_id, request=tasks)
        log.info(f"Importing tasks to project: {project.title} ID: {project.id}")
    except Exception as e:
        log.error(f"Error: {e}")
        return None