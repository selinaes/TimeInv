/*
Add a table for login 
*/

use timeinv_db;

drop table if exists userpass;

create table userpass(
    uid int auto_increment,
    username varchar(10) not null,
    hashed char(60),
    unique(username),
    index(username),
    primary key (uid)
);
