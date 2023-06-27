from django.shortcuts import render, HttpResponse
from .models import data
import json
from django.core.serializers import serialize
from .choices import IITS,BRANCHES,SEAT_TYPES,GENDERS
# Create your views here.


def upload_csv(request):
    if request.method == 'POST':
        print(request.FILES)
        csv_file = request.FILES['document']
        file_data = csv_file.read().decode('utf-8')
        csv_data = file_data.split('\n')
        for x in csv_data:
            fields = x.split(',')
            print(fields)
            info = data(institute=fields[1], program=fields[2], seat_type=fields[3], gender=fields[4], opening_rank=fields[5],
                        closing_rank=fields[6], year=fields[7], roundNo=fields[8], institute_type=fields[10])
            info.save()
    return render(request, 'main/upload.html')

def printdata(request):
    # alldata = data.objects.filter(institute='Indian Institute of Technology Guwahati').all()

    # jsdata = alldata.values('year','closing_rank','roundNo','program')
    # jsdata = list(jsdata)
    # jsdata = json.dumps(jsdata)
    context = {
        'colleges':IITS,
        'branches':BRANCHES,
        'seat_types':SEAT_TYPES,
        'genders':GENDERS,
    }
    if request.method == 'POST':
        seat_type = request.POST.get('seat_type')
        institute = request.POST.get('college_name')
        branch_name = request.POST.get('branch_name')
        gender = request.POST.get('gender')
        alldata = data.objects.filter(seat_type=seat_type,institute=institute,gender=gender,program=branch_name).all()

        jsdata = alldata.values('year','closing_rank','roundNo','program')
        jsdata = list(jsdata)
        jsdata = json.dumps(jsdata)
        context1 = {
            'colleges':IITS,
            'branches':BRANCHES,
            'seat_types':SEAT_TYPES,
            'genders':GENDERS,
            'alldata':alldata,
            'jsdata':jsdata}
        return render(request, 'main/index.html',context1)
        


    return render(request, 'main/index.html',context)



def dig_q1(request):
    popular_branches = [
        'Computer Science and Engineering (4 Years Bachelor of Technology)',
        'Electrical Engineering (4 Years Bachelor of Technology)',
        'Mechanical Engineering (4 Years Bachelor of Technology)',
        'Mathematics and Computing (4 Years Bachelor of Technology)',
        ]
    filtered_data = data.objects.filter(roundNo='6',seat_type='OPEN',gender='Gender-Neutral',program__in=popular_branches)

    jsdata = filtered_data.values('institute','year','program','opening_rank','closing_rank')
    jsdata = json.dumps(list(jsdata))
    context = {
        'alldata':filtered_data,
        'jsdata':jsdata,
    }

    return render(request, 'main/digvijay_q1.html',context)