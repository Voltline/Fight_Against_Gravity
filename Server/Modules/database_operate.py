import sqlite3 as sql
import os

if not os.path.isdir('Database'):  # 创建目录Database
    os.makedirs('Database')


# 创建账户表，包含ID，密码，时间，邮箱

def get_all_reg_acc() -> dict:
    """获取账户数据库所有信息
    :参数：无参数
    :返回：返回一个用户相关的字典
    """
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS acc(ID,password,time,email)")
    accounts = {'admin': ['admin123456', 'fag_identify_norep@yeah.net']}  # 内置一个管理员账户
    cur_acc.execute("SELECT * FROM acc")  # 账户库指针选中acc表中的所有内容
    acc = cur_acc.fetchall()  # 账户库指针复制acc表中的所有内容
    for each in acc:  # 遍历账户库指针中获取到的内容，并依次添加进入accounts字典
        profile = [each[1], each[3]]
        accounts[each[0]] = profile
    return accounts  # 返回所有账户字典


def check_duplicate(username: str) -> bool:
    """注册过程检查重复函数
    :参数：username：用户名
    :返回：是否重复（布尔值）
    """
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS acc(ID,password,time,email)")
    cur_acc.execute("SELECT * FROM acc")  # 账户库指针选中acc表中的所有内容
    acc = cur_acc.fetchall()  # 账户库指针复制acc表中的所有内容
    acc_username_key, acc_email_key = {}, {}
    for each in acc:  # 遍历账户库指针中获取到的内容，并依次添加进入accounts字典
        acc_username_key[each[0]] = each[3]
    check = False

    if username in acc_username_key:
        check = True

    return check


def check_match(info: list) -> bool:
    """检查用户名与邮箱是否匹配
    :参数：info：连接用户的信息列表
    :返回：返回修改结果
    """
    accounts = get_all_reg_acc()
    username, email = info
    if username in accounts and accounts[username][1] == email:
        return True
    else:
        return False


def insert_acc_data(info: list) -> bool:
    """注册插入用户数据
    :参数：info：用户信息列表
    :返回：返回添加结果
    """
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS acc(ID,password,time,email)")
    try:
        cur_acc.execute("INSERT INTO acc(ID,password,time,email) VALUES(?,?,?,?)", info)
        con_account.commit()
        return True
    except:
        return False


def insert_connection_data(info: list) -> bool:
    """插入一条连接信息
    :参数：info：连接用户的信息列表
    :返回：返回插入结果
    """
    con_con = sql.connect("Database/connection.db")  # 连接账户数据库文件connection.db
    cur_con = con_con.cursor()  # 创建connection数据库对应的指针cur_con
    cur_con.execute("CREATE TABLE IF NOT EXISTS acc(IP,time)")
    try:
        cur_con.execute("INSERT INTO acc(IP, time) VALUES(?,?)", info)
        con_con.commit()
        return True
    except:
        return False


def insert_login_data(info: list) -> bool:
    """插入一条登录记录
    :参数：info：连接用户的信息列表
    :返回：返回插入结果
    """
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS login_history(ID,time)")
    try:
        cur_acc.execute("INSERT INTO login_history(ID,time) VALUES(?,?)", info)
        con_account.commit()
        return True
    except:
        return False


def reset_password_data(info: list) -> bool:
    """重置用户密码数据
    :参数：info：连接用户的信息列表
    :返回：返回修改结果
    """
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS acc(ID,password,time,email)")
    try:
        cur_acc.execute("UPDATE acc SET password = ? where ID = ?", info)
        con_account.commit()
        return True
    except:
        return False
