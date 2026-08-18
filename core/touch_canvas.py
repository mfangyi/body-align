"""触屏画布组件：HTML5 Canvas 交互，支持手势缩放/旋转/拖拽"""
import streamlit.components.v1 as components
import base64
import cv2
import numpy as np


def img_to_base64(img: np.ndarray) -> str:
    """将 numpy 数组图像转换为 base64 字符串"""
    _, buffer = cv2.imencode('.png', img)
    return base64.b64encode(buffer).decode('utf-8')


def render_touch_canvas(img_before: np.ndarray, img_after: np.ndarray, height: int = 600):
    """渲染交互式触屏画布组件"""
    before_b64 = img_to_base64(img_before)
    after_b64 = img_to_base64(img_after)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                background: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                font-family: Arial, sans-serif;
            }}
            .canvas-container {{
                position: relative;
                background: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            canvas {{
                display: block;
                touch-action: none;
            }}
            .controls {{
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
                background: rgba(255,255,255,0.9);
                padding: 10px 20px;
                border-radius: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            .btn {{
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                background: #007bff;
                color: white;
                cursor: pointer;
                font-size: 14px;
            }}
            .btn:hover {{
                background: #0056b3;
            }}
            .btn:active {{
                background: #004085;
            }}
        </style>
    </head>
    <body>
        <div class="canvas-container">
            <canvas id="canvas"></canvas>
            <div class="controls">
                <button class="btn" onclick="resetTransform()">重置</button>
                <button class="btn" onclick="downloadImage()">下载 PNG</button>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');

            // 图像数据
            const imgBeforeData = 'data:image/png;base64,{before_b64}';
            const imgAfterData = 'data:image/png;base64,{after_b64}';

            // 加载图像
            const imgBefore = new Image();
            const imgAfter = new Image();
            let imagesLoaded = 0;

            imgBefore.onload = imgAfter.onload = () => {{
                imagesLoaded++;
                if (imagesLoaded === 2) {{
                    initCanvas();
                }}
            }};

            imgBefore.src = imgBeforeData;
            imgAfter.src = imgAfterData;

            // 变换状态
            let transform = {{
                scale: 1,
                rotation: 0,
                x: 0,
                y: 0
            }};

            // 触摸状态
            let touches = {{}};
            let lastDistance = 0;
            let lastAngle = 0;

            function initCanvas() {{
                const maxWidth = Math.min(window.innerWidth - 40, 1200);
                const maxHeight = {height};

                const totalWidth = imgBefore.width + imgAfter.width + 20;
                const maxHeight_img = Math.max(imgBefore.height, imgAfter.height);

                const scaleX = maxWidth / totalWidth;
                const scaleY = maxHeight / maxHeight_img;
                const scale = Math.min(scaleX, scaleY, 1);

                canvas.width = totalWidth * scale;
                canvas.height = maxHeight_img * scale;

                draw();
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.save();
                ctx.translate(canvas.width / 2 + transform.x, canvas.height / 2 + transform.y);
                ctx.scale(transform.scale, transform.scale);
                ctx.rotate(transform.rotation * Math.PI / 180);

                const scale = canvas.width / (imgBefore.width + imgAfter.width + 20);
                const offsetX = -(imgBefore.width + 10) * scale;
                const offsetY = -imgBefore.height * scale / 2;

                ctx.drawImage(imgBefore, offsetX, offsetY, imgBefore.width * scale, imgBefore.height * scale);
                ctx.drawImage(imgAfter, 10 * scale, offsetY, imgAfter.width * scale, imgAfter.height * scale);

                ctx.restore();

                // 绘制标签
                ctx.font = 'bold 32px Arial';
                ctx.fillStyle = 'red';
                ctx.fillText('前', 20, 40);
                ctx.fillText('后', canvas.width / 2 + 20, 40);
            }}

            // 鼠标事件
            let isDragging = false;
            let lastX = 0;
            let lastY = 0;

            canvas.addEventListener('mousedown', (e) => {{
                isDragging = true;
                lastX = e.clientX;
                lastY = e.clientY;
            }});

            canvas.addEventListener('mousemove', (e) => {{
                if (!isDragging) return;
                const dx = e.clientX - lastX;
                const dy = e.clientY - lastY;
                transform.x += dx;
                transform.y += dy;
                lastX = e.clientX;
                lastY = e.clientY;
                draw();
            }});

            canvas.addEventListener('mouseup', () => isDragging = false);
            canvas.addEventListener('mouseleave', () => isDragging = false);

            // 滚轮缩放
            canvas.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                transform.scale *= delta;
                transform.scale = Math.max(0.5, Math.min(3, transform.scale));
                draw();
            }});

            // 触摸事件
            canvas.addEventListener('touchstart', (e) => {{
                e.preventDefault();
                for (let touch of e.touches) {{
                    touches[touch.identifier] = {{
                        x: touch.clientX,
                        y: touch.clientY
                    }};
                }}

                if (e.touches.length === 2) {{
                    const t1 = e.touches[0];
                    const t2 = e.touches[1];
                    lastDistance = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
                    lastAngle = Math.atan2(t2.clientY - t1.clientY, t2.clientX - t1.clientX);
                }}
            }});

            canvas.addEventListener('touchmove', (e) => {{
                e.preventDefault();

                if (e.touches.length === 1) {{
                    // 单指拖拽
                    const touch = e.touches[0];
                    const prev = touches[touch.identifier];
                    if (prev) {{
                        transform.x += touch.clientX - prev.x;
                        transform.y += touch.clientY - prev.y;
                        touches[touch.identifier] = {{
                            x: touch.clientX,
                            y: touch.clientY
                        }};
                        draw();
                    }}
                }} else if (e.touches.length === 2) {{
                    // 双指缩放和旋转
                    const t1 = e.touches[0];
                    const t2 = e.touches[1];
                    const distance = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
                    const angle = Math.atan2(t2.clientY - t1.clientY, t2.clientX - t1.clientX);

                    if (lastDistance > 0) {{
                        const scaleDelta = distance / lastDistance;
                        transform.scale *= scaleDelta;
                        transform.scale = Math.max(0.5, Math.min(3, transform.scale));
                    }}

                    if (lastAngle !== 0) {{
                        const angleDelta = (angle - lastAngle) * 180 / Math.PI;
                        transform.rotation += angleDelta;
                    }}

                    lastDistance = distance;
                    lastAngle = angle;
                    draw();
                }}
            }});

            canvas.addEventListener('touchend', (e) => {{
                for (let touch of e.changedTouches) {{
                    delete touches[touch.identifier];
                }}
                lastDistance = 0;
                lastAngle = 0;
            }});

            function resetTransform() {{
                transform = {{
                    scale: 1,
                    rotation: 0,
                    x: 0,
                    y: 0
                }};
                draw();
            }}

            function downloadImage() {{
                const link = document.createElement('a');
                link.download = 'body_comparison.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
            }}
        </script>
    </body>
    </html>
    """

    return components.html(html_content, height=height + 100)
