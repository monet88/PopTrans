"""
测试 llama.cpp 集成
"""

import sys
import os
import time

# Windows 控制台默认 cp1252，无法输出中文/越南语，强制 stdout 使用 UTF-8
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from translator import Translator

def test_translation():
    """测试翻译功能"""
    print("=" * 50)
    print("测试 llama.cpp 集成")
    print("=" * 50)
    
    # 创建翻译器实例
    translator = Translator()
    
    # 测试状态
    print(f"初始状态: {translator.status}")
    print(f"就绪状态: {translator.ready}")
    
    # 定义回调函数
    def on_ready(success):
        if success:
            print("✓ 翻译引擎初始化成功")
        else:
            print("✗ 翻译引擎初始化失败")
    
    def on_status(message):
        print(f"状态更新: {message}")
    
    # 初始化翻译引擎
    print("\n正在初始化翻译引擎...")
    translator.setup(on_ready=on_ready, on_status=on_status)
    
    # 等待初始化完成（status 失败信息为英文，匹配 "Failed"）
    while not translator.ready and "Failed" not in translator.status:
        time.sleep(1)
        print(f"等待中... 当前状态: {translator.status}")
    
    if not translator.ready:
        print("翻译引擎初始化失败，无法进行测试")
        return
    
    # 测试翻译：任意语言 → 越南语
    test_cases = [
        ("Hello, how are you?", "英→越"),
        ("今天天气真好", "中→越"),
        ("This is a test sentence.", "英→越"),
        ("我喜欢编程", "中→越"),
        ("人工知能はとても面白いです。", "日→越"),
        ("The quick brown fox jumps over the lazy dog.", "英→越"),
    ]
    
    print("\n" + "=" * 50)
    print("开始翻译测试")
    print("=" * 50)
    
    for text, expected_direction in test_cases:
        print(f"\n原文: {text}")
        print(f"期望方向: {expected_direction}")
        
        result, error = translator.translate(text)
        
        if error:
            print(f"错误: {error}")
        else:
            print(f"译文: {result}")
        
        print("-" * 30)
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_translation()
