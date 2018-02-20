from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from . import forms,tokens,models
from django.views.generic.edit import UpdateView

# Create your views here.
def signup(request):
    form = forms.Signup(request.POST)
    a = reverse('register:signup')

    if form.is_valid():
        ##if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
            ##return HttpResponse(render(request, 'form.html', {'form':form, 'form_id': a, 'error': 'passwords don`t match'}))
        if form.cleaned_data['username'].split('@')[1] not in ['itbhu.ac.in','iitbhu.ac.in']:
            #return HttpResponse(render(request,'',context=))
            return 0
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.email = form.cleaned_data['username']
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        account_activation = tokens.Activate_user()
        ctx = {'user': user, 'domain':current_site.domain,'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation.make_token(user)}
        message = render_to_string('account_activation.html', {'user': user, 'domain':current_site.domain,'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation.make_token(user)})
        message = get_template('account_activation.html').render(ctx)
        subject = 'Activate Your IITBHU HostelPortal Account'
        sender = form.cleaned_data['email']
        try:
            msg = EmailMessage(subject, message, to=[sender])
            msg.content_subtype = 'html'
            msg.send()
        except:
            user.delete()
            form = forms.Signup()
            return HttpResponse(render(request, 'form.html', {'form': form, 'form_id': a}))
        return HttpResponseRedirect(reverse('register:profile', kwargs={'pk': user.pk}))
    else:
        try:
            form = forms.Signup(request.POST)
        except:
            form = forms.Signup()
        return HttpResponse(render(request,'form.html', {'form': form, 'form_id': a}))