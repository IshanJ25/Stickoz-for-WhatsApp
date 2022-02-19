# WhatsApp Sticker Maker 🦩


Python project that automates processing mass image files to produce stickers as per [WhatsApp Guidelines](https://faq.whatsapp.com/general/how-to-create-stickers-for-whatsapp/)


## `make_stickers()` function:

Function to automate processing mass image files to produce stickers as per WhatsApp Guides.
8 px thick white border around the image fit in 512x512 square with 16 px distance from edge.

Currently supports reading `png`, `jpg`, `jpeg` and `gif` formats.
Able to write images in `png`, `gif` and `webp` formats.


# Result ✨

Output in png form
![presentation_image](https://user-images.githubusercontent.com/86649457/147594726-66c99a45-fbe4-48e6-865a-d321d8283bc3.jpg)


# How to use ℹ️

## Requirements

you must have these libraries installed with your python package:

`os, pathlib, glob, numpy, PIL, cv2`

This program has only been tested on **`Windows 10 & 11`** with **`Python 3.10`**

## Usage
place the `whatsapp_sticker_maker.py` file beside your own python file and use these commands:

```Python
import whatsapp_sticker_maker

# Requirements: you must have these libraries installed with your python package
# os, pathlib, glob, numpy, PIL, cv2

whatsapp_sticker_maker.make_stickers(folder='doge', output_folder='exports', empty_if_contents=True, animated=False)
```

Prameters:

Argument | What is does | Value type
--- | --- | ---
folder | Folder location where all images are present. |  string
output_folder | Export folder. New folder is made if already not exists. |  string
animated | Is the image animated? Default is False | boolean
empty_if_contents | Empty exports' folder if already contains files. Default is False. Use with caution ⚠️ | boolean
save_as_webp | Export as webp instead of native format. Default is False. | boolean
