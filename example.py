import whatsapp_sticker_maker

# Requirements: you must have these libraries installed with your python package
# os, pathlib, glob, numpy, PIL, cv2

whatsapp_sticker_maker.make_stickers(folder='doge', output_folder='exports', empty_if_contents=True, animated=False)

whatsapp_sticker_maker.give_code_format(folder='exports')
