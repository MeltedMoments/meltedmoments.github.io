import argparse
import portfolio.logging_utils as logging_utils
import portfolio.common.labelstudio_helper as labelstudio
# from portfolio.common.labelstudio_helper import list_projects, create_project, delete_project
# import logging

log = logging_utils.log


def parse_args():
    parser = argparse.ArgumentParser(description="Manage Label Studio projects.")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command')

    # Create project
    create_parser = subparsers.add_parser('create-project', help='Create a new project')
    create_parser.add_argument('name', help='The name of the new project')
    create_parser.add_argument('config', help='File path to the label configuration XML file')

    # Delete project
    delete_parser = subparsers.add_parser('delete-project', help='Delete an existing project')
    delete_parser.add_argument('project_id', help='The ID of the project to delete', type=int)

    # List projects
    subparsers.add_parser('list', help='List all projects')

    # Delete all tasks in a project
    delete_all_tasks_parser = subparsers.add_parser('delete-all-tasks', help='Delete all tasks in a project')
    delete_all_tasks_parser.add_argument('project_id', help='The ID of the project', type=int)

    # Import tasks into a project
    # import_tasks_parser = subparsers.add_parser('import-tasks', help='Import tasks into a project')
    # import_tasks_parser.add_argument('project_id', help='The ID of the project', type=int)
    # import_tasks_parser.add_argument('json_file', help='The JSON file to import', type=str)

    # Project info
    project_info_parser = subparsers.add_parser('project-info', help='Infomation about a project')
    project_info_parser.add_argument('project_id', help='The ID of the project', type=int)

    args = parser.parse_args()

    return args

cmdline_args = parse_args()


def main():

    # Handle different subcommands
    if cmdline_args.command == 'create-project':
        project = labelstudio.create_project(title=cmdline_args.name, 
                                label_config_file=cmdline_args.config)
        # log.info(f"Project type: {type(project)}")
        log.info(f"Project created: {project.title} ID: {project.id})")
    elif cmdline_args.command == 'list':
        labelstudio.list_projects()
    elif cmdline_args.command == 'delete-project':
        labelstudio.delete_project(cmdline_args.project_id)
        log.info(f"Project deleted ID: {cmdline_args.project_id}")
        labelstudio.list_projects()
    elif cmdline_args.command == 'delete-all-tasks':
        labelstudio.delete_all_tasks(cmdline_args.project_id)
    elif cmdline_args.command == 'import-tasks':
        labelstudio.import_tasks(cmdline_args.project_id, cmdline_args.json_file)
    elif cmdline_args.command == 'project-info':
        project = labelstudio.list_project_info(cmdline_args.project_id)
        # log.info(f"Project info: {project}")
    # elif args.command == 'export':
    #     annotations = export_annotations(args.project_id)
    #     print(f"Annotations exported: {annotations}")

if __name__ == '__main__':
    main()
