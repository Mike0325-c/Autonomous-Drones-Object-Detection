import os
import random
import shutil
from PIL import Image, ImageOps
import numpy as np


def augment_image_and_annotations(img_path, anno_path, img_output_folder, anno_output_folder, augment_times=3):
    # 确保输出文件夹存在
    os.makedirs(img_output_folder, exist_ok=True)
    os.makedirs(anno_output_folder, exist_ok=True)

    # 加载图片和注释
    image = Image.open(img_path)
    with open(anno_path, 'r') as file:
        annotations = [line.strip().split(',') for line in file]

    # 增强类型和次数
    augmentations = ["crop", "translate", "mirror", "rotate"]

    # 对每种增强进行 augment_times 次
    for aug_type in augmentations:
        for i in range(augment_times):
            # 随机生成增强参数
            augmented_image, new_annotations = apply_augmentation(image, annotations, aug_type)

            # 构建新的文件名
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            new_img_name = f"{base_name}_{aug_type}_{i}.jpg"
            new_anno_name = f"{base_name}_{aug_type}_{i}.txt"

            # 保存增强后的图片和注释文件
            augmented_image.save(os.path.join(img_output_folder, new_img_name))
            with open(os.path.join(anno_output_folder, new_anno_name), 'w') as f:
                for anno in new_annotations:
                    f.write(','.join(map(str, anno)) + '\n')


def apply_augmentation(image, annotations, aug_type):
    width, height = image.size
    new_annotations = []

    if aug_type == "crop":
        # 随机裁剪区域，裁剪图像并调整注释
        crop_x = random.randint(0, int(width * 0.1))
        crop_y = random.randint(0, int(height * 0.1))
        crop_w = width - random.randint(0, int(width * 0.1))
        crop_h = height - random.randint(0, int(height * 0.1))
        augmented_image = image.crop((crop_x, crop_y, crop_w, crop_h))

        # 更新 bbox
        for anno in annotations:
            x, y, w, h = int(anno[1]), int(anno[2]), int(anno[3]), int(anno[4])
            x_new, y_new = max(0, x - crop_x), max(0, y - crop_y)
            w_new, h_new = min(w, crop_w - x_new), min(h, crop_h - y_new)
            new_annotations.append([anno[0], x_new, y_new, w_new, h_new, anno[5], anno[6], anno[7]])

    elif aug_type == "translate":
        # 随机平移距离，平移图像并调整注释
        trans_x = random.randint(-int(width * 0.1), int(width * 0.1))
        trans_y = random.randint(-int(height * 0.1), int(height * 0.1))

        # 创建新图像并将原图平移后粘贴
        augmented_image = Image.new("RGB", (width, height))
        augmented_image.paste(image, (trans_x, trans_y))

        # 更新 bbox
        for anno in annotations:
            x, y, w, h = int(anno[1]), int(anno[2]), int(anno[3]), int(anno[4])
            x_new, y_new = max(0, x + trans_x), max(0, y + trans_y)
            new_annotations.append([anno[0], x_new, y_new, w, h, anno[5], anno[6], anno[7]])

    elif aug_type == "mirror":
        # 镜像图片并调整注释
        augmented_image = ImageOps.mirror(image)

        # 更新 bbox
        for anno in annotations:
            x, y, w, h = int(anno[1]), int(anno[2]), int(anno[3]), int(anno[4])
            x_new = width - x - w
            new_annotations.append([anno[0], x_new, y, w, h, anno[5], anno[6], anno[7]])

    elif aug_type == "rotate":
        # 随机旋转角度，旋转图像并调整注释
        angle = random.choice([15, 30, 45])  # 选择随机角度
        augmented_image = image.rotate(angle, expand=True)
        new_width, new_height = augmented_image.size
        rad = np.deg2rad(angle)

        for anno in annotations:
            x, y, w, h = int(anno[1]), int(anno[2]), int(anno[3]), int(anno[4])
            x_center = x + w / 2
            y_center = y + h / 2

            # 旋转bbox中心点
            x_rot = new_width / 2 + (x_center - width / 2) * np.cos(rad) - (y_center - height / 2) * np.sin(rad)
            y_rot = new_height / 2 + (x_center - width / 2) * np.sin(rad) + (y_center - height / 2) * np.cos(rad)

            new_annotations.append([anno[0], int(x_rot - w / 2), int(y_rot - h / 2), w, h, anno[5], anno[6], anno[7]])

    return augmented_image, new_annotations


# 参数设置
input_image_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Aug_11'  # 待增强图片文件夹路径
input_anno_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\11'  # 待增强文本文件夹路径
output_image_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_11_img'  # 增强后图片文件夹路径
output_anno_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_11_text'  # 增强后文本文件夹路径

# 遍历文件夹，逐个增强
for img_file in os.listdir(input_image_folder):
    if img_file.endswith(".jpg"):  # 假设图片文件为 .jpg
        img_path = os.path.join(input_image_folder, img_file)
        anno_path = os.path.join(input_anno_folder, os.path.splitext(img_file)[0] + ".txt")
        augment_image_and_annotations(img_path, anno_path, output_image_folder, output_anno_folder)
