from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.urls import reverse
from django.db.models import Avg, Count
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.views.decorators.vary import vary_on_headers

from recipient.forms import LoginForm, UserRegistrationForm, AddReview, SearchForm, ReviewEditForm
from recipient.models import Review, Recipient


def polzovatelskoe_soglashenie(request):
    return render(request, 'about_site/polzovatelskoe_soglashenie.html')


def politika_konfidencialnosti(request):
    return render(request, 'about_site/politika_konfidencialnosti.html')


@cache_page(60 * 15)
def o_kompanii(request):
    return render(request, 'about_site/o_kompanii.html')


def base_page(request):
    recipients = (
        Recipient.objects.filter(reviews__is_published=True)
        .annotate(avg_rating=Avg('reviews__rate'))
        .prefetch_related('specialities')
        .order_by('-avg_rating')
    )
    users = User.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')

    return render(request,
                  'recipient/base_page.html',
                  {'users': users, 'recipients': recipients})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вы успешно аунтентифицировались!')
                else:
                    return HttpResponse('Аутентификация не прошла!')
            else:
                return HttpResponse('Невалидный аккаунт!')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@require_GET
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {"user_form": user_form})


@login_required
def self_cabinet(request):
    user = get_object_or_404(User, username=request.user.username)
    reviews = Review.objects.select_related('recipient', 'user').prefetch_related('recipient__specialities').filter(user=user)

    return render(request,
                  'recipient/self_cabinet.html',
                  {"user": user,
                   "reviews": reviews})


def recipients_info(request):
    recipients = Recipient.objects.prefetch_related('specialities')

    return render(request,
                  'recipient/all_recipients.html',
                  {'recipients': recipients
                   })


def recipient_info(request, recipient_id):
    recipient = Recipient.objects.prefetch_related('specialities', 'reviews').get(pk=recipient_id)

    return render(request,
                  'recipient/recipient_info.html',
                  {'recipient': recipient})


def user_info(request, user_id):
    user = User.objects.prefetch_related('reviews').order_by('-reviews').get(pk=user_id)

    return render(request,
                  'recipient/user_info.html',
                  {'user': user})


@login_required
def add_review(request, recipient_id):
    recipient = get_object_or_404(Recipient.objects.prefetch_related("specialities"), pk=recipient_id)

    if request.method == 'POST':
        form = AddReview(request.POST)

        if form.is_valid():
            review_object = form.save(commit=False)
            review_object.recipient = recipient
            if request.user.is_authenticated:
                review_object.user = request.user

            if request.META.get('REMOTE_ADDR'):
                review_object.user_ip = request.META.get('REMOTE_ADDR')

            review_object.save()
            return redirect(reverse('success_review'))
        else:
            messages.error(request, 'Должно быть хотя бы 100 символов')

    else:
        form = AddReview()

    return render(request,
                  'recipient/add_review.html',
                  {'recipient': recipient, 'form': form
                   })


def success_review(request):
    return render(request, 'recipient/success_review.html', )


def edit_review(request, pk):
    print(pk)
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewEditForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['modified_review'])
            print('top')
            return redirect(reverse('not_published_reviews'))
    else:
        form = ReviewEditForm(instance=review)

    return render(request,
                  'recipient/edit_review.html',
                  {'review': review, 'form': form})


@user_passes_test(lambda u: u.is_superuser)
def not_published_reviews(request):
    reviews = (
        Review.objects.select_related('recipient', 'user')
        .prefetch_related('recipient__specialities')
        .filter(is_published=False)
    )

    return render(request, 'recipient/not_published_reviews.html', {'reviews': reviews})

def recipient_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Recipient.objects.filter(first_name__icontains=query)

    return render(request,
                  'recipient/search_recipient.html',
                  {'form': form,
                   'query': query,
                   'results': results})
