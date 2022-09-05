import argparse

from utils import split_image_into_tiles, fuse_images_into_one

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="util_function", required=True)

    parser_split = subparsers.add_parser('split', help='Split an image into NxN images')
    parser_split.add_argument("file_to_split", type=str)
    parser_split.add_argument("tile_dimension", type=int)

    parser_fuse = subparsers.add_parser("fuse", help="Merge a folder of images into one")
    parser_fuse.add_argument("source_folder", type=str)

    args = parser.parse_args()
    args = vars(args)
    
    if args["util_function"] == "split":
        split_image_into_tiles(args["file_to_split"], args["tile_dimension"])
    elif args["util_function"] == "fuse":
        fuse_images_into_one(args["source_folder"])
