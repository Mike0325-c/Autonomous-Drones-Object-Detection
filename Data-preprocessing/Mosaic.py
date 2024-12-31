import random

import cv2
import os
import glob
import numpy as np
from PIL import Image
from lxml import etree
from ipdb import set_trace

OUTPUT_SIZE = (1024, 1024)  # Height, Width
SCALE_RANGE = (0.5, 0.5)
FILTER_TINY_SCALE = 1 / 50  # if height or width lower than this scale, drop it.

# voc格式的数据集，anno_dir是标注xml文件，img_dir是对应jpg图片
ANNO_DIR = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Augmentation_img'
IMG_DIR = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Mosaic_text'


# category_name = ['background', 'person']


def main():
    img_paths, annos = get_dataset(ANNO_DIR, IMG_DIR)

    # set_trace()
    idxs = random.sample(range(len(annos)), 4)  # 从annos列表长度中随机取4个数
    # set_trace()

    new_image, new_annos = update_image_and_anno(img_paths, annos,
                                                 idxs,
                                                 OUTPUT_SIZE, SCALE_RANGE,
                                                 filter_scale=FILTER_TINY_SCALE)
    # 更新获取新图和对应anno
    # img_p=os.path.join(r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train',f'{img_name}.jpg')
    cv2.imwrite('./img/wind_output.jpg', new_image)
    # annos是
    for anno in new_annos:
        start_point = (int(anno[1] * OUTPUT_SIZE[1]), int(anno[2] * OUTPUT_SIZE[0]))  # 左上角点
        end_point = (int(anno[3] * OUTPUT_SIZE[1]), int(anno[4] * OUTPUT_SIZE[0]))  # 右下角点
        cv2.rectangle(new_image, start_point, end_point, (0, 255, 0), 1, cv2.LINE_AA)  # 每循环一次在合成图画一个矩形

    cv2.imwrite('./img/wind_output_box.jpg', new_image)

    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    new_image = Image.fromarray(new_image.astype(np.uint8))
    # new_image.show()
    # cv2.imwrite('./img/wind_output111.jpg', new_image)


def update_image_and_anno(all_img_list, all_annos, idxs, output_size, scale_range, filter_scale=0.):
    output_img = np.zeros([output_size[0], output_size[1], 3], dtype=np.uint8)
    scale_x = scale_range[0] + random.random() * (scale_range[1] - scale_range[0])
    scale_y = scale_range[0] + random.random() * (scale_range[1] - scale_range[0])
    divid_point_x = int(scale_x * output_size[1])
    divid_point_y = int(scale_y * output_size[0])

    new_anno = []
    for i, idx in enumerate(idxs):
        set_trace()
        path = all_img_list[idx]
        img_annos = all_annos[idx]

        img = cv2.imread(path)
        if i == 0:  # top-left
            img = cv2.resize(img, (divid_point_x, divid_point_y))
            output_img[:divid_point_y, :divid_point_x, :] = img
            for bbox in img_annos:
                xmin = bbox[1] * scale_x
                ymin = bbox[2] * scale_y
                xmax = bbox[3] * scale_x
                ymax = bbox[4] * scale_y
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax])

        elif i == 1:  # top-right
            img = cv2.resize(img, (output_size[1] - divid_point_x, divid_point_y))
            output_img[:divid_point_y, divid_point_x:output_size[1], :] = img
            for bbox in img_annos:
                xmin = scale_x + bbox[1] * (1 - scale_x)
                ymin = bbox[2] * scale_y
                xmax = scale_x + bbox[3] * (1 - scale_x)
                ymax = bbox[4] * scale_y
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax])
        elif i == 2:  # bottom-left
            img = cv2.resize(img, (divid_point_x, output_size[0] - divid_point_y))
            output_img[divid_point_y:output_size[0], :divid_point_x, :] = img
            for bbox in img_annos:
                xmin = bbox[1] * scale_x
                ymin = scale_y + bbox[2] * (1 - scale_y)
                xmax = bbox[3] * scale_x
                ymax = scale_y + bbox[4] * (1 - scale_y)
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax])
        else:  # bottom-right
            img = cv2.resize(img, (output_size[1] - divid_point_x, output_size[0] - divid_point_y))
            output_img[divid_point_y:output_size[0], divid_point_x:output_size[1], :] = img
            for bbox in img_annos:
                xmin = scale_x + bbox[1] * (1 - scale_x)
                ymin = scale_y + bbox[2] * (1 - scale_y)
                xmax = scale_x + bbox[3] * (1 - scale_x)
                ymax = scale_y + bbox[4] * (1 - scale_y)
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax])

    return output_img, new_anno


def get_dataset(anno_dir, img_dir):
    # class_id = category_name.index('person')

    img_paths = []
    annos = []
    for anno_file in glob.glob(os.path.join(anno_dir, '*.txt')):
    # for anno_file in glob.glob(os.path.join(anno_dir, '*.xml')):

        anno_id = anno_file.split('/')[-1].split('_')[0]
        # anno_id = anno_file.split('/')[-1].split('x')[0]
        # set_trace()

        # with open(anno_file, 'r') as f:
        #     num_of_objs = int(f.readline())

        # set_trace()
        img_path = os.path.join(img_dir, f'{anno_id}jpg')
        print(img_path)

        img = cv2.imread(img_path)
        # set_trace()
        img_height, img_width, _ = img.shape
        print(img.shape)
        del img

        boxes = []
        bnd_box = parseXmlFiles(anno_file)
        print(bnd_box)
        for bnd_id, box in enumerate(bnd_box):
            # set_trace()

            categories_id = box[0]

            xmin = max(int(box[1]), 0) / img_width

            ymin = max(int(box[2]), 0) / img_height

            xmax = min(int(box[3]), img_width) / img_width

            ymax = min(int(box[4]), img_height) / img_height

            boxes.append([categories_id, xmin, ymin, xmax, ymax])
            print(boxes)

            if not boxes:
                continue

        img_paths.append(img_path)
        annos.append(boxes)
    print("annos:所有对原图缩放后的坐标：", annos)
    print(img_paths)
    return img_paths, annos


def parseXmlFiles(anno_dir):
    tree = etree.parse(anno_dir)
    root = tree.getroot()
    objectes = root.findall('.//object')
    bnd_box = []
    for object in objectes:
        name = object.find("name").text

        bndbox = object.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        xmax = float(bndbox.find("xmax").text)
        ymin = float(bndbox.find("ymin").text)
        ymax = float(bndbox.find("ymax").text)

        # bnd_box.append([name, xmin, xmax, ymin, ymax])
        bnd_box.append([name, xmin, ymin, xmax, ymax])
        # print(len(bnd_box),bnd_box)
    return bnd_box


if __name__ == '__main__':
    main()
