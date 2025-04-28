from label_studio_sdk import LabelStudio
from label_studio_sdk.label_interface import LabelInterface
from label_studio_sdk.label_interface.create import choices

LABEL_STUDIO_URL = "http://localhost:8080"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6ODA1MzA2MDc2OSwiaWF0IjoxNzQ1ODYwNzY5LCJqdGkiOiIxY2ZhZGFiYWY3ZDE0NDcxOTllZGE1NGI1NTdjNWFjMiIsInVzZXJfaWQiOjF9.VDUStRpZS8xy1oyxr5ViRtivS1AlMe8vmF5qU9mYNcU"


label_studio = LabelStudio(
    api_key=API_KEY,
)


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
