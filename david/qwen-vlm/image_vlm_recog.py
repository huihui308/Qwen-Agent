
"""
    sudo apt install fonts-wqy-microhei fonts-noto-cjk

"""

import os, random, shutil
from pathlib import Path
from dashscope import MultiModalConversation
import dashscope
from PIL import Image, ImageDraw, ImageFont


# 设置你的 API Key（需提前在阿里云百炼平台获取）
dashscope.api_key = "sk-5a3fe1f20d1a408e8560ded9f2e22525"


# windows
# def add_chinese_text_to_image(input_image_path, output_image_path, text, position, font_size=20, text_color=(0, 0, 0)):
#     img = Image.open(input_image_path)
#     draw = ImageDraw.Draw(img)
    
#     # Use a font that supports Chinese characters on Windows
#     try:
#         font_path = r"C:\Windows\Fonts\msyh.ttc"  # Microsoft YaHei
#         font = ImageFont.truetype(font_path, font_size)
#     except:
#         try:
#             font_path = r"C:\Windows\Fonts\simhei.ttf"  # SimHei
#             font = ImageFont.truetype(font_path, font_size)
#         except:
#             font = ImageFont.load_default()
#             print("Warning: Chinese font not found, text may display incorrectly")
    
#     draw.text(position, text, font=font, fill=text_color)
#     img.save(output_image_path)
#     print(f"Image with text saved to: {output_image_path}")


def add_chinese_text_to_image(input_image_path, output_image_path, text, position, font_size=20, text_color=(0, 0, 0)):
    """
    Add Chinese text to an image and save the result
    
    Args:
        input_image_path (str): Path to input image
        output_image_path (str): Path to save output image
        text (str): Chinese text to add
        position (tuple): (x, y) coordinates for text position
        font_size (int): Font size
        text_color (tuple): RGB color for text
    """
    # Open the image
    img = Image.open(input_image_path)
    draw = ImageDraw.Draw(img)
    
    # Use a font that supports Chinese characters
    try:
        # Try to use a system font that supports Chinese
        font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"  # Common on Ubuntu
        font = ImageFont.truetype(font_path, font_size)
    except:
        try:
            # Fallback to another common Chinese font
            font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
            font = ImageFont.truetype(font_path, font_size)
        except:
            # Final fallback - will display incorrectly if system lacks Chinese fonts
            font = ImageFont.load_default()
            print("Warning: Chinese font not found, text may display incorrectly")
    
    # Add text to image
    draw.text(position, text, font=font, fill=text_color)
    
    # Save the image
    img.save(output_image_path)
    print(f"Image with text saved to: {output_image_path}")


def prepare_directory_simple(directory_path, class_cnt):
    """More concise version that removes and recreates the directory"""
    dir_path = Path(directory_path)
    if dir_path.exists():
        shutil.rmtree(dir_path)
    dir_path.mkdir(parents=True)
    for i in range(class_cnt):
        sub_dir = os.path.join(directory_path, str(i))
        # print(sub_dir)
        dir_path = Path(sub_dir)
        dir_path.mkdir(parents=True)


def get_image_files(directory, extensions=None):
    """
    Get all image files from a directory and its subdirectories.
    
    Args:
        directory (str): Path to the directory to scan
        extensions (list, optional): List of image extensions to include.
            Defaults to common image extensions.
    
    Returns:
        list: List of absolute paths to image files
    """
    if extensions is None:
        extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.tiff', '.webp', '.svg', '.heic', '.raw'
        ]
    
    image_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in extensions:
                image_files.append(os.path.join(root, file))
    
    return image_files


def get_random_image_files(directory, sample_size=10, extensions=None):
    """
    Get random image files from a directory and its subdirectories.
    
    Args:
        directory (str): Path to the directory to scan
        sample_size (int): Number of random files to return
        extensions (list, optional): List of image extensions to include.
            Defaults to common image extensions.
    
    Returns:
        list: List of absolute paths to randomly selected image files
    """
    if extensions is None:
        extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.tiff', '.webp', '.svg', '.heic', '.raw'
        ]
    
    all_images = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in extensions:
                all_images.append(os.path.join(root, file))
    
    # Ensure we don't try to sample more than available
    sample_size = min(sample_size, len(all_images))
    
    return random.sample(all_images, sample_size)


