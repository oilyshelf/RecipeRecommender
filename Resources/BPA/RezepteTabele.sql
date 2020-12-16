
/* Create Database and Drop if it already there*/
Drop database if exists BPA;
create Database BPA;
/*select Database*/
use BPA;
/* Create Tables*/
CREATE TABLE Rezepte (
    rezeptID VARCHAR(50) NOT NULL,
    rezeptname VARCHAR(255) NOT NULL,
    rezeptheadline VARCHAR(255),
    rezeptDisc VARCHAR(255),
    rezeptdifficulty INT,
    prepTime VARCHAR(30),
    totalTime varchar(30),
    servingSize INT,
    link VARCHAR(255),
    rating FLOAT,
    steps INT,
    PRIMARY KEY (rezeptID)
);

create Table Nutrition(
  ntype varchar(50) Not null,
  nName varchar(255) not Null,
  amount int,
  unit varchar(20),
  primary key(ntype)

);

create table NutrInRezept(
  ntype varchar(50) not null references Nutration(ntype),
  rezeptID varchar(50) not null references Rezepte(rezeptID),
  primary key(ntype, rezeptID)
);

create Table Ingfamily(
  familienID varchar(50) not null primary key,
  familienName varchar(255) not null
);


create table Ingredients(
  ingID varchar(50) not null primary key,
  ingName varchar(255) not null,
  familienID varchar(50) not null references Ingfamily(familienID)
);


create table IngInRezept(
  ingID varchar(50) not null references Ingredients(ingID),
  rezeptID varchar(50) not null references Rezepte(rezeptID),
  primary key(ingID,rezeptID)
);
