import os
import importlib

class Config:
    """配置管理类"""
    def __init__(self):
        # 获取当前环境
        self.env = os.environ.get('ENV', 'dev')

        # 动态导入环境配置 - 修复导入路径
        env_module = importlib.import_module(f'config.env.{self.env}')
        
        # 将环境配置加载到当前实例
        for key, value in env_module.__dict__.items():
            if not key.startswith('__'):
                setattr(self, key, value)