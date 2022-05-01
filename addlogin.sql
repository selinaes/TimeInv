/*
Add a table for login 
*/

use timeinv_db;

drop table if exists userpass;

create table userpass(
    username varchar(10) not null,
    hashed char(60) not null,
    unique(username),
    index(username),
    primary key (username)
);
