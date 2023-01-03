import smtplib
import random
import json
import sys
import os
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/"
print(path)
from email.mime.text import MIMEText
from email.header import Header


def generate_id_code() -> str:
    """生成验证码
    :参数：无参数
    :返回：返回生成的验证码
    """
    char_check = ''
    for i in range(6):
        # 生成一个不包括0,o和O的字符
        char1 = random.choice([chr(random.randint(65, 78)), chr(random.randint(80, 90)), str(random.randint(1, 9)),
                               chr(random.randint(97, 110)), chr(random.randint(112, 122))])
        char_check += char1
    return char_check


def send_email(user_name: str, target_email: str, id_code: str) -> bool:
    """发送验证邮件
    :参数：user_name：用户名，target_email：目标邮箱，id_code：验证码
    :返回：无返回
    """
    with open(path + "settings/settings.json", 'r') as f:
        information = json.load(f)
    my_mail = information["Email"]["Addr"]
    password = information["Email"]["Password"]
    smtp_server = information["Email"]["SMTP_Server"]
    port = information["Email"]["SMTP_Port"]
    information = ""

    content2 = """<!doctype html>
<html lang="zh" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
  <title> 欢迎注册Fight Against Gravity账户！ </title>
  <!--[if !mso]><!-- -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <!--<![endif]-->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style type="text/css">
    #outlook a {
      padding: 0;
    }

    body {
      margin: 0;
      padding: 0;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }

    table,
    td {
      border-collapse: collapse;
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
    }

    img {
      border: 0;
      height: auto;
      line-height: 100%;
      outline: none;
      text-decoration: none;
      -ms-interpolation-mode: bicubic;
    }

    p {
      display: block;
      margin: 13px 0;
    }
  </style>
  <!--[if mso]>
        <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
  <!--[if lte mso 11]>
        <style type="text/css">
          .mj-outlook-group-fix { width:100% !important; }
        </style>
        <![endif]-->
  <!--[if !mso]><!-->
  <link href="https://fonts.googleapis.com/css?family=Muli:300,400,700" rel="stylesheet" type="text/css">
  <style type="text/css">
    @import url(https://fonts.googleapis.com/css?family=Muli:300,400,700);
  </style>
  <!--<![endif]-->
  <style type="text/css">
    @media only screen and (min-width:480px) {
      .mj-column-per-100 {
        width: 100% !important;
        max-width: 100%;
      }
    }
  </style>
  <style type="text/css">
    @media only screen and (max-width:480px) {
      table.mj-full-width-mobile {
        width: 100% !important;
      }

      td.mj-full-width-mobile {
        width: auto !important;
      }
    }
  </style>
  <style type="text/css">
    a,
    span,
    td,
    th {
      -webkit-font-smoothing: antialiased !important;
      -moz-osx-font-smoothing: grayscale !important;
    }
  </style>
</head>

<body style="background-color:#f9f0e6;">
  <div style="background-color:#f9f0e6;">
    <!--[if mso | IE]>
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:600px;"
            >
          <![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tr>
                    <td style="font-size:0px;word-break:break-word;">
                      <!--[if mso | IE]>
    
        <table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td height="20" style="vertical-align:top;height:20px;">
      
    <![endif]-->
                      <div style="height:20px;"> &nbsp; </div>
                      <!--[if mso | IE]>
    
        </td></tr></table>
      
    <![endif]-->
                    </td>
                  </tr>
                  <tr>
                    <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                        <tbody>
                          <tr>
                            <td style="width:75px;">
                              <img height="auto" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="75">
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </table>
              </div>
              <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
        <table
           align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:600px;" width="600"
        >
          <tr>
            <td  style="line-height:0;font-size:0;mso-line-height-rule:exactly;">
              <v:image
                 style="border:0;mso-position-horizontal:center;position:absolute;top:0;width:600px;z-index:-3;" src="https://www.convtool.com/FAGDark.png"  xmlns:v="urn:schemas-microsoft-com:vml"
              />
      <![endif]-->
    <div style="margin:0 auto;max-width:600px;">
      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tr style="vertical-align:top;">
          <td background="https://www.convtool.com/FAGDark.png" 
          style="background:#ffffff url(https://www.convtool.com/FAGDark.png) no-repeat center center /
           cover;background-position:center center;background-repeat:no-repeat;padding:0px;vertical-align:top;" 
           height="240">
            <!--[if mso | IE]>
        <table
           border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
        >
          <tr>
            <td  style="">
      <![endif]-->
            <div class="mj-hero-content" style="margin:0px auto;">
              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;margin:0px;">
                <tr>
                  <td style>
                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;margin:0px;">
                    </table>
                  </td>
                </tr>
              </table>
            </div>
            <!--[if mso | IE]>
            </td>
          </tr>
        </table>
      <![endif]-->
          </td>
        </tr>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
    
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:0px;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:600px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Muli, Arial, sans-serif;font-size:20px;font-weight:400;line-height:30px;text-align:left;color:#333333;">
                                  <h1 style="margin: 0; font-size: 24px; line-height: normal; font-weight: bold;">完成注册您的Fight Against Gravity账户</h1>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <p style="border-top: solid 1px #F4F5FB; font-size: 1px; margin: 0px auto; width: 100%;">
                                </p>
                                <!--[if mso | IE]>
        <table
           align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 1px #F4F5FB;font-size:1px;margin:0px auto;width:550px;" role="presentation" width="550px"
        >
          <tr>
            <td style="height:0;line-height:0;">
              &nbsp;
            </td>
          </tr>
        </table>
      <![endif]-->
                              </td>
                            </tr>
                            <tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Muli, Arial, sans-serif;font-size:16px;font-weight:400;line-height:20px;text-align:left;color:#333333;">
                                  <p style="margin: 0;">您好！""" + user_name + """，您的验证码为：</p>
                                </div>
                              </td>
                            </tr>
                            <br>
                            <tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Muli, Arial, sans-serif;font-size:30px;font-weight:400;
                                line-height:20px;text-align:center;font-weight:bold;color:rgb(61, 139, 240);">
                                  <p style="margin: 0;"> """ + id_code + """</p>
                                </div>
                              </td>
                            </tr>
                          </table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:600px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:0;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:600px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Muli, Arial, sans-serif;font-size:14px;font-weight:400;line-height:20px;text-align:left;color:#333333;">
                                  <br>
                                  <p style="margin: 0;">请不要将该验证码发给任何人！ </p>
                                  <p style="margin: 0;">如果您从未选择注册Fight Against Gravity账户，请忽略此邮件！ </p>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td align="right" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Muli, Arial, sans-serif;font-size:16px;font-weight:400;
                                line-height:20px;text-align:right;color:#333333;">
                                  <p style="margin: 0;"> 此致, <br> Fight Against Gravity团队</p>
                                </div>
                              </td>
                            </tr>
                          </table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:600px;"
            >
          <![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tr>
                    <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                      <div style="font-family:Muli, Arial, sans-serif;font-size:14px;font-weight:400;
                      line-height:20px;text-align:center;
                      color:#616161;">Copyright © 2023 Fight Against Gravity Team. <br>
                      欢迎访问我们的项目主页<a href="https://github.com/Voltline/Fight_Against_Gravity">Fight Against Gravity</a></div>
                    </td>
                  </tr>
                </table>
              </div>
              <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:600px;"
            >
          <![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tr>
                    <td style="font-size:0px;word-break:break-word;">
                      <!--[if mso | IE]>
    
        <table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td height="1" style="vertical-align:top;height:1px;">
      
    <![endif]-->
                      <div style="height:1px;"> &nbsp; </div>
                      <!--[if mso | IE]>
    
        </td></tr></table>
      
    <![endif]-->
                    </td>
                  </tr>
                </table>
              </div>
              <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      <![endif]-->
  </div>
</body>

</html>"""

    msg = MIMEText(content2, 'HTML', 'utf-8')
    msg['From'] = Header("Fight Against Gravity<fag_identify_norep@yeah.net>")
    head = user_name+f"<{target_email}>"
    msg['To'] = Header(head)
    msg["Subject"] = Header("验证您的身份")

    try:
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, port)
        server.login(my_mail, password)
        server.sendmail(my_mail, target_email, msg.as_string())

        server.quit()
        return True
    except Exception as e:
        print(f"[Error]: {e}")
        return False
