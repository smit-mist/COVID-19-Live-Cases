from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ReviewForm, Review, Search, Searchform
import requests
import json


def index(request):
    selected_tret = 0

    all_con = 0
    all_rec = 0
    all_dead = 0
    top_t_con = 0
    top_t_tret = 0
    death_rate = 0
    top_t_dead = 0
    top_t_rec = 0
    data_json = requests.get("https://api.covid19api.com/summary")
    list_all = []
    top_t = []
    data = data_json.text
    data_d = json.loads(data)
    list_l = data_d['Countries']
    for e in range(len(list_l)):
        if list_l[e]['Country'] == 'India':

            selected_con = int(list_l[e]['TotalConfirmed'])
            selected_dead = int(list_l[e]['TotalDeaths'])
            selected_rec = int(list_l[e]['TotalRecovered'])
            selected_tret = selected_con - selected_dead - selected_rec
            if selected_con == 0:
                sel_death_rate = 0
            else:
                sel_death_rate = round(selected_dead * 100 / selected_con, 2)
            selected_name = list_l[e]['Country']

    for j in list_l:
        list_all.append(int(j['TotalConfirmed']))
        all_con += int(j['TotalConfirmed'])
        all_dead += int(j['TotalDeaths'])
        all_rec += int(j['TotalRecovered'])
        if all_con == 0:
            death_rate = 0
        else:
            death_rate = round((all_dead / all_con) * 100, 2)

    list_all.sort()
    list_all.reverse()
    k = list_all[0:10]
    for r in range(len(k)):
        for s in list_l:

            if k[r] == s['TotalConfirmed']:
                top_t.append(s)
                top_t_con += s['TotalConfirmed']

    for o in top_t:
        top_t_dead += int(o['TotalDeaths'])
        top_t_rec += int(o['TotalRecovered'])
    top_t_tret = top_t_dead + top_t_rec

    if request.method == "POST":
        error = ""
        a = False
        form = Searchform(request.POST)
        country_name = form.data['country_name']
        for h in list_l:
            if country_name == str(h['Country']) or country_name == h['Country'].upper() or country_name == h[
                'Country'].lower():
                selected_name = h['Country']
                selected_con = int(h['TotalConfirmed'])
                selected_dead = int(h['TotalDeaths'])
                selected_rec = int(h['TotalRecovered'])
                selected_tret = selected_con - selected_dead - selected_rec
                sel_death_rate = round((selected_dead / selected_con) * 100, 2)
                a = True
        data = requests.get(
            "https://pkgstore.datahub.io/core/country-list/data_json/data/8c458f2d15d9f2119654b29ede6e45b8/data_json.json")

        final = data.text

        smit = json.loads(final)

        code = "IN"
        # print(smit)
        for c in smit:
            if selected_name == c['Name'] or selected_name == c['Name'].lower() or selected_name == c['Name'].upper():
                code = c['Code']
                break

        if not a:
            error = "This Country is not found make sure you type country name properly!!"
        context = {'form': form,
                   'list': list_l,
                   "top_t": top_t,
                   "top_t_con": top_t_con,
                   "top_t_dead": top_t_dead,
                   "top_t_rec": top_t_rec,
                   "top_t_tret": top_t_tret,
                   "all_con": all_con,
                   "all_dead": all_dead,
                   "all_rec": all_rec,
                   "death_rate": death_rate,
                   "selected_name": selected_name,
                   "selected_con": selected_con,
                   "selected_rec": selected_rec,
                   "selected_dead": selected_dead,
                   "selected_tret": selected_tret,
                   "sel_death_rate": sel_death_rate,
                   "error": error,
                   "code": code
                   }
        return render(request, 'data/main.html', context)
    else:
        code = "IN"
        form = Searchform()
        context = {'form': form,
                   'list': list_l,
                   "top_t": top_t,
                   "top_t_con": top_t_con,
                   "top_t_dead": top_t_dead,
                   "top_t_rec": top_t_rec,
                   "top_t_tret": top_t_tret,
                   "all_con": all_con,
                   "all_dead": all_dead,
                   "all_rec": all_rec,
                   "death_rate": death_rate,
                   "selected_name": selected_name,
                   "selected_con": selected_con,
                   "selected_rec": selected_rec,
                   "selected_dead": selected_dead,
                   "selected_tret": selected_tret,
                   "code": code,
                   "sel_death_rate": sel_death_rate,

                   }
        return render(request, 'data/main.html', context)


def sug(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mob = form.cleaned_data['mob']
            msg = form.cleaned_data['msg']
            a = Review(name=name, mob=mob, msg=msg)
            a.save()
            return redirect('/')

        else:
            form = ReviewForm()
            return render(request, 'data/contact.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'data/contact.html', {'form': form})


def rank(request):
    data_json = requests.get("https://api.covid19api.com/summary")

    data = data_json.text
    data_d = json.loads(data)
    list_l = data_d['Countries']
    list_l.pop(0)
    list_l.pop(0)
    return render(request, 'data/rank.html', {'list_l': list_l})
