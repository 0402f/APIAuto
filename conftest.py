# pytest配置文件,用于定义fixtures插件
import pytest
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from utils.http_client import HttpClient
from config.config import Config
from utils.logger import setup_logger

# 设置日志
logger = setup_logger()

# 确保reports目录结构存在
def ensure_reports_structure():
    """确保reports目录结构存在"""
    dirs = [
        'reports/html',
        'reports/xml', 
        'reports/coverage/html',
        'reports/allure-results',
        'reports/logs',
        'reports/screenshots'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

# 在测试开始前创建目录结构
ensure_reports_structure()

@pytest.fixture(scope="session")
def config():
    """加载配置"""
    return Config()

@pytest.fixture(scope="session")
def http_client(config):
    """创建HTTP客户端"""
    return HttpClient(base_url=config.base_url)

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """pytest配置钩子"""
    # 确保reports目录存在
    ensure_reports_structure()
    
    # 设置测试报告的元数据
    config._metadata = {
        'Project': 'AutoAPI Test Framework',
        'Test Environment': os.getenv('TEST_ENV', 'dev'),
        'Python Version': sys.version,
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """自定义HTML报告标题"""
    report.title = "AutoAPI 接口自动化测试报告"

def pytest_html_results_summary(prefix, summary, postfix):
    """自定义HTML报告摘要"""
    prefix.extend([f"<p>测试环境: {os.getenv('TEST_ENV', 'dev')}</p>"])