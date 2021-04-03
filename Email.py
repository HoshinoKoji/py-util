import smtplib, traceback, sys
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def sendEmail(SERVER, SENDER, PASSWORD, ADDRESS, Subject, Text):
    ret = True
    try:
        msg = MIMEText(Text, 'html', 'utf-8')
        msg['From'] = formataddr([SENDER, SENDER])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(['', ADDRESS])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = Subject

        server = smtplib.SMTP_SSL(SERVER, 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(SENDER, PASSWORD)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(SENDER, [ADDRESS, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:
        print('发送失败！')
        traceback.print_exc()
        ret = False
    
    return ret