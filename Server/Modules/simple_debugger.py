# 这是一个用于服务端进行指令调试的debugger
import re
from Server.server_main import ServerMain
from Server.Modules.User import User
from Server.Modules.Room import Room


def debugger(self: ServerMain):
    """服务器端的简单指令调试器
    :参数：指令字符串
    :返回：无返回值
    """
    help_script1 = """*| 目前调试器支持以下指令：
*| echo    ls    rm    kick    ban    unban    help    exit
*| 指令格式：[command] [args](中间用空格分隔)
"""

    help_script2 = """*| echo [args] (args可选room-roomid、player-用户名，打印出房间信息、用户信息)
    例如: echo room-24819290 或 echo player-FAG_Admin
    
*| ls [args] (args可选room/player，分别列出当前所有在线的房间名与roomid、用户名)
    例如: ls room 或 ls player
"""

    help_script3 = """
*| rm [roomid] (args需要输入一个roomid，用于关闭/删除当前存在的一个房间)
    例如: rm 24819290
    
*| kick [username] (需要输入一个用户名，用于将用户踢出游戏)
    例如: kick FAG_Admin
    当且仅当被提出用户在房间中时才会被踢出
"""

    help_script4 = """
*| ban [username] [days] (需要输入用户名与天数(1~365)，用于封禁玩家特定天数)
    例如: ban FAG_Admin 365
    
*| unban [username] (输入一个用户名，立即解除当前封禁状态) 
    例如: unban FAG_Admin
    
*| help (无参数，打印帮助)
    例如: help
"""

    def echo(args: str) -> bool:
        room_type = """房间基本信息
* 标识:    %s
* 名字:    %s
* 地图:    %s
* 房主:    %s
* 玩家:
"""
        user_type = """用户基本信息
* 用户名:  %s
* 房间:    %s
* 地址:    %s
"""

        if "-" in args:
            echo_type = args.split("-")[0]
            echo_object_id = args.split("-")[1]
            if echo_type == 'room':
                if echo_object_id in self.room_list:
                    echo_object = self.room_list[echo_object_id]
                    room_info = echo_object.get_all_info()
                    for user in room_info[3]:
                        room_type += f"{user.get_name()}"
                    print(room_type % (room_info[0], room_info[2],
                                       room_info[4], room_info[1]))
                    return True
            elif echo_type == 'player':
                if echo_object_id in self.user_list:
                    echo_object = self.user_list[echo_object_id]
                    user_roomid = echo_object.get_roomid()
                    if user_roomid is None:
                        user_roomid = "未加入任何游戏"
                    print(user_type % (echo_object.get_name(),
                                       user_roomid,
                                       echo_object.get_address()))
                    return True
        return False

    def ls(args: str) -> bool:
        if args.strip(" ") == "room":
            for room_id, room in self.room_list.items():
                print(f"{room_id} , 房间名 : {room.get_roomname()} , 房主 : {room.get_owener()}")
            return True
        elif args.strip(" ") == "player":
            for username, user in self.user_list.items():
                print(f"{username} , 地址 : {user.get_address()}")
            return True
        return False

    def rm(args: str) -> None:
        print("暂时还没完成") # TODO: 等Room有了解散之后再做
        pass

    def kick(args: str) -> bool:
        username = args.strip(" ")
        if username in self.user_list:
            roomid = self.user_list[username].get_roomid()
            if roomid is not None:
                self.room_list[roomid].del_user(username)
                return False
            else:
                print("该用户不在任何房间中！")
                return False
        return False

    def ban(args: list) -> None:
        username = args[0]
        day = args[1]
        # TODO: 等我之后把验证服务器之类的改一改再来做ban和unban

    def unban(args: str) -> None:
        pass

    def help_debug() -> None:
        print(help_script1)
        input("按回车查看第2页")
        print(help_script2)
        input("按回车查看第3页")
        print(help_script3)
        input("按回车查看第4页")
        print(help_script3)

    commands = {'echo': echo, 'ls': rm, 'kick': kick, 'unban': unban}
    pattern = re.compile("(.*?) (.*)")  # 两个部分分别匹配指令与参数
    pattern_ban = re.compile("ban (.*?) (\d+)")
    while True:
        ans = True
        command = input()
        if len(command) <= 1000:
            while "  " in command:
                command = command.replace("  ", " ")
            list_cmd = re.findall(pattern, command)
            if list_cmd:
                list_cmd = list_cmd[0]
                if list_cmd[0] in commands:
                    func = commands[list_cmd[0]]
                    ans = func(list_cmd[1])
                else:
                    ans = False
            else:
                ban_cmd = re.findall(pattern_ban, command)
                if ban_cmd is None:
                    if command.strip(" ") == 'help':
                        help_debug()
                    else:
                        ans = False
                else:
                    ban_cmd = ban_cmd[0]
                    ban(ban_cmd[1:])
        else:
            print("指令长度太长！请重新输入！")

        if not ans:
            print("指令输入有误/操作失败！请重新输入！")


if __name__ == "__main__":
    debugger(None)
