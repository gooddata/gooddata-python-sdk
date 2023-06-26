import argparse
import json

def process_json_file(file_path) -> dict:
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data

def file_structure_from_json(data: dict) -> dict:
    pass

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file')
    parser.add_argument('file', metavar='FILE', help='path to the JSON file')
    args = parser.parse_args()

    file_path = args.file
    process_json_file(file_path)

main()