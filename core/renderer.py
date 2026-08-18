"""文字渲染：中文字体加载、标签与数据叠加绘制"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


def load_chinese_font(size: int = 32) -> ImageFont.FreeTypeFont:
    """加载中文字体，支持 Windows 系统字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",     # 黑体
        "C:/Windows/Fonts/simsun.ttc",     # 宋体
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    # 回退到默认字体
    return ImageFont.load_default()


def draw_label(img: np.ndarray, text: str, position: tuple, font_size: int = 40) -> np.ndarray:
    """在图像上绘制红色标签文字"""
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = load_chinese_font(font_size)

    # 获取文字边界框
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x, y = position

    # 绘制半透明背景
    padding = 10
    bg_rect = [x - padding, y - padding, x + text_w + padding, y + text_h + padding]
    draw.rectangle(bg_rect, fill=(255, 255, 255, 200))

    # 绘制红色文字
    draw.text((x, y), text, fill=(255, 0, 0), font=font)

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def draw_body_data(img: np.ndarray, data_text: str, position: tuple, font_size: int = 28) -> np.ndarray:
    """在图像上绘制身体数据文字"""
    if not data_text.strip():
        return img

    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = load_chinese_font(font_size)

    x, y = position
    lines = data_text.strip().split('\n')

    for i, line in enumerate(lines):
        line_y = y + i * (font_size + 8)
        # 绘制白色描边
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                draw.text((x + dx, line_y + dy), line, fill=(255, 255, 255), font=font)
        # 绘制黑色文字
        draw.text((x, line_y), line, fill=(0, 0, 0), font=font)

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def add_labels_and_data(
    img_concat: np.ndarray,
    img_width: int,
    data_before: str = "",
    data_after: str = ""
) -> np.ndarray:
    """在拼接图上加标签和身体数据"""
    h, w = img_concat.shape[:2]

    # 添加"前"标签（左上角）
    result = draw_label(img_concat, "前", (20, 20), font_size=48)

    # 添加"后"标签（右半部分左上角）
    result = draw_label(result, "后", (img_width + 40, 20), font_size=48)

    # 添加身体数据
    if data_before:
        result = draw_body_data(result, data_before, (20, 100), font_size=32)
    if data_after:
        result = draw_body_data(result, data_after, (img_width + 40, 100), font_size=32)

    return result
