"""csci250 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from main import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),

    url(r'^$', views.index, name='index'),
    url(r'^my_questions/', views.my_questions),
    url(r'^grade_assignments/', views.grade_assignments),
    #start with most specific url
    url(r'^grade_assignment/(\d+)/(\d+)/(\d+)', views.grade_assignment_open), #will open student id page
    url(r'^grade_assignment/(\d+)/(\d+)', views.grade_assignments_students), #will open section's students page
    url(r'^grade_assignment/(\d+)', views.grade_assignments_sections),
    #url(r'^grade_assignment/(\d+)', views.grade_assignments_sections),#will open section page. define new function for
    #displaying sections (simply display list of sections)
    url(r'^update_password/', views.update_password, name='update_pass'),
    url(r'^assignments/(\d+)', views.assigment_id_method, name='assignments_id'),
    url(r'^assignments/', views.assignments, name='assignments'),
    url(r'^structure/', views.structure, name='structure'),
    #url(r'^admin/', admin.site.urls),
    url(r'^(\d+)/(\w+)', views.index, name='index_semester'),
    url(r'^schedule/', views.csci250_schedule),
    url(r'^create_lesson/', views.create_lesson),
    url(r'^create_ass/', views.create_ass),
    url(r'^admin/(\d+)/', views.csci250_edit_quiz),
    #url(r'^assignment/(\d+)', views.cisci250_assignment), # csci250.amhajja.com/assignment/3
    url(r'^login/', views.csci250_login),
    url(r'^sign_up/', views.csci250_sign_up),
    url(r'^questions/', views.csci250_view_questions),
]
