/*==============================================================*/
/* DBMS name:      Microsoft SQL Server 2012                    */
/* Created on:     2025/5/21 14:05:47                           */
/*==============================================================*/


if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('"ORDER"') and o.name = 'FK_ORDER_ORDER_STUDENT')
alter table "ORDER"
   drop constraint FK_ORDER_ORDER_STUDENT
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('"ORDER"') and o.name = 'FK_ORDER_ORDER2_MAINTAIN')
alter table "ORDER"
   drop constraint FK_ORDER_ORDER2_MAINTAIN
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('"ORDER"') and o.name = 'FK_ORDER_ORDER3_CLASSIFY')
alter table "ORDER"
   drop constraint FK_ORDER_ORDER3_CLASSIFY
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('"ORDER"') and o.name = 'FK_ORDER_ORDER4_ROOMS')
alter table "ORDER"
   drop constraint FK_ORDER_ORDER4_ROOMS
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('ROOMS') and o.name = 'FK_ROOMS_CHECKROOM_ADMINIST')
alter table ROOMS
   drop constraint FK_ROOMS_CHECKROOM_ADMINIST
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('STUDENT') and o.name = 'FK_STUDENT_LIVE_ROOMS')
alter table STUDENT
   drop constraint FK_STUDENT_LIVE_ROOMS
go

if exists (select 1
            from  sysobjects
           where  id = object_id('ADMINISTRATOR')
            and   type = 'U')
   drop table ADMINISTRATOR
go

if exists (select 1
            from  sysobjects
           where  id = object_id('CLASSIFY')
            and   type = 'U')
   drop table CLASSIFY
go

if exists (select 1
            from  sysobjects
           where  id = object_id('MAINTAINER')
            and   type = 'U')
   drop table MAINTAINER
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('"ORDER"')
            and   name  = 'ORDER4_FK'
            and   indid > 0
            and   indid < 255)
   drop index "ORDER".ORDER4_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('"ORDER"')
            and   name  = 'ORDER3_FK'
            and   indid > 0
            and   indid < 255)
   drop index "ORDER".ORDER3_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('"ORDER"')
            and   name  = 'ORDER2_FK'
            and   indid > 0
            and   indid < 255)
   drop index "ORDER".ORDER2_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('"ORDER"')
            and   name  = 'ORDER_FK'
            and   indid > 0
            and   indid < 255)
   drop index "ORDER".ORDER_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('"ORDER"')
            and   type = 'U')
   drop table "ORDER"
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('ROOMS')
            and   name  = 'checkroom_FK'
            and   indid > 0
            and   indid < 255)
   drop index ROOMS.checkroom_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('ROOMS')
            and   type = 'U')
   drop table ROOMS
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('STUDENT')
            and   name  = 'live_FK'
            and   indid > 0
            and   indid < 255)
   drop index STUDENT.live_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('STUDENT')
            and   type = 'U')
   drop table STUDENT
go

/*==============================================================*/
/* Table: ADMINISTRATOR                                         */
/*==============================================================*/
create table ADMINISTRATOR (
   ano                  varchar(8)           not null,
   aname                varchar(10)          not null,
   apwd                 varchar(10)          not null,
   alink                varchar(11)          not null,
   constraint PK_ADMINISTRATOR primary key nonclustered (ano)
)
go

/*==============================================================*/
/* Table: CLASSIFY                                              */
/*==============================================================*/
create table CLASSIFY (
   cno                  varchar(100)         not null,
   class                char(4)              not null,
   ccontent             text                 not null,
   pay                  int                  not null default 0,
   constraint PK_CLASSIFY primary key nonclustered (cno),
   constraint CK_CLASS check (class IN ('固有资产维修','特殊情况'))
)
go

/*==============================================================*/
/* Table: MAINTAINER                                            */
/*==============================================================*/
create table MAINTAINER (
   mno                  varchar(8)           not null,
   mname                varchar(10)          not null,
   mpwd                 varchar(10)          not null,
   mlink                varchar(11)          not null,
   allscore             int                  not null default 0,
   constraint PK_MAINTAINER primary key nonclustered (mno)
)
go

/*==============================================================*/
/* Table: "ORDER"                                               */
/*==============================================================*/
create table "ORDER" (
   sno                  char(8)              not null,
   mno                  varchar(8)           not null,
   cno                  varchar(100)         not null,
   rno                  varchar(10)          not null,
   ono                  bigint               identity,
   status               int                  not null,
   ocontent             text                 not null,
   starttime            datetime             not null,
   finishtime           datetime             null,
   comment              text                 null,
   score                int                  not null default 3,
   constraint PK_ORDER primary key (ono)
)
go

/*==============================================================*/
/* Index: ORDER_FK                                              */
/*==============================================================*/
create index ORDER_FK on "ORDER" (
sno ASC
)
go

/*==============================================================*/
/* Index: ORDER2_FK                                             */
/*==============================================================*/
create index ORDER2_FK on "ORDER" (
mno ASC
)
go

/*==============================================================*/
/* Index: ORDER3_FK                                             */
/*==============================================================*/
create index ORDER3_FK on "ORDER" (
cno ASC
)
go

/*==============================================================*/
/* Index: ORDER4_FK                                             */
/*==============================================================*/
create index ORDER4_FK on "ORDER" (
rno ASC
)
go

/*==============================================================*/
/* Table: ROOMS                                                 */
/*==============================================================*/
create table ROOMS (
   rno                  varchar(10)          not null,
   ano                  varchar(8)           null,
   address              varchar(30)          not null,
   assert               text                 not null,
   constraint PK_ROOMS primary key nonclustered (rno)
)
go

/*==============================================================*/
/* Index: checkroom_FK                                          */
/*==============================================================*/
create index checkroom_FK on ROOMS (
ano ASC
)
go

/*==============================================================*/
/* Table: STUDENT                                               */
/*==============================================================*/
create table STUDENT (
   sno                  char(8)              not null,
   rno                  varchar(10)          null,
   sname                varchar(10)          not null,
   spwd                 varchar(10)          not null,
   slink                varchar(11)          not null,
   constraint PK_STUDENT primary key nonclustered (sno)
)
go

/*==============================================================*/
/* Index: live_FK                                               */
/*==============================================================*/
create index live_FK on STUDENT (
rno ASC
)
go

alter table "ORDER"
   add constraint FK_ORDER_ORDER_STUDENT foreign key (sno)
      references STUDENT (sno)
go

alter table "ORDER"
   add constraint FK_ORDER_ORDER2_MAINTAIN foreign key (mno)
      references MAINTAINER (mno)
go

alter table "ORDER"
   add constraint FK_ORDER_ORDER3_CLASSIFY foreign key (cno)
      references CLASSIFY (cno)
go

alter table "ORDER"
   add constraint FK_ORDER_ORDER4_ROOMS foreign key (rno)
      references ROOMS (rno)
go

alter table ROOMS
   add constraint FK_ROOMS_CHECKROOM_ADMINIST foreign key (ano)
      references ADMINISTRATOR (ano)
go

alter table STUDENT
   add constraint FK_STUDENT_LIVE_ROOMS foreign key (rno)
      references ROOMS (rno)
go

