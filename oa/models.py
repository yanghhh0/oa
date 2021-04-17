# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone


# class ClassInfo(models.Model):
#     # 班级信息表  字段:班级名称
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name
#
#
# class MajorInfo(models.Model):
#     # 专业信息表 字段：专业名称
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name


class Teacher(models.Model):
    # 教师信息表 字段：教师编号，手机号，姓名，邮箱，密码
    uid = models.AutoField(null=False, primary_key=True)
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=15)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=64)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return self.uid


class Student(models.Model):
    # 学生信息表 字段：学号，密码，姓名，学院，专业，班级
    uid = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=16)
    institute = models.CharField(max_length=32)
    major = models.CharField(max_length=32)
    cls = models.CharField(max_length=32)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.uid


class Item(models.Model):
    # 课程信息表 字段:课程编号，课程名称，教师编号，课程其余信息
    uid = models.AutoField(null=False, primary_key=True)
    name = models.CharField(max_length=15)
    t_uid = models.IntegerField(null=False)
    info = models.JSONField()  # json形式表示额外数据

    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.uid


class CheckInfo(models.Model):
    # 某次签到的信息
    check_id = models.AutoField(null=False, primary_key=True)
    t_uid = models.IntegerField(null=False)
    check_time = models.IntegerField(null=False)
    checked_count = models.IntegerField(null=False)
    total_count = models.IntegerField(null=False)
    item_id = models.IntegerField(null=False)

    class Meta:
        db_table = 'check_info'


class CheckRecord(models.Model):
    # 签到记录
    check_id = models.IntegerField(null=False)  # 签到id
    uid = models.IntegerField(null=False)  # 签到人id
    check_time = models.IntegerField(null=False)  # 签到时间

    class Meta:
        db_table = 'check_record'


class StuItem(models.Model):
    # 名单详细
    item_id = models.IntegerField(null=False)
    stu_id = models.IntegerField(null=False)

    class Meta:
        db_table = 'stu_item'



