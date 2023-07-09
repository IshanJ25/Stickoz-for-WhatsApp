import whatsapp_sticker_maker

# Requirements: you must have these libraries installed with your python package
# os, pathlib, glob, numpy, PIL, cv2

whatsapp_sticker_maker.make_stickers(folder='stickers', output_folder='exports', native_format_output=False, skip_if_exists=True)

whatsapp_sticker_maker.give_code_format(folder='exports')
