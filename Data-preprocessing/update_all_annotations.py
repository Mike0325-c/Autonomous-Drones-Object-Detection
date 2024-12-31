import os
import cv2
import glob

# 输入目录
ORIGINAL_ANNO_DIR = r'E:\FInal_data\n_annotations'  # 不需要增强的数据集描述文件路径
ORIGINAL_IMG_DIR = r'E:\FInal_data\images'  # 图像文件路径

# 输出目录
UPDATED_ANNO_DIR = r'E:\FInal_data\n_annotations_update'  # 统一格式后的描述文件保存路径
OUTPUT_BBOX_IMG_DIR = r'E:\FInal_data\images_bbox'  # 保存包含bbox可视化的图像路径

# 创建输出文件夹
os.makedirs(UPDATED_ANNO_DIR, exist_ok=True)
os.makedirs(OUTPUT_BBOX_IMG_DIR, exist_ok=True)


def convert_annotations_and_visualize():
    for anno_file in glob.glob(os.path.join(ORIGINAL_ANNO_DIR, '*.txt')):
        img_path = os.path.join(ORIGINAL_IMG_DIR, os.path.basename(anno_file).replace('.txt', '.jpg'))
        img = cv2.imread(img_path)

        if img is None:
            print(f"Image {img_path} not found.")
            continue

        img_height, img_width, _ = img.shape
        boxes = []

        # 读取描述文件
        with open(anno_file, 'r') as f:
            for line in f:
                values = line.strip().split(',')
                categories_id = int(values[0])
                xmin = max(int(values[1]), 0) / img_width
                ymin = max(int(values[2]), 0) / img_height
                width = int(values[3]) / img_width
                height = int(values[4]) / img_height
                xmax = min(xmin + width, 1.0)
                ymax = min(ymin + height, 1.0)
                aaa = int(values[5])
                bbbb = int(values[6])
                ccc = int(values[7])

                # 保存格式转换后的bbox
                boxes.append([categories_id, xmin, ymin, xmax, ymax, aaa, bbbb, ccc])

                # 绘制边界框
                start_point = (int(xmin * img_width), int(ymin * img_height))
                end_point = (int(xmax * img_width), int(ymax * img_height))
                cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)

        # 保存转换后的描述文件
        updated_anno_path = os.path.join(UPDATED_ANNO_DIR, os.path.basename(anno_file))
        with open(updated_anno_path, 'w') as f:
            for box in boxes:
                f.write(f"{box[0]},{box[1]:.6f},{box[2]:.6f},{box[3]:.6f},{box[4]:.6f},{box[5]},{box[6]},{box[7]}\n")

        # 保存带bbox的可视化图像
        bbox_img_save_path = os.path.join(OUTPUT_BBOX_IMG_DIR, os.path.basename(img_path))
        cv2.imwrite(bbox_img_save_path, img)
        print(f"Processed and saved: {bbox_img_save_path}")


if __name__ == "__main__":
    convert_annotations_and_visualize()
