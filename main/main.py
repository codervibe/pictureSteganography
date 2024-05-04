# main.py
import argparse
from version import VERSION
from image_utils import validate_image_path, validate_message, hide_message, extract_message

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
