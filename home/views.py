from django.contrib.auth import authenticate, login, logout
from django.views import generic
from .models import Blog, Comment, Profile, Category, Commercial
from .forms import RegisterForm, AddBlogForm, CommentForm
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.core.validators import validate_email
import datetime
from django.db.models import Q


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.

# sākuma lapa - iegūst rakstus, kategorijas, reklāmas
# pārbauda vai netiek izmantota 'search funkcija'
# ja tiek, tad filtrē attiecīgos datus padodot tos uz html failu
def index(request):
    blogs = Blog.objects.all()
    categories = Category.objects.all().order_by('name')
    commercials = Commercial.objects.all()
    query = request.GET.get("q")
    if query:
        blogs = blogs.filter(
            Q(title__icontains=query)
        )
        search = True
        ctx = {'blogs': blogs, 'categories': categories, 'commercials': commercials, 'search':search}
        return render(request, 'home/index.html', ctx)
    ctx = {'blogs': blogs, 'categories': categories, 'commercials': commercials}
    return render(request, 'home/index.html', ctx)

# Vienīgais uz klasi bazētais skats, atlasa rakstus pēc to kategorijas
class CategoryView(generic.DetailView):
    model = Category
    template_name = 'home/index.html'
    def get_context_data(request, **kwargs):
        context = super(CategoryView, request).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        context['blogs'] = Blog.objects.all().filter(category=request.get_object())
        context['commercials'] = Commercial.objects.all()
        return context

#atrod lietotāju, kurš veic pieprasījumu
#atrod pieprasīto rakstu, ja nav tāda, tad 404, sameklē kategorijas
#izveido komentāra formu un iegūst komentāra datus
#apstrādā komentāras datus, ja tādi ir, kā arī izveidotā komentāra datus
#padod html failam
def blogview(request, blog_pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=blog_pk)
    categories = Category.objects.all().order_by('name')
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        comment = form.save(commit=False)
        text = request.POST['text']
        date_created = datetime.datetime.now()
        author = user
        comment.text = text
        comment.author = author
        comment.date_created = date_created
        comment.blog = blog
        comment.save()
    return render(request, 'home/article.html', {'blog': blog, 'user':user, 'categories': categories})

#Cita cilvēka profila skats
def profileview(request, pro_pk):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    user = get_object_or_404(User,pk=pro_pk)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'home/profile.html', {'profile': profile, 'user': user})

#Sava profila skats ar formām, par attiecīgajiem datu tipiem un to apstrādi
def userview(request, usr_pk):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        date = request.POST['date_of_birth']
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return render(request, 'home/user.html', {'profile': profile, 'user': user, 'error_message': 'Correct date format is YYYY-MM-DD'})
        profile.date_of_birth = request.POST['date_of_birth']
        profile.sex = request.POST['gender']
        profile.occupation = request.POST['occupation']
        if 'show_email' in request.POST:
            show_email = request.POST['show_email']
        else:
            show_email = False
        profile.show_email = show_email
        profile.bio = request.POST['bio']
        try:
            validate_email(request.POST['email'])
        except:
            return render(request, 'home/user.html', {'profile': profile, 'user': user, 'error_message': 'Incorrect e-mail format!'})
        all_users = User.objects.all()
        for users in all_users:
            if (users.email==request.POST['email']):
                if not (users.id==user.id):
                    return render(request, 'home/user.html', {'profile': profile, 'user': user, 'error_message': 'E-mail is already taken'})
            else:
                user.email = request.POST['email']
        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
            file_type = profile.picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'profile': profile,
                    'error_message': 'Image file must be PNG, JGP or JPEG',
                    'user': user,
                }
                return render(request, 'home/edit-blog.html', context)
        profile.save()
        user.save()
    return render(request, 'home/user.html', {'profile': profile, 'user':user})


#izdzēš interneta rakstu (var dzēst tikai savus rakstus)
def delete_blog(request, blog_pk):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    blog = Blog.objects.get(pk=blog_pk)
    blog.delete()
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'home/user.html', {'profile': profile, 'user': user})

