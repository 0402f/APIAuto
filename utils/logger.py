import logging
import os
import time

def setup_logger():
    """配置日志"""
    # 创建日志目录
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志文件名
    log_file = os.path.join(log_dir, f"test_{time.strftime('%Y%m%d_%H%M%S')}.log")
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("autoapi")