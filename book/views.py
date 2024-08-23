from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from .models import Book, Star, Rating, Tag
from django.contrib import messages
from likeordislike.models import Like, Dislike
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from comment.forms import ParentCommentForm, ChildCommentForm
from comment.models import ParentComment, ChildComment

# Create your views here.




#delete book

def delete_book_view(request, book):
    book = Book.objects.get(name = book)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST':
        book.delete()

        messages.success(request, 'Your book successfuly deleted!')
        return redirect('/')

    context = {
        'book': book
    }
    return render(request, 'book/delete_book.html', context)
    







#book update view function
@login_required
def update_book_function(request, book):
    user = request.user
    book = get_object_or_404(Book.objects.select_related("owner", "tag"), name = book)
    
    form = BookForm(request.POST or None, request.FILES or None, instance=book)

    if form.is_valid():
        form.save()
        messages.success(request, f"\"{book.name}\" book succesfully updated!")
        return redirect('book:detail', book.pk)


    context = {
        'form': form,
        'book': book
    }
    return render(request, 'book/update_book.html', context)








# BOOK DETAIL VIEW GET

def check_is_liked(request, book):
    """
    This function help us to know if user liked return True otherwase False
    """
    user = request.user
    is_liked = False
    if user.is_authenticated:
        if book.get_like_or_not(user):
            is_liked = True
        else:
            is_liked = False
    return is_liked


def check_is_disliked(request, book):
    """
    This function help us to know if user disliked return True otherwase False
    """
    user = request.user
    is_disliked = False
    if user.is_authenticated:
        if book.get_dislike_or_not(user):
            is_disliked = True
        else:
            is_disliked = False
    return is_disliked


def add_to_views(user, book):
    """
    This function current user is checked detail of the Book object
    then added user to views
    """
    if user.is_authenticated:
        if user not in book.views.all():
            book.views.add(user)


def get_comments(book):
    """
    This function gives Book's comment
    """
    return ParentComment.objects.select_related("user", "book", "parent").prefetch_related("likes", "dislikes").filter(book = book)


def add_to_comment(request, form, book):
    """
    This function add to comment when write comment
    """
    if request.method == 'POST':
        form = ParentCommentForm(request.POST or None)
        user = request.POST.get('user')

        if user != 'AnonymousUser':
            if form.is_valid():
                obj = form.save(commit=False)
                obj.book = book
                obj.user = request.user
                obj.save()
                return redirect('book:detail', book.pk)

        else:
            messages.error(request, 'Comment qaldiriw ushin siz dizimnen yamasa loginnen otiwin\'izge tuwri keledi!')
            return redirect('book:detail', book.pk)


def get_is_rating(user, book):
    """
    This function define user set rating of the book or not
    """
    if user.is_authenticated:
        get_rating = book.get_rating(user)
        if get_rating is not None:
            return True
        return False


def get_score(user, book):
    score = None
    if user.is_authenticated:
        if book.get_score(user) != False:
            score = book.get_score(user).score
    return score
    


def book_detail_view(request, *args, **kwargs):
    user = request.user
    pk = kwargs.get('pk')
    book = get_object_or_404(Book.objects.select_related("owner", "tag").prefetch_related("views", "book_star"), pk = pk)

    # ADD TO VIEWS
    add_to_views(user, book)
    # END ADD TO VIEWS

    # COMMENT FORM & ADD TO COMMENT
    form = ParentCommentForm()
    add_to_comment(request, form, book)
    # END COMMENT FORM & ADD TO COMMENT
    
    #aldinnan created etip qoyamiz
    liked_book, created = Like.objects.get_or_create(book = book)
    disliked_book, created = Dislike.objects.get_or_create(book = book)
    
    recommend_books = Book.objects.select_related("tag", "owner").filter(tag = book.tag).exclude(name  = book.name)
    first_book = Book.objects.filter(tag = book.tag).exclude(name  = book.name).first()
    
    context = {
        'book': book,
        'is_rating': get_is_rating(user, book),
        'score': get_score(user, book),
        'is_liked': check_is_liked(request, book),
        'is_disliked': check_is_disliked(request, book),
        'recommend_books': recommend_books,
        'first_book': first_book,
        'form': form,
        'comments': get_comments(book),
    }
    return render(request, 'book/book_detail.html', context)
# END BOOK DETAIL VIEW GET






# Rating for star

def star_rating_view(request):
    user = request.user
    if request.method == 'POST':
        book_name = request.POST.get('book')
        score = int(request.POST.get('score'))
        book = Book.objects.filter(name = book_name).first()
        rating, created = Rating.objects.select_related("book", "user").get_or_create(book = book, user = user)
        star, created = Star.objects.select_related("book").prefetch_related("users").get_or_create(book = book, star = score)

        if rating.score != score:
            rating.score = score
            rating.save()

            define_users = Star.objects.prefetch_related("users").filter(book = book).exclude(star = score)
        
            if define_users.exists():
                for obj in define_users:
                    if user in obj.users.all():
                        obj.users.remove(user)
                

            if user not in star.users.all() and star.star != score:
                star.users.add(user)
                star.percentage_of_score = 0.1
                star.save()
                
            elif user not in star.users.all() and star.star == score:
                star.users.add(user)
                star.percentage_of_score = float(star.percentage_of_score) + 0.1
                star.save()
    

    return JsonResponse({'data': 'Saved'})







#Add book
@login_required
def add_book(request):
    context = { }
    tags = Tag.objects.all()
    


    if request.method == 'POST':
        form = BookForm(request.POST or None, request.FILES or None)

        tag = request.POST.get('tag') or None
        
        if tag is not None:
            get_tag, created = Tag.objects.get_or_create(title = tag)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner = request.user
                obj.tag = get_tag
                obj.save()

                messages.success(request, 'Kitap awmetli saqlandi!')
                return redirect('myaccount:my-account', request.user.pk)

        else:
            messages.error(request, 'Siz qaysi turine tiyisli ekenin kiritiwiniz shart')
            return redirect('book:add-book')

    else:
        form = BookForm(request.POST or None, request.FILES or None)


    context['tags'] = tags        
    context['form'] = form        

    
    return render(request, 'book/add_book.html', context)




