import os
import random
from PIL import Image, ImageDraw, ImageFile

# 忽略图片截断错误
ImageFile.LOAD_TRUNCATED_IMAGES = True


def reduce_objects(directory_path, image_folder, target_counts):
    count_1, count_4 = 0, 0  # 初始化计数
    target_count_1, target_count_4 = target_counts

    # 获取所有描述文件并打乱顺序
    files = [f for f in os.listdir(directory_path) if f.endswith(".txt")]
    random.shuffle(files)

    for filename in files:
        # 停止条件：满足目标数量
        if count_1 >= target_count_1 and count_4 >= target_count_4:
            break

        # 读取描述文件
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 标记是否修改该文件
        modified = False
        new_lines = []

        # 遍历每一行，找到符合条件的对象
        for line in lines:
            parts = line.strip().split(',')

            # 检查是否符合条件：第一个数字为1或4，第八个数字为0
            category = int(parts[0])
            occlusion = int(parts[7])
            if (category == 1 and count_1 < target_count_1 and occlusion == 0) or \
                    (category == 4 and count_4 < target_count_4 and occlusion == 0):

                # 读取bbox信息并进行遮挡
                x, y, w, h = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])

                # 检查宽度和高度是否为正数
                if w > 0 and h > 0:
                    image_name = os.path.splitext(filename)[0] + ".jpg"
                    image_path = os.path.join(image_folder, image_name)

                    if os.path.exists(image_path):
                        try:
                            # 尝试加载和验证图片
                            with Image.open(image_path) as img:
                                img.verify()  # 验证图片是否损坏
                            with Image.open(image_path) as img:
                                # 在图片上遮挡对象
                                draw = ImageDraw.Draw(img)
                                draw.rectangle([(x, y), (x + w, y + h)], fill=(0, 0, 0))  # 使用黑色遮挡
                                img.save(image_path)  # 保存遮挡后的图片以替换原图

                            # 修改第八个数字为2，表示严重遮挡
                            parts[7] = '2'
                            modified = True

                            # 更新计数
                            if category == 1:
                                count_1 += 1
                            elif category == 4:
                                count_4 += 1

                        except (OSError, AttributeError) as e:
                            print(f"跳过损坏或截断的图片 {image_path}：{e}")
                            continue  # 跳过无法处理的图片

            # 将修改后的行添加到新行列表
            new_lines.append(','.join(parts))

            # 检查是否达到目标数量
            if count_1 >= target_count_1 and count_4 >= target_count_4:
                break

        # 如果该文件被修改，更新描述文件内容
        if modified:
            with open(file_path, 'w') as file:
                file.write('\n'.join(new_lines))  # 替换原描述文件内容

    print(f"遮挡完成：种类1的对象遮挡数量为 {count_1}，种类4的对象遮挡数量为 {count_4}")


# 参数设置
directory_path = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\copy_annotions'  # 描述文件夹路径
image_folder = r'D:\self_document\Australia\UNSW\2024\T3\COMP9444\group_p\VisDrone2019-DET-train\copy_img'  # 图片文件夹路径
target_counts = (0, 40000)  # 目标遮挡数量：种类1为40000，种类4为70000

# 运行函数
reduce_objects(directory_path, image_folder, target_counts)
