from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt
import json

from main.models import Services, PhoneManager

def index(request):
    services = check_services()
    print(services)

    phone_condtion = check_phone()

    return render(request, 'index.html', {"services" : services, "phone" : phone_condtion})


# sending post request to service - this is actual url on website

def get_employees(request):

    selected_service = Services.objects.filter(is_service_selected=True)

    service = list(selected_service.values())[0]

    response = get_employees_request(service['service_url'], service['service_login'], service['service_password'])
    people_list = response.json()['Parameters']

    result = filterNames(people_list)

    return JsonResponse(result)

# actual post request execution with url, login and pass params - this is not url on website, just a function
def get_employees_request(url, login, password):

    response = requests.post(url, verify=False, auth=HTTPBasicAuth(login, password), json=
    {
    "Request_id": "e1477272-88d1-4acc-8e03-7008cdedc81e", 
    "ClubId": "59115d1e-9052-11eb-810c-6eae8b56243b", 
    "Method": "GetSpecialistList", 
    "Parameters": {}
    })

    # print(response) 
    return response



def filterNames(data):

    unfiltred_names = []

    result = {'Parameters' : []}

    for element in data:
        unfiltred_names.append(element['Name'])

    filtred_names = sorted(unfiltred_names)

    phone_condition = check_phone()


    for new_name in filtred_names:
        x = 0
        for old_name in unfiltred_names:
            if new_name == old_name:
                if (phone_condition == True):
                    result["Parameters"].append({'id' : data[x]['ID'], 'name' : data[x]['Name'], 'last_name' : data[x]['Surname'], 'phone' : data[x]['Phone'], 'image_url' : data[x]['Photo']})
                else:
                    result["Parameters"].append({'id' : data[x]['ID'], 'name' : data[x]['Name'], 'last_name' : data[x]['Surname'], 'image_url' : data[x]['Photo']})

            x = x + 1
        filtred_names = [x for x in filtred_names if x != new_name]

    return result


@csrf_exempt
def add_new_service(request):

    if request.method == 'POST': 

        # Reading incoming json
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)

        # print(body) 	

        # Parsing json
        service_url = body['url']
        service_login = body['login']
        service_password = body['password']

        # Adding new entry for database from json
        service_entry = Services(service_url=service_url, service_login=service_login, service_password=service_password)
        service_entry.save()

        print("Added new service.") 

        return HttpResponse("Success")
    return HttpResponse("Required POST method.")






@csrf_exempt
def remove_service(request):
    if request.method == 'POST': 

        # Reading incoming json
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)

        service = Services.objects.get(service_url=body['url'])
        service.delete()


        print("Service removed") 

        return HttpResponse("Success")
    return HttpResponse("Required POST method.")


@csrf_exempt
def change_selected_service(request):
    if request.method == 'POST': 

        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)

        service_db = check_services()

        for element in service_db:
            service = Services.objects.get(service_url=element['url'])
            service.is_service_selected = False
            service.save()

        service = Services.objects.get(service_url=body['url'])
        service.is_service_selected = True
        service.save()




        print("Selected service changed.") 

        return HttpResponse("Success")
    return HttpResponse("Required POST method.")




@csrf_exempt
def changePhone(request):
    if request.method == 'POST': 

        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        phone = PhoneManager.objects.get(id=1)
        
        phone.phone_enable = body['phone_changeTo']
        phone.save()
        
        print("Changed phone condition.") 

        return HttpResponse("Success")
    return HttpResponse("Required POST method.")



def check_services():
    # Check database for outside services and return all entries in dict-format with url, login and password
    services_db = Services.objects.all()
    services = []
    for element in services_db:
        entry = {"url": element.service_url, "login": element.service_login, "pass" : element.service_password, "selected" : element.is_service_selected}
        services.append(entry)
    return services


def check_phone():
    phone_condition = PhoneManager.objects.get(id=1)
    return phone_condition.phone_enable
