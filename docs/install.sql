CREATE DATABASE `myclip` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE `clips` (
  `id` int(11) NOT NULL auto_increment,
  `pid` int(11) NOT NULL default '0',
  `title` varchar(20) default NULL,
  `content` text,
  `created_time` datetime default NULL,
  `changed_time` datetime default NULL,
  PRIMARY KEY  (`id`)
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
