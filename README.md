# whatsapp_sticker_maker

Python project that automates processing mass image files to produce stickers as per WhatsApp Guides


# Result

![slide_1](https://user-images.githubusercontent.com/86649457/147594726-66c99a45-fbe4-48e6-865a-d321d8283bc3.jpg)


# How to use

place the whatsapp_sticker_maker.py file beside your own python file
uses these commands:

```Python
from whatsapp_sticker_maker import make_stickers

# Requirements: you must have these libraries installed with your python package
# os, pathlib, glob, numpy, PIL, cv2

make_stickers(folder='folder\path', output_folder='export_folder\path', file_type='png', empty_if_contents=True)
```

Prameters:

Argument | What is does | Value type
--- | --- | ---
folder |  Folder location where all images are present. |  string
output_folder | Export folder. New folder is made if already not exists. |  string
file_type | 'jpg' or 'png'. Default is 'png'. Currently, only 'png' and 'jpg' are supported. | string
empty_if_contents | If exports folder already has files, then delete them. Default is False. |  boolean
