from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
import csv, io, os
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
import mimetypes
from django.utils.encoding import smart_text
from .filters import *
from django.utils import timezone
from django.contrib.sessions.models import Session
from .render import Render

def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request,'403.html')
        return function(request, *args, **kwargs)
    return _inner

def staff_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request,'403.html')
        return function(request, *args, **kwargs)
    return _inner

def student_only(function):
    def _inner(request, *args, **kwargs):
        if request.user.is_staff:
            return render(request,'403.html')
        return function(request, *args, **kwargs)
    return _inner

@login_required
def home(request):
    title = "Training And Placement"
    if request.user.is_superuser:
        return redirect('admin/')
    return render(request, 'index.html')

@login_required
@staff_only
def viewcompany(request):
    title = "Training And Placement"
    vc = Company.objects.all()
    context = {'vc': vc}
    return render(request, 'viewcompany.html', context)

@login_required
@staff_only
def student_profile(request, pk):
    vs = get_object_or_404(Student, pk=pk)
    return render(request, 'student_profile.html', {'object': vs})

@login_required
def company_profile(request, pk):
    vc = get_object_or_404(Company, pk=pk)
    return render(request, 'company_profile.html', {'object': vc})

@login_required
def my_profile(request):
    Student_obj = Student.objects.all()
    for i in range(len(Student_obj)):
        if request.user.id == Student_obj[i].user_id:
            key=Student_obj[i].s_id
            vs = get_object_or_404(Student, pk=key)
            return render(request, 'student_profile.html', {'object': vs})
    return render(request, 'profile_not_found.html')

@login_required
def my_company(request):
    Student_obj = Student.objects.all()
    for i in range(len(Student_obj)):
        if request.user.id == Student_obj[i].user_id:
            key=Student_obj[i].placed_company_id
            if key is not 0 and key is not None and key is not '' and key is not '0':
                vc = get_object_or_404(Company, pk=key)
                return render(request, 'my_company.html', {'object': vc})
    return render(request, 'no_company.html')

@login_required
@staff_only
def viewstudent(request):
    title = "Training And Placement"
    vs = Student.objects.all()
    context = {'vs': vs}
    return render(request, 'viewstudent.html', context)

@login_required
@staff_only
def student_create(request):
    form = StudentForm(request.POST or None)
    user=User.objects.all()
    if form.is_valid():
        fs=form.save(commit=False)
        fs.user_id= int([user[i].id for i in range(len(user)) if user[i].email == fs.email][0])
        fs.save()
        return redirect('viewstudent')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form':form})

@login_required
@staff_only
def student_update(request, pk):
    vs = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=vs)
    user=User.objects.all()
    if form.is_valid():
        fs=form.save(commit=False)
        fs.user_id= int([user[i].id for i in range(len(user)) if user[i].email == fs.email][0])
        fs.save()
        return redirect('viewstudent')
    return render(request, 'student_edit.html', {'form': form})

@login_required
@staff_only
def student_delete(request, pk):
    vs = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        vs.delete()
        return redirect('viewstudent')
    return render(request, 'student_confirm_delete.html', {'object': vs})

@login_required
@staff_only
def company_create(request):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('viewcompany')
    else:
        form = CompanyForm()
    return render(request, 'company_form.html', {'form': form})


@login_required
@staff_only
def company_update(request, pk):
    vc = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, instance=vc)
    if form.is_valid():
        form.save()
        return redirect('viewcompany')
    return render(request, 'company_edit.html', {'form': form})

@login_required
@staff_only
def company_delete(request, pk):
    vc = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        vc.delete()
        return redirect('viewcompany')
    return render(request, 'company_confirm_delete.html', {'object': vc})

@login_required
@staff_only
def place_student(request):
    Suggested.objects.all().delete()
    company_ob = Company.objects.all()
    student_ob = Student.objects.all()

    for i in range(len(Student.objects.all())):
        for j in range(len(Company.objects.all())):
            if student_ob[i].CGPA >= company_ob[j].criteria and student_ob[i].placed == 0 :
                suggested = Suggested(std_id=student_ob[i].s_id,cmp_id=company_ob[j].c_id)
                suggested.save()
    return redirect('home')

@login_required
def suggested_company(request):
    student_ob = Student.objects.all()
    suggested_ob = Suggested.objects.all()
    lst=[]
    context={}
    for i in range(len(student_ob)):
        if request.user.id == student_ob[i].user_id:
            if student_ob[i].placed == 0:
                for j in range(len(suggested_ob)):
                    if student_ob[i].s_id == suggested_ob[j].std_id:
                        for company in Company.objects.all().filter(c_id=suggested_ob[j].cmp_id).exclude(required_recruitment=0):
                            lst.append(company)
                        context = Company.objects.filter(c_id__in=[x.c_id for x in lst])
                return render(request,'suggested_company.html',{'companies':context})
    return render(request,'suggested_company.html',{'companies':''})

