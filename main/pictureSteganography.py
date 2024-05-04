import argparse
from PIL import Image


def hide_message(image_path, message):
    """
    将消息隐藏到图像中。

    :param image_path: 图像文件的路径
    :param message: 要隐藏的消息
    """
    try:
        img = Image.open(image_path)
        # 使用最低有效位（LSB）方法隐藏消息
        data = img.getdata()
        encoded_data = []
        message += "\0"  # 在消息末尾添加空字符，用于标记消息的结束
        message_bits = ''.join(format(ord(char), '08b') for char in message)  # 将消息转换为二进制字符串
        message_length = len(message_bits)

        if len(data) * 3 < message_length:
            raise ValueError("消息过长，无法隐藏在图像中。")

        index = 0
        for pixel in data:
            if index < message_length:
                # 修改像素的最后一个比特位
                encoded_pixel = list(pixel)
                encoded_pixel[-1] = int(message_bits[index])
                encoded_data.append(tuple(encoded_pixel))
                index += 1
            else:
                encoded_data.append(pixel)

        img.putdata(encoded_data)
        img.save(image_path)
        print("消息隐藏成功!")
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
            extracted_bits.append(str(pixel[-1]))  # 获取每个像素的最后一个比特位

        binary_message = ''.join(extracted_bits)
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            message += chr(int(byte, 2))
            if message[-1] == "\0":
                break
        print("提取的消息:", message.rstrip("\0"))
    except Exception as e:
        print("错误:", e)


def main():
    parser = argparse.ArgumentParser(description="从图像中隐藏或提取消息")
    parser.add_argument("--hide", metavar="<image_path> <message>", nargs=2, help="在图像中隐藏信息")
    parser.add_argument("--extract", metavar="<image_path>", help="从图像中提取消息")

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
