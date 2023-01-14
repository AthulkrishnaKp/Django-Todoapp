import re
from webbrowser import get
from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView,UpdateView
from todo.models import Task
from todo.forms import RegistrationForm,LoginForm,TaskUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache

# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)    
    return wrapper

decs=[signin_required,never_cache]


# class IndexView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,"index.html")

# class LoginView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,"login.html")      

# class RegisterView(View):     
#     def get(self,request,*args,**kwargs):
#         return render(request,"register.html")




@method_decorator(decs,name="dispatch")
class AddTaskView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"addtask.html")

    def post(self,request,*args,**kwargs):
        name=request.user
        task=request.POST.get("task")
        Task.objects.create(user=name,task_name=task)
        messages.success(request,"Task has been created")
        return redirect("todo-all")   


@method_decorator(decs,name="dispatch")
class TaskListView(ListView):
    model=Task
    template_name="tasklist.html"
    context_object_name="todos"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    # {"object_list":qs}

# class TaskListView(View):
#     def get(self,request,*args,**kwargs): 
#         if request.user.is_authenticated:
#             qs=Task.objects.filter(user=request.user)
#             # qs=request.user.task_set.all()
#             return render(request,"tasklist.html",{"todos":qs})
#         else:
#             return redirect('signin')    
         





@method_decorator(decs,name="dispatch")
class TaskDetailsView(DetailView):
    model=Task
    template_name="taskdetails.html"
    context_object_name="todo"
    pk_url_kwarg="id"
    
# class TaskDetailsView(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("id")
#         task=Task.objects.get(id=id)
#         return render(request,"taskdetails.html",{"todo":task})





@method_decorator(decs,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Task.objects.filter(id=id).delete() 
        messages.success(request,"Task deleted") 
        return redirect("todo-all")    


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{'form':form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account Created")
            return redirect("signin")
        else:
            messages.error(request,"Registration Failed")
            return render(request,"register.html",{'form':form}) 



class LoginFormView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")   
            pwd=form.cleaned_data.get("password") 
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                # print("success")
                login(request,usr)
                return redirect("todo-all")
            else:
                # print("failed")
                messages.error(request,"Invalid Credentials")
                return render(request,"login.html",{"form":form})    

@method_decorator(decs,name="dispatch")
class TaskUpdateView(UpdateView):
    model=Task
    form_class=TaskUpdateForm
    template_name="taskupdate.html"
    pk_url_kwarg="id"
    success_url=reverse_lazy("todo-all")


    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     qs=Task.objects.get(id=id)
    #     form=TaskUpdateForm(instance=qs)
    #     return render(request,"todo_update.html",{"form":form})




@signin_required
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")





#  Add View  Add task    

#  {{}} - Simple task
#  {%%} - Complex task