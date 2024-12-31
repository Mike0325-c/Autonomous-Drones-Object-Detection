import os
import shutil


def copy_images_based_on_texts(text_folder, image_folder, target_folder):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 遍历合并文件夹中的每个文本文件
    for filename in os.listdir(text_folder):
        if filename.endswith(".txt"):
            # 去除文件扩展名以获取对应的图片文件名
            file_base_name = os.path.splitext(filename)[0]
            image_path = os.path.join(image_folder, file_base_name + ".jpg")  # 假设图片格式为.jpg

            # 检查图片是否存在并复制到目标文件夹
            if os.path.exists(image_path):
                shutil.copy(image_path, os.path.join(target_folder, file_base_name + ".jpg"))
            else:
                print(f"图片 {file_base_name}.jpg 不存在于 {image_folder} 中。")

    print(f"已将所有对应的图片复制到 {target_folder}。")


# 参数设置
text_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Augmentation_text'  # 合并文本文件的文件夹路径
image_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\images'  # 图片文件夹的路径
target_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\Augmentation_img'  # 新图片文件夹的路径

# 运行函数
copy_images_based_on_texts(text_folder, image_folder, target_folder)
