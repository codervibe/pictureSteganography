#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- 作者： codervibe -*-
# -*- 时间: 18 ：46 -*-
# -*- 图片隐写术 -*-
# -*-  2.0.0  -*-


VERSION = "2.0.0"

# image_utils.py
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
        img = Image.open(image_path)
        data = img.getdata()
        encoded_data = []
        message += "\0"
        message_bits = ''.join(format(ord(char), '08b') for char in message)
        message_length = len(message_bits)

        if len(data) * 3 < message_length:
            raise ValueError("消息过长，无法隐藏在图像中。")

        index = 0
        for pixel in data:
            if index < message_length:
                encoded_pixel = list(pixel)
                encoded_pixel[-1] = int(message_bits[index])
                encoded_data.append(tuple(encoded_pixel))
                index += 1
            else:
                encoded_data.append(pixel)

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
        img = Image.open(image_path)
        data = img.getdata()
        extracted_bits = []
        for pixel in data:
            extracted_bits.append(str(pixel[-1]))

        binary_message = ''.join(extracted_bits)
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            message += chr(int(byte, 2))
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
    parser.add_argument("--extract", metavar="<image_path>", type=str, help="从图像中提取消息")
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
