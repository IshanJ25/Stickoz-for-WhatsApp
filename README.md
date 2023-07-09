![WA_sticker_formatting](https://socialify.git.ci/IshanJ25/WA_sticker_formatting/image?description=1&descriptionEditable=Python%20project%20that%20automates%20processing%20mass%20image%20files%20to%20produce%20stickers%20as%20per%20WhatsApp%20Guidelines&font=Inter&name=1&owner=1&pattern=Charlie%20Brown&theme=Auto)

### Table of Contents
- [WhatsApp Sticker Maker](#whatsapp-sticker-maker-)
  -  [`make_stickers()`](#make_stickers-function)
- [Result](#result-)
- [How to use](#how-to-use-ℹ%EF%B8%8F)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Parameters](#prameters)


# WhatsApp Sticker Maker 🦩


Python project that automates processing mass image files to produce stickers as per [WhatsApp Guidelines](https://faq.whatsapp.com/219571822467807/)


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

whatsapp_sticker_maker.make_stickers(folder='doge', output_folder='exports', native_format_output=False, skip_if_exists=True)
```

## Parameters:

Argument | What is does | Value type | Default value | Required
--- | --- | --- | --- | --- 
folder | Folder location where all images are present. | `String` | `None` | Yes
output_folder | Export folder. New folder is made if already not exists and/or provided. | `String` | `None` | No
native_format_output | Export in native formats instead of webp. | `Boolean` | `False` | No
skip_if_exists | Skip exporting if expected output exists. | `Boolean` | `False` | No

