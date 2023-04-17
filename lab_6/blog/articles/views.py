from articles.models import Article
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "GET":
            return render(request, 'form.html', {})
        else:
            form = {
                'text': request.POST['text'].strip(),'author':request.user, 'title': request.POST['title'].strip()
            }
            if form['text'] and form['title']:
                try:
                    post = Article.objects.get(title=form['title'])
                    form['errors'] = u"Такая статья уже существует"
                    return render(request, 'form.html', {'form':form})
                except Article.DoesNotExist:
                    per=Article.objects.create(text=form['text'],author=form['author'], title=form['title'])
                    return redirect('archive')
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'form.html', {'form': form})
    else:
        raise Http404


def register_user(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            if request.POST["username"]and request.POST["email"] and request.POST["password"]:

                form = {
                    'username': request.POST["username"],
                    'email': request.POST["email"],
                    'password': request.POST["password"],
                }
                if form["username"] == '' or form["email"] == ''  or form["password"] == '' :
                    form['errors'] = u"вы отправили пустую строку в одно из полей"
                    return render(request, 'register.html', {'form': form})

                if_username_unique = User.objects.filter(username=form["username"])
                if_email_unique = User.objects.filter(email=form["email"])

                if len(if_username_unique) == 0 and len(if_email_unique) == 0:
                    article = User.objects.create_user(form["username"], form["email"], form["password"])
                    # form['errors'] = u"Вы зарегистрированы! Теперь войдите в систему"
                    # return render(request, 'login.html', {'form': form})
                    return redirect('login_user', form=form)
                else:
                    form['errors'] = u"Не уникальный юзернейм/почта"
                    return render(request, 'register.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'register.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'register.html', {})
    else:
        raise Http404

def login_user(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'username': request.POST["username"],
                 'password': request.POST["password"],
            }
            if form["username"] and form["password"]:
                if form["username"] == '' or form["password"] == '' :
                    form['errors'] = u"вы отправили пустую строку в одно из полей"
                    return render(request, 'login.html', {'form': form})

                user = authenticate(username=form["username"], password=form["password"])

                if user:
                    form['errors'] = u"Вы успешно вошли!"
                    login(request, user)
                    return render(request, 'login.html', {'form': form})
                else:
                    form['errors'] = u"Не правильный пароль или логин"
                    return render(request, 'login.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'login.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'login.html', {})
    else:
        return render(request, 'archive.html', {})
