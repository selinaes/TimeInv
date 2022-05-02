/*
Edit userpass table to reference staff
table
*/

alter table userpass
add contraint username
foreign key (username)
references staff(username);