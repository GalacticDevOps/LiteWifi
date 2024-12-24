# WiFi热点管理工具

![License](https://img.shields.io/github/license/GalacticDevOps/LiteWifi)
![Version](https://img.shields.io/github/v/release/GalacticDevOps/LiteWifi)
[![Build Release](https://github.com/GalacticDevOps/LiteWifi/actions/workflows/release.yml/badge.svg)](https://github.com/GalacticDevOps/LiteWifi/actions/workflows/release.yml)
![Downloads](https://img.shields.io/github/downloads/GalacticDevOps/LiteWifi/latest/total.svg)
![Issues](https://img.shields.io/github/issues/GalacticDevOps/LiteWifi)

## 说明

> [!IMPORTANT]
>
> ### 严肃警告
>
> - 请务必遵守 [GNU Affero General Public License (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.html) 许可协议
> - 在您的修改、演绎、分发或派生项目中，必须同样采用 **AGPL-3.0** 许可协议，**并在适当的位置包含本项目的许可和版权信息**
> - **禁止用于售卖或其他盈利用途**，如若发现，作者保留追究法律责任的权利
> - 禁止在二开项目中修改程序原版权信息（ 您可以添加二开作者信息 ）
> - 感谢您的尊重与理解

- 欢迎各位大佬 `Star` 😍

## 👀 项目简介

这是一个基于Windows系统的WiFi热点管理工具，可以在没有网络的情况下创建和管理移动热点。本工具提供图形化界面，支持系统托盘运行，适合日常使用。

## ⚙️ 环境要求
- Windows 10/11 操作系统
- 支持WiFi的网卡
- 需要管理员权限运行

## 🎉 功能
1. 热点管理
   - 创建/开启/关闭WiFi热点
   - 自定义热点名称(SSID)和密码
   - 实时显示热点状态
   - 支持系统托盘运行

2. 使用特点
   - 单实例运行，避免重复开启
   - 支持最小化到系统托盘
   - 自动保存上次的配置
   - 界面简洁易用

## 技术特性
- 使用 PyQt6 构建现代化界面
- 采用 Windows 原生 API 创建热点
- 支持静默运行，不显示命令行窗口
- 打包体积优化，仅包含必要组件

## 使用说明
1. 以管理员身份运行程序
2. 输入热点名称和密码（密码至少8位）
3. 点击"开启热点"按钮创建热点
4. 可以最小化到系统托盘继续运行
5. 双击托盘图标可以重新打开主窗口

## 注意事项
1. 首次运行需要以管理员权限启动
2. 确保系统的移动热点服务已启用
3. 如果创建失败，请检查WiFi适配器是否支持热点功能
4. 程序可以最小化到系统托盘，不会直接退出

## 版本历史
- v1.0.0
  - 初始版本
- v1.0.1
  - 优化系统托盘功能
  - 修复窗口激活问题
  - 减小程序体积
  - 改进错误提示
- v1.0.2
  - 支持密码显示/隐藏
  - 支持密码自动保存


## 技术架构
- 开发语言：Python 3.8+
- GUI框架：PyQt6
- 网络管理：Windows API
- 打包工具：PyInstaller

## 项目结构
```
LiteWifi/
├── main.py # 程序入口文件
├── wifi_hotspot.spec # PyInstaller打包配置
├── file_version_info.txt # 程序版本信息
├── README.md # 项目说明文档
├── assets/ # 资源文件目录
│ └── icon.ico # 程序图标
├── core/ # 核心功能模块
│ ├── init.py
│ └── hotspot.py # 热点管理核心类
└── gui/ # 图形界面模块
├── init.py
├── main_window.py # 主窗口类
└── styles.py # 界面样式定义
```