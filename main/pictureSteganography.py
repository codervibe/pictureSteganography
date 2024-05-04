import argparse
from PIL import Image

# 定义当前版本号
VERSION = "1.0.0"


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
    parser = argparse.ArgumentParser(description="从图像中隐藏或提取消息")
    parser.add_argument("--hide", metavar="<image_path> <message>", nargs=2, help="在图像中隐藏信息")
    parser.add_argument("--extract", metavar="<image_path>", help="从图像中提取消息")
    parser.add_argument("-v", "--version", action="version", version=f"版本号: {VERSION}", help="显示当前版本号")

    args = parser.parse_args()

    if args.hide:
        image_path, message = args.hide
        hide_message(image_path, message)
    elif args.extract:
        extract_message(args.extract)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()