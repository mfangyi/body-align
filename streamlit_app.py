"""BodyAlign - 瑜伽练习前后对比照片制作工具"""
import streamlit as st
import cv2
import numpy as np
from core.processor import load_image, resize_image, horizontal_concat, apply_affine_transform, img_to_pil
from core.alignment import auto_align
from core.renderer import add_labels_and_data
from core.touch_canvas import render_touch_canvas
from utils.helper import generate_filename

# 页面配置
st.set_page_config(page_title="BodyAlign - 瑜伽对比照", layout="wide")

st.title("BodyAlign - 瑜伽练习对比照")

# 初始化 session state
if 'aligned' not in st.session_state:
    st.session_state.aligned = False
if 'img_before' not in st.session_state:
    st.session_state.img_before = None
if 'img_after' not in st.session_state:
    st.session_state.img_after = None

# 输入信息区域
st.subheader("输入信息")
member_name = st.text_input("会员姓名", placeholder="请输入姓名")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 练习前")
    uploaded_before = st.file_uploader("上传练习前照片", type=["jpg", "jpeg", "png"], key="before")
    data_before = st.text_area("身体数据（练习前）", placeholder="胸围: 90cm\n腰围: 70cm\n臀围: 95cm", height=100)

with col2:
    st.markdown("### 练习后")
    uploaded_after = st.file_uploader("上传练习后照片", type=["jpg", "jpeg", "png"], key="after")
    data_after = st.text_area("身体数据（练习后）", placeholder="胸围: 88cm\n腰围: 65cm\n臀围: 93cm", height=100)

# 处理图像
if uploaded_before and uploaded_after:
    # 加载图像
    img_before = load_image(uploaded_before)
    img_after = load_image(uploaded_after)

    # 缩放到合适大小
    img_before = resize_image(img_before, max_height=600)
    img_after = resize_image(img_after, max_height=600)

    # 自动对齐
    st.subheader("图像对齐")
    align_option = st.checkbox("启用自动对齐", value=True)

    if align_option:
        img_before_aligned, img_after_aligned, scale = auto_align(img_before, img_after)
        st.info(f"对齐缩放比例: {scale:.2f}")
    else:
        img_before_aligned = img_before
        img_after_aligned = img_after

    # 手动微调
    st.subheader("手动微调（练习后）")
    col_adj1, col_adj2, col_adj3 = st.columns(3)

    with col_adj1:
        scale_adjust = st.slider("缩放", 0.8, 1.2, 1.0, 0.01, key="scale")
    with col_adj2:
        rotation_adjust = st.slider("旋转", -30, 30, 0, 1, key="rotation")
    with col_adj3:
        tx_adjust = st.slider("水平偏移", -100, 100, 0, 1, key="tx")
        ty_adjust = st.slider("垂直偏移", -100, 100, 0, 1, key="ty")

    # 应用变换
    img_after_transformed = apply_affine_transform(
        img_after_aligned,
        scale=scale_adjust,
        rotation=rotation_adjust,
        tx=tx_adjust,
        ty=ty_adjust
    )

    # 水平拼接
    img_concat = horizontal_concat(img_before_aligned, img_after_transformed, gap=30)

    # 添加标签和数据
    img_width = img_before_aligned.shape[1]
    img_with_labels = add_labels_and_data(
        img_concat,
        img_width,
        data_before=data_before,
        data_after=data_after
    )

    # 显示结果
    st.subheader("对比效果")

    # 触屏画布
    render_touch_canvas(img_before_aligned, img_after_transformed, height=500)

    # 下载按钮
    img_pil = img_to_pil(img_with_labels)
    import io
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    buf.seek(0)

    filename = generate_filename(member_name if member_name else "未命名")
    st.download_button(
        label="下载 PNG",
        data=buf,
        file_name=filename,
        mime="image/png"
    )

else:
    st.info("请上传练习前和练习后的照片")
