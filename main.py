import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow
import win32event
import win32api
import winerror
import mmap
import time
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

class ActivationMonitor(QThread):
    """监控其他实例的激活请求"""
    activation_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        try:
            # 创建共享内存
            self.mm = mmap.mmap(-1, 1024, "Global\\WiFiHotspotActivation")
            while self.running:
                # 检查激活信号
                self.mm.seek(0)
                if self.mm.read_byte() == 1:
                    # 重置信号
                    self.mm.seek(0)
                    self.mm.write_byte(0)
                    # 发送激活信号
                    self.activation_requested.emit()
                time.sleep(0.1)
        except Exception as e:
            print(f"Monitor error: {e}")

    def stop(self):
        self.running = False

def send_activation_signal():
    """发送激活信号给现有实例"""
    try:
        mm = mmap.mmap(-1, 1024, "Global\\WiFiHotspotActivation")
        mm.seek(0)
        mm.write_byte(1)
        mm.close()
        return True
    except Exception as e:
        print(f"Send activation error: {e}")
        return False

def get_asset_path(relative_path):
    """获取资源文件的路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def exception_hook(exctype, value, traceback):
    print(f'An exception has occurred: {exctype.__name__}: {value}')
    sys.__excepthook__(exctype, value, traceback)  # 调用默认的异常处理
    
sys.excepthook = exception_hook

def main():
    # 创建一个全局互斥量
    mutex_name = 'Global\\WiFiHotspotManagerMutex'
    mutex = win32event.CreateMutex(None, False, mutex_name)
    last_error = win32api.GetLastError()
    
    # 如果互斥量已存在，说明程序已经在运行
    if last_error == winerror.ERROR_ALREADY_EXISTS:
        win32api.CloseHandle(mutex)  # 关闭互斥量句柄
        # 发送激活信号给现有实例
        if send_activation_signal():
            time.sleep(0.5)  # 等待一下让现有实例有时间响应
        return

    # 如果是新实例，继续运行
    app = QApplication(sys.argv)
    
    icon_path = get_asset_path(os.path.join('assets', 'icon.ico'))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.setWindowTitle("WiFi热点管理工具")
    
    # 创建并启动激活监控器
    monitor = ActivationMonitor()
    monitor.activation_requested.connect(window.activate_from_tray)
    monitor.start()
    
    window.show()
    
    # 在程序退出时清理资源
    try:
        result = app.exec()
    finally:
        monitor.stop()
        monitor.wait()
        win32api.CloseHandle(mutex)
    sys.exit(result)

if __name__ == "__main__":
    main() 