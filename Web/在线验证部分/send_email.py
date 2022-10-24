import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header
# email用于构建邮件内容

def generate_id_code():
    char_check = ''
    for i in range(8):
    # 生成一个不包括0,o和O的字符
        char1 = random.choice([chr(random.randint(65, 78)), chr(random.randint(80, 90)), str(random.randint(1, 9)),
                            chr(random.randint(97, 110)), chr(random.randint(112, 122))])
        char_check += char1
    return char_check

def send_email(user_name, target_email, id_code):
    my_mail = "fag_identify_norep@yeah.net"
    password = "KCJUXGAPEJWSLDLT"
    #target_email = "2502136346@qq.com"
    #user_name = "D_S_O_"
    #id_code = "FAGYYDS"

    content2 = """<div>
        <includetail>
            <div style="font:Verdana normal 14px;color:#000;">
                <div style="position:relative;">
                    <div class="eml-w eml-w-sys-layout">
                        <div style="font-size: 0px;">
                            &emsp;
                            <div class="eml-w-sys-line">
                                <div class="eml-w-sys-line-left"></div>
                                <div class="eml-w-sys-line-right"></div>
                            </div>
                            &emsp;
                            <div class="eml-w-sys-logo">
                                <img src="https://www.convtool.com/2_BigPic.png" style="width: 50px; height: 50px;" onerror="">
                            </div>
                        </div>
                        <div class="eml-w-sys-content">
                            <h1>完成注册Fight Against Gravity账户</h1>
                            <h2>&emsp;</h2>
                            &emsp;
                            <div class="dragArea gen-group-list">
                                <div class="gen-item">
                                    <div class="eml-w-item-block" style="padding: 0px;">
                                        <div class="eml-w-phase-normal-16"><b>你好，"""+user_name+"""，你的注册验证码为：</b></div>
                                </div>
                                </div>

                                <div class="gen-item">

                                    <div class="eml-w-item-block" style="padding: 0px;">
                                        <div class="eml-w-phase-normal-16" style="color: rgb(61, 139, 240);text-align: center;font-weight:bold;font-size: 30px"> """+id_code+""" </div>
                                    </div>
                                </div>
                                <div class="gen-item" draggable="false">
                                    <div class="eml-w-item-block" style="padding: 0px 0px 0px 1px;">
                                        <div class="eml-w-title-level3"><b>请不要将该验证码发给任何人！</b></div>
                                        <div class="eml-w-title-level3">如果您从未选择注册，请忽略该邮件。</div>
                                    </div>
                                </div>

                                <div class="gen-item" draggable="false">
                                    <div class="eml-w-item-block" style="padding: 0px;">
                                    </div>
                                </div>

                            </div>
                        </div>
                        <div class="eml-w-sys-footer">Fight Against Gravity 团队</div>
                    </div>
                </div>
            </div><!--<![endif]-->
        </includetail>
    </div>

    <style>
        .eml-w .eml-w-phase-normal-16 {
            color: #2b2b2b;
            font-size: 16px;
            line-height: 1.75
        }

        .eml-w .eml-w-phase-bold-16 {
            font-size: 16px;
            color: #2b2b2b;
            font-weight: 500;
            line-height: 1.75
        }

        .eml-w-title-level1 {
            font-size: 20px;
            font-weight: 500;
            padding: 15px 0
        }

        .eml-w-title-level3 {
            font-size: 16px;
            font-weight: 500;
            padding-bottom: 10px
        }

        .eml-w-title-level3.center {
            text-align: center
        }

        .eml-w-phase-small-normal {
            font-size: 14px;
            color: #2b2b2b;
            line-height: 1.75
        }

        .eml-w-picture-wrap {
            padding: 10px 0;
            width: 100%;
            overflow: hidden
        }

        .eml-w-picture-full-img {
            display: block;
            width: auto;
            max-width: 100%;
            margin: 0 auto
        }

        .eml-w-sys-layout {
            background: #fff;
            box-shadow: 0 2px 8px 0 rgba(0, 0, 0, .2);
            border-radius: 4px;
            margin: 50px auto;
            max-width: 700px;
            overflow: hidden
        }

        .eml-w-sys-line-left {
            display: inline-block;
            width: 88%;
            background: #2984ef;
            height: 3px
        }

        .eml-w-sys-line-right {
            display: inline-block;
            width: 11.5%;
            height: 3px;
            background: #8bd5ff;
            margin-left: 1px
        }

        .eml-w-sys-logo {
            text-align: right
        }

        .eml-w-sys-logo img {
            display: inline-block;
            margin: 30px 50px 0 0
        }

        .eml-w-sys-content {
            position: relative;
            padding: 20px 50px 0;
            min-height: 216px;
            word-break: break-all
        }

        .eml-w-sys-footer {
            font-weight: 500;
            font-size: 12px;
            color: #bebebe;
            letter-spacing: .5px;
            padding: 0 0 30px 50px;
            margin-top: 60px
        }

        .eml-w {
            font-family: Helvetica Neue, Arial, PingFang SC, Hiragino Sans GB, STHeiti, Microsoft YaHei, sans-serif;
            -webkit-font-smoothing: antialiased;
            color: #2b2b2b;
            font-size: 14px;
            line-height: 1.75
        }

        .eml-w a {
            text-decoration: none
        }

        .eml-w a, .eml-w a:active {
            color: #186fd5
        }

        .eml-w h1, .eml-w h2, .eml-w h3, .eml-w h4, .eml-w h5, .eml-w h6, .eml-w li, .eml-w p, .eml-w ul {
            margin: 0;
            padding: 0
        }

        .eml-w-item-block {
            margin-bottom: 10px
        }

        @media (max-width: 420px) {
            .eml-w-sys-layout {
                border-radius: none !important;
                box-shadow: none !important;
                margin: 0 !important
            }

            .eml-w-sys-layout .eml-w-sys-line {
                display: none
            }

            .eml-w-sys-layout .eml-w-sys-logo img {
                margin-right: 30px !important
            }

            .eml-w-sys-layout .eml-w-sys-content {
                padding: 0 35px !important
            }

            .eml-w-sys-layout .eml-w-sys-footer {
                padding-left: 30px !important
            }
        }
    </style>"""

    msg = MIMEText(content2, 'HTML', 'utf-8')
    msg['From'] = Header("Fight Against Gravity<fag_identify_norep@yeah.net>")
    msg['To'] = Header(user_name)
    msg["Subject"] = Header("验证您的身份")


    smtp_server = "smtp.yeah.net"

    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    server.login(my_mail, password)
    server.sendmail(my_mail, target_email, msg.as_string())

    server.quit()
