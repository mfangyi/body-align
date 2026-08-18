"""图像处理：加载、缩放、水平拼接、仿射变换"""
import cv2
import numpy as np
from PIL import Image


def load_image(uploaded_file) -> np.ndarray:
    """从上传文件加载图像为 numpy 数组 (BGR)"""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    uploaded_file.seek(0)
    return img


def resize_image(img: np.ndarray, max_height: int = 800) -> np.ndarray:
    """按比例缩放图像到指定最大高度"""
    h, w = img.shape[:2]
    if h <= max_height:
        return img.copy()
    scale = max_height / h
    new_w = int(w * scale)
    return cv2.resize(img, (new_w, max_height), interpolation=cv2.INTER_AREA)


def horizontal_concat(img_left: np.ndarray, img_right: np.ndarray, gap: int = 20) -> np.ndarray:
    """水平拼接两张图像，中间添加白色间隙"""
    h1, w1 = img_left.shape[:2]
    h2, w2 = img_right.shape[:2]

    # 统一高度
    target_h = max(h1, h2)
    if h1 < target_h:
        pad = target_h - h1
        img_left = cv2.copyMakeBorder(img_left, 0, pad, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    if h2 < target_h:
        pad = target_h - h2
        img_right = cv2.copyMakeBorder(img_right, 0, pad, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # 创建白色间隙
    gap_img = np.ones((target_h, gap, 3), dtype=np.uint8) * 255

    return np.hstack([img_left, gap_img, img_right])


def apply_affine_transform(
    img: np.ndarray,
    scale: float = 1.0,
    rotation: float = 0.0,
    tx: float = 0.0,
    ty: float = 0.0
) -> np.ndarray:
    """应用仿射变换：缩放、旋转、平移"""
    h, w = img.shape[:2]
    center = (w // 2, h // 2)

    # 组合变换矩阵
    M_rot = cv2.getRotationMatrix2D(center, rotation, scale)
    M_rot[0, 2] += tx
    M_rot[1, 2] += ty

    return cv2.warpAffine(img, M_rot, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=[255, 255, 255])


def img_to_pil(img_bgr: np.ndarray) -> Image.Image:
    """将 BGR numpy 数组转换为 PIL Image"""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)
