create table if not exists ClassInfo(
    name varchar(20) not null
)DEFAULT CHARSET=utf8;

create table if not exists MajorInfo(
    name varchar(20) not null
)

create table if not exists Teacher(
    uid int not null,
    phone varchar(11) not null,
    name varchar(20) not null,
    email varchar(50) not null,
    password varchar(32) not null,
    primary key(uid)
)DEFAULT CHARSET=utf8;

create table if not exists Course(
    uid int not null,
    name varchar(20) not null,
    t_uid int not null,
    info text,
    primary key(uid)
)DEFAULT CHARSET=utf8;



create table if not exists UserInfo(
    studentNum varchar(15) not null ,
    password varchar(64) not null ,
    name varchar(15) not null ,
    c_uid int not null ,
    major varchar(20) not null ,
    email varchar(50) not null ,
    phone varchar(20) not null
)DEFAULT CHARSET=utf8;




