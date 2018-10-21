'''
#简单邮件发送，纯文件。每次发送一封都要连接一次smtp服务器
import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings';

if __name__ == "__main__":
    result = send_mail('注册信息认证邮件','你好,您的验证码是：asak2jf2 .很高兴您注册本站,thx!','emoly00@yeah.net',['2303186535@qq.com'],)
'''

#发送HTML格式邮件
import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings';

if __name__ == "__main__":
    subject,from_email,to = "来自<-X->的注册邮件",'emoly00@yeah.net',"2303186535@qq.com";
    text_content = "hello,welcome to the X WebSite of Library,your signd info code:as39f1l2";
    html_content = '<p>欢迎访问<a href="https://www.cnblogs.com/dontgiveup">MySite</a>这里是我的学习的记录园地!@</p>';
    msg = EmailMultiAlternatives(subject,text_content,from_email,[to]);
    msg.attach_alternative(html_content,'text/html');
    msg.send();