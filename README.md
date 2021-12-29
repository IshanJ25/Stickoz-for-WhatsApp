# WhatsApp Sticker Maker 🦩


Python project that automates processing mass image files to produce stickers as per [WhatsApp Guidelines](https://faq.whatsapp.com/general/how-to-create-stickers-for-whatsapp/)


## `make_stickers()` function:

Function to automate processing mass image files to produce stickers as per WhatsApp Guides.
8 px thick white border around the image fit in 512x512 square with 16 px distance from edge.
Only supports `png`, `jpg` & `jpeg` files. Makes `png` files in specified output folder.


# Result ✨

Output in png form
![slide_1](https://user-images.githubusercontent.com/86649457/147594726-66c99a45-fbe4-48e6-865a-d321d8283bc3.jpg)


# How to use ℹ️

## Requirements

you must have these libraries installed with your python package:

`os, pathlib, glob, numpy, PIL, cv2`

This program has only been tested on **`Windows 10 & 11`** with **`Python 3.10`**

## Usage
place the `whatsapp_sticker_maker.py` file beside your own python file and use these commands:

```Python
from whatsapp_sticker_maker import make_stickers

# Requirements: you must have these libraries installed with your python package
# os, pathlib, glob, numpy, PIL, cv2

make_stickers(folder='folder/path', output_folder='export_folder_path', empty_if_contents=True)
```

Prameters:

Argument | What is does | Value type
--- | --- | ---
folder |  Folder location where all images are present. |  string
output_folder | Export folder. New folder is made if already not exists. |  string
empty_if_contents | If exports folder already has files, then delete them. Default is False. Use with caution ⚠️ |  boolean
