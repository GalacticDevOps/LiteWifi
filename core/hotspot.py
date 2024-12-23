import subprocess
import tempfile
import os
from typing import Tuple
import win32process
import win32con

class HotspotManager:
    def __init__(self):
        self.ssid = None
        self.password = None
        self.is_running = False
        self.temp_dir = tempfile.gettempdir()

    def _run_ps_script(self, script_content: str, script_name: str) -> subprocess.CompletedProcess:
        """运行PowerShell脚本并自动清理"""
        script_path = os.path.join(self.temp_dir, script_name)
        try:
            # 写入临时脚本文件
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # 设置启动信息，使窗口完全隐藏
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = win32con.SW_HIDE
            
            # 运行脚本，添加更多的静默参数
            result = subprocess.run([
                'powershell.exe',
                '-ExecutionPolicy', 'Bypass',
                '-WindowStyle', 'Hidden',
                '-NonInteractive',
                '-NoLogo',           # 不显示 Logo
                '-NoProfile',        # 不加载配置文件
                '-Command',
                f"$ErrorActionPreference='SilentlyContinue'; $ProgressPreference='SilentlyContinue'; . '{script_path}'"
            ], 
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
            creationflags=win32process.CREATE_NO_WINDOW  # 创建无窗口进程
            )
            
            return result
        finally:
            # 清理临时文件
            try:
                if os.path.exists(script_path):
                    os.remove(script_path)
            except Exception as e:
                print(f"清理临时文件错误: {str(e)}")

    def create_hotspot(self, ssid: str, password: str) -> bool:
        """创建并启动WiFi热点"""
        try:
            ps_command = f'''
            # 禁用进度条和错误显示
            $ProgressPreference = 'SilentlyContinue'
            $ErrorActionPreference = 'SilentlyContinue'

            $connectionProfile = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
            $tetheringManager = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]::CreateFromConnectionProfile($connectionProfile)
            
            # 配置热点设置
            $tetheringManager.MaxClientCount = 8
            $config = $tetheringManager.GetCurrentAccessPointConfiguration()
            $config.Ssid = "{ssid}"
            $config.Passphrase = "{password}"
            
            # 强制启用热点（即使没有互联网连接）
            $tetheringManager.ConfigureAccessPointAsync($config).AsTask().Wait()
            $tetheringManager.StartTetheringAsync().AsTask().Wait()
            '''
            
            result = self._run_ps_script(ps_command, 'enable_hotspot.ps1')
            
            if result.returncode == 0:
                self.ssid = ssid
                self.password = password
                self.is_running = True
                print("热点创建成功")
                return True
            else:
                print(f"热点创建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"创建热点错误: {str(e)}")
            return False

    def stop_hotspot(self) -> bool:
        """停止热点"""
        try:
            ps_command = '''
            # 禁用进度条和错误显示
            $ProgressPreference = 'SilentlyContinue'
            $ErrorActionPreference = 'SilentlyContinue'

            $connectionProfile = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
            $tetheringManager = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]::CreateFromConnectionProfile($connectionProfile)
            $tetheringManager.StopTetheringAsync().AsTask().Wait()
            '''
            
            result = self._run_ps_script(ps_command, 'stop_hotspot.ps1')
            
            if result.returncode == 0:
                self.is_running = False
                print("热点已停止")
                return True
            else:
                print(f"停止热点失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"停止热点错误: {str(e)}")
            return False 