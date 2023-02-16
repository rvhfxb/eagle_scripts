import argparse
import sys
from PIL import Image
import glob
import json

def get_tags(str):
    tags = [x.replace('(','').replace(')','').split(':')[0].strip()
        for x in str.split(',')]
    return [x for x in tags if x != '']

def get_info_tags(str):
    items = [x.strip() for x in str.split(',')]
    tags = []
    for item in items:
        if item.startswith("Model: "):
            tags.append(item)
        if item.startswith("Sampler: "):
            tags.append(item)
    return tags

def main(args):
    paths = glob.glob(args.library+'/images/*.info')

    print(f"{len(paths)} file found")

    for path in paths:
        metadata_path = path+'/metadata.json'
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        image_path = f"{path}/{metadata['name']}.{metadata['ext']}"
        with Image.open(image_path) as image:
            parameters = (image.info or {}).pop('parameters', None)

        for line in parameters.split("\n"):
            if line.startswith("Negative prompt: "):
                pass
            elif line.startswith("Steps: "):
                info_tags = get_info_tags(line)
            else:
                tags = get_tags(line)
        
        metadata["annotation"] = parameters
        metadata["tags"] = [*tags, *info_tags]

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f)

        print(metadata_path+' saved')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("library", type=str)

    args = parser.parse_args()
    main(args)
