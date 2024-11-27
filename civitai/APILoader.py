def load_api_key(file_name):
    with open(file_name, 'r') as file:
        return file.read()

api = load_api_key('/content/drive/MyDrive/api-key.txt')