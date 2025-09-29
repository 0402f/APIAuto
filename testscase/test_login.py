import pytest
import allure

@allure.feature("登录模块")
class TestLogin:
    
    @allure.story("访问首页")
    @allure.title("验证首页可访问")
    @pytest.mark.api
    def test_home_page(self, http_client):
        """测试首页可访问"""
        # 发送请求
        with allure.step("访问首页"):
            response = http_client.get("/")
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        

    @allure.story("用户登录")
    @allure.title("验证用户成功登录")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_user_login_success(self, http_client):
        """测试用户成功登录"""
        # 准备请求数据
        login_data = {
            "userNumber": "admin",
            "password": "admin"
        }
        
        # 发送请求
        with allure.step("调用登录接口"):
            response = http_client.post("/api/user/login", json=login_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            
            # 验证响应结构
            with allure.step("验证响应结构完整性"):
                assert "code" in response_json, "响应中缺少code字段"
                assert "msg" in response_json, "响应中缺少msg字段"
                assert "data" in response_json, "响应中缺少data字段"
            
            # 验证成功登录
            with allure.step("验证登录成功码"):
                assert response_json["code"] == 1, f"期望登录成功码为1，实际为{response_json['code']}"
            
            with allure.step("验证返回的JWT Token"):
                token = response_json["data"]
                assert token is not None, "登录成功但未返回token"
                assert isinstance(token, str), "token应该是字符串类型"
                assert len(token) > 0, "token不能为空"
                
                # 验证JWT token格式（基本格式检查）
                token_parts = token.split('.')
                assert len(token_parts) == 3, "JWT token格式不正确，应该包含3个部分"
            
            with allure.step("验证消息字段"):
                # msg字段在成功时通常为null或成功消息
                msg = response_json["msg"]
                assert msg is None or isinstance(msg, str), "msg字段类型不正确"
                
        # 添加响应详情到报告
        allure.attach(
            str(response_json),
            name="登录成功响应详情",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # 添加token信息到报告（仅显示前20个字符，保护敏感信息）
        token_preview = response_json["data"][:20] + "..." if len(response_json["data"]) > 20 else response_json["data"]
        allure.attach(
            f"Token预览: {token_preview}",
            name="JWT Token信息",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.story("用户登录")
    @allure.title("验证用户不存在情况")
    @pytest.mark.api
    def test_user_login(self, http_client):
        """测试用户不存在的情况"""
        # 准备请求数据
        login_data = {
            "userNumber": "dd",
            "password": "ddd"
        }
        
        # 发送请求
        with allure.step("调用登录接口"):
            response = http_client.post("/api/user/login", json=login_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            assert "code" in response_json
            
            # 验证用户不存在的情况
            with allure.step("验证错误码"):
                # 假设错误码为非0值，例如10001表示用户不存在
                assert response_json["code"] == 0, "期望登录失败，但返回成功码"
            
            with allure.step("验证错误信息"):
                assert "msg" in response_json
                # 检查错误消息中是否包含"用户不存在"或类似文字
                assert "用户不存在" in response_json["msg"] or "不存在" in response_json["msg"] or "invalid" in response_json["msg"].lower()



    @allure.story("用户登录") 
    @allure.title("户存在情况密码错误")
    @pytest.mark.api
    def test_user_wrong_password(self, http_client):
        """测试用户存在但密码错误的情况"""
        # 准备请求数据
        login_data = {
            "userNumber": "admin",  # 假设这是存在的用户
            "password": "123456"  # 错误的密码
        }
        
        # 发送请求
        with allure.step("调用登录接口"):
            response = http_client.post("/api/user/login", json=login_data)
        
        # 断言结果
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应内容"):
            response_json = response.json()
            assert "code" in response_json
            
            # 验证密码错误的情况
            with allure.step("验证错误码"):
                # 假设错误码为非0值，例如10002表示密码错误
                assert response_json["code"] == 0, "期望登录失败，但返回成功码"
            
            with allure.step("验证错误信息"):
                assert "msg" in response_json
                # 检查错误消息中是否包含"密码错误"或类似文字
                assert "密码错误" in response_json["msg"] or "密码" in response_json["msg"] or "password" in response_json["msg"].lower()
                
            # 添加详细的错误信息日志
            allure.attach(
                str(response_json),
                name="响应详情",
                attachment_type=allure.attachment_type.TEXT
            )
