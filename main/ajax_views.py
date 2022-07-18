from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from . import models


def find_guest_equip(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    try:
        user_equip = request.user.guestequipment
    except ObjectDoesNotExist:
        user_equip = models.GuestEquipment(user=request.user)

    return user_equip


def get_guest_by_hash(guest_hash):
    try:
        guest = models.Guest.objects.get(hash=guest_hash)
        return guest

    except models.Guest.DoesNotExist:
        return None


def authenticate(request):
    guest = get_guest_by_hash(request.POST["guest_code"])
    
    if guest is None:
        response_data = {
            'status': 'not_found',
        }

    else:
        # For now email not used
        # guest_email = request.POST["guest_email"]

        # try:
        #     validate_email(guest_email)
        #     guest.email = guest_email
        #     guest.save()

        # except ValidationError:
        #     pass

        response_data = {
            'status': 'success',
        }
        user = guest.user
        login(request, user)

    return JsonResponse(response_data)


def get_guest_content(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    else:
        user_equip = find_guest_equip(request)
        message_objects = models.Message.objects.order_by('-date_created').all()
        messages_content = [{'date': msg.date_created, 'html': msg.html_text} for msg in message_objects]
        guest_content = {
            'guest_data': {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'guest_status': request.user.guest.status,
            },
            'guest_equip': {
                'has_car': user_equip.has_car,
                'mats': user_equip.mats_cnt,
                'tents': user_equip.tents_cnt,
            },
            'messages_content': messages_content,
        }
        return JsonResponse(guest_content)


def update_guest_status(request):
    user_equip = find_guest_equip(request)
    guest_obj = request.user.guest

    try:
        guest_obj.status = request.GET['guest_status']
        user_equip.has_car = bool(request.GET['has_car'] == 'true')
        user_equip.mats_cnt = int(request.GET['mats'])
        user_equip.tents_cnt = int(request.GET['tents'])

        guest_obj.save()
        user_equip.save()

    except:
        return HttpResponseBadRequest()

    response_data = {'status': 'success'}
    return JsonResponse(response_data)
