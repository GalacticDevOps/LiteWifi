from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QMessageBox, QFrame,
                            QSystemTrayIcon, QMenu, QApplication)
from PyQt6.QtCore import Qt, QSettings, QTimer, QSize
from PyQt6.QtGui import QIcon, QAction, QPainter, QColor, QPixmap, QImage
import os
import sys
from core.hotspot import HotspotManager
from gui.styles import MAIN_STYLE
import base64

def get_asset_path(relative_path):
    """获取资源文件的路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi热点管理工具")
        self.setFixedSize(400, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.setStyleSheet(MAIN_STYLE)
        
        # 添加眼睛图标的SVG定义
        self.eye_open_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="#666666" d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
        </svg>
        """
        
        self.eye_closed_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="#666666" d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/>
        </svg>
        """
        
        # 设置窗口图标
        icon_path = get_asset_path(os.path.join('assets', 'icon.ico'))
        self.icon = QIcon(icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(self.icon)
        
        self.settings = QSettings('WiFiHotspot', 'Settings')
        self.hotspot = HotspotManager()
        self.is_processing = False
        
        # 创建系统托盘
        self.setup_tray()
        self.setup_ui()
        self.load_settings()

    def setup_tray(self):
        """设置系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setToolTip("WiFi热点管理工具 - 双击显示主窗口")
        
        # 创建托盘菜单并设置样式
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px 8px 35px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #e6f3ff;
                color: #000;
            }
            QMenu::separator {
                height: 1px;
                background: #d0d0d0;
                margin: 5px 10px;
            }
        """)
        
        # 定义所有SVG图标为样其他方法可以访问
        self.power_on_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="#4CAF50" d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"/>
        </svg>
        """
        
        self.power_off_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="#FF5252" d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"/>
        </svg>
        """
        
        window_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="#2196F3" d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8h16v10z"/>
        </svg>
        """
        
        quit_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="#757575" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
        </svg>
        """
        
        # 将SVG转换为QIcon的函数保持不变
        def svg_to_icon(svg_data, size=24):
            svg_bytes = svg_data.encode('utf-8')
            svg_base64 = base64.b64encode(svg_bytes).decode('utf-8')
            icon = QIcon()
            icon.addPixmap(QPixmap.fromImage(QImage.fromData(base64.b64decode(svg_base64))))
            return icon
        
        # 示主窗口动作
        show_window_action = QAction("显示主窗口", self)
        show_window_action.setIcon(svg_to_icon(window_svg))  # 使用内嵌SVG图标
        show_window_action.triggered.connect(self.activate_from_tray)
        tray_menu.addAction(show_window_action)

        # 热点控制动作
        self.toggle_action = QAction("开启热点", self)
        self.toggle_action.setIcon(svg_to_icon(self.power_on_svg))
        self.toggle_action.triggered.connect(self.toggle_hotspot)
        tray_menu.addAction(self.toggle_action)
        
        tray_menu.addSeparator()
        
        # 退出动作
        quit_action = QAction("退出程序", self)
        quit_action.setIcon(svg_to_icon(quit_svg))  # 使用内嵌SVG图标
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        
        # 连接托盘图标的点击信号
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        # 显示托盘图标
        self.tray_icon.show()

    def on_tray_activated(self, reason):
        """处理托盘图标的点击事件"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.activate_from_tray()

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        event.ignore()  # 忽略关闭事件
        self.hide()     # 隐藏窗口
        self.tray_icon.showMessage(
            "WiFi热点管理工具",
            "已小化到统托盘，双击图标可以重新打开窗口。",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def quit_application(self):
        """退出应用程序"""
        if self.hotspot.is_running:
            reply = QMessageBox.question(
                self,
                "确认退出",
                "热点正在运行中，是否确认退出",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
            self.hotspot.stop_hotspot()
        
        # 确托图标被除
        self.tray_icon.setVisible(False)
        QApplication.quit()

    def toggle_hotspot(self):
        """切换热点状态"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.start_button.setEnabled(False)
        
        try:
            if not self.hotspot.is_running:
                ssid = self.ssid_input.text()
                password = self.password_input.text()
                
                if len(ssid) < 1 or len(password) < 8:
                    QMessageBox.warning(self, "错误", "热点名称不能为空，密码至少8位！")
                    return
                
                if self.hotspot.create_hotspot(ssid, password):
                    self.start_button.setText("关闭热点")
                    self.start_button.setStyleSheet("""
                        #primaryButton {
                            background-color: #ff5252;
                        }
                        #primaryButton:hover {
                            background-color: #ff6e6e;
                        }
                    """)
                    self.toggle_action.setText("关闭热点")
                    self.toggle_action.setIcon(self.svg_to_icon(self.power_off_svg))
                    self.status_label.setText("状态: 运行中")
                    self.status_label.setStyleSheet("color: #4CAF50;")
                    self.save_settings()
                    
                    # 显示系统托盘通知
                    self.tray_icon.showMessage(
                        "WiFi热点已开启",
                        f"热点名称: {ssid}\n密码: {password}",
                        QSystemTrayIcon.MessageIcon.Information,
                        3000
                    )
                else:
                    QMessageBox.warning(self, "错误", 
                                      "热点启动失败！\n"
                                      "请检查：\n"
                                      "1. 是否以管理员权限运行\n"
                                      "2. WiFi适配器是否支持热点功能\n"
                                      "3. 系统移动热点服务是否已启用")
                    return
            else:
                if self.hotspot.stop_hotspot():
                    self.start_button.setText("开启热点")
                    self.start_button.setStyleSheet("")  # 恢复默认样式
                    self.toggle_action.setText("开启热点")
                    self.toggle_action.setIcon(self.svg_to_icon(self.power_on_svg))
                    self.status_label.setText("状态: 已停止")
                    self.status_label.setStyleSheet("color: #757575;")
                    
                    # 显示系统托盘通知
                    self.tray_icon.showMessage(
                        "WiFi热点已关闭",
                        "热点服务已停止运行",
                        QSystemTrayIcon.MessageIcon.Information,
                        3000
                    )
                else:
                    QMessageBox.warning(self, "错误", "热点关闭失败！")
        finally:
            self.is_processing = False
            self.start_button.setEnabled(True)

    def setup_ui(self):
        """设界面布局"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 热点控制卡片
        control_card = self.create_card()
        control_layout = QVBoxLayout(control_card)
        control_layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("WiFi热点")
        title_label.setObjectName("cardTitle")
        control_layout.addWidget(title_label)
        
        # SSID输入
        ssid_label = QLabel("热点名称")
        ssid_label.setObjectName("inputLabel")
        ssid_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
            }
        """)
        
        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText("输入热点名称")
        self.ssid_input.setMinimumHeight(48)  # 与密码输入框保持一致
        self.ssid_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 12px 15px;
                background: white;
                font-size: 15px;
                color: #333333;
            }
            QLineEdit:hover {
                border-color: #4CAF50;
                background-color: #fafafa;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
                background-color: white;
                outline: none;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
            }
            QLineEdit::placeholder {
                color: #999999;
                font-size: 14px;
            }
        """)
        
        # 创建SSID输入区域容器
        ssid_section = QWidget()
        ssid_section_layout = QVBoxLayout(ssid_section)
        ssid_section_layout.setContentsMargins(0, 0, 0, 0)
        ssid_section_layout.setSpacing(8)
        ssid_section_layout.addWidget(ssid_label)
        ssid_section_layout.addWidget(self.ssid_input)
        
        control_layout.addWidget(ssid_section)
        
        # 修改密码输入区域
        password_container = QWidget()
        password_container.setObjectName("inputContainer")
        password_container.setMinimumHeight(48)
        password_container.setStyleSheet("""
            #inputContainer {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
            }
            #inputContainer:hover {
                border-color: #4CAF50;
                background-color: #fafafa;
            }
            #inputContainer:focus {
                border-color: #4CAF50;
                background-color: white;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
            }
        """)
        
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入热点密码（至少8位）")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("passwordInput")
        self.password_input.setMinimumHeight(48)
        # 添加文本变化和焦点变化的事件处理
        self.password_input.textChanged.connect(self.update_password_visibility_button)
        self.password_input.focusInEvent = self.password_focus_in
        self.password_input.focusOutEvent = self.password_focus_out
        self.password_input.setStyleSheet("""
            #passwordInput {
                border: none;
                padding: 12px 15px;
                background: transparent;
                font-size: 15px;
                color: #333333;
            }
            #passwordInput::placeholder {
                color: #999999;
                font-size: 14px;
            }
        """)
        
        # 创建显示/隐藏密码按钮
        self.toggle_password_btn = QPushButton()
        self.toggle_password_btn.setObjectName("togglePasswordButton")
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.setFixedSize(48, 48)
        self.toggle_password_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        self.toggle_password_btn.hide()  # 初始状态隐藏按钮
        
        # 防止按钮点击导致输入框失焦
        self.toggle_password_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 设置初始图标
        self.toggle_password_btn.setIcon(self.svg_to_icon(self.eye_closed_svg))
        self.toggle_password_btn.setIconSize(QSize(22, 22))
        
        # 添加样式
        self.toggle_password_btn.setStyleSheet("""
            #togglePasswordButton {
                border: none;
                background: transparent;
                margin-right: 8px;
                border-radius: 24px;
                opacity: 0.7;
            }
            #togglePasswordButton:hover {
                opacity: 1;
            }
        """)
        
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_btn)
        
        # 创建密码输入区域容器
        password_section = QWidget()
        password_section_layout = QVBoxLayout(password_section)
        password_section_layout.setContentsMargins(0, 0, 0, 0)
        password_section_layout.setSpacing(8)
        
        # 密码标签
        password_label = QLabel("密码")
        password_label.setObjectName("inputLabel")
        password_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
            }
        """)
        
        password_section_layout.addWidget(password_label)
        password_section_layout.addWidget(password_container)
        
        control_layout.addWidget(password_section)
        
        # 按钮
        self.start_button = QPushButton("开启热点")
        self.start_button.setObjectName("primaryButton")
        self.start_button.clicked.connect(self.toggle_hotspot)
        control_layout.addWidget(self.start_button)
        
        # 状态显示
        self.status_label = QLabel("状态: 未启动")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.status_label)
        
        # 添加版权信息
        copyright_label = QLabel("© 2024 Soleil | <a href='https://github.com/GalacticDevOps/LiteWifi' style='color: #666666; text-decoration: none;'>GitHub</a>")
        copyright_label.setObjectName("copyrightLabel")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setOpenExternalLinks(True)
        copyright_label.setStyleSheet("""
            #copyrightLabel {
                color: #666666;
                font-size: 12px;
                margin-top: 10px;
            }
            #copyrightLabel a:hover {
                color: #4CAF50;
                text-decoration: underline;
            }
        """)
        
        main_layout.addWidget(control_card)
        main_layout.addWidget(copyright_label)
        main_layout.addStretch()

    def create_card(self) -> QWidget:
        """创建卡片式面板"""
        card = QFrame()
        card.setObjectName("card")
        return card

    def load_settings(self):
        """加载保存的设置"""
        ssid = self.settings.value('ssid', '')
        password = self.settings.value('password', '')
        self.ssid_input.setText(ssid)
        self.password_input.setText(password)

    def save_settings(self):
        """保存设置"""
        self.settings.setValue('ssid', self.ssid_input.text())
        self.settings.setValue('password', self.password_input.text())

    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 只在必要时重绘
        if not self.isActiveWindow():
            self.repaint()

    def activate_from_tray(self):
        """从托盘激活窗口"""
        if self.isMinimized():
            self.showNormal()
        
        # 如果窗口经可见且活跃，则不需要做任何事
        if self.isVisible() and self.isActiveWindow():
            return
        
        # 确保窗口可见
        self.show()
        
        # 设置窗口位置到屏幕中心
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # 激活窗口
        self.activateWindow()
        self.raise_()

    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setIcon(self.svg_to_icon(self.eye_open_svg))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setIcon(self.svg_to_icon(self.eye_closed_svg))
        # 点击后让输入框重新获得焦点
        self.password_input.setFocus()

    def svg_to_icon(self, svg_data, size=24):
        """将SVG数据转换为QIcon"""
        if not hasattr(self, '_icon_cache'):
            self._icon_cache = {}
        
        # 使用SVG数据作为缓存键
        cache_key = hash(svg_data)
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]
        
        svg_bytes = svg_data.encode('utf-8')
        svg_base64 = base64.b64encode(svg_bytes).decode('utf-8')
        icon = QIcon()
        icon.addPixmap(QPixmap.fromImage(QImage.fromData(base64.b64decode(svg_base64))))
        
        # 缓存图标
        self._icon_cache[cache_key] = icon
        return icon

    def update_password_visibility_button(self):
        """根据密码输入框的状态更新显示/隐藏按钮的可见性"""
        if self.password_input.text() and self.password_input.hasFocus():
            self.toggle_password_btn.show()
        else:
            self.toggle_password_btn.hide()
            # 如果隐藏按钮时密码是可见的，将其切换回隐藏状态
            if self.password_input.echoMode() == QLineEdit.EchoMode.Normal:
                self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.toggle_password_btn.setIcon(self.svg_to_icon(self.eye_closed_svg))

    def password_focus_in(self, event):
        """密码输入框获得焦点时的处理"""
        QLineEdit.focusInEvent(self.password_input, event)
        if self.password_input.text():
            self.toggle_password_btn.show()

    def password_focus_out(self, event):
        """密码输入框失去焦点时的处理"""
        QLineEdit.focusOutEvent(self.password_input, event)
        # 检查新的焦点是否是显示/隐藏按钮
        if QApplication.focusWidget() != self.toggle_password_btn:
            # 延迟隐藏按钮，以便点击按钮时能够正常工作
            QTimer.singleShot(200, self.delayed_hide_button)

    def delayed_hide_button(self):
        """延迟隐藏密码可见性按钮"""
        # 检查密码输入框是否真的失去了焦点
        if not self.password_input.hasFocus() and not self.toggle_password_btn.isDown():
            self.toggle_password_btn.hide()
            # 确保密码在失去焦点时恢复隐藏状态
            if self.password_input.echoMode() == QLineEdit.EchoMode.Normal:
                self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.toggle_password_btn.setIcon(self.svg_to_icon(self.eye_closed_svg))