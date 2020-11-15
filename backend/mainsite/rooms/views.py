import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
from rooms.models import NormalRoom, DeluxeRoom
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

def check_availability(request, *args):
    normal_rooms = NormalRoom.objects.filter(availability=1)
    deluxe_rooms = DeluxeRoom.objects.filter(availability=1)
    normal_room_objs = normal_rooms.values('room_no')
    deluxe_room_objs = deluxe_rooms.values('room_no')
    normal_room_nums = [obj.get("room_no", 0) for obj in normal_room_objs]
    deluxe_room_nums = [obj.get("room_no", 0) for obj in deluxe_room_objs]
    return JsonResponse({"normal": {"avail_count": len(normal_room_nums), "room_nums":normal_room_nums },
                        "deluxe": {"avail_count": len(deluxe_room_nums), "room_nums": deluxe_room_nums }})

def student_booking(request):
    params_dict = request.GET
    params_dict = json.loads(list(params_dict.keys())[0])
    try:
        _type = params_dict.get("_type", "")
        student = params_dict.get("student", "")
        dept = params_dict.get("dept", "")
        _id = params_dict.get("_id", "")
        mobile_num = params_dict.get("mobile_num", "")
        guest_name = params_dict.get("guest_name", "")
        guest_num = params_dict.get("guest_num", "")
        check_in = params_dict.get("check_in", "")
        check_out = params_dict.get("check_out", "")
        relation = params_dict.get("relation", "")
        purpose = params_dict.get("purpose", "")
        food = params_dict.get("food", "")
        food = 1 if food.lower() == 'yes' else 0
        if _type == "normal":
            normal_rooms = NormalRoom.objects.filter(availability=1)
            normal_room_objs = normal_rooms.values('room_no')
            normal_room_nums = [int(obj.get("room_no", 0)) for obj in normal_room_objs]
            room_no = normal_room_nums[0]

            n_obj = NormalRoom.objects.filter(room_no=room_no)
            n_obj.update(student=student, dept=dept, _id=_id, mobile_num=mobile_num,\
                    guest_name=guest_name, guest_num=guest_num, check_in=check_in, check_out=check_out,\
                    relation=relation, purpose=purpose,food=food, availability=0)
        else:
            deluxe_rooms = DeluxeRoom.objects.filter(availability=1)
            deluxe_room_objs = deluxe_rooms.values('room_no')
            deluxe_room_nums = [int(obj.get("room_no", 0)) for obj in deluxe_room_objs]
            room_no = deluxe_room_nums[0]
            d_obj = DeluxeRoom.objects.filter(room_no=room_no)
            d_obj.update(room_no=room_no, student=student, dept=dept, _id=_id, mobile_num=mobile_num,\
                    guest_name=guest_name, guest_num=guest_num, check_in=check_in, check_out=check_out,\
                    relation=relation, purpose=purpose,food=food, availability=0)

        message = "Room No: {} is booked for you...!!!  -BITS Pilani".format(str(room_no))
        guest_num = str(guest_num)
        payload = PAYLOAD.format(msg=message, num=guest_num)
        response = requests.request("POST", URL, data=payload, headers=HEADERS)
        print(response.text)

        # Send messsage to Food Dept, if guest opted for food.
        if food:
            message = "Food Department..please note {_type} room {num} requires food".format(num=str(room_no), _type=_type)
            payload = PAYLOAD.format(msg=message, num='80')
            response = requests.request("POST", URL, data=payload, headers=HEADERS)
            print(response.text)

        message = "Maintenance Department..please note {_type} room {num} is booked".format(num=str(room_no),_type=_type)
        payload = PAYLOAD.format(msg=message, num='77')
        response = requests.request("POST", URL, data=payload, headers=HEADERS)
        print(response.text)

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

    deluxe_rooms = DeluxeRoom.objects.filter(availability=0)
    deluxe_rooms_json = json.loads(serializers.serialize('json', deluxe_rooms))
    return_deluxe_room_objs = []

    for obj in deluxe_rooms_json:
        fields = obj["fields"]
        return_deluxe_room_objs.append(fields)
        rmal_rooms_json = json.loads(serializers.serialize('json', normal_rooms))

    return JsonResponse({"normal_rooms": return_normal_room_objs, "deluxe_rooms": return_deluxe_room_objs})
