import sqlite3 as sql
import os
if not os.path.isdir('Database'):  # 创建目录Database
    os.makedirs('Database')
# 创建账户表，包含ID，密码，时间，邮箱

def get_all_reg_acc() -> dict:  # 获取已经注册过的id等数据,需要传入账户库指针
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS acc(ID,password,time,email)")  
    accounts = {'admin': ['admin123456', '2022/09/20', 'fag_identify_norep@yeah.net']}  # 内置一个管理员账户
    cur_acc.execute("SELECT * FROM acc")  # 账户库指针选中acc表中的所有内容
    acc = cur_acc.fetchall()  # 账户库指针复制acc表中的所有内容
    for each in acc:  # 遍历账户库指针中获取到的内容，并依次添加进入accounts字典
        profile = [each[1], each[2], each[3]]
        accounts[each[0]] = profile
    return accounts  # 返回所有账户字典

def insert_acc_data(info : list) -> bool:
    con_account = sql.connect("Database/account.db")  # 连接账户数据库文件account.db
    cur_acc = con_account.cursor()  # 创建account数据库对应的指针cur_acc
    cur_acc.execute("CREATE TABLE IF NOT EXISTS acc(ID,password,time,email)")  
    try:
        cur_acc.execute("INSERT INTO acc(ID,password,time,email) VALUES(?,?,?,?)", info)
        con_account.commit()
        return True
    except:
        return False