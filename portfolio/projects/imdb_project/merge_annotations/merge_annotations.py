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
    annotations_file = 'annotations.csv'
    all_tasks_file = 'all_tasks.csv'
    output_path = 'merged_annotations.json'

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
            print(annotations[task_id])
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

"""
  # annotations are not required and are the list of annotation results matching the labeling config schema
  "annotations": [{
    "result": [{
      "from_name": "sentiment_class",
      "to_name": "message",
      "type": "choices",
      "readonly": false,
      "hidden": false,
      "value": {
        "choices": ["Positive"]
      }
    }]
  }],
"""


def merge_annotations(annotations:dict, all_tasks:list):
    print(f"Annotations: {annotations}")
    merged_tasks = []
    for task in all_tasks:
        task_id = task['data']['id']
        if task_id in annotations and annotations[task_id]:
            # Merge the annotations with the task data
            result = format_annotation(annotations[task_id])
            task['data'].update(annotations[task_id])
            print(task['data'])
        merged_tasks.append(task)
    return merged_tasks


# Main function to read the annotations, merge them with all tasks, and save to a JSON file
def main_loop():
    # Define the file paths
    annotations_file = 'test-annotations.csv'
    all_tasks_file = 'all_tasks.csv'
    output_path = 'merged_annotations.json'
    log.info(f"Reading annotations from {annotations_file}")
    log.info(f"Reading all tasks from {all_tasks_file}")
    log.verbose(f"Writing merged annotations to {output_path}")    

    # # Read the annotations from the CSV file
    # annotations = read_annotations(annotations_file)
    # all_tasks = read_all_tasks(all_tasks_file)
    # merged_tasks = merge_annotations(annotations, all_tasks)

    # # Write the merged annotations to a JSON file
    # with open(output_path, 'w') as jsonfile:
    #     json.dump(merged_tasks, jsonfile, indent=4)
    # print(f"Merged annotations saved to {output_path}")


if __name__ == "__main__":
    main_loop()
