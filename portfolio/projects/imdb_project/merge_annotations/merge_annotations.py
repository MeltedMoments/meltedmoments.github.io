# merge_annotations.py
# Script to merge annotations from an earlier set of annotations
# from Label Studio, specifically for the IMDB dataset. 
# This is useful for merging annotations from multiple rounds of labeling, 
# or after changing the labelling configuration.

import csv
import json

import portfolio.logging_utils as logging_utils

log = logging_utils.log

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
    log.info(f"Writing merged annotations to {output_path}")    

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
