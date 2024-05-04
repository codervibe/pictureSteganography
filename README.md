# 项目名称：图片信息隐藏工具

* 描述：
* 这是一个使用 Python 编写的工具，可以隐藏消息到图像中，或从图像中提取隐藏的消息。
## 安装：
1. 确保安装了 Python 3.x。
2. 安装 Pillow 库：`pip install Pillow`

## 使用说明：
* 下载项目
~~~shell
git clone https://github.com/codervibe/pictureSteganography.git
pip install -r requirements.txt
cd pictureSteganography
~~~

1. 隐藏消息：
   ~~~
   python pictureSteganography.py --hidden <image_path> <message>
   python pictureSteganography.py --hd <image_path> <message>
   ~~~
   选项说明：
   --hidden 或 --hd：指定要隐藏消息的图像文件和消息内容。

2. 提取消息：
  `python pictureSteganography.py -e <image_path>`
   选项说明：
   -e：指定要从中提取消息的图像文件。

## 示例：
1. 隐藏消息：
   `python script.py --hidden image.jpg "This is a hidden message"`
   `python script.py --hd image.png "Another hidden message"`

2. 提取消息：
   `python script.py -e hidden_image.jpg`
   `python script.py -e hidden_image.png`

## 注意事项：
- 仅支持 PNG 和 JPEG 图像格式。
- 隐藏的消息会直接修改原始图像文件，请谨慎操作。

