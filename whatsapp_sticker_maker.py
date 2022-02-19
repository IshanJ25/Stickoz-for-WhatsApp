from glob import glob
from os import remove
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageSequence

"""
Program made by Ishan Jindal
Github: https://github.com/IshanJ25/whatsapp_sticker_maker
"""

#########################################

img_types = ['png', 'jpg', 'jpeg']  # image types to be converted
gif_types = ['gif']  # gif types to be converted

#########################################

square_side = 512

side_gap = 16
stroke_size = 8
threshold = 20

white = (255, 255, 255)

total_gap = side_gap + stroke_size

gif_loop_count = 0


#########################################


def make_stickers(folder: str = None, output_folder: str = None, animated: bool = False,
                  empty_if_contents=False, save_as_webp=False):
    """
    Function to automate processing mass image files to produce stickers as per WhatsApp Guides.
    8 px thick white border around the image fit in 512x512 square with 16 px distance from edge.

    Supports png, jpg, jpeg and gif formats.

    :param save_as_webp: Export as webp instead of native format. Default is False.
    :param animated: Is the image animated? Default is False.
    :param folder: Folder location where all images are present.
    :param output_folder: Export folder. New folder is made if already not exists.
    :param empty_if_contents: Empty exports' folder if already contains files. Default is False.

    :return: None. Makes specified type files in specified output folder.
    """

    #########################################

    if folder is None and output_folder is None:
        print('Error: Please provide "folder" and "output_folder" parameters')
        return
    elif folder is None:
        print('Error: Please provide "folder" parameter')
        return
    elif output_folder is None:
        print('Error: Please provide "output_folder" parameter')
        return

    def stroke(origin_image, threshold, stroke_size: int, color):

        def change_matrix(input_mat, stroke_size):
            stroke_size -= 1
            mat = np.ones(input_mat.shape)
            check_size = stroke_size + 1.0
            mat[input_mat > check_size] = 0
            border = (input_mat > stroke_size) & (input_mat <= check_size)
            mat[border] = 1.0 - (input_mat[border] - stroke_size)
            return mat

        def cv2pil(cv_img):
            pil_img = Image.fromarray(cv_img.astype("uint8"))
            return pil_img

        img = np.array(origin_image)
        h, w, _ = img.shape

        padding = stroke_size
        alpha = img[:, :, 3]
        rgb_img = img[:, :, 0:3]
        bigger_img = cv2.copyMakeBorder(rgb_img, padding, padding, padding, padding,
                                        cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
        alpha = cv2.copyMakeBorder(alpha, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=0)
        bigger_img = cv2.merge((bigger_img, alpha))
        h, w, _ = bigger_img.shape

        _, alpha_without_shadow = cv2.threshold(alpha, threshold, 255, cv2.THRESH_BINARY)  # threshold=0 in photoshop
        alpha_without_shadow = 255 - alpha_without_shadow
        dist = cv2.distanceTransform(alpha_without_shadow, cv2.DIST_L2, cv2.DIST_MASK_3)  # dist l1 : L1 , dist l2 : l2
        stroked = change_matrix(dist, stroke_size)
        stroke_alpha = (stroked * 255).astype(np.uint8)

        stroke_b = np.full((h, w), color[2], np.uint8)
        stroke_g = np.full((h, w), color[1], np.uint8)
        stroke_r = np.full((h, w), color[0], np.uint8)

        stroke = cv2.merge((stroke_b, stroke_g, stroke_r, stroke_alpha))
        stroke = cv2pil(stroke)
        bigger_img = cv2pil(bigger_img)
        result = Image.alpha_composite(stroke, bigger_img)
        return result

    def get_x_y(img):
        im_w, im_h = img.size

        if im_w > im_h:
            new_w = square_side - 2 * total_gap
            new_h = round(im_h * new_w / im_w)
            x = side_gap
            y = round(square_side / 2 - new_h / 2)
        elif im_w < im_h:
            new_h = square_side - 2 * total_gap
            new_w = round(im_w * new_h / im_h)
            x = round(square_side / 2 - new_w / 2)
            y = side_gap
        else:
            new_w = square_side - 2 * total_gap
            new_h = square_side - 2 * total_gap
            x = side_gap
            y = side_gap

        return x, y, new_w, new_h

    def gen_frame(im):
        alpha = im.getchannel('A')
        # Convert the image into P mode but only use 255 colors in the palette out of 256
        im = im.convert('RGBA').convert('P', palette=Image.ADAPTIVE, colors=255)
        # Set all pixel values below 128 to 255 , and the rest to 0
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        # Paste the color of index 255 and use alpha as a mask
        im.paste(255, mask)
        # The transparency index is 255
        im.info['transparency'] = 255
        return im

    #########################################

    Path(f'{output_folder}').mkdir(parents=True, exist_ok=True)

    if empty_if_contents:
        for file in glob(f'{output_folder}/*'):
            remove(file)

    image_count = 0
    error_img = []

    if not animated:

        file_list = []

        for i in img_types:
            file_list += glob(f'{folder}/*{i}')

        input_type = 'picture'

        if save_as_webp:
            output_extension = 'webp'
        else:
            output_extension = 'png'

        for file in file_list:

            try:
                im = Image.open(file)
                im_name = str(im.filename[len(folder) + 1:]).split('.')[0]
                print(f"{output_folder}/{im_name}.{output_extension} ... ", end='')
            except:
                print("Error!")
                error_img.append(str(file[len(folder) + 1:]))
                continue

            x, y, new_w, new_h = get_x_y(im)

            im = im.convert('RGBA').resize((new_w, new_h))

            try:
                im = stroke(im, threshold=threshold, stroke_size=stroke_size, color=white)
            except:
                error_img.append(im_name)
                print("Error!")
                continue

            image = Image.new('RGBA', (square_side, square_side))
            image.paste(im, (x, y), im)

            im_name = im_name.split('.')[0]
            image.save(f"{output_folder}/{im_name}.{output_extension}")
            image_count += 1
            print("Done!")


    elif animated:

        file_list = []

        for i in gif_types:
            file_list += glob(f'{folder}/*{i}')

        input_type = 'gif'

        if save_as_webp:
            output_extension = 'webp'
        else:
            output_extension = 'gif'

        for file in file_list:

            try:
                im = Image.open(file)
                im_name = str(im.filename[len(folder) + 1:]).split('.')[0]
                print(f"{output_folder}/{im_name}.{output_extension} ... ", end='')
            except:
                print("Error!")
                error_img.append(str(file[len(folder) + 1:]))
                continue

            x, y, new_w, new_h = get_x_y(im)

            im_list = []

            for frame in ImageSequence.Iterator(im):

                try:
                    frame = frame.convert('RGBA').resize((new_w, new_h))
                    frame = stroke(frame, threshold=threshold, stroke_size=stroke_size, color=white)
                    image = Image.new('RGBA', (square_side, square_side))
                    image.paste(frame, (x, y), frame)
                    image = gen_frame(image)
                    im_list.append(image)

                except:
                    error_img.append(im_name)
                    print("Error!")
                    break

            duration = im.info['duration']

            img = im_list[0]
            imgs = im_list[1:]

            img.save(f"{output_folder}/{im_name}.{output_extension}", save_all=True, append_images=imgs,
                     duration=duration, loop=gif_loop_count, optimize=False, disposal=2, lossless=True)

            image_count += 1
            print("Done!")

    if image_count == 0:
        print(f'\nNo {input_type}s were found in provided folder\n')
    elif image_count == 1:
        print(f'\n1 {input_type} was converted\n')
    else:
        print(f'\n{image_count} {input_type}s were processed.\n')

    if error_img:
        if len(error_img) == 1:
            print(f'\nError processing 1 {input_type}: {error_img[0]}\n')
        else:
            print(f'\nError processing {len(error_img)} {input_type}s:')
            for i in error_img:
                print(i)
            print('\n')


def give_code_format(folder: str = None, img_type: str = None):
    """
    Function to automate and print names of image according to suitable syntax.

    :param img_type: Type of image to index (png/gif/webp).
    :param folder: Folder location where all exported pngs are present.

    :return: None. Prints android app syntax with file names
    """

    if folder is None and img_type is None:
        print('No folder or type provided')
        return
    elif folder is None:
        print('No folder provided')
        return
    elif img_type is None:
        print('No type provided')
        return

    if img_type != 'png' and img_type != 'gif' and img_type != 'webp':
        print('Invalid type')
        return

    lst = []
    for file in glob(f'{folder}/*.{img_type}'):
        lst.append(file.split('.')[0])

    for i in lst:
        print('        {')
        print('            "image_file": "{}.webp",'.format(i))
        print('            "emojis": []')
        print('        },')