#ielogošanas datu apstrāde.
def login_user(request):
    if request.user.is_authenticated():
        blogs = Blog.objects.all()
        categories = Category.objects.all().order_by('name')
        commercials = Commercial.objects.all()
        ctx = {'blogs': blogs, 'categories': categories, 'commercials': commercials}
        return render(request, 'home/index.html', ctx)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                blogs = Blog.objects.all().order_by('-date_created')
                categories = Category.objects.all().order_by('name')
                commercials = Commercial.objects.all()
                ctx = { 'blogs': blogs, 'categories': categories,'commercials':commercials }
                return render(request, 'home/index.html', ctx)
            else:
                return render(request, 'home/login-form.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'home/login-form.html', {'error_message': 'Invalid login'})
    return render(request, 'home/login-form.html')

#piereģistrēšanās datu apstrāde
def register_user(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        all_users = User.objects.all()
        for users in all_users:
            if (users.email == form.cleaned_data['email']):
                return render(request, 'home/register-form.html', {'form':form, 'error_message': 'E-mail is already taken'})
        user.save()
        profile = Profile(user=user)
        date = request.POST['date_of_birth']
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return render(request, 'home/register-form.html',{'form': form, 'error_message': 'Correct date format is YYYY-MM-DD'})
        profile.date_of_birth = date
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                blogs = Blog.objects.all()
                profile = Profile.objects.all()
                categories = Category.objects.all()
                commercials = Commercial.objects.all()
                ctx = { 'blogs': blogs, 'profile': profile,'user':user, 'categories':categories, 'commercials':commercials }
                return render(request, 'home/index.html', ctx)
    context = {
        "form": form,
    }
    return render(request, 'home/register-form.html', context)

#izlogoties
def logout_user(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    logout(request)
    form = RegisterForm(request.POST or None)
    blogs = Blog.objects.all().order_by('-date_created')
    categories = Category.objects.all().order_by('name')
    commercials = Commercial.objects.all()
    context = {
        'form': form, 'blogs': blogs, 'categories': categories,'commercials':commercials
    }
    return render(request, 'home/index.html', context)

#pievienot rakstu
def add_blog(request):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    else:
        form = AddBlogForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.text = request.POST['text']
            blog.author = request.user
            blog.date_created = datetime.datetime.now()
            blog.picture = request.FILES['picture']
            file_type = blog.picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'blog': blog,
                    'form': form,
                    'error_message': 'Image file must be PNG, JGP or JPEG',
                }
                return render(request, 'home/add-blog.html', context)
            blog.save()
            categories = Category.objects.all().order_by('name')
            comments = Comment.objects.all().order_by('-date_created').filter(blog=blog)
            context = {
                'blog':blog, 'categories':categories, 'comments':comments, 'just_created':True
            }
            return render(request, 'home/article.html', context)
        context = {
            'form':form,
        }
        return render(request, 'home/add-blog.html', context)

#izveido pieprasījumu uz raksta labošanu un nosūta uz citu lapu/formu
def edit_blog(request, blog_pk):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    user = request.user
    blog = get_object_or_404(Blog,pk=blog_pk)
    categories = get_list_or_404(Category)
    return render(request, 'home/edit-blog.html', {'user':user, 'blog':blog, 'categories': categories})

#var veikt attiecīgās korekcijas rakstam (var labot tikai savus rakstus)
def save_edit_blog(request, blog_pk):
    if not request.user.is_authenticated():
        return render(request, 'home/login-form.html')
    user = request.user
    blog = get_object_or_404(Blog, pk=blog_pk)
    categories = Category.objects.all()
    if request.method == "POST":
        if 'save' in request.POST:
            blog.title = request.POST['title']
            blog.text = request.POST['blog_text']
            blog.category_id = request.POST['category']
            if 'picture' in request.FILES:
                blog.picture = request.FILES['picture']
                file_type = blog.picture.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                       'blog': blog,
                        'error_message': 'Image file must be PNG, JGP or JPEG',
                        'categories': categories,
                        'user':user,
                    }
                    return render(request, 'home/edit-blog.html', context)
            blog.save()
        else:
            form = CommentForm(request.POST or None)
            comment = form.save(commit=False)
            text = request.POST['text']
            date_created = datetime.datetime.now()
            author = user
            comment.text = text
            comment.author = author
            comment.date_created = date_created
            comment.blog = blog
            comment.save()
    return render(request, 'home/article.html', {'blog': blog, 'user':user, 'categories': categories})

