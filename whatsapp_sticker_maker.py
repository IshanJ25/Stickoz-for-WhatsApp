from PIL import Image
import cv2
from os import remove
import numpy as np
from glob import glob
from pathlib import Path

"""
Program made by Ishan Jindal
Github: https://github.com/IshanJ25/whatsapp_sticker_maker
"""

#########################################
square_side = 512

side_gap = 16
stroke_size = 8
threshold = 20

white = (255, 255, 255)

total_gap = side_gap + stroke_size


#########################################


def make_stickers(folder: str = None, output_folder: str = None, empty_if_contents=False):
    """
    Function to automate processing mass image files to produce stickers as per WhatsApp Guides.

    8 px thick white border around the image fit in 512x512 square with 16 px distance from edge.

    Only supports png, jpg and jpeg files.
    :param folder: Folder location where all images are present.
    :param output_folder: Export folder. New folder is made if already not exists.
    :param empty_if_contents: If exports folder already has files, then delete them. Default is False..

    :return: None. Makes png files in specified output folder.
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

    #########################################

    Path(f'{output_folder}').mkdir(parents=True, exist_ok=True)

    if empty_if_contents:
        for file in glob(f'{output_folder}/*'):
            remove(file)

    image_count = 0
    error_img = []

    for file in glob(f'{folder}/*.png') + glob(f'{folder}/*.jpg') + glob(f'{folder}/*.jpeg'):
        im = Image.open(file)
        im_name = str(im.filename[len(folder) + 1:])

        im = im.convert('RGBA')

        im_w, im_h = im.size

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

        im = im.resize((new_w, new_h))
        try:
            im = stroke(im, threshold=threshold, stroke_size=stroke_size, color=white)
        except:
            error_img.append(im_name)
            continue
        image = Image.new('RGBA', (square_side, square_side))
        image.paste(im, (x, y), im)

        im_name = im_name.split('.')[0]
        image.save(f"{output_folder}/{im_name}.png", "PNG")
        image_count += 1
        print(f"{output_folder}/{im_name}.png ... Done!")

    if image_count == 0:
        print('\nNo images were found in provided folder')
    else:
        print(f'\n{image_count} images were processed.')

    if error_img:
        if len(error_img) == 1:
            print(f'\nError processing 1 image: {error_img[0]}')
        else:
            print(f'\nError processing {len(error_img)} images:')
            for i in error_img:
                print(i)
