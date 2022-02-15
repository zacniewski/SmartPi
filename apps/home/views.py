# -*- encoding: utf-8 -*-

import json
import os
from django import template
from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .forms import SettingsForm


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'home/dashboard.html')


@login_required(login_url="/login/")
def settings(request):
    with open(os.path.join(conf_settings.CORE_DIR, 'secrets.json'), 'r+') as secrets_file:
        file_data = json.load(secrets_file)
        default_location = file_data["default_location"]
        another_setting = file_data["another_setting"]
        # another settings will be here!
    return render(request, 'home/settings.html',
                  {"default_location": default_location,
                   "another_setting": another_setting})


@login_required(login_url="/login/")
def update_settings(request):
    default_location = request.GET.get("id_location")
    print(f"default_location = {default_location}")
    another_setting = request.GET.get("id_another_setting")
    print(f"another_setting = {another_setting}")

    with open(os.path.join(conf_settings.CORE_DIR, 'secrets.json'), 'r+') as secrets_file:
        file_data = json.load(secrets_file)
        file_data["default_location"] = default_location
        file_data["another_setting"] = another_setting
        secrets_file.seek(0)
        # convert back to json.
        json.dump(file_data, secrets_file, indent=4)
    return render(request, 'home/update-settings.html',
                  {"default_location": default_location,
                   "another_setting": another_setting})
