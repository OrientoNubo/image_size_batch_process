#!/user/bin/env python
# -*- coding:utf-8 -*-

import os
from sys import byteorder
from tarfile import SUPPORTED_TYPES
import cv2
import numpy as np




def not_keep_scale(img_dir, size, alpha):
    img = cv2.imread(img_dir, flags=alpha)
    img = cv2.resize(img, (size[0], size[1]))
    return img

class OutletResize:
    def __init__(self) -> None:
        pass

    def outlet_resize_updown(img, size, border_info):
        scale = int(img.shape[1]) / int(size[1])
        img = cv2.resize(img, (int(size[1]), int(img.shape[0] / scale)))
        top_size, bottom_size, left_size, right_size = int((size[0] - int(img.shape[0]))/2), int((size[0] - int(img.shape[0]))/2), 0, 0
        # if 
        img = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, border_info[0], value=border_info[1])
        img = cv2.resize(img, (int(size[1]), int(size[0])))
        return img

    def outlet_resize_lefrig(img, size, border_info):
        scale = int(img.shape[0]) / int(size[0])
        img = cv2.resize(img, (int(img.shape[1] / scale), int(size[0])))
        top_size, bottom_size, left_size, right_size = 0, 0, int((size[1] - int(img.shape[1]))/2), int((size[1] - int(img.shape[1]))/2)
        img = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, border_info[0], value=border_info[1])
        img = cv2.resize(img, (int(size[1]), int(size[0])))
        return img

    def keep_scale_outlet(img, size, border_info):
        print(img.shape)
        
        # which is the max length
        w_flag = 0
        max_length = img.shape[0]
        if img.shape[1] > max_length:
            max_length = img.shape[1]
            w_flag = 1

        # weigth is longer
        if w_flag:
            if size[0] >= size[1]:
                img = OutletResize.outlet_resize_updown(img, size, border_info)
            elif size[0] < size[1]:
                img = OutletResize.outlet_resize_lefrig(img, size, border_info)
            else:
                print("error code: KI_02")
        else:
            if size[0] > size[1]:
                img = OutletResize.outlet_resize_updown(img, size, border_info)
            elif size[0] <= size[1]:
                img = OutletResize.outlet_resize_lefrig(img, size, border_info)
            else:
                print("error code: KI_03")

        print(img.shape)
        return img

def border_info_set(BorderType, BorderConstantValue):
    border_info = [0, 0]
    border_info[1] = BorderConstantValue

    if BorderType == 'CONSTANT':
        border_info[0] = cv2.BORDER_CONSTANT
    elif BorderType == 'REPLICATE':
        border_info[0] = cv2.BORDER_REPLICATE
    elif BorderType == 'REFLECT':
        border_info[0] = cv2.BORDER_REFLECT
    elif BorderType == 'WRAP':
        border_info[0] = cv2.BORDER_WRAP
    elif BorderType == 'REFLECT_101':
        border_info[0] = cv2.BORDER_REFLECT_101
    # elif BorderType == 'TRANSPARENT':
    #     border_info[0] = cv2.BORDER_TRANSPARENT
    elif BorderType == 'REFLECT101':
        border_info[0] = cv2.BORDER_REFLECT101
    elif BorderType == 'DEFAULT':
        border_info[0] = cv2.BORDER_DEFAULT
    # elif BorderType == 'ISOLATED':
    #     border_info[0] = cv2.BORDER_ISOLATED
    else:
        print("error code: KI_01")
    
    return border_info


class ImageRead:
    SUPPORTED_TYPES = ['jpg', 'png']
    def __init__(self) -> None:
        pass

    def read_img_info(img_dir):
        _, img_fullname = os.path.split(img_dir)
        img_filename = img_fullname.split('.')[0]
        _, img_ext = os.path.splitext(img_dir)
        return img_fullname, img_filename, img_ext

    def read_img_data(img_dir, alpha):
        img = cv2.imread(img_dir, flags=alpha)
        return img

'''
resize
    not_keep_scale
    keep_scale_inlet
        BorderType
            CONSTANT    = 0,
            REPLICATE   = 1,
            REFLECT     = 2,
            WRAP        = 3,
            REFLECT_101 = 4,
            # TRANSPARENT = 5,
            REFLECT101  = BORDER_REFLECT_101,
            DEFAULT     = BORDER_REFLECT_101,
            # ISOLATED    = 16,

'''

if __name__ == '__main__':

    img_dirs = './image/'
    save_dir = './image_resized/'
    if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    imgs = os.listdir(img_dirs)
    print(imgs)
    # exit(0)
    

    for one_img in imgs:

        img_dir = img_dirs + one_img
        img_fullname, img_filename, img_ext = ImageRead.read_img_info(img_dir)
        img = ImageRead.read_img_data(img_dir, alpha=1)

        size = [600, 600]   # h, w
        border_info = border_info_set('REPLICATE', 1)
        img_new = OutletResize.keep_scale_outlet(img, size=size, border_info=border_info)

        # cv2.imshow('image', img_new)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # exit(0)

        cv2.imwrite(save_dir + img_filename + '_resized_h' + str(size[0]) + '_w' + str(size[1]) + '_' + str(border_info[0]) + img_ext, img_new)



