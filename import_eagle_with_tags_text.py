import argparse
import os
import glob
from eagleapi import api_item
from eagleapi import api_util


def main(args):
    image_dir = args.image_dir
    folder = api_util.find_or_create_folder(args.library)
    items = []
    image_paths = glob.glob(os.path.join(image_dir, "*.jpg")) + \
    glob.glob(os.path.join(image_dir, "*.png")) + glob.glob(os.path.join(image_dir, "*.webp"))
    for image_path in image_paths:
        tags_path = os.path.splitext(image_path)[0] + '.txt'
        with open(tags_path, "rt", encoding='utf-8') as f:
            tags = [x.strip() for x in f.readlines()[0].split(",")]
        item = api_item.EAGLE_ITEM_PATH(
            filefullpath=image_path,
            filename=os.path.basename(image_path),
            tags=tags,
            annotation=os.path.basename(image_dir),
        )
        items.append(item)
    api_item.add_from_paths(
        files=items,
        folderId=folder,
        step=1000
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("library", type=str)
    parser.add_argument("image_dir", type=str)

    args = parser.parse_args()
    main(args)
