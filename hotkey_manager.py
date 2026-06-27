"""
hotkey_manager.py — 全局热键管理模块

使用 pynput 监听全局快捷键（默认 Ctrl+Alt+Q），获取选中文本并触发翻译。
pynput 不需要管理员权限即可在 Windows 上捕获全局按键。
通过模拟 Ctrl+C 获取选中文本，翻译完成后恢复原始剪贴板内容。
"""

import time
import threading
import logging
import ctypes
import ctypes.wintypes
import uuid

from pynput import keyboard
import pyperclip

logger = logging.getLogger(__name__)


class HotkeyManager:
    """全局热键管理器（基于 pynput）"""

    DEFAULT_HOTKEY = "<ctrl>+<alt>+q"

    def __init__(self, on_translate, hotkey: str = None):
        """
        Args:
            on_translate: 获取到选中文本后的回调 callback(text: str)
            hotkey: 自定义快捷键，默认为 Ctrl+Alt+Q
        """
        self.on_translate = on_translate
        self.hotkey = hotkey or self.DEFAULT_HOTKEY
        self._active = False
        self._lock = threading.Lock()
        self._listener = None
        self._hotkey_listener = None

    def start(self):
        """注册全局热键并开始监听"""
        if self._active:
            return

        # 使用 pynput 的 GlobalHotKeys 监听组合键
        self._hotkey_listener = keyboard.GlobalHotKeys({
            self.hotkey: self._on_hotkey_pressed,
        })
        self._hotkey_listener.daemon = True
        self._hotkey_listener.start()

        self._active = True
        logger.info(f"Đã đăng ký phím tắt toàn cục: {self.hotkey}")

    def stop(self):
        """停止监听并注销热键"""
        if not self._active:
            return

        try:
            if self._hotkey_listener:
                self._hotkey_listener.stop()
                self._hotkey_listener = None
        except Exception as e:
            logger.warning(f"Lỗi khi hủy đăng ký phím tắt: {e}")

        self._active = False
        logger.info("Đã hủy đăng ký phím tắt toàn cục")

    def _on_hotkey_pressed(self):
        """
        热键按下时的处理流程：
        1. 保存当前剪贴板
        2. 模拟 Ctrl+C 复制选中内容
        3. 读取剪贴板获取选中文本
        4. 恢复原始剪贴板
        5. 触发翻译回调
        """
        # 使用锁防止快速重复按键导致的竞争
        if not self._lock.acquire(blocking=False):
            return

        try:
            logger.info("Phím tắt được kích hoạt, đang lấy văn bản đã bôi đen...")
            self._capture_and_translate()
        except Exception as e:
            logger.error(f"Lỗi khi xử lý phím tắt: {e}")
        finally:
            self._lock.release()

    def _capture_and_translate(self):
        """捕获选中文本并触发翻译"""
        # Step 1: 保存当前剪贴板内容
        original_clipboard = ""
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            logger.debug("Không đọc được nội dung clipboard")

        # Step 2: 写入哨兵值，后续用它判断 Ctrl+C 是否真的更新了剪贴板
        sentinel = f"__translate_plugin_clipboard_sentinel_{uuid.uuid4()}__"
        try:
            pyperclip.copy(sentinel)
        except Exception as e:
            logger.debug(f"Không chuẩn bị được clipboard: {e}")
            return

        # Step 3: 模拟 Ctrl+C 复制选中内容
        time.sleep(0.15)
        self._simulate_ctrl_c()

        # Step 4: 等待剪贴板更新
        selected_text = ""
        deadline = time.time() + 0.8
        while time.time() < deadline:
            try:
                selected_text = pyperclip.paste()
            except Exception:
                logger.debug("Không đọc được văn bản đã bôi đen")
                break

            if selected_text != sentinel:
                break

            time.sleep(0.05)

        # Step 5: 恢复原始剪贴板
        try:
            pyperclip.copy(original_clipboard)
        except Exception:
            logger.debug("Không khôi phục được clipboard")

        # Step 6: 触发翻译
        if selected_text and selected_text != sentinel and selected_text.strip():
            text = selected_text.strip()
            logger.info(f"Đã lấy văn bản bôi đen: {text[:50]}...")
            self.on_translate(text)
        else:
            logger.warning("Không phát hiện văn bản bôi đen, hãy chắc ứng dụng hiện tại hỗ trợ Ctrl+C để sao chép nội dung đã chọn")

    @staticmethod
    def _simulate_ctrl_c():
        """使用 Windows API 模拟 Ctrl+C 按键"""
        VK_CONTROL = 0x11
        VK_MENU = 0x12
        VK_SHIFT = 0x10
        VK_C = 0x43
        KEYEVENTF_KEYUP = 0x0002

        user32 = ctypes.windll.user32

        # 热键触发时 Ctrl/Alt 可能仍处于按下状态；先释放修饰键，避免发送成 Ctrl+Alt+C。
        user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.03)

        # 按下 Ctrl
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        # 按下 C
        user32.keybd_event(VK_C, 0, 0, 0)
        # 释放 C
        user32.keybd_event(VK_C, 0, KEYEVENTF_KEYUP, 0)
        # 释放 Ctrl
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
