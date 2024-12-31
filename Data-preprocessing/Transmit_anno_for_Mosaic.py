import os

# 定义输入和输出路径
annotation_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Augmentation_text'
output_dir = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Mosaic_text'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 遍历 annotation 文件
for filename in os.listdir(annotation_dir):
    if filename.endswith('.txt'):
        input_path = os.path.join(annotation_dir, filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
            for line in infile:
                # 分割行内容，转换为数字列表
                parts = line.strip().split(',')

                # 只保留第二到第五列（索引 1 到 4）
                selected_parts = parts[0:5]

                # 将保留的内容重新组合成字符串，并写入新文件
                outfile.write(','.join(selected_parts) + '\n')

print("处理完成，关键位置信息已保存到新的文件夹中。")
