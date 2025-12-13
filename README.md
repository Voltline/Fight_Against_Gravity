<div align="center">
  <img src=assets/texture/FAGtitle.png >
</div>

# Fight Against Gravity
> *Hope all of you can enjoy Fight Against Gravity!*

![License](https://img.shields.io/github/license/Voltline/Fight_Against_Gravity)
![Issues](https://img.shields.io/github/issues/Voltline/Fight_Against_Gravity)
![Stars](https://img.shields.io/github/stars/Voltline/Fight_Against_Gravity)

## 目录结构/Project Structure
- `main.py`：客户端入口，启动 Pygame 窗口与场景。
- `server.py`：无头专用服务器入口。
- `Server/`：房间/用户管理、TCP/UDP 通信、日志等后台逻辑。
- `content/`：游戏场景、实体、地图定义与 UI 组件。
- `assets/`：纹理、音频等静态资源。
- `settings/`：多套配置 JSON 与加载器 `all_settings.py`。
- 工具：`joysticktest.py` 手柄检测，`test.py` 网络探针。

## 快速开始/Getting Started
1. 准备 Python 3.10+，建议虚拟环境：
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 本地一键跑通（服务器 + 客户端，连接 127.0.0.1）：
   ```bash
   ./scripts/run_local.sh
   ```
   默认使用 `settings/settings_local.json`（本地 IP/端口，内置本地注册服务器一起启动）。
3. 单独启动客户端：
   ```bash
   python main.py [--debug] [--nogui]
   ```
   `--nogui` 仅启动网络层，便于联机测试。
4. 单独启动专用服务器（默认绑定设置文件中的本地 IP/端口）：
   ```bash
   python server.py [--debug]
   ```
   `server.py` 已内置 SDL dummy 驱动，适合无显示的主机。
5. 配置：修改 `settings/settings.json`（或 `settings_local.json` / `settings_sakura.json`），`--debug` 使用本地配置。

## 成员/Collaborators
* [ZYH (Voltline)](https://github.com/Voltline)
* [LTY (D_S_O_)](https://github.com/DissipativeStructureObject)
* [LKY (ShiinaRikka)](https://github.com/lky1433223)
* [CDC (Cdccc1)](https://github.com/Cdccc1)

## 项目概况
* 项目开始于2022年9月27日
* 总代码数约为8000行（截至2023年1月5日）

## Project Brief Introduction
* The project starts on September 27, 2022
* The total number of codes is about 8000 lines (as of January 5, 2023)

## 游戏简介
* 以宇宙为背景，两名玩家分别操控自己的飞船在有限地图中遨游
* 地图中包含位居中心的行星或处于运动中的多星系统
* 玩家需要在行星引力的干扰之下控制自己的飞船和子弹
* 所有玩家需要在尽力击落对方飞船的同时避免自己被吸入行星或被对方子弹攻击导致摧毁

## Game Brief Introduction
* With the universe as the background, two players control their own spaceships to travel in a limited map. 
* The map contains a planet in the center or a multi satellite system in motion. 
* Players need to control their spaceship and bullets under the interference of the planet's gravity. 
* All of players have to shoot down the opponent's spaceship while avoiding being sucked into the planet or being destroyed by the opponent's bullet.

## 项目信息/About Fight Against Gravity
### 语言与模块/Lang & Modules
* 语言/Lang：Python
* 主体/Main Part：pygame
* 在线/Online Part：socket，pycryptodome，base64，smtplib
* 数据/Data Part：json，sqlite3
* 其他/Other Part: os，sys
### 开源协议/Open-Source Protocol
* GNU General Public License 3.0
### 反馈
&emsp;&emsp;游戏制作周期不长，难免有所疏漏，我们也很期待您能给我们提供您所发现的问题，这对于我们有着非常非常大的帮助。

&emsp;&emsp;遇到问题时，您可以发送邮件到我们的Bug报告邮箱：fag_bug_report@yeah.net，当然您也可以在GitHub中开启讨论，我们一定会尽快回复。

&emsp;&emsp;最后，衷心地感谢您对Fight Against Gravity的支持！
### Feed Back
&emsp;The project's development spends not so long, which inevitably leads to some omissions. We also look forward to 
your providing us with the problems you found, which will be so helpful to us.

&emsp;When you encounter problems, you can send email to our BugReport Email: fag_bug_report@yeah.net , you can also 
open a discussion in GitHub, we'll reply you in very soon.

&emsp;Finally, we sincerely thank you for your support to Fight Against Gravity!
 
