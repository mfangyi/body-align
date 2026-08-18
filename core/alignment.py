"""自动对齐：OpenCV 边缘检测、人体主体高度检测、缩放比例计算"""
import cv2
import numpy as np


def detect_body_region(img: np.ndarray) -> tuple:
    """检测人体主体区域，返回 (x, y, w, h) 边界框"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用 Canny 边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 形态学操作连接边缘
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        h, w = img.shape[:2]
        return (0, 0, w, h)

    # 找到最大轮廓（假设是人体）
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)

    return (x, y, w, h)


def calculate_alignment_scale(img_before: np.ndarray, img_after: np.ndarray) -> float:
    """计算对齐缩放比例，使两张图片中的人体高度一致"""
    _, _, _, h1 = detect_body_region(img_before)
    _, _, _, h2 = detect_body_region(img_after)

    if h1 == 0 or h2 == 0:
        return 1.0

    # 以练习前图片为基准
    return h1 / h2


def auto_align(img_before: np.ndarray, img_after: np.ndarray) -> tuple:
    """自动对齐两张图片，返回 (aligned_before, aligned_after, scale)"""
    scale = calculate_alignment_scale(img_before, img_after)

    # 对练习后图片进行缩放
    if scale != 1.0:
        h, w = img_after.shape[:2]
        new_h = int(h * scale)
        new_w = int(w * scale)
        img_after_aligned = cv2.resize(img_after, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        img_after_aligned = img_after.copy()

    return img_before.copy(), img_after_aligned, scale


def get_body_center(img: np.ndarray) -> tuple:
    """获取人体主体中心坐标"""
    x, y, w, h = detect_body_region(img)
    return (x + w // 2, y + h // 2)
