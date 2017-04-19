本文档用来探讨以下几个问题：
1. 外键规则
2. Django中定义带有外键的model
3. 带有外键的model怎么导入数据？
4. 利用外键做关联查询及优化

#### 1. 外键规则  
数据库的外键可以为空，也可以非空，**但是如果非空，则这个值必须在主表中存在**。  
**举一个例子：**  
主表是班级，主键是班级id;子表是学生分配班级表，主键是学生id，外键是所在班级id。  
如果一个学生的外键id为空，说明这个学生还没有被分配到任何一个班级  
如果一个学生的外键id非空，并且是班级表中的某个id，则说明学生分配到这个班级  
如果一个学生的外键id非空，并且不属于任何班级，则数据插入肯定报错。也就是说这种情况不存在。  
#### 2. Django中定义带有外键的model
大学和专业是两个主表，大学名称和专业名称是唯一的；大学专业的分数线是子表。子表中大学名称和专业名称有些没在主表中。具体表格如下：  
college.txt(主表)  
```
college_name,location,rank
清华大学,北京,1
中山大学,广州,10
XXX大学,新疆,100
```
major.txt(主表)  
```
major_name,major_code
英语,1234
经济学,2222
计算机,1357
```
college_major_score.txt(子表)  
```
college,major,score
清华大学,英语,650
清华大学,计算机,670
清华大学,经济学,660
清华大学,法学,650
中山大学,计算机,620
中山大学,临川医学,640
BBB大学,计算机,540
BBB大学,法学,520
```
其中清华大学的法学专业没有在专业表中，BBB大学没在学校表中。  
在mysql数据库中，college, major表有主键id，college_major_score中引用主表的
主键作为外键，如果大学或专业没在主表中，外键就为空。  
在django的model定义中，和mysql略有不同：  
```
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class College(models.Model):
    college_name=models.CharField(max_length=30)
    location=models.CharField(max_length=30)
    rank=models.IntegerField()

    def __unicode__(self):
        return self.college_name

class Major(models.Model):
    major_name=models.CharField(max_length=30)
    major_code = models.CharField(max_length=30)

    def __unicode__(self):
        return self.major_name

class College_major_score(models.Model):
    college=models.ForeignKey(College,null=True)
    college_name=models.CharField(max_length=30)
    major = models.ForeignKey(Major,null=True)
    major_name = models.CharField(max_length=30)
    score=models.FloatField()

    def __unicode__(self):
        return "%s %s %s" % (self.college_name,self.major_name,self.score)
```
需要注意下面几点：    
1. 不需要显示定义主键  
2. 通过ForeignKey引用整个主表，null = True   

#### 3. 带外键的model导入数据  

```
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
```

注意以下几点：
1. 先导入主表
2. 往子表中导入一条数据时，通过专业名称从专业表中查找对应的对象（查不到则为None）
将该专业对象赋给子表的外键。  

#### 4. 利用外键做关联查询及优化

查询出college_major_score的一条数据后，比如cms, 可以直接通过cms访问
大学或专业的其他信息，例如:  
```
cms=College_major_score.objects.get(college_name=u'清华大学',major_name=u'英语')
ms.college
cms.college.rank
cms.major.code
```
如果cms.major为None，表明cms.major没在专业表中，外键为空。

**查询优化：**  
通过上面的代码查询，在后台实际分为两步：  
1. 执行sql语句查找到清华大学英语专业对应的college_major_score对象  
2. 再执行sql语句查询专业代码  

可以通过下面方法优化：
```
cms=College_major_score.objects.\
filter(college_name=u'清华大学',major_name=u'英语').\
select_related('major')#外键名称
cms.major.code#不会再次执行sql查询
```