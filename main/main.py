#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- 作者： codervibe -*-
# -*- 时间: 18 ：46 -*-
# -*- 图片隐写术 -*-
# -*-  2.0.0 -*-

VERSION = "2.0.0"

# 导入所需的库
import os
from PIL import Image
import argparse


def validate_image_path(image_path):
    """
    验证图像文件路径是否有效。

    :param image_path: 图像文件的路径
    :return: 有效的图像文件路径
    :raises argparse.ArgumentTypeError: 如果图像文件不存在，则引发异常
    """
    if not os.path.exists(image_path):
        raise argparse.ArgumentTypeError("图像文件不存在。")
    return image_path


def validate_message(message):
    """
    验证消息内容是否有效。

    :param message: 要隐藏的消息
    :return: 验证通过的消息内容
    :raises argparse.ArgumentTypeError: 如果消息为空，则引发异常
    """
    if not message:
        raise argparse.ArgumentTypeError("消息不能为空。")
    return message


def hide_message(image_path, message):
    """
    将消息隐藏到图像中。

    :param image_path: 图像文件的路径
    :param message: 要隐藏的消息
    """
    try:
        # 打开图像文件
        img = Image.open(image_path)
        # 获取图像的像素数据
        data = img.getdata()
        encoded_data = []
        # 在消息末尾添加一个空字符，以便在解码时知道消息的结束
        message += "\0"
        # 将消息转换为二进制字符串
        message_bits = ''.join(format(ord(char), '08b') for char in message)
        message_length = len(message_bits)

        # 检查消息长度是否超过了图像像素数的三倍，如果是，则无法隐藏消息
        if len(data) * 3 < message_length:
            raise ValueError("消息过长，无法隐藏在图像中。")

        # 检查消息中是否只包含 '0' 和 '1' 的二进制字符
        for char in message_bits:
            if char not in ('0', '1'):
                raise ValueError("消息包含无效的二进制字符，无法隐藏在图像中。")

        index = 0
        # 遍历图像的每个像素
        for pixel in data:
            if index < message_length:
                encoded_pixel = list(pixel)
                # 将消息的二进制位嵌入到像素的最低有效位中
                encoded_pixel[-1] = int(message_bits[index])
                encoded_data.append(tuple(encoded_pixel))
                index += 1
            else:
                encoded_data.append(pixel)

        # 将修改后的像素数据写回图像
        img.putdata(encoded_data)
        img.save(image_path)
        print("消息隐藏成功!")
    except FileNotFoundError:
        print("错误: 图像文件不存在。")
    except ValueError as ve:
        print("错误:", ve)
    except Exception as e:
        print("错误:", e)


def extract_message(image_path):
    """
    从图像中提取隐藏的消息。

    :param image_path: 图像文件的路径
    """
    try:
        # 打开图像文件
        img = Image.open(image_path)
        # 获取图像的像素数据
        data = img.getdata()
        extracted_bits = []
        # 遍历图像的每个像素，并提取最后一个位，这个位就是消息的隐藏位
        for pixel in data:
            extracted_bits.append(str(pixel[-1]))

        binary_message = ''.join(extracted_bits)
        message = ""
        # 将提取的二进制消息转换为字符串
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            message += chr(int(byte, 2))
            # 如果遇到空字符，则表示消息结束
            if message[-1] == "\0":
                break
        print("提取的消息:", message.rstrip("\0"))
    except FileNotFoundError:
        print("错误: 图像文件不存在。")
    except Exception as e:
        print("错误:", e)


def main():
    """
    主函数，用于解析命令行参数并调用对应的功能函数。
    """
    parser = argparse.ArgumentParser(description="从图像中隐藏或提取消息")
    parser.add_argument("--hide", metavar="<image_path> <message>", nargs=2, type=str, help="在图像中隐藏信息")
    parser.add_argument("-e","--extract", metavar="<image_path>", type=str, help="从图像中提取消息")
    parser.add_argument("-v", "--version", action="version", version=f"版本号: {VERSION}", help="显示当前版本号")

    args = parser.parse_args()

    if args.hide:
        image_path, message = args.hide
        try:
            image_path = validate_image_path(image_path)
            message = validate_message(message)
        except argparse.ArgumentTypeError as e:
            print("错误:", e)
            return
        hide_message(image_path, message)
    elif args.extract:
        try:
            image_path = validate_image_path(args.extract)
        except argparse.ArgumentTypeError as e:
            print("错误:", e)
            return
        extract_message(image_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