def write_result_copy_image(local_file_path, save_directory, dir_num, result):
    save_image_name = os.path.join(save_directory, dir_num, os.path.basename(local_file_path))
    print('save_image_name: {}'.format(save_image_name))
    add_chinese_text_to_image(local_file_path, save_image_name, result, (50, 50), 80, (0, 0, 255))


def call_with_local_file():
    """Sample of use local file.
       linux&mac file schema: file:///home/images/test.png
       windows file schema: file://D:/images/abc.png
    """
    save_directory = '/home/david/david/code/Qwen-Agent/david/qwen-vlm/results'
    directory_path = '/home/david/david/code/Qwen-Agent/david/qwen-vlm/images'
    test_cnt = 20
    class_cnt = 7

    prepare_directory_simple(save_directory, class_cnt)
    images = get_random_image_files(directory_path, test_cnt)
    
    print(f"Found {len(images)} image files:")
    result_list = [0 for _ in range(7)]
    # print(result_list)
    for local_file_path in images:  # Print first 10 as example
        # print(local_file_path)
        # local_file_path = '/home/david/david/code/Qwen-Agent/david/images/444.jpg'
        messages = [{
            'role': 'system',
            'content': [{
                'text': 'You are a helpful assistant.'
            }]
        }, {
            'role':
            'user',
            'content': [
                {
                    'image': local_file_path
                },
                {
                    'text': "将这张图片进行分类，列别包括动植物、自然景观、人物、美食、交通、设施建筑、文化艺术。分类时需要遵守如下规则：1、如果照片中出现人物，输出列别必须包含人物列别; 2、如果图片中出现美食，输出列别为美食。3、输出结果为其中一个或两个最有可能的列别，不需要说明原因，输出结果只有列别名称，不要输出其他内容。"
                },
            ]
        }]
        response = MultiModalConversation.call(model='qwen-vl-plus', messages=messages)
        print(response)
        print('---------------------------')
        if response.status_code == 200:
            result = response.output.choices[0].message.content[0]['text']
            print('result: {}'.format(result))
            # print("图片情感分析结果：")
            # print(result)

            dir_num = "0"
            if "动植物" in result:
                result_list[0] = result_list[0] + 1
                dir_num = "0"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            elif "动物" in result:
                result_list[0] = result_list[0] + 1
                dir_num = "0"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            elif "植物" in result:
                result_list[0] = result_list[0] + 1
                dir_num = "0"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            if "自然景观" in result:
                result_list[1] = result_list[1] + 1
                dir_num = "1"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            if "人物" in result:
                result_list[2] = result_list[2] + 1
                dir_num = "2"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            if "美食" in result:
                result_list[3] = result_list[3] + 1
                dir_num = "3"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            if "交通" in result:
                result_list[4] = result_list[4] + 1
                dir_num = "4"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            if "设施建筑" in result:
                result_list[5] = result_list[5] + 1
                dir_num = "5"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
            if "文化艺术" in result:
                result_list[6] = result_list[6] + 1
                dir_num = "6"
                write_result_copy_image(local_file_path, save_directory, dir_num, result)
        else:
            print(f"请求失败：{response.message}")
    result_list = [val/test_cnt for val in result_list]
    print(result_list)
    print('-------------- results --------------')
    print('动植物: {}'.format(result_list[0]))
    print('自然景观: {}'.format(result_list[1]))
    print('人物: {}'.format(result_list[2]))
    print('美食: {}'.format(result_list[3]))
    print('美食: {}'.format(result_list[4]))
    print('设施建筑: {}'.format(result_list[5]))
    print('文化艺术: {}'.format(result_list[6]))
    print('-------------------------------------')


if __name__ == '__main__':
    call_with_local_file()