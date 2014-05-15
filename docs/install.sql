CREATE DATABASE `myclip` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE clips (
    id int auto_increment not null primary key,
    pid int not null,
    cateid int not null,
    title varchar(32) not null,
    `content` text not null,
    created_time datetime not null,
    changed_time datetime not null,
    key(pid),
    key(title)
);

create table clip_cate(
    id int auto_increment not null primary key,
    pid int not null,
    name varchar(32) not null,
    created_time datetime not null
);

create table users (
    id int auto_increment not null primary key,
    username varchar(32) not null,
    nickname varchar(32) not null,
    password varchar(32) not null,
    salt int not null,
    usertype tinyint not null,
    openid varchar(64) not null,
    register_time datetime not null,
    register_ip varchar(16) not null,
    lastlogin_time datetime not null,
    lastlogin_ip varchar(16) not null,
    unique key(username),
    key(openid),
    key(register_time),
    key(lastlogin_time)
);

create table messages(
    id int auto_increment not null primary key,
    from_userid int not null,
    to_userid int not null,
    created_time datetime not null,
    `content` varchar(2048) not null,
    msgtype tinyint not null,
    unread tinyint(1) not null default 1,
    key(from_userid),
    key(to_userid)
);

create table twitters(
    id int auto_increment not null primary key,
    pid int not null,
    userid int not null,
    created_time datetime not null,
    `content` varchar(512) not null,
    deleted tinyint(1) not null,
    key(userid)
);
