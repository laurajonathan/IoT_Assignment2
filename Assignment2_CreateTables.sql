create table User (
    UserID int not null auto_increment,
    Username nvarchar(256) not null,
    constraint PK_User primary key (UserID),
    constraint UN_Username unique (Username)
);

create table Book (
    BookID int not null auto_increment,
    Title text not null,
    Author text not null,
    ISBN text not null,
    Quantity int not null,
    constraint PK_Book primary key (BookID)
);

create table Record (
    RecordID int not null auto_increment,
    UserID int not null,
    BookID int not null,
    Status text not null,
    Quantity int not null,
    BorrowedDate datetime not null,
    ReturnedDate datetime null,
    constraint PK_Record primary key (RecordID),
    constraint FK_Record_User foreign key (UserID) references User (UserID),
    constraint FK_Record_Book foreign key (BookID) references Book (BookID)
);
