from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.
def index(request):
    return render(request,"index.html")

def spam(request):
    
    return render(request,"spamtest.html")

def predict(request):
    if request.method=="POST":
        spam=request.POST['mail']
        import numpy as np # linear algebra
        import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
        data=pd.read_csv(r'static/spam.csv',encoding='unicode_escape')
        print(data)
        print(data.columns)
        print(data.info())
        print(data.isna().sum())
        data['Spam']=data['Category'].apply(lambda x:1 if x=='spam' else 0)
        print(data.head(5))
        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test=train_test_split(data.Message,data.Spam,test_size=0.25)
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import Pipeline
        clf=Pipeline([
        ('vectorizer',CountVectorizer()),
        ('nb',MultinomialNB())
        ])
        clf.fit(X_train,y_train)
        emails=[spam]
        pred=clf.predict(emails)
        print("Predicted Spam Email: ",clf.predict(emails))
        print("Accuracy Score: ",clf.score(X_test,y_test))
        return render(request,"predict.html",{"spam":pred})
    else:
        return render(request,"spamtest.html")

def register(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['fname']
        email=request.POST['email']
        psw=request.POST['psw']
        psw1=request.POST['psw1']
        if psw==psw1:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"Username Exists")
                return render(request,"register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Exists")
                return render(request,"register.html")
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,
                email=email,username=uname,password=psw)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password not Matching")
            return render(request,"register.html")
    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        psw=request.POST['psw']
        user=auth.authenticate(username=uname,password=psw)
        if user is not None:
            auth.login(request,user)
            return redirect('spam')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request,"login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')