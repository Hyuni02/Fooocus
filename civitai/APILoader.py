import os
def load_api_key(file_name):
    with open(file_name, 'r') as file:
        return file.read()

print(os.path.abspath(__file__))
print(os.path.exists('/content/Fooocus/civitai/api-key.txt'))
api = load_api_key('/content/Fooocus/civitai/api-key.txt')
