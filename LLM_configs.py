from dotenv import load_dotenv
import os

load_dotenv()

# Kimi API Config

kimi_weak_llm_config = {
    "config_list": [
        {
            "model": "moonshot-v1-8k",
            "api_key": os.environ.get("Kimi_API_KEY"),
            "api_type": "openai",
            "base_url": "https://api.moonshot.cn/v1",
            "price": [0.000012, 0.000012],
            "cache_seed": None
        }],
    "temperature": 0.1,
    "timeout": 300,
}

kimi_strong_llm_config = {
    "config_list": [
        {
            "model": "moonshot-v1-128k",
            "api_key": os.environ.get("Kimi_API_KEY"),
            "api_type": "openai",
            "base_url": "https://api.moonshot.cn/v1",
            "price": [0.00006, 0.00006],
            "cache_seed": None
        }],
    "temperature": 0.1,
    "timeout": 300
}

# Ali Qwen Config

Qwen_weak_llm_config = {
    "config_list": [
        {
            "model": "qwen-plus",
            "api_key": os.environ.get("Qwen_API_KEY"),
            "api_type": "openai",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "price": [0.000004, 0.000012],
            "cache_seed": None,
        }],
    "temperature": 0.1,
    "max_tokens": 2000,
    "timeout": 300
}

Qwen_strong_llm_config = {
    "config_list": [
        {
            "model": "qwen-max",
            "api_key": os.environ.get("Qwen_API_KEY"),
            "api_type": "openai",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "price": [0.00004, 0.00012],
            "cache_seed": None,
        }],
    "temperature": 0.5,
    "max_tokens": 2000,
    "timeout": 300
}