@login_required
def company_select(request, pk):
    vc = get_object_or_404(Company, pk=pk)
    student_ob = Student.objects.all()
    suggested_ob = Suggested.objects.all()
    if request.method == 'POST':
        for i in range(len(student_ob)):
            if request.user.id == student_ob[i].user_id:
                student_ob[i].placed_company_id=vc.c_id
                student_ob[i].placed=1
                vc.hired_count=vc.hired_count+1
                vc.required_recruitment=vc.required_recruitment-1
                vc.save()
                student_ob[i].save()

                for j in range(len(suggested_ob)):
                    if student_ob[i].s_id == suggested_ob[j].std_id:
                        suggested_ob[j].delete()
        
        return redirect('home')
    return render(request, 'company_confirm_select.html', {'object': vc})

@login_required
@staff_only
def placement(request):
    return render(request,'placement.html')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
@staff_only
def import_credential(request):
    try:
        template = "import_credential.html"
        data = User.objects.all()

        if request.method == "GET":
            return render(request, template)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            return render(request, template)
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            created = User.objects.update_or_create(
            password=make_password(column[0]) if len(column[0]) < 40 else column[0],
            last_login=column[1],
            is_superuser=column[2],
            username=column[3],
            first_name=column[4],
            email=column[5],
            is_staff=column[6],
            is_active=column[7],
            date_joined=column[8],
            last_name=column[9],
        )
        context = {}
        messages.info(request, 'Successfully Imported !')
        return render(request, template, context)

    except:
        return render(request,'csv_error.html')

@login_required
def export_credential(request):
    users = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export_csv.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ['password', 'last_login', 'is_superuser', 'username', 'first_name', 'email', 'is_staff', 'is_active',
         'date_joined', 'last_name'])

    for user in users:
        writer.writerow([user.password, user.last_login, user.is_superuser, user.username, user.first_name, user.email,
                         user.is_staff, user.is_active, user.date_joined, user.last_name])
    return response


@login_required
@student_only
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES,)
        if form.is_valid():
            fs=form.save(commit=False)
            fs.user_id= request.user.id
            fs.save()
            messages.info(request, 'Successfully Uploaded !')
            return redirect('upload_document')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})


@login_required
@staff_only
def folders_list(request):
    return render(request,'folders_list.html',{'total_folder':os.listdir(settings.MEDIA_ROOT),'path':settings.MEDIA_ROOT})


@login_required
@staff_only
def files_list(request,folder_name):
    return render(request,'files_list.html',{'total_files':os.listdir("media/"+folder_name),'path':folder_name})


@login_required
@staff_only
def download_files(request,folder_name,file_name):
    file_path = settings.MEDIA_ROOT+'/'+ folder_name +'/'+ file_name
    print(file_path)
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_text(file_name) 
    return response


@login_required
@staff_only
def search_student(request):
    student_list = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'student_search_list.html', {'filter': student_filter})

@login_required
@staff_only
def search_company(request):
    company_list = Company.objects.all()
    company_filter = CompanyFilter(request.GET, queryset=company_list)
    return render(request, 'company_search_list.html', {'filter': company_filter})

@login_required
@staff_only
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        fs=form.save(commit=False)
        fs.author_id= request.user.id
        fs.save()
        messages.info(request, 'Successfully Uploaded !')
        return redirect('post')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form':form})


