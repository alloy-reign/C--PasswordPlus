from django.shortcuts import redirect, render
from .models import *
# Create your views here.



def index(request):
    # check user in session
    if 'user' not in request.session:
        return redirect('/login')

    passwords = SavedPassword.objects.filter(user=request.session['user'])
    import base64
    for password in passwords:
        
        password.password = base64.b64decode(password.password).decode('utf-8')
    return render(request, 'index.html', {'passwords': passwords})

def login(request):
    return render(request, 'login.html')


def checkuser(requset):
    email = requset.POST.get('email')
    password = requset.POST.get('password')

    user = User.objects.filter(email=email, password=password)
    if user:
        requset.session['user'] = user[0].id
        return redirect('/')
    else:
        return render(requset, 'login.html', {'error': 'Invalid email or password'})


def register(request):
    return render(request, 'register.html')

def adduser(request):
    email = request.POST.get('email')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 != password2:
        return render(request, 'register.html', {'error': 'Passwords do not match'})
    
    user = User.objects.filter(email=email)
    if user:
        return render(request, 'register.html', {'error': 'Email already exists'})

    user = User(email=email, fname=fname, lname=lname, password=password1)
    user.save()
    # store session
    request.session['user'] = user.id
    return redirect('/')

def logout(request):
    del request.session['user']
    return render(request,'login.html')

def addpassword(request):
    sitename = request.POST.get('sitename')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.get(id=request.session['user'])
    import base64
    encoded_password = base64.b64encode( str(password).encode('utf-8'))
    savedpassword = SavedPassword(user=user, name=sitename, username=username, password=encoded_password.decode('utf-8'))
    savedpassword.save()
    return redirect('/')

def deletepassword(request,id):
    pwd = SavedPassword.objects.get(id=id)
    pwd.delete()
    return redirect('/')