from django.shortcuts import render,redirect
from .models import User
from .forms import UserForm,RegisterForm
from .models import ConfirmString
import hashlib
from django.core.mail import EmailMultiAlternatives
from mysite import settings
import datetime
# Create your views here.

def hash_code(s,salt='B1t8yte'):
    h = hashlib.sha256();
    s+=salt;
    h.update(s.encode());
    return h.hexdigest();

def index(request):
    pass
    return render(request,'login/index.html');

def login(request):
    if request.session.get('is_login',None):
        return redirect('login/index.html');
    if request.method == 'POST':
        login_form = UserForm(request.POST);
        print(request.session['_auth_user_hash'])
        if login_form.is_valid():
            username = login_form.cleaned_data['username'];
            password = login_form.cleaned_data['password'];
            try: #如果没有错误
                user = User.objects.get(name=username);
                if not user.has_confirmed:
                    message = '该用户还没通过邮件验证';
                    return render(request,'login/login.html',locals());
                if user.password == hash_code(password):
                    request.session['is_login']=True;
                    request.session['user_id']=user.id;
                    request.session['user_name']=user.name;
                    return redirect('/index/');
                else:
                    message = '密码不正确!';
            except:
                    message = '用户名不存在!';
        return render(request,'login/login.html',locals());
    login_form = UserForm();
    return render(request,'login/login.html',locals());

def register(request):
    if request.session.get('is_login',None):
        #登录状态不允许注册
        return redirect('/index/');
    if request.method == 'POST':
        register_form = RegisterForm(request.POST);
        if register_form.is_valid():
            username = register_form.cleaned_data['username'];
            password = register_form.cleaned_data['password'];
            password2 = register_form.cleaned_data['password2'];
            email = register_form.cleaned_data['email'];
            sex = register_form.cleaned_data['sex'];
            if password != password2:
                message = "两次输入的密码不同！"
                return render(request,'login/register.html',locals());
            else:
                same_user_name = User.objects.filter(name=username);
                print(same_user_name);
                if same_user_name:
                    message = '用户名已经存在，请重新选择用户名';
                    return render(request,'login/register.html',locals());
                same_email_user = User.objects.filter(email=email);
                if same_email_user:
                    message = '该邮箱已存在，请使用别的邮箱!';
                    return render(request,'login/register.html',locals());
                # 当用户名/邮箱不存在，且密码校验正确则注册
                new_user = User();
                new_user.name = username;
                new_user.password = hash_code(password);
                new_user.email = email;
                new_user.sex = sex;
                new_user.save();
                code = make_confirm_string(new_user);
                send_mail(email,code);
                message = '请前往注册邮箱，确认邮件!';
                return render(request,'login/confirm.html',locals());
    register_form = RegisterForm();
    return render(request,'login/register.html',locals());

def logout(request):
    if request.session.get('is_login',None):
        del request.session['is_login'];
        del request.session['user_id'];
        del request.session['user_name'];
        # or request.session.flush();
    return redirect('/index/');

def send_mail(email,code):
    subject = "注册邮件";
    to_email = '2303186535@qq.com';
    text_content = '你好，欢迎注册X。看到这个页面说明你的邮箱不支持html，请联系管理员！';
    html_content = '''<p>感谢注册<a href="http://{}/confirm/?code={}" target="blank">localhost</a>\
                    这里是我的博客，专注与技术的分享！</p>
                    <p>清点击链接完成注册</p>
                    <p>注册码有效期:{}</p>
                    '''.format('127.0.0.1:8000',code,settings.CREATE_DAYS);
    msg = EmailMultiAlternatives(subject=subject,body=text_content,from_email=settings.EMAIL_HOST_USER,to=[to_email]);
    msg.attach_alternative(html_content,'text/html');
    msg.send();

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    code = hash_code(user.name,now);
    ConfirmString.objects.create(code=code,user=user);
    return code;

def user_confirm(request):
    code = request.GET.get('code',None);
    message ='';
    try:
        confirm = ConfirmString.objects.get(code=code);
    except:
        message = '无效的确认请求';
        return render(request,'login/confirm.html',locals());
    c_time = confirm.c_time;
    now = datetime.datetime.now();
    if now > c_time + datetime.timedelta(settings.CREATE_DAYS):
        confirm.user.delete();
        message = '您的邮件已经过期了,请重新注册!';
        return render(request,'login/confirm.html',locals());
    else:
        confirm.user.has_confirmed = True;
        confirm.user.save();
        confirm.delete();
        message = '感谢确认,请使用账户登录';
        return render(request,'login/confirm.html',locals());