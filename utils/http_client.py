import requests
import json
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class HttpClient:
    """HTTP请求客户端封装"""
    
    def __init__(self, base_url, timeout=10, max_retries=3):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 默认请求头
        self.default_headers = {
            "Content-Type": "application/json",
            "User-Agent": "AutoAPI-TestFramework"
        }
    
    def get(self, url, params=None, headers=None, **kwargs):
        """发送GET请求"""
        return self._request("GET", url, params=params, headers=headers, **kwargs)
    
    def post(self, url, data=None, json=None, headers=None, **kwargs):
        """发送POST请求"""
        return self._request("POST", url, data=data, json=json, headers=headers, **kwargs)
    
    def put(self, url, data=None, headers=None, **kwargs):
        """发送PUT请求"""
        return self._request("PUT", url, data=data, headers=headers, **kwargs)
    
    def delete(self, url, headers=None, **kwargs):
        """发送DELETE请求"""
        return self._request("DELETE", url, headers=headers, **kwargs)
    
    def _request(self, method, url, headers=None, **kwargs):
        """发送HTTP请求"""
        # 合并请求头
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)
        
        # 构建完整URL
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        
        # 设置超时
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        
        try:
            response = self.session.request(
                method=method,
                url=full_url,
                headers=request_headers,
                **kwargs
            )
            
            # 记录请求和响应信息
            self._log_request_response(method, full_url, request_headers, kwargs, response)
            
            return response
        except Exception as e:
            logging.error(f"请求异常: {str(e)}")
            raise
    
    def _log_request_response(self, method, url, headers, kwargs, response):
        """记录请求和响应信息"""
        logging.info(f"请求方法: {method}")
        logging.info(f"请求URL: {url}")
        logging.info(f"请求头: {headers}")
        
        if "json" in kwargs:
            logging.info(f"请求体: {kwargs['json']}")
        elif "data" in kwargs:
            logging.info(f"请求体: {kwargs['data']}")
        
        logging.info(f"响应状态码: {response.status_code}")
        try:
            logging.info(f"响应体: {response.json()}")
        except:
            logging.info(f"响应体: {response.text}")