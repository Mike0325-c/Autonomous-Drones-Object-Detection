import os


def delete_files_based_on_folders(source_folder, reference_folders, file_extension):
    # 遍历每个参考文件夹中的文件
    for ref_folder in reference_folders:
        for filename in os.listdir(ref_folder):
            # 构造文件名和文件路径
            file_base_name = os.path.splitext(filename)[0]  # 去除扩展名
            target_file = os.path.join(source_folder, file_base_name + file_extension)

            # 如果文件存在于源文件夹中，则删除
            if os.path.exists(target_file):
                os.remove(target_file)
                print(f"已删除文件：{target_file}")
            else:
                print(f"文件不存在或已删除：{target_file}")


# 参数设置
image_source_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\copy_img'  # 包含所有图片的文件夹路径
text_source_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\copy_annotions'  # 包含所有文本文件的文件夹路径

reference_folders = [r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\1_over80%-12600',
                     r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\4_over70%_38406']  # 包含目标文件的两个参考文件夹路径

# 删除图片
delete_files_based_on_folders(image_source_folder, reference_folders, '.jpg')  # 假设图片扩展名为 .jpg

# 删除文本文件
delete_files_based_on_folders(text_source_folder, reference_folders, '.txt')  # 假设文本文件扩展名为 .txt
