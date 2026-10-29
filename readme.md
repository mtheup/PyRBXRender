PyRBXRender is a Python utility based on reverse engineering of the November 2007 version of RBXGS it attempts to recreate the renders that the original render

RBXRender — Quick Start
A small Python tool that recriate 2006-2008 renders Roblox 
Requirements
Python 3.10 or newer
numpy and Pillow
Install the libraries:
python -m pip install numpy Pillow
Prepare the assets (first use)
Run python rbxrender.py setup <file.msi>
Render a character model
Render a specific .rbxm file:
python rbxrender.py render character.rbxm -o render.png
If the model argument is omitted, the tool looks for character.rbxm in the assets folder:
python rbxrender_english.py render
Common settings
python rbxrender.py render character.rbxm \
  -o render.png \
  --size 1024 \
  --yaw 30 \
  --pitch 25 \
  --bg transparent
-o, --out: output image filename (default: render.png)
--size: image size, such as 512, 1024, or 1024x768
--yaw: horizontal camera angle in degrees (default: 30)
--pitch: vertical camera angle in degrees (default: 25)
--bg: background: transparent, sky, or a hex color such as #202020
--ss: antialiasing/supersampling factor (default: 4; use 1 for faster rendering)
--assets: assets directory (default: assets)
--margin: padding around the model (default: 0.08)
You can change the camera angles whenever you want. For example, --yaw 90 --pitch 10 gives a different viewpoint.
Render a standalone mesh
python rbxrender.py mesh item.mesh -o item.png --color 194
You can provide a texture with -t:
python rbxrender.py mesh item.mesh -t texture.png -o item.png
Helpful commands
Show all available options for a command:
python rbxrender.py --help
python rbxrender.py render --help
python rbxrender.py mesh --help
List available BrickColor values:
python rbxrender.py colors
