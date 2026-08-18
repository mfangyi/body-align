"""工具函数：文件名生成、日期格式化"""
from datetime import datetime


def generate_filename(name: str, body_part: str = "全身") -> str:
    """生成导出文件名，格式：姓名_部位_日期.png"""
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{name}_{body_part}_{date_str}.png"


def format_date(dt: datetime = None) -> str:
    """格式化日期为 YYYY-MM-DD"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")
