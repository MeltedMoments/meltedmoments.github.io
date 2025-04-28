import argparse
import portfolio.logging_utils as logging_utils
from portfolio.common.labelstudio_helper import list_projects, create_project, delete_project
# import logging

log = logging_utils.log


def parse_args():
    parser = argparse.ArgumentParser(description="Manage Label Studio projects.")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command')

    # Create project
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', help='The name of the new project')
    create_parser.add_argument('config', help='File path to the label configuration XML file')

    # Delete project
    delete_parser = subparsers.add_parser('delete', help='Delete an existing project')
    delete_parser.add_argument('project_id', help='The ID of the project to delete', type=int)

    # List projects
    subparsers.add_parser('list', help='List all projects')

    args = parser.parse_args()

    return args

cmdline_args = parse_args()


def main():

    # Handle different subcommands
    if cmdline_args.command == 'create':
        project = create_project(title=cmdline_args.name, 
                                label_config_file=cmdline_args.config)
        # log.info(f"Project type: {type(project)}")
        log.info(f"Project created: {project.title} ID: {project.id})")
    elif cmdline_args.command == 'list':
        list_projects()
    elif cmdline_args.command == 'delete':
        delete_project(cmdline_args.project_id)
        log.info(f"Project deleted ID: {cmdline_args.project_id}")
        list_projects()
    # elif args.command == 'export':
    #     annotations = export_annotations(args.project_id)
    #     print(f"Annotations exported: {annotations}")

if __name__ == '__main__':
    main()
