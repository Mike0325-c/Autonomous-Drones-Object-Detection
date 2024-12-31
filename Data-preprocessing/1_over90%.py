import os
import shutil
from collections import Counter


def find_and_copy_majority_class_files(text_folder, target_folder, target_classes, threshold):
    # 用于记录符合条件的文件和目标类别对象的总数
    selected_files = []
    total_target_count = 0

    # 遍历text文件夹中的每个文件
    for filename in os.listdir(text_folder):
        if filename.endswith(".txt"):
            # 读取文件并统计类别数量
            category_counts = Counter()
            total_count = 0
            with open(os.path.join(text_folder, filename), 'r') as file:
                for line in file:
                    category = int(line.split(',')[0])
                    category_counts[category] += 1
                    total_count += 1

            # 计算目标类别的比例
            target_count = sum(count for cat, count in category_counts.items() if cat in target_classes)
            if total_count > 0 and (target_count / total_count) >= threshold:
                # 符合条件的文件记录到列表
                selected_files.append(filename)
                total_target_count += target_count

    # 显示统计信息并等待用户确认
    print(f"共有 {len(selected_files)} 个文件符合条件。")
    print(f"在这些文件中，类别 {target_classes} 的对象总数为 {total_target_count}。")
    input("按下回车键以复制这些文件到目标文件夹...")

    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 将符合条件的文件复制到目标文件夹
    for filename in selected_files:
        source_path = os.path.join(text_folder, filename)
        target_path = os.path.join(target_folder, filename)
        shutil.copy(source_path, target_path)

    print(f"已将 {len(selected_files)} 个文件复制到 {target_folder}。")


# 参数设置
text_folder = r'E:\FInal_data\n_annotations'  # 替换为存放文本文件的文件夹路径
target_folder = r'E:\FInal_data\1_over'  # 替换为目标文件夹路径
target_classes = [1]  # 目标类别
threshold = 0.5  # 阈值%

# 运行函数
find_and_copy_majority_class_files(text_folder, target_folder, target_classes, threshold)
