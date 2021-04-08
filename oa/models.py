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


class Course(models.Model):
    # 课程信息表 字段:课程编号，课程名称，教师编号，课程其余信息
    uid = models.AutoField(null=False, primary_key=True)
    name = models.CharField(max_length=15)
    t_uid = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    info = models.TextField()  # json形式表示额外数据


# class CheckRecord(models.Model):
#     uid = models.AutoField(null=False, primary_key=True)
#     check_time = models.IntegerField(max_length=18)



