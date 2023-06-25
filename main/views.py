from django.shortcuts import render, HttpResponse
from .models import data
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
