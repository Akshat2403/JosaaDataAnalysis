from django.shortcuts import render, HttpResponse
from .models import data
import json
from django.core.serializers import serialize
from django.db.models import Max
from .choices import IITS, BRANCHES, SEAT_TYPES, GENDERS
# Create your views here.

def base(request):
    context={
        'colleges':IITS,
        'branches':BRANCHES,
        'seat_types':SEAT_TYPES,
        'genders':GENDERS,
    }
    return render(request,'main/base.html',context)

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
        'colleges': IITS,
        'branches': BRANCHES,
        'seat_types': SEAT_TYPES,
        'genders': GENDERS,
    }
    if request.method == 'POST':
        seat_type = request.POST.get('seat_type')
        institute = request.POST.get('college_name')
        branch_name = request.POST.get('branch_name')
        gender = request.POST.get('gender')
        alldata = data.objects.filter(
            seat_type=seat_type, institute=institute, gender=gender, program=branch_name).all()

        jsdata = alldata.values('year', 'closing_rank', 'roundNo', 'program')
        jsdata = list(jsdata)
        jsdata = json.dumps(jsdata)
        context1 = {
            'colleges': IITS,
            'branches': BRANCHES,
            'seat_types': SEAT_TYPES,
            'genders': GENDERS,
            'alldata': alldata,
            'jsdata': jsdata}
        return render(request, 'main/index.html', context1)

    return render(request, 'main/index.html', context)


def trenddual(request):
    if request.method == 'POST':
        filters = {'roundNo': 6, 'program__contains': 5}
        filter_gender = request.POST.get('gender', None)
        filter_institute = request.POST.get('college_name', None)
        filter_seat = request.POST.get('seat_type', None)
        if filter_gender is not None:
            filters['gender'] = filter_gender
        if filter_institute is not None:
            filters['institute'] = filter_institute
        if filter_seat is not None:
            filters['seat_type'] = filter_seat
        dualdata = data.objects.filter(**filters)
    else:
        dualdata = data.objects.filter(program__contains='5', roundNo=6)

    year_set = set()
    branches = {'computer': "Computer Science", 'electrical': 'Electrical/Electronics Engineering',
                'electronics': 'Electrical/Electronics Engineering', 'math': 'Mathematics', 'physics': 'Physics', 'chemical': 'Chemical Engineering', 'mech': 'Mechanical Engineering'}
    options = ['computer', 'electrical', 'electronics',
               'math', 'physics', 'chemical', 'mech']
    dataset = {}
    for val in dualdata:
        dict = {}
        flag = ''
        for branch in options:
            if branch in val.program.lower():
                flag = branches[branch]
                break
        if flag:
            year_set.add(val.year)
            if flag in dataset:
                if val.year in dataset[flag]:
                    dataset[flag][val.year].append(
                        int(val.opening_rank+val.closing_rank)/2)
                else:
                    dataset[flag][val.year] = []
                    dataset[flag][val.year].append(
                        int(val.opening_rank+val.closing_rank)/2)
            else:
                dataset[flag] = {}
                dataset[flag][val.year] = []
                dataset[flag][val.year].append(
                    int(val.opening_rank+val.closing_rank)/2)

    # print(dataset)
    colors = [
        "#ae1029",
        "#0065c2",
        "#26c238",
        "#9876aa",
        "#fb8649",
        "#57904b",
        "#d35b5c",
    ]
    i = 0
    final = []
    branches = []
    for k, v in dataset.items():
        branches.append(k)

        dict = {}
        dict['name'] = k
        dict['type'] = 'line'
        dict['smooth'] = True
        dict['color']: colors[i]
        dict['data'] = []
        print(v, '\n')
        for year in year_set:
            print(year)
            if year in v:
                dict['data'].append(int((sum(v[year]))/len(v[year])))
            else:
                dict['data'].append(None)
        final.append(dict)
        i += 1

    context = {
        'data': json.dumps(final), 'year': json.dumps(list(year_set)), 'branches': branches, 'seat_type': SEAT_TYPES, 'colleges': IITS, 'gender': GENDERS
    }
    # if request.method == 'POST':
    return render(request, 'main/dualtrends.html', context)


