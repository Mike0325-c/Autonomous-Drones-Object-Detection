import os
import shutil
from collections import Counter


def find_texts_for_augmentation(text_folder, target_folder, target_categories, threshold):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    selected_files = []  # 用于记录符合条件的text文件

    # 遍历每个text文件
    for filename in os.listdir(text_folder):
        if filename.endswith(".txt"):
            # 读取文件并统计类别数量
            category_counts = Counter()
            with open(os.path.join(text_folder, filename), 'r') as file:
                for line in file:
                    category = int(line.split(',')[0])
                    # 只统计目标类别
                    if category in target_categories:
                        category_counts[category] += 1

            # 检查是否有任何一个目标类别的数量超过阈值
            for category in target_categories:
                if category_counts[category] >= threshold:
                    selected_files.append(filename)  # 添加到符合条件的文件列表
                    break  # 一旦满足条件就可以跳出检查，避免重复

    # 显示符合条件的文件数量并等待用户确认
    print(f"共有 {len(selected_files)} 个符合条件的text文件。")
    input("按下回车键以复制这些文件到目标文件夹...")

    # 将符合条件的text文件复制到目标文件夹
    for filename in selected_files:
        source_path = os.path.join(text_folder, filename)
        target_path = os.path.join(target_folder, filename)
        shutil.copy(source_path, target_path)

    print(f"已复制 {len(selected_files)} 个text文件到 {target_folder} 用于数据增强。")


# 参数设置
text_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\n_annotations'  # 存放文本文件的文件夹路径
target_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\9'  # 存放符合条件文本文件的目标文件夹路径
target_categories = [9]  # 目标类别36789
threshold = 35# 数量阈值，可以调整

# 运行函数
find_texts_for_augmentation(text_folder, target_folder, target_categories, threshold)
