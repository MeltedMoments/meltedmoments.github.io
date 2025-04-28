# merge_annotations.py
# Script to merge annotations from an earlier set of annotations
# from Label Studio, specifically for the IMDB dataset. 
# This is useful for merging annotations from multiple rounds of labeling, 
# or after changing the labelling configuration.
import argparse
import csv
import json
import logging

import portfolio.logging_utils as logging_utils
log = logging_utils.log


def parse_args():
    program_description = f"Merge annotations from a CSV file with all tasks for the IMDB project. This is useful for merging annotations from multiple rounds of labeling, or after changing the labelling configuration."
    datadir = 'data'
    # Default file names
    annotations_file = f"{datadir}/annotations.csv"
    all_tasks_file = f"{datadir}/all_tasks.csv"
    output_path = f"{datadir}/merged_annotations.json"

    parser = argparse.ArgumentParser(description=program_description,
                                     formatter_class=argparse.RawTextHelpFormatter)

    # input filename
    parser.add_argument("--annotations-file",  
                        required=False, 
                        default=annotations_file,
                        help=f"Name of the annotation CSV file [{annotations_file}]. The CSV file should contain the following columns: id, sentiment, notes, highlight.")
    parser.add_argument("--all-tasks-file", 
                        required=False, 
                        default=all_tasks_file,
                        help=f"Name of the all tasks CSV file [{all_tasks_file}]. The CSV file should contain the following columns: id, review, filename, url.")
    parser.add_argument("--output-file",    
                        required=False, 
                        default=output_path,
                        help=f"Name of the output JSON file [{output_path}]. The JSON file will contain the merged annotations.")
    
    # Logging parameters: log file and loglevel
    logparams = parser.add_argument_group('Logging options')
    logparams.add_argument("--logfile", 
                        default="", 
                        help=f"Name of the log file, default is logging to the terminal")
    choices = ["verbose", "debug", "info", "warning", "error", "critical"]
    logparams.add_argument("--loglevel",
                        choices=choices,
                        default="info",
                        help=f"Set the logging level, default is 'info'")

    args = parser.parse_args()

    # Replace the string entered for the log level with a numeric value 
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {args.loglevel}')

    args.loglevel = numeric_level


    return args

# Configure logging from command line arguments
# Set it up before any other code is run
cmdline_args = parse_args()
log_filename = cmdline_args.logfile 
log_level = cmdline_args.loglevel
logging_utils.reconfigure_logging(loglevel=log_level, logfile=log_filename)


# Read the annotnations from the CSV file   
# and store them in a dictionary
def read_annotations(file_path:str):
    # Make sure the file exists
    try:
        with open(file_path, 'r') as f:
            pass
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        log.error(f"Error opening file: {file_path}")
        raise   
    
    annotations = {}
    with open(file=file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task_id = row['id']
            sentiment = row['sentiment']
            notes = row['notes']
            highlight = row['highlight']
            annotations[task_id] = { 
                'sentiment': sentiment,
                'notes': notes,
                'highlight': json.loads(highlight) if highlight else []
            }
            log.debug(f"{annotations[task_id]}")
    return annotations


# Read all tasks from the CSV file
def read_all_tasks(file_path:str):
    all_tasks = []
    with open(file=file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task = {
                "data": {
                    "id": row['id'],
                    "review_text": row['review'],       # must match LS config
                    "filename": row['filename'],
                    "url": row['url'],
                }
            }
            all_tasks.append(task)
    return all_tasks


def format_annotation(annotation:dict):
    result = {
        "from_name": "sentiment",
        "to_name": "review_text",
        "type": "choices",
        "readonly": False,
        "hidden": False,
        "value": {
            "choices": [annotation['sentiment']]
        }
    }
    return result

def merge_annotations(annotations:dict, all_tasks:list):
    """
    Merge the annotations with the all tasks
    The annotations are stored in a dictionary with the task id as the key
    
    Args:
        annotations (dict): The annotations dictionary
        all_tasks (list): The list of all tasks
    Returns:
        merged_tasks (list): The list of all tasks with the annotations merged
    """
    merged_tasks = []
    for task in all_tasks:
        results = []
        task_id = task['data']['id']
        if task_id in annotations and annotations[task_id]:
            log.debug(f"Found task {task_id} in annotations")
            # Merge the annotations with the task data
            result = format_annotation(annotations[task_id])
            results.append(result)
            task['annotations'] = [{
                "result": results,
                "completed_by": 1,
            }]
            # task['data'].update(annotations[task_id])
            log.debug(f"Merged task:\n{task}")
        merged_tasks.append(task)
    return merged_tasks


# Main function to read the annotations, merge them with all tasks, and save to a JSON file
def main_loop():
    # Define the file paths
    annotations_file = cmdline_args.annotations_file
    all_tasks_file = cmdline_args.all_tasks_file
    output_path = cmdline_args.output_file
    log.info(f"Reading annotations from {annotations_file}")
    log.info(f"Reading all-tasks from {all_tasks_file}")
    log.info(f"Writing merged-annotations to {output_path}")    

    # # Read the annotations from the CSV file
    annotations = read_annotations(annotations_file)
    all_tasks = read_all_tasks(all_tasks_file)
    log.info(f"Read {len(annotations)} annotations from {annotations_file}")
    log.info(f"Read {len(all_tasks)} tasks from {all_tasks_file}")
    # log.info(f"First task: {all_tasks[0]}")
    merged_tasks = merge_annotations(annotations=annotations, 
                                     all_tasks=all_tasks)
    log.info(f"Merged {len(merged_tasks)} tasks with annotations")
    # log.info(f"merged tasks: {merged_tasks}")

    # Write the merged annotations to a JSON file
    with open(output_path, 'w') as jsonfile:
        json.dump(merged_tasks, jsonfile, indent=4)
    log.info(f"Merged annotations saved to {output_path}")


if __name__ == "__main__":
    main_loop()
