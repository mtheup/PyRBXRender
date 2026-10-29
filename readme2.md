# Roblox Renderer — Quick Start

A small Python tool that renders Roblox `.rbxm` character models and standalone `.mesh` files to PNG images.

## 1. Requirements

- Python 3.10 or newer
- `numpy` and `Pillow`

Install the libraries:

```bash
python -m pip install numpy Pillow
```

## 2. Prepare the assets (first use)

If you have the Roblox Studio/renderer installer MSI that contains the required assets, extract them with:

```bash
python rbxrender_english.py setup path/to/installer.msi
```

This creates an `assets/` folder. If you want to choose another folder, use `--assets`:

```bash
python rbxrender_english.py setup path/to/installer.msi --assets my_assets
```

Keep the assets folder available when rendering. If you use a custom folder, pass the same folder with `--assets` in your render command.

## 3. Render a character model

Render a specific `.rbxm` file:

```bash
python rbxrender_english.py render character.rbxm -o render.png
```

If the model argument is omitted, the tool looks for `character.rbxm` in the assets folder:

```bash
python rbxrender_english.py render
```

## 4. Common settings

```bash
python rbxrender_english.py render character.rbxm \
  -o render.png \
  --size 1024 \
  --yaw 30 \
  --pitch 25 \
  --bg transparent
```

- `-o`, `--out`: output image filename (default: `render.png`)
- `--size`: image size, such as `512`, `1024`, or `1024x768`
- `--yaw`: horizontal camera angle in degrees (default: `30`)
- `--pitch`: vertical camera angle in degrees (default: `25`)
- `--bg`: background: `transparent`, `sky`, or a hex color such as `#202020`
- `--ss`: antialiasing/supersampling factor (default: `4`; use `1` for faster rendering)
- `--assets`: assets directory (default: `assets`)
- `--margin`: padding around the model (default: `0.08`)

You can change the camera angles whenever you want. For example, `--yaw 90 --pitch 10` gives a different viewpoint.

## 5. Render a standalone mesh

```bash
python rbxrender_english.py mesh item.mesh -o item.png --color 194
```

You can provide a texture with `-t`:

```bash
python rbxrender_english.py mesh item.mesh -t texture.png -o item.png
```

## 6. Helpful commands

Show all available options for a command:

```bash
python rbxrender_english.py --help
python rbxrender_english.py render --help
python rbxrender_english.py mesh --help
```

List available BrickColor values:

```bash
python rbxrender_english.py colors
```

## Notes

- Run commands from the folder containing `rbxrender_english.py`, or use its full path.
- Replace example filenames and paths with the actual files on your computer.
- The default camera angles are **yaw 30°** and **pitch 25°**.
