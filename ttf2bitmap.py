import os
import argparse
from cf_wrapper import Config
from bitmap_font_generator import BitmapFontGenerator

DEFAULT_CONFIG_PATH = "config_default.yaml"


def main():
    args = _construct_cli_args()

    font_path = args.font_path
    file_name = os.path.basename(font_path)
    export_filename = args.export_filename if args.export_filename else os.path.splitext(file_name)[0]

    custom_config_path = DEFAULT_CONFIG_PATH if args.config_path is None else args.config_path

    config = Config(custom_config_path, DEFAULT_CONFIG_PATH)

    BitmapFontGenerator(config).ttf_to_fnt(font_path, args.export_dir, export_filename)


def _construct_cli_args():
    parser = argparse.ArgumentParser(
        description="Convert a ttf font to a bitmap PNG and .fnt descriptor. Can edit custom config settings within a .yaml file"
    )

    parser.add_argument("font_path", help="Path of `.ttf` font file.")
    parser.add_argument("--config_path", help="Path of YAML config file within configs directory. Defaults to config_default.yaml", default = None)
    parser.add_argument("--export_dir", help="Path to export directory. Defaults to base directory", default=None)
    parser.add_argument("--export_filename", help="Name of export files. Defaults to same basename as fontname", default=None)

    return parser.parse_args()

if __name__ == "__main__":
    main()