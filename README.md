# AutoApi - API自动化测试框架

基于pytest和allure的接口自动化测试框架，支持多环境配置、详细测试报告生成。

## 项目特性

- ✅ 基于pytest测试框架
- ✅ 集成Allure测试报告
- ✅ 支持多环境配置
- ✅ HTTP客户端封装
- ✅ 一键执行测试和报告生成
- ✅ 完整的测试用例覆盖

## 项目结构
<img width="2239" height="1055" alt="image" src="https://github.com/user-attachments/assets/7f7da35d-dd39-4126-b3a7-c5c2e880730a" />

<img width="2560" height="1370" alt="image" src="https://github.com/user-attachments/assets/963bcb07-f4d8-4737-9bd1-c51dad0d6591" />

<img width="2560" height="1382" alt="image" src="https://github.com/user-attachments/assets/d8b1c91c-84b7-428e-815a-f90e3c07b598" />

<img width="2560" height="1384" alt="image" src="https://github.com/user-attachments/assets/3d471901-aaf5-4dab-8ac5-83569bcd3a73" />
<img width="2560" height="1402" alt="image" src="https://github.com/user-attachments/assets/58141e37-3cb6-461f-9aad-619a87faa37e" />
## 快速开始

### 1. 安装依赖

```bash
pip install pytest allure-pytest requests

# 运行测试
pytest

# 生成报告
allure generate reports/allure-results -o reports/allure-report --clean

# 查看报告
allure serve reports/allure-results

生成allure报告如图：