class announcement_list(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'announcement_list.html'

class announcement_detail(generic.DetailView):
    model = Post
    template_name = 'announcement_detail.html'


@login_required
@staff_only
def get_current_users(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    users=User.objects.filter(id__in=user_id_list)
    return render(request, 'current_users.html', {'users':users})


@login_required
@staff_only
def other_utilities(request):
    return render(request, 'other_utilities.html')

@login_required
@staff_only
def import_student_data(request):
    try:
        user=User.objects.all()
        if request.method == "GET":
            return render(request, "import_student_data.html")

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')  
            return render(request, "import_student_data.html")  
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            created = Student.objects.update_or_create(
                enrollment_number=column[0],
                first_name=column[1],
                last_name=column[2],
                email=column[3],
                phone=column[4],
                gender=column[5],
                branch=column[6],
                birth_date=column[7],
                permanent_address=column[8],
                current_address=column[9],
                aadhaar_number=column[10],
                HSC_board=column[11],
                HSC_year=column[12],
                HSC_marks=column[13],
                HSC_school_name=column[14],
                SSC_board=column[15],
                SSC_year=column[16],
                SSC_marks=column[17],
                SSC_school_name=column[18],
                active_back=column[19],
                passive_back=column[20],
                course=column[21],
                college_name=column[22],
                university=column[23],
                passing_year=column[24],
                CGPA=column[25],
                lock=column[26],
                user_id=int([user[i].id for i in range(len(user)) if user[i].email == column[3]][0]),
                placed_company_id=column[28],
                placed=column[29],
                )
        context = {}
        messages.info(request, 'Successfully Imported !')
        return render(request,"import_student_data.html",context)
    except:
        return render(request,'csv_error.html')


@login_required
@staff_only
def export_student_csv(request):

    users = Student.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['enrollment_number','first_name','last_name','email','phone','gender','branch','birth_date','permanent_address','current_address','aadhaar_number','HSC_board','HSC_year','HSC_marks','HSC_school_name','SSC_board','SSC_year','SSC_marks','SSC_school_name','active_back','passive_back','course','college_name','university','passing_year','CGPA','lock','user_id','placed_company_id','placed'])

    for user in users:
        writer.writerow([user.enrollment_number,user.first_name,user.last_name,user.email,user.phone,user.gender,user.branch,user.birth_date,user.permanent_address,user.current_address,user.aadhaar_number,user.HSC_board,user.HSC_year,user.HSC_marks,user.HSC_school_name,user.SSC_board,user.SSC_year,user.SSC_marks,user.SSC_school_name,user.active_back,user.passive_back,user.course,user.college_name,user.university,user.passing_year,user.CGPA,user.lock,user.user_id,user.placed_company_id,user.placed])

    return response

@login_required
@staff_only
def generate_placement_report(request):
    today=timezone.now()
    s=Student.objects.all()
    c=Company.objects.all()
    lst=[]
    lst1=[]
    for i in range(len(s)):
        for j in range(len(c)):
            if str(s[i].placed_company_id) == str(c[j].c_id):
                lst.append(s[i])
                lst1.append(c[j])
    obj_list=list(zip(lst,lst1))
    return Render.render(request,'generate_placement_report.html',{'obj_list':obj_list,'today':today})

#for testing purpose
def reset_app(request):
    Company.objects.all().delete()
    Suggested.objects.all().delete()
    Document.objects.all().delete()
    Post.objects.all().delete()
    Student.objects.all().delete()
    return redirect('home')

#for testing purpose
def reset_profiles(request):
    company_ob=Company.objects.all()
    student_ob = Student.objects.all()
    Suggested.objects.all().delete()
    for i in range(len(student_ob)):
        student_ob[i].placed=0
        student_ob[i].placed_company_id=''
        student_ob[i].save()
    for i in range(len(company_ob)):
        company_ob[i].required_recruitment=company_ob[i].required_recruitment+company_ob[i].hired_count
        company_ob[i].hired_count=0
        company_ob[i].save()
    return redirect('home')


@login_required
@staff_only
def export_company_csv(request):
    companies = Company.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="company_data.csv"'
    writer = csv.writer(response)
    
    writer.writerow(['name', 'criteria', 'contact_number', 'email','address','required_recruitment','other_details','position','package','website','hired_count'])
    for company in companies:
        writer.writerow([company.name,company.criteria,company.contact_number,company.email,company.address,company.required_recruitment,company.other_details,company.position,company.package,company.website,company.hired_count])
    
    return response


@login_required
@staff_only
def import_company_data(request):
    try:
        if request.method == "GET":
            return render(request, 'import_company_data.html')
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            return render(request, "import_company_data.html")   
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            created = Company.objects.update_or_create(
          name=column[0],
          criteria=column[1],
          contact_number=column[2],
          email=column[3],
          address=column[4],
          required_recruitment=column[5],
          other_details=column[6],
          position=column[7],
          package=column[8],
          website=column[9],
          hired_count=column[10],
            )
        context = {}
        messages.info(request, 'Successfully Imported !')
        return render(request, 'import_company_data.html', context)
    except:
        return render(request,'csv_error.html')


@login_required
@staff_only
def placed_students(request):
    s=Student.objects.all()
    c=Company.objects.all()
    lst=[]
    lst1=[]
    for i in range(len(s)):
        for j in range(len(c)):
            if str(s[i].placed_company_id) == str(c[j].c_id):
                lst.append(s[i])
                lst1.append(c[j])
    obj_list=list(zip(lst,lst1))
    return render(request,'placed_students.html',{'obj_list':obj_list})
