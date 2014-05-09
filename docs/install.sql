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

