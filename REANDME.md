# AutoAPI - 接口自动化测试框架

基于 Pytest 的接口自动化测试框架，用于测试 RESTful API。

## 特性

- 基于 Pytest 测试框架
- 支持多环境配置
- HTTP 请求封装
- 日志记录
- 测试报告生成（HTML 和 Allure）
- 数据驱动测试
- 并发执行测试

## 安装

    pip install -r requirements.txt


## 使用
    命令行: 
    # 执行自动化测试
    pytest
    # 生成allure测试报告并打开
    allure serve reports/allure-results
    # 生成测试报告并保存
    allure generate reports/allure-results -o reports/allure-report --clean
    



