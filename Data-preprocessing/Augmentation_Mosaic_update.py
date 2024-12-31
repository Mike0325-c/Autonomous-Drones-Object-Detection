import random
import cv2
import os
import glob
import numpy as np
from PIL import Image
from lxml import etree
from ipdb import set_trace

OUTPUT_SIZE = (765, 1360)  # Height, Width
SCALE_RANGE = (0.5, 0.5)
FILTER_TINY_SCALE = 1 / 50  # if height or width lower than this scale, drop it.

ANNO_DIR = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\before_Augmentation_text'#需要被增强的文件的描述文件
IMG_DIR = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\before_Augmentation_img'#需要被增强的文件的图片文件
# category_name = ['background', 'person']

def main():
    rounds = 30  # 设置增强轮数
    img_paths, annos = get_dataset(ANNO_DIR, IMG_DIR)

    # 创建保存图像和描述文件的目标文件夹
    img_save_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_Aug'  # 保存纯图片
    bbox_img_save_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_Aug_bbox'  # 保存有bbox图片
    anno_save_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_Aug_text_Normalization'  # 保存归一化后的图片
    os.makedirs(img_save_dir, exist_ok=True)
    os.makedirs(bbox_img_save_dir, exist_ok=True)
    os.makedirs(anno_save_dir, exist_ok=True)

    for round_num in range(rounds):
        for i in range(len(annos)):
            # 每次包含索引 `i` 和其他随机选择的3个索引
            other_idxs = [j for j in range(len(annos)) if j != i]
            idxs = [i] + random.sample(other_idxs, 3)

            # 生成新图像和描述
            new_image, new_annos = update_image_and_anno(img_paths, annos, idxs, OUTPUT_SIZE, SCALE_RANGE, filter_scale=FILTER_TINY_SCALE)

            # 保存不含标注框的新图像
            img_save_path = os.path.join(img_save_dir, f'wind_output_round{round_num}_img_{i}.jpg')  # 加上轮次和索引编号
            cv2.imwrite(img_save_path, new_image)

            # 在图像上绘制边界框
            for anno in new_annos:
                start_point = (int(anno[1] * OUTPUT_SIZE[1]), int(anno[2] * OUTPUT_SIZE[0]))  # 左上角点
                end_point = (int(anno[3] * OUTPUT_SIZE[1]), int(anno[4] * OUTPUT_SIZE[0]))  # 右下角点
                cv2.rectangle(new_image, start_point, end_point, (0, 255, 0), 1, cv2.LINE_AA)

            # 保存带标注框的图像
            bbox_img_save_path = os.path.join(bbox_img_save_dir, f'wind_output_round{round_num}_bbox_{i}.jpg')  # 加上轮次和索引编号
            cv2.imwrite(bbox_img_save_path, new_image)

            # 保存描述文件
            anno_save_path = os.path.join(anno_save_dir, f'wind_output_round{round_num}_text_{i}.txt')  # 加上轮次和索引编号
            with open(anno_save_path, 'w') as f:
                for anno in new_annos:
                    f.write(f"{anno[0]},{anno[1]:.6f},{anno[2]:.6f},{anno[3]:.6f},{anno[4]:.6f},{anno[5]},{anno[6]},{anno[7]}\n")

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
        # set_trace()
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
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax,bbox[5],bbox[6],bbox[7]])

        elif i == 1:  # top-right
            img = cv2.resize(img, (output_size[1] - divid_point_x, divid_point_y))
            output_img[:divid_point_y, divid_point_x:output_size[1], :] = img
            for bbox in img_annos:
                xmin = scale_x + bbox[1] * (1 - scale_x)
                ymin = bbox[2] * scale_y
                xmax = scale_x + bbox[3] * (1 - scale_x)
                ymax = bbox[4] * scale_y
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax,bbox[5],bbox[6],bbox[7]])
        elif i == 2:  # bottom-left
            img = cv2.resize(img, (divid_point_x, output_size[0] - divid_point_y))
            output_img[divid_point_y:output_size[0], :divid_point_x, :] = img
            for bbox in img_annos:
                xmin = bbox[1] * scale_x
                ymin = scale_y + bbox[2] * (1 - scale_y)
                xmax = bbox[3] * scale_x
                ymax = scale_y + bbox[4] * (1 - scale_y)
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax,bbox[5],bbox[6],bbox[7]])
        else:  # bottom-right
            img = cv2.resize(img, (output_size[1] - divid_point_x, output_size[0] - divid_point_y))
            output_img[divid_point_y:output_size[0], divid_point_x:output_size[1], :] = img
            for bbox in img_annos:
                xmin = scale_x + bbox[1] * (1 - scale_x)
                ymin = scale_y + bbox[2] * (1 - scale_y)
                xmax = scale_x + bbox[3] * (1 - scale_x)
                ymax = scale_y + bbox[4] * (1 - scale_y)
                new_anno.append([bbox[0], xmin, ymin, xmax, ymax,bbox[5],bbox[6],bbox[7]])

    return output_img, new_anno
def get_dataset(anno_dir, img_dir):
    img_paths = []
    annos = []

    # 遍历标注文件夹中所有 .txt 文件
    for anno_file in glob.glob(os.path.join(anno_dir, '*.txt')):

        img_path = os.path.join(img_dir, os.path.basename(anno_file).replace('.txt', '.jpg'))

        # 读取图像以获取宽高信息
        img = cv2.imread(img_path)
        if img is None:
            print(f"Image {img_path} not found.")
            continue

        img_height, img_width, _ = img.shape
        print(f"Image size: {img.shape}")
        del img  # 释放图像资源

        boxes = []

        # 打开标注文件并读取内容
        with open(anno_file, 'r') as f:
            for line in f:
                values = line.strip().split(',')

                # 提取类别ID和位置信息
                categories_id = int(values[0])
                xmin = max(int(values[1]), 0) / img_width
                ymin = max(int(values[2]), 0) / img_height
                width = int(values[3]) / img_width
                height = int(values[4]) / img_height
                xmax = min(xmin + width, 1.0)  # 确保坐标不超过边界
                ymax = min(ymin + height, 1.0)#归一化
                aaa=int(values[5])
                bbbb=int(values[6])
                ccc=int(values[7])
                # categories_id = int(values[0])
                # xmin = max(int(values[1]), 0)  # 不进行归一化
                # ymin = max(int(values[2]), 0)  # 不进行归一化
                # width = int(values[3])  # 不进行归一化
                # height = int(values[4])  # 不进行归一化
                # xmax = xmin + width  # 计算右下角点
                # ymax = ymin + height#非归一化

                # 将每个框的信息存入boxes列表
                boxes.append([categories_id, xmin, ymin, xmax, ymax,aaa,bbbb,ccc])
                print(f"Processed box: {boxes[-1]}")

        # 如果有标注框信息，将图像路径和标注添加到结果列表
        if boxes:
            img_paths.append(img_path)
            annos.append(boxes)


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
