import os
from collections import Counter
import matplotlib.pyplot as plt


def count_categories_in_text_files(directory_path):
    category_counts = Counter()

    # 遍历文件夹中的每个文件
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            # 读取文件的每一行
            with open(os.path.join(directory_path, filename), 'r') as file:
                for line in file:
                    # 通过逗号分割行，将每一部分解析为列表
                    parts = line.strip().split(',')

                    # 如果最后一个数字为2，表示严重遮挡，跳过计数
                    if int(parts[7]) == 2:
                        continue

                    # 获取第一个数字作为类别
                    category = int(parts[0])
                    # 增加该类别的计数
                    category_counts[category] += 1

    return category_counts


# 使用文件夹路径调用函数
directory_path = r'E:\FInal_data\After_Aug_text_Normalization_after_occ'  # 替换为你的文件夹路径
category_counts = count_categories_in_text_files(directory_path)

# 打印每个类别的具体数量
print("类别数量统计：")
for category, count in category_counts.items():
    print(f"类别 {category}: {count} 个")

# 绘制柱状图
plt.figure(figsize=(10, 6))
bars = plt.bar(category_counts.keys(), category_counts.values())
plt.xlabel('Category')
plt.ylabel('Count')
plt.title('Count of Each Category in Text Files')
plt.xticks(range(12))  # 假设类别是从0到11

# 在每个柱顶端显示数量
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 5, int(yval), ha='center', va='bottom')

plt.show()
