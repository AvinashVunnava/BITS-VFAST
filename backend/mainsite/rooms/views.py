import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
from rooms.models import NormalRoom
from django.core import serializers

# TODO list
#API decorator
#timings
#logs

URL = "https://www.fast2sms.com/dev/bulk"
PAYLOAD = "sender_id=anilFSTSMS&message={msg}&language=english&route=p&numbers={num}"
HEADERS = {
    'authorization': "sWnHgwGl1pPB0mC54kAdohOY7EvuR8rc2yiX6QtNaTLKf3ZSeb7GMCYAnTNL0b5ZpaIhmwviUsg169XO",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
 }

def index(request):
    return  JsonResponse({"success": True})

def student_booking(request):
    params_dict = request.GET
    params_dict = json.loads(list(params_dict.keys())[0])
    try:
        _type = params_dict.get("_type", "")
        student = params_dict.get("student", "")
        dept = params_dict.get("dept", "")
        _id = params_dict.get("_id", "")
        mobile_num = params_dict.get("mobile_num", "")
        purpose = params_dict.get("purpose", "")

        normal_rooms = NormalRoom.objects.filter(availability=1)
        normal_room_objs = normal_rooms.values('room_no')
        normal_room_nums = [int(obj.get("room_no", 0)) for obj in normal_room_objs]
        room_no = normal_room_nums[0] if normal_room_nums else 1

        n_obj = NormalRoom.objects.filter(room_no=room_no)
        n_obj.update(student=student, dept=dept, _id=_id, mobile_num=mobile_num,\
                purpose=purpose, availability=0)

        message = "Room No: {} is booked for you...!!!  -SRM AP".format(str(room_no))

        return  JsonResponse({"success": True})

    except:
        return  JsonResponse({"success": False})

def get_bookings(request):
    normal_rooms = NormalRoom.objects.filter(availability=0)
    normal_rooms_json = json.loads(serializers.serialize('json', normal_rooms))
    return_normal_room_objs = []

    for obj in normal_rooms_json:
        fields = obj["fields"]
        return_normal_room_objs.append(fields)

    return JsonResponse({"normal_rooms": return_normal_room_objs })
