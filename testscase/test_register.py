import pytest
import allure

@allure.feature("注册模块")
class TestRegister:
    
    @allure.story("用户注册")
    @allure.title("验证用户成功注册")
    @pytest.mark.api
    def test_user_register_success(self, http_client):
        """测试用户成功注册"""
        # 准备请求数据
        register_data = {
            "userNumber": "fwjqs",
            "password": "123456"
        }
        
        # 发送请求
        with allure.step("调用注册接口"):
            response = http_client.post("/api/user/register", json=register_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            
            # 验证响应结构
            with allure.step("验证响应结构完整性"):
                assert "code" in response_json, "响应中缺少code字段"
                assert "data" in response_json, "响应中缺少data字段"
            
            # 验证成功注册
            with allure.step("验证注册成功码"):
                assert response_json["code"] == 1, f"期望注册成功码为1，实际为{response_json['code']}"
            
            with allure.step("验证成功消息"):
                data = response_json["data"]
                assert data is not None, "注册成功但消息为空"
                assert "成功" in str(data) or "success" in str(data).lower(), "注册成功消息不正确"
                
        # 添加响应详情到报告
        allure.attach(
            str(response_json),
            name="注册成功响应详情",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # 添加用户信息到报告
        allure.attach(
            f"注册用户名: {register_data['userNumber']}",
            name="注册用户信息",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.story("用户注册")
    @allure.title("验证用户名已存在注册失败")
    @pytest.mark.api
    def test_user_register_username_exists(self, http_client):
        """测试用户名已存在的注册失败情况"""
        # 准备请求数据 - 使用已存在的用户名
        register_data = {
            "userNumber": "admin",  # 假设admin用户已存在
            "password": "123456"
        }
        
        # 发送请求
        with allure.step("调用注册接口"):
            response = http_client.post("/api/user/register", json=register_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            assert "code" in response_json
            
            # 验证用户名已存在的情况
            with allure.step("验证错误码"):
                assert response_json["code"] == 0, "期望注册失败，但返回成功码"
            
            with allure.step("验证错误信息"):
                assert "msg" in response_json
                msg = response_json["msg"]
                assert "已存在" in str(msg) or "exist" in str(msg).lower() or "重复" in str(msg), "用户名已存在错误信息不正确"
                
        # 添加响应详情到报告
        allure.attach(
            str(response_json),
            name="用户名已存在响应详情",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.story("用户注册")
    @allure.title("验证注册参数验证")
    @pytest.mark.api
    def test_user_register_invalid_params(self, http_client):
        """测试注册参数验证"""
        # 测试用户名为空的情况
        register_data = {
            "userNumber": "",
            "password": "123456"
        }
        
        # 发送请求
        with allure.step("调用注册接口 - 用户名为空"):
            response = http_client.post("/api/user/register", json=register_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            assert "code" in response_json
            
            # 验证参数错误的情况
            with allure.step("验证错误码"):
                assert response_json["code"] == 0, "期望参数验证失败，但返回成功码"
            
            with allure.step("验证错误信息"):
                assert "msg" in response_json
                msg = response_json["msg"]
                assert "用户名" in str(msg) or "username" in str(msg).lower() or "参数" in str(msg), "参数验证错误信息不正确"
                
        # 添加响应详情到报告
        allure.attach(
            str(response_json),
            name="参数验证失败响应详情",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.story("用户注册")
    @allure.title("验证密码为空注册失败")
    @pytest.mark.api
    def test_user_register_empty_password(self, http_client):
        """测试密码为空的注册失败情况"""
        # 准备请求数据 - 密码为空
        register_data = {
            "userNumber": "test",
            "password": ""
        }
        
        # 发送请求
        with allure.step("调用注册接口 - 密码为空"):
            response = http_client.post("/api/user/register", json=register_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            assert "code" in response_json
            
            # 验证密码为空的情况
            with allure.step("验证错误码"):
                assert response_json["code"] == 0, "期望注册失败，但返回成功码"
            
            with allure.step("验证错误信息"):
                assert "msg" in response_json
                msg = response_json["msg"]
                assert "密码" in str(msg) or "password" in str(msg).lower() or "参数" in str(msg), "密码为空错误信息不正确"
                
        # 添加响应详情到报告
        allure.attach(
            str(response_json),
            name="密码为空响应详情",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.story("用户注册")
    @allure.title("验证缺少必要参数注册失败")
    @pytest.mark.api
    def test_user_register_missing_params(self, http_client):
        """测试缺少必要参数的注册失败情况"""
        # 准备请求数据 - 只有用户名，缺少密码
        register_data = {
            "userNumber": "testa"
        }
        
        # 发送请求
        with allure.step("调用注册接口 - 缺少密码参数"):
            response = http_client.post("/api/user/register", json=register_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            assert "code" in response_json
            
            # 验证缺少参数的情况
            with allure.step("验证错误码"):
                assert response_json["code"] == 0, "期望注册失败，但返回成功码"
            
            with allure.step("验证错误信息"):
                assert "msg" in response_json
                msg = response_json["msg"]
                assert "参数" in str(msg) or "required" in str(msg).lower() or "缺少" in str(msg), "缺少参数错误信息不正确"
                
        # 添加响应详情到报告
        allure.attach(
            str(response_json),
            name="缺少参数响应详情",
            attachment_type=allure.attachment_type.TEXT
        )
    