from django.shortcuts import render
from .models import Entry, Game_table, Language_table, Favorites_table, Recent_table
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect



# Create your views here.
def home_function(request, option='home', optional_game=False):
    e = Entry.objects.all().order_by('-viewers')
    if option == 'game':
        e = Entry.objects.filter(Game_table__game=optional_game)

    query = request.GET.get('q')
    if query:
        e = e.filter(
            Q(title__icontains=query) |
            Q(name_display__icontains=query) |
            Q(Game_table__game__icontains=query) |
            Q(source__icontains=query)
            ).distinct()



    if request.GET.get('source'):
        e = e.filter(source=request.GET.get('source'))
    if request.GET.get('language'):
        e = e.filter(Language_table__language=request.GET.get('language'))

    if request.GET.get('source', False) or request.GET.get('language', False):
        get_url = '?'+request.build_absolute_uri().split('/?')[1]
    else:
        get_url = False

    if option == 'favorites':
        e = Entry.objects.filter(Favorites_table__user=request.user)

    if option == 'recent':
        e = Entry.objects.filter(Recent_table__user=request.user).order_by('-Recent_table__updated')

    p = Paginator(e, 20)
    cur_page = int(request.GET.get('start', '1'))
    num_pages = p.num_pages
    total_items = p.count

    favorites_array = []
    favorites_entry = Favorites_table.objects.values_list('source_id', flat=True).filter(user=request.user)
    for f in range(len(favorites_entry)):
        favorites_array.append(favorites_entry[f])

    if cur_page < 7:
        page_start = 1
    elif (num_pages - cur_page) < 4:
        page_start = num_pages - 9
    else:
        page_start = cur_page - 5

    if (num_pages - cur_page) > 9:
        page_end = page_start + 9
    else:
        page_end = num_pages + 1

    game_table = Game_table.objects.values('game').distinct().order_by('game')
    source_tab = Entry.objects.values('source').distinct().order_by('source')
    language_tab = Language_table.objects.values('language').distinct().order_by('language')
    home_context = {
        'entry' : p.page(cur_page),
        'num_pages' : num_pages,
        'cur_page' : cur_page,
        'loop' : range(page_start, page_end),
        'total_items' : total_items,
        'game_table' : game_table,
        'source_tab' : source_tab,
        'source_get' : request.GET.get('source', False),
        'option' : option,
        'language_tab' : language_tab,
        'language_get' : request.GET.get('language', False),
        'abs' : 'http://davidykan.pythonanywhere.com/',
        'optional_game' : optional_game,
        'query' : query,
        'get_url' : get_url,
        'favorites_array' : favorites_array,
    }
    return home_context




# Create your views here.
def home(request):
    context = home_function(request)
    if context == 'redirect':
        return HttpResponseRedirect(request.get_full_path())
    else:
        return render(request, 'home.html', context)

def game(request, slug):
    context = home_function(request, 'game', slug)
    if context == 'redirect':
        return HttpResponseRedirect(request.get_full_path())
    else:
        return render(request, 'home.html', context)

def favorites(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        context = home_function(request, 'favorites')
        return render(request, 'home.html', context)

def recent(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        context = home_function(request, 'recent')
        return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('http://davidykan.pythonanywhere.com')

def delete(request):
    if request.user.is_authenticated():
        Favorites_table.objects.filter(user=request.user).filter(source_id=request.GET.get('source_id')).delete()
    return redirect('http://davidykan.pythonanywhere.com')

def external(request):
    if request.user.is_authenticated():
        a = request.GET.get('source_id')
        b = Recent_table(source_id_user=a+'_'+request.user.username, source_id=a, user=request.user.username)
        b.save()
        c = Entry.objects.get(source_id=a)
        b.entry.add(c)
    return redirect(request.GET.get('external'))

def add(request):
    if request.user.is_authenticated():
        a = request.GET.get('source_id')
        b = Favorites_table(source_id_user=a+'_'+request.user.username, source_id=a, user=request.user.username)
        b.save()
        c = Entry.objects.get(source_id=a)
        b.entry.add(c)
        return redirect('http://davidykan.pythonanywhere.com')
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))





