import os

# 源文件夹路径
source_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\annotations'
# 目标文件夹路径
target_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\n_annotations'

# 如果目标文件夹不存在，则创建
os.makedirs(target_folder, exist_ok=True)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 构建源文件和目标文件的完整路径
    source_file_path = os.path.join(source_folder, filename)
    target_file_path = os.path.join(target_folder, filename)

    # 确保是文件而不是文件夹
    if os.path.isfile(source_file_path):
        with open(source_file_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        # 处理每一行
        for line in lines:
            # 去掉换行符并按逗号分割
            parts = line.strip().split(',')

            # 提取倒数第三个数字并将其移到第一个位置
            modified_line = [parts[-3]] + parts[: -3] + parts[-2:]

            # 重新合并成字符串，并添加到新行列表中
            new_lines.append(','.join(modified_line) + '\n')

        # 将修改后的内容写入到目标文件中
        with open(target_file_path, 'w') as f:
            f.writelines(new_lines)

print("Processing complete. The modified files are saved in the target folder.")
