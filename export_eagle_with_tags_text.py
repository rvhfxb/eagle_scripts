import argparse
import os
import glob
import json
import shutil

def main(args):
    item_paths = glob.glob(os.path.join(args.library_dir, "images/*.info"))
    for item_path in item_paths:
        try:
            json_path = os.path.join(item_path, "metadata.json")
            with open(json_path, 'rt', encoding='utf-8') as json_file:
                json_value = json.load(json_file)
            tags = ", ".join(json_value['tags'])
            export_path = os.path.join(args.export_dir, json_value['id'] + "." +  json_value['ext'])
            image_path = os.path.join(item_path, json_value['name'] + "." + json_value['ext'])
            tags_path = os.path.join(args.export_dir, json_value['id'] + ".txt")
            if os.path.exists(export_path):
                continue
            shutil.copyfile(image_path, export_path)

            with open(tags_path, 'w', encoding='utf-8') as tags_file:
                tags_file.write(tags)

        except Exception as e:
            print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("library_dir", type=str)
    parser.add_argument("export_dir", type=str)

    args = parser.parse_args()
    main(args)
