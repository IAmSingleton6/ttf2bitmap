# ttf2bitmap

A Python CLI tool to convert `.ttf` font files into bitmap font atlases (`.png`) and BMFont-compatible descriptor files (`.fnt`). Supports custom export settings via a YAML config file.

---

## 🚀 Features

- Converts TrueType Fonts (`.ttf`) to `.png` texture atlas + `.fnt` descriptor
- BMFont-compatible output format
- Supports monospaced or proportional fonts
- Configurable padding, line height, texture size, character 
- Designed for use in games, pixel art engines, or any software that supports BMFont format

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/IAmSingleton6/ttf2bitmap.git
cd ttf2bitmap
pip install -r requirements.txt
```

## 🛠️ Usage

```bash
python ttf2bitmap.py font_path.ttf --config_path=config.yaml --export_dir=exports --export_filename=exported_bitmap_font
```

To change font settings and export settings, edit the default 'config_default.yaml' config file with your desired settings, or create your own config file with custom settings and link via --config_path

### Positional Arguments

| Argument       | Description                              |
|----------------|------------------------------------------|
| `font_path`     | Path of `.ttf` font file.               |

### Optional Flags

| Flag                | Description                                                                           |
|---------------------|---------------------------------------------------------------------------------------|
| `--config_path`     | Path of YAML config file. Defaults to config_default.yaml                             |
| `--export_dir`      | Path to export directory. Defaults to base directory                                  |
| `--export_filename` | Name of export files. Defaults to same base name as font_path                         |

## 🧾 Example
```bash
python ttf2bitmap.py assets/example_font.ttf --export_dir=exports --export_filename=example_export
```

Generates:
- `exports/example_export.png` – the texture atlas
- `exports/example_export.fnt` – BMFont descriptor
