import os

# 文件夹路径
descriptions_folder = r'E:\FInal_data\After_Aug_text_Normalization_after_occ'

# 遍历描述文件夹
for filename in os.listdir(descriptions_folder):
    # 只处理.txt文件
    if filename.endswith('.txt'):
        file_path = os.path.join(descriptions_folder, filename)

        # 读取文件内容
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 过滤掉类别为1或4，且遮掩程度为0的行
        updated_lines = []
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) < 8:
                continue

            category = int(parts[0])
            occlusion = int(parts[7])

            # 只保留非类别1或4，或者遮掩程度不为0的行
            if not (category == 1 or category == 4):
                updated_lines.append(line)

        # 写回文件
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)

print("所有符合条件的对象已从描述文件中删除。")
