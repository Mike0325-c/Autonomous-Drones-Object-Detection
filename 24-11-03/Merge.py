import os
import shutil


def merge_text_files(source_folders, target_folder):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 用于跟踪已经复制的文件，避免重复
    copied_files = set()

    # 遍历每个源文件夹
    for folder in source_folders:
        for filename in os.listdir(folder):
            if filename.endswith(".txt") and filename not in copied_files:
                # 复制文件到目标文件夹
                source_path = os.path.join(folder, filename)
                target_path = os.path.join(target_folder, filename)
                shutil.copy(source_path, target_path)
                copied_files.add(filename)  # 记录已复制的文件名

    print(f"已将来自 {len(source_folders)} 个文件夹的文件合并到 {target_folder} 中，共合并 {len(copied_files)} 个文件。")


# 参数设置
source_folders = [

    r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\3',  # 替换为类别3的文件夹路径
    r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\6',  # 替换为类别6的文件夹路径
    r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\7',  # 替换为类别7的文件夹路径
    r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\8',  # 替换为类别8的文件夹路径
    r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\9',  # 替换为类别9的文件夹路径

]
target_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Augmentation_text'  # 替换为新文件夹的路径

# 运行函数
merge_text_files(source_folders, target_folder)
