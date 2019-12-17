from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *
from .forms import CommentForm
from django.http import HttpResponseRedirect





class EventList(ListView):
    model = Event
    template_name = 'event/index.html'
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# class EventDetail(DetailView):
#     model = Event
#     template_name = 'event/event_detail.html'


#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         is_favourites = False
#         event = get_object_or_404(Event, id=id)
#         if event.favorites.filter(pk=request.user.pk).exists():
#             is_favourites = True
#         context['is_favourites'] = is_favourites
#         return context

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    categories = Category.objects.all()
    is_favourite = False

    if event.favorites.filter(pk=request.user.pk).exists():
        is_favourite = True

    # new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.event = event
            new_comment.save()
    else:
        comment_form = CommentForm()
    comment_form = event.events.filter(active=True)

    context = {
        'event': event,
        'categories': categories,
        'is_favourite': is_favourite,
        'comment_form': comment_form,
    }
    return render(request, 'event/event_detail.html', context=context)




def event_favorite_list(request):
    user = request.user
    favorite_events = user.favorites.all()
    return render(request, 'event/event_favorite_list.html', context={'favorite_events': favorite_events})


def favorite_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.favorites.filter(pk=request.user.pk).exists():
        event.favorites.remove(request.user)
    else:
        event.favorites.add(request.user)
    return HttpResponseRedirect(event.get_absolute_url())



def filter_by_category(request, pk):
    category = Category.objects.get(pk=pk)
    filtered_event = Event.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'event/category.html', {

        'category': category,
        'filtered_event': filtered_event,
        'categories': categories
    })


def filter_by_tag(request, pk):
    tag = Tag.objects.get(pk=pk)
    filtered_event = Event.objects.filter(tags=tag)
    categories = Category.objects.all()
    return render(request, 'event/tag.html', {

        'tag': tag,
        'filtered_event': filtered_event,
        'categories': categories
    })

def filter_by_date(request):
    try:
        date = request.GET.get('calendar')
        filtered_event = Event.objects.filter(date=date)
        if filtered_event.exists():
            categories = Category.objects.all()
            return render(request, 'event/date.html', {
                'date': date,
                'filtered_event': filtered_event,
                'categories': categories
            })
        else:
            categories = Category.objects.all()
            return render(request, 'event/not_gound.html', {
                'categories': categories
            })

    except ValidationError:
        events = Event.objects.all()
        categories = Category.objects.all()
        return render(request, 'event/index.html', {
            'events': events,
            'categories': categories
        })

def add_subscribes(request, pk):
    # Subscriber.objects.create(subscriber=request.user, category=category_id)
    # return render(request, 'event/category.html', {
    #     'events': events,
    #     'categories': categories
    # })
    category = get_object_or_404(Category, pk=pk)
    if category.subscriber.filter(pk=request.user.pk).exists():
        category.subscriber.remove(request.user)
    else:
        category.subscriber.add(request.user)
    return HttpResponseRedirect('/')




class CategoryListView(ListView):
    model = Category
    template_name = "event/category_list.html"
    context_object_name = "categories_list"

class CategoryDetailView(DetailView):
    model = Category
    template_name = "event/category_detail.html"
    context_object_name = "category_item"

