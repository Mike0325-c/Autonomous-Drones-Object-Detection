import os
import cv2  # 用于读取图像

def normalize_bbox(bbox, image_width, image_height):
    x, y, width, height = bbox
    x_normalized = x / image_width
    y_normalized = y / image_height
    width_normalized = width / image_width
    height_normalized = height / image_height
    return [x_normalized, y_normalized, width_normalized, height_normalized]

# 文件夹路径
annotations_folder = 'annotations'
images_folder = 'images'
normalized_folder = 'normalized_annotations'

# 创建新文件夹以保存归一化后的数据
os.makedirs(normalized_folder, exist_ok=True)

# 获取所有图像文件
image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.png'))]

for image_file in image_files:
    # 获取对应的图像路径
    image_path = os.path.join(images_folder, image_file)
    # 读取图像以获取尺寸
    image = cv2.imread(image_path)
    image_height, image_width = image.shape[:2]

    # 获取对应的注释文件
    annotation_file = os.path.splitext(image_file)[0] + '.txt'  # 假设注释文件是txt格式
    annotation_path = os.path.join(annotations_folder, annotation_file)

    # 新的注释文件路径
    normalized_annotation_path = os.path.join(normalized_folder, annotation_file)

    # 读取注释文件并进行归一化
    with open(annotation_path, 'r') as f:
        with open(normalized_annotation_path, 'w') as nf:
            for line in f:
                # 解析行数据
                parts = line.strip().split(',')
                bbox = list(map(int, parts[:4]))  # 只提取坐标和尺寸
                normalized_bbox = normalize_bbox(bbox, image_width, image_height)

                # 替换原有坐标为归一化后的坐标
                normalized_line = f"{normalized_bbox[0]:.6f},{normalized_bbox[1]:.6f},{normalized_bbox[2]:.6f},{normalized_bbox[3]:.6f}," + ','.join(parts[4:]) + '\n'
                nf.write(normalized_line)

print(f"归一化后的坐标已保存到文件夹 '{normalized_folder}' 中。")
