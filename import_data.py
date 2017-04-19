# -*- coding: utf-8 -*-
import os
import django
import codecs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foreignkey_test.settings")

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from app.models import College, Major, College_major_score

def import_college():
    with codecs.open('data/college.txt', 'r', encoding='utf8') as f:
        for line in f.readlines()[1:]:
            college_name,location,rank=line.strip().split(',')
            College.objects.create(college_name=college_name,location=location,rank=rank)
    print("complete college data importing!")



def import_major():
    with codecs.open('data/major.txt', 'r', encoding='utf8') as f:
        for line in f.readlines()[1:]:
            major_name,major_code=line.strip().split(',')
            Major.objects.create(major_name=major_name,major_code=major_code)
    print("complete major data importing!")

def import_college_major():
    with codecs.open('data/college_major_score.txt', 'r', encoding='utf8') as f:
        for line in f.readlines()[1:]:
            college_name,major_name,score = line.strip().split(',')
            try:
                college=College.objects.get(college_name=college_name)#或者在College中或者为null
            except:
                college=None
            try:
                major=Major.objects.get(major_name=major_name)#或者在Major中或者为null
            except:
                major=None
            College_major_score.objects.create(college_name=college_name,major_name=major_name,college=college,major=major,score=int(score))
    print("complete score importing")

if __name__=="__main__":
    import_college()
    import_major()
    import_college_major()