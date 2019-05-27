try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication 
    import pynvml
    import datetime
    import time
    import sys
    import fire
except ImportError:
    print('import error')
    sys.exit(1)


def send(sendinfo):
    # sendinfo: str, the infomation you need to send.
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = 'hdusrt@163.com'  
    #密码(部分邮箱为授权码) 
    mail_pass = 'SRT13579'   
    #邮件发送方邮箱地址
    sender = 'hdusrt@163.com'  
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['hdusrt@163.com']  

    #设置email信息
    #邮件内容设置
    message = MIMEText(sendinfo,'plain','utf-8')
    #邮件主题       
    message['Subject'] = '112 GPU status' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('send success ')
        return True
    except smtplib.SMTPException as e:
        print('send error ',e) #打印错误
        return False

def GPUcheck():
    sendinfo = 'server 112,'
    set_free_percent = 60
    pynvml.nvmlInit()
    # all GPU numbers
    gpu_num = pynvml.nvmlDeviceGetCount() # real numbers
    for id in range(gpu_num):
        handle = pynvml.nvmlDeviceGetHandleByIndex(id)# i is the GPU id
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        #print(meminfo.total) #第二块显卡总的显存大小
        #print(meminfo.used)#这里是字节bytes，所以要想得到以兆M为单位就需要除以1024**2
        #print(meminfo.free) #第二块显卡剩余显存大小

        # get the free percent
        free_per = meminfo.free/meminfo.total*100
        if (free_per > set_free_percent):
            sendinfo = sendinfo + 'GPU ' + 'id '
            sendinfo = sendinfo + 'free percent more than '
            sendinfo = sendinfo + str(set_free_percent) + '      '
    flag = send(sendinfo)
    #if not os.path.exists('log'):
        #os.system(r'touch %s' % filename)
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(currenttime)
    if (flag):
        with open('GPUchecklog', 'a+') as f:
            f.writelines('send successfully at ' + currenttime + '\n')
    else:
        with open('GPUchecklog', 'a+') as f:
            f.writelines('failed to send at ' + currenttime + '\n')

if __name__ == "__main__":
    GPUcheck()
