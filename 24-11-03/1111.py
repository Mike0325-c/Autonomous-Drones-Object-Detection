import os
import random
import cv2

def main():
    img_paths, annos = get_dataset(ANNO_DIR, IMG_DIR)

    # 创建保存图像和描述文件的目标文件夹
    img_save_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_Aug'
    bbox_img_save_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_Aug_bbox'
    anno_save_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\After_Aug_text'
    os.makedirs(img_save_dir, exist_ok=True)
    os.makedirs(bbox_img_save_dir, exist_ok=True)
    os.makedirs(anno_save_dir, exist_ok=True)

    for i in range(len(annos)):
        # 每次包含索引 `i` 和其他随机选择的3个索引
        other_idxs = [j for j in range(len(annos)) if j != i]
        idxs = [i] + random.sample(other_idxs, 3)

        # 生成新图像和描述
        new_image, new_annos = update_image_and_anno(img_paths, annos, idxs, OUTPUT_SIZE, SCALE_RANGE, filter_scale=FILTER_TINY_SCALE)

        # 保存不含标注框的新图像
        img_save_path = os.path.join(img_save_dir, f'wind_output_{i}.jpg')
        cv2.imwrite(img_save_path, new_image)

        # 在图像上绘制边界框
        for anno in new_annos:
            start_point = (int(anno[1] * OUTPUT_SIZE[1]), int(anno[2] * OUTPUT_SIZE[0]))  # 左上角点
            end_point = (int(anno[3] * OUTPUT_SIZE[1]), int(anno[4] * OUTPUT_SIZE[0]))  # 右下角点
            cv2.rectangle(new_image, start_point, end_point, (0, 255, 0), 1, cv2.LINE_AA)

        # 保存带标注框的图像
        bbox_img_save_path = os.path.join(bbox_img_save_dir, f'wind_output_bbox_{i}.jpg')
        cv2.imwrite(bbox_img_save_path, new_image)

        # 保存描述文件
        anno_save_path = os.path.join(anno_save_dir, f'wind_output_{i}.txt')
        with open(anno_save_path, 'w') as f:
            for anno in new_annos:
                # 将每个边界框按格式写入文件，格式为：类别ID, xmin, ymin, xmax, ymax
                f.write(f"{anno[0]},{anno[1]:.6f},{anno[2]:.6f},{anno[3]:.6f},{anno[4]:.6f}\n")
