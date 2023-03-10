import os
import csv
from subprocess import call


def clone_repos(path, save_dir='resources'):
    with open(path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        walking_dir = f'{save_dir}/{"/".join(line.strip().split("/")[-2:])}'
        call(['git', 'clone', line.strip(), walking_dir])


def find_files(path, save_dir='resources', max_size=1000000, extensions=None):
    if extensions is None:
        extensions = ['py']
    with open(path, 'r') as f:
        lines = f.readlines()
    total_files_path = []
    for line in lines:
        walking_dir = f'{save_dir}/{"/".join(line.strip().split("/")[-2:])}'
        for (current_path, folders, files) in os.walk(walking_dir):
            for file in files:
                size = os.path.getsize(path)
                # Only files with certain extensions and under max_size
                if (file.split('.')[-1] in extensions) & (size < max_size):
                    total_files_path.append(os.path.join(current_path, file))
    return total_files_path


def jsonify(files_path, bos_token='<BOS>', eos_token='<EOS>'):
    json = []
    for path in files_path:
        with open(path, 'r') as f:
            try:
                content = f.readlines()
            except UnicodeDecodeError:
                print('DecoderError: ', path)
            summary = ''.join(content)
            summary = str(summary).strip()
            data = bos_token + summary + eos_token
            repo_name = '/'.join(path.split('/')[1:3])
            file_path = '/'.join(path.split('/')[3:])
            json.append({'text': data,
                         'repo_name': repo_name,
                         'path': file_path})
    return json


def json_to_csv(json, path, fieldnames=None):
    if fieldnames is None:
        fieldnames = ['text', 'repo_name', 'path']
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in json:
            writer.writerow(data)


clone_repos('repos.txt')
files_path_list = find_files('repos.txt')
json_data = jsonify(files_path_list)
json_to_csv(json_data, 'data/data.csv')