def trendspecial(request):
    if request.method == 'POST':
        filters = {'roundNo': 6}
        filter_gender = request.POST.get('gender', None)
        filter_institute = request.POST.get('college_name', None)
        filter_seat = request.POST.get('seat_type', None)
        if filter_gender is not None:
            filters['gender'] = filter_gender
        if filter_institute is not None:
            filters['institute'] = filter_institute
        if filter_seat is not None:
            filters['seat_type'] = filter_seat
        dualdata = data.objects.filter(**filters)
    else:
        dualdata = data.objects.filter(roundNo=6)
    year_set = set()

    branches = {'computer': "Computer Science",
                'aero': 'Aerospace', 'bio': 'Bio Technology', 'arti': 'Data Science Artificial Intelligence', 'data': 'Data Science Artificial Intelligence', 'textile': 'Textile', 'agri': 'Agricultural', 'instru': 'Instrumental', 'ocean': 'Ocean and Naval'}
    options = ['computer', 'aero', 'bio', 'arti', 'textile', 'agri', 'instru', 'ocean', 'data'
               ]
    dataset = {}
    for val in dualdata:
        dict = {}
        flag = ''
        for branch in options:
            if branch in val.program.lower():
                flag = branches[branch]
                break
        if flag:
            year_set.add(val.year)
            if flag in dataset:
                if val.year in dataset[flag]:
                    dataset[flag][val.year].append(
                        int(val.opening_rank+val.closing_rank)/2)
                else:
                    dataset[flag][val.year] = []
                    dataset[flag][val.year].append(
                        int(val.opening_rank+val.closing_rank)/2)
            else:
                dataset[flag] = {}
                dataset[flag][val.year] = []
                dataset[flag][val.year].append(
                    int(val.opening_rank+val.closing_rank)/2)

    print(dataset)
    colors = [
        "#ae1029",
        "#0065c2",
        "#26c238",
        "#9876aa",
        "#fb8649",
        "#57904b",
        "#d35b5c",
    ]
    i = 0
    final = []
    branches = []
    for k, v in dataset.items():
        dict = {}
        dict['name'] = k
        dict['type'] = 'line'
        dict['smooth'] = True
        dict['color']: colors[i]
        dict['data'] = []
        for year in year_set:
            if year in v:
                dict['data'].append(int((sum(v[year]))/len(v[year])))
            else:
                dict['data'].append(None)
        final.append(dict)
        i += 1
    context = {
        'data': json.dumps(final), 'year': json.dumps(list(year_set)), 'seat_type': SEAT_TYPES, 'colleges': IITS, 'gender': GENDERS

    }
    # if request.method == 'POST':
    return render(request, 'main/trendspecial.html', context)


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

def dev_q3(request):
    filtered_data = data.objects.filter(roundNo='6')

    seat_types = ['OPEN','EWS','SC','ST','OBC-NCL']
    result = []

    for seat_type in seat_types:
        for year in range(2000, 2024):  # Assuming the range of years you want to consider
            max_closing_rank = filtered_data.filter(seat_type=seat_type, year=year).aggregate(Max('closing_rank'))
            if max_closing_rank['closing_rank__max']:
                obj = filtered_data.filter(seat_type=seat_type, year=year, closing_rank=max_closing_rank['closing_rank__max']).first()
                result.append({
                    'seat_type': obj.seat_type,
                    'year': obj.year,
                    'closing_rank': obj.closing_rank,
                    'institute':obj.institute,
                    # Add more fields if necessary
                })

    jsdata = json.dumps(result)
    context = {
        'alldata':result,
        'jsdata':jsdata,
    }
    return render(request, 'main/dev_q3.html',context)

def dig_q2(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        print(year)
        filtered_data = data.objects.filter(year=(year),roundNo='6',seat_type='OPEN',gender='Gender-Neutral',closing_rank__lt = '1000',program__contains='4').filter(program__contains='Technology').exclude(program__contains='Mechanical').exclude(program__contains='Power').exclude(program__contains='Physics')
        jsdata = filtered_data.values('institute','year','program','opening_rank','closing_rank')
        jsdata = json.dumps(list(jsdata))
        context = {
            'alldata':filtered_data,
            'jsdata':jsdata,
            'years':YEARS,
        }
        return render(request, 'main/digvijay_q2.html',context)

    year = 2016
    filtered_data = data.objects.filter(year=year,roundNo='6',seat_type='OPEN',gender='Gender-Neutral',closing_rank__lt = '1000',program__contains='4').filter(program__contains='Technology').exclude(program__contains='Mechanical').exclude(program__contains='Power').exclude(program__contains='Physics')

    jsdata = filtered_data.values('institute','year','program','opening_rank','closing_rank')
    jsdata = json.dumps(list(jsdata))
    context = {
        'alldata':filtered_data,
        'jsdata':jsdata,
        'years':YEARS,
    }

    return render(request, 'main/digvijay_q2.html',context)
