# Create database
CREATE database world;
use world;

# CREATE TABLE (read from Simio)
CREATE TABLE Simio (
Id int(11) NOT NULL auto_increment,
Q int(11) NULL,
Tally1 double NULL, Tally2 double NULL, Tally3 double NULL, Tally4 double NULL, Tally5 double NULL, Tally6 double NULL,
Tally7 double NULL, Tally8 double NULL, Tally9 double NULL, Tally10 double NULL, Tally11 double NULL, Tally12 double NULL,
Num1 int(11) NULL, Num2 int(11) NULL, Num3 int(11) NULL, Num4 int(11) NULL, Num5 int(11) NULL, Num6 int(11) NULL,
Num7 int(11) NULL, Num8 int(11) NULL, Num9 int(11) NULL, Num10 int(11) NULL, Num11 int(11) NULL, Num12 int(11) NULL,
DateTime datetime NULL,
PRIMARY KEY (`Id`));
 
# CREATE TABLE (write to Simio)
CREATE TABLE BrokTab (
Id int(11) NOT NULL auto_increment,
Bridge1 double NOT NULL, Bridge2 double NOT NULL, Bridge3 double NOT NULL, Bridge4 double NOT NULL,
Bridge5 double NOT NULL, Bridge6 double NOT NULL, Bridge7 double NOT NULL, Bridge8 double NOT NULL,
PRIMARY KEY (`Id`));

# Insert value for assigning the probability of being broken
# (value can be any real number bewteen 0 and 1)
insert into BrokTab
(Bridge1, Bridge2, Bridge3, Bridge4, Bridge5, Bridge6, Bridge7, Bridge8)
values (1,1,1,1,1,1,1,1);