import os
import argparse
from cf_wrapper import Config
from bitmap_font_generator import BitmapFontGenerator

# TODO: Change paths to exports, configs 
# TODO: README.md with examples
# TODO: Make only one obvious script entry point

DEFAULT_CONFIG_PATH = "configs/config_default.yaml"


def main():
    args = _construct_cli_args()
    fontfile = args.fontfile
    output_name = args.output_filename if args.output_filename else os.path.splitext(fontfile)[0]
    output_path = os.path.join("exports", output_name)
    font_path = os.path.join("fonts", fontfile)
    custom_config_path = DEFAULT_CONFIG_PATH if args.config_name is None else os.path.join("configs", args.config_name)

    config = Config(custom_config_path, DEFAULT_CONFIG_PATH)

    BitmapFontGenerator(config).ttf_to_fnt(font_path, output_path)


def _construct_cli_args():
    parser = argparse.ArgumentParser(
        description="Convert a ttf font to a bitmap PNG and .fnt descriptor. Can edit custom config settings within a .yaml file"
    )

    parser.add_argument("fontfile", help="Path to ttf font")
    parser.add_argument("--config_name", default=None, help="Name to custom font/export config file")
    parser.add_argument("--output_filename", help="Name of the output file without extension", default=None)

    return parser.parse_args()

if __name__ == "__main__":
    main()