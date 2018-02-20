from django.shortcuts import render
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
from . import models,forms,tokens
from django.forms import formset_factory
from django.views.generic.edit import UpdateView
from datetime import *
# Create your views here.

Room_allot = True    #Change it after room allotment


def RoomAllotment(request):
    user = request.user
    if Room_allot:

        ##get hostel from user info and hostels
        hostel = models.HostelBranchYear.objects.get(year=User.personal.year, branch=User.personal.dept) ##get hostel
        rooms = models.Roominfo.objects.filter(hostel=hostel.hostel, is_filled=False,room_no__gte=hostel.start_room, room_no__lte=hostel.end_room)
        current_time = datetime.now()
        for room in rooms:
            if not is_check(room.timestamp , current_time):
                room.timestamp = None
                room.member1 = None
                room.member2 = None
                room.member3 = None
                room.save()
        ##Updating time f
        return HttpResponse(render(request,'room_list.html', {'rooms':rooms}))
    else:
        return HttpResponse("Sorry")


def RoomConfirm(request,pk):
    n  = models.Roominfo.objects.get(pk=pk).hostel.per_room - 1
    if request.method=='POST':
        formset = formset_factory(forms.RoomEntry)
        filled_forms = formset(request.POST)
        receivers = []
        room = models.Roominfo.objects.get(pk=pk)
        #room.member1 = request.user.personal
        if filled_forms.is_valid():
            count = 1
            for form in filled_forms:
                count +=1
                rec = form.cleaned_data['mail_id']
                user = User.objects.get(email=rec)
                current_site = get_current_site(request)
                account_activation = tokens.Confirm_room_mail()
                ctx = {'room': room, 'domain': current_site.domain,
                       'uidb64': urlsafe_base64_encode(force_bytes(room.pk)),
                       'token': account_activation.make_token(room)}
                message = render_to_string('account_activation.html', {'room': room, 'domain': current_site.domain,
                                                                       'uidb64': urlsafe_base64_encode(
                                                                           force_bytes(room.pk)),
                                                                       'token': account_activation.make_token(room)})
                message = get_template('account_activation.html').render(ctx)
                subject = 'Confirm your room allotment'

                try:
                    if count == 2:
                        room.member2 = User.objects.get(email=rec)
                    else:
                        room.member3 = User.objects.get(email=rec)
                    msg = EmailMessage(subject, message, to=[rec])
                    msg.content_subtype = 'html'
                    msg.send()
                except:
                    return HttpResponse('tera kata')
                #room.save()
            room.member1 = request.user.personal
            room.timestamp = datetime.now()
            room.in_queue = True
            room.save()
            return HttpResponse('Success')
        else:
            return HttpResponse('sorry')
    else:
        mailing = formset_factory(forms.RoomEntry, extra=n)
        return HttpResponseRedirect(render(request,'email_conf.html'))


def activate(request,uidb64,token):
    account_token = tokens.Confirm_room_mail()
    try:
        room_id = force_text(urlsafe_base64_decode(uidb64))
        room = models.Roominfo.objects.get(pk=room_id)

    except:
        room = None

    if room is not None and account_token.check_token(room, token) and room.timestamp is not None:#and ##time:
        room.is_filled = True
        room.in_queue = False
        room.save()
        return HttpResponse('successfully verified')
    else:
        return HttpResponse('invalid link')




def is_check(timestamp1, timestamp2):
    if timestamp1 is None:
        return False
    c = timestamp2 - timestamp1
    c = c.seconds/60
    if c<6:
        return True
    return False

def process(request):
    pk = request['select']
    return HttpResponseRedirect(reverse('room:confirm', kwargs={'pk':pk} ))