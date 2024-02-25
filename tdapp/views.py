from django.shortcuts import render, redirect
from django.views.generic import View
from tdapp.models import Activity
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
decs=[signin_required,never_cache]


class TodoForm(forms.ModelForm):
    class Meta:
        model=Activity
        exclude=('user_object',)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

@method_decorator(decs,name="dispatch")
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Activity.objects.filter(user_object=request.user)
        return render(request, "todo_list.html",{"data":qs})

@method_decorator(decs,name="dispatch")
class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            # form.save()
            data=form.cleaned_data
            Activity.objects.create(**data,user_object=request.user)
            messages.success(request,"activity added successfully")
            return redirect("todo-all")
        else:
            messages.error(request,"failed to add transaction")
            return render(request,"todo_add.html",{"form":form})

@method_decorator(decs,name="dispatch")
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Activity.objects.get(id=id)
        return render(request,"todo_detail.html",{"data":qs})

@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Activity.objects.get(id=id).delete()
        messages.success(request,"activity has been removed")
        return redirect("todo-all")

@method_decorator(decs,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Activity.objects.get(id=id)
        form=TodoForm(instance=todo_object)
        return render(request,"todo_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Activity.objects.get(id=id)
        data=request.POST
        form=TodoForm(data,instance=todo_object)
        if form.is_valid():
            form.save()
            messages.success(request,"To-do updated")
            return redirect("todo-all")
        else:
            messages.error(request,"updation failed")
            return render(request, "todo_list.html",{"form":form})


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("record has been added")
            return redirect("signin")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("todo-all")
        print("invalid")
        return render(request,"signin.html",{"form":form})

@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")