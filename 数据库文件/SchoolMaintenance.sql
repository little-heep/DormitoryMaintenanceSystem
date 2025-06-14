USE [master]
GO
/****** Object:  Database [SchoolMaintainance]    Script Date: 2025/6/11 23:20:36 ******/
CREATE DATABASE [SchoolMaintainance]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'SchoolMaintainance', FILENAME = N'D:\download\sql\MSSQL16.MSSQLSERVER\MSSQL\DATA\SchoolMaintainance.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'SchoolMaintainance_log', FILENAME = N'D:\download\sql\MSSQL16.MSSQLSERVER\MSSQL\DATA\SchoolMaintainance_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [SchoolMaintainance] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [SchoolMaintainance].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [SchoolMaintainance] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET ARITHABORT OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [SchoolMaintainance] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [SchoolMaintainance] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET  DISABLE_BROKER 
GO
ALTER DATABASE [SchoolMaintainance] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [SchoolMaintainance] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET RECOVERY FULL 
GO
ALTER DATABASE [SchoolMaintainance] SET  MULTI_USER 
GO
ALTER DATABASE [SchoolMaintainance] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [SchoolMaintainance] SET DB_CHAINING OFF 
GO
ALTER DATABASE [SchoolMaintainance] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [SchoolMaintainance] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [SchoolMaintainance] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [SchoolMaintainance] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'SchoolMaintainance', N'ON'
GO
ALTER DATABASE [SchoolMaintainance] SET QUERY_STORE = ON
GO
ALTER DATABASE [SchoolMaintainance] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [SchoolMaintainance]
GO
/****** Object:  Table [dbo].[CLASSIFY]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CLASSIFY](
	[cno] [varchar](100) NOT NULL,
	[class] [char](4) NOT NULL,
	[ccontent] [text] NOT NULL,
	[pay] [int] NOT NULL,
 CONSTRAINT [PK_CLASSIFY] PRIMARY KEY NONCLUSTERED 
(
	[cno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ORDER]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ORDER](
	[sno] [char](8) NOT NULL,
	[mno] [varchar](8) NOT NULL,
	[cno] [varchar](100) NOT NULL,
	[rno] [varchar](10) NOT NULL,
	[ono] [bigint] IDENTITY(1,1) NOT NULL,
	[status] [int] NOT NULL,
	[ocontent] [text] NOT NULL,
	[starttime] [datetime] NOT NULL,
	[finishtime] [datetime] NULL,
	[comment] [text] NULL,
	[score] [int] NOT NULL,
 CONSTRAINT [PK_ORDER] PRIMARY KEY CLUSTERED 
(
	[ono] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  View [dbo].[BILL]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[BILL]
AS
SELECT dbo.[ORDER].sno AS 维修单号, dbo.[ORDER].starttime AS 申请时间, dbo.[ORDER].finishtime AS 完成时间, dbo.CLASSIFY.pay AS 金额
FROM   dbo.CLASSIFY INNER JOIN
          dbo.[ORDER] ON dbo.CLASSIFY.cno = dbo.[ORDER].cno
WHERE (dbo.[ORDER].status >= 2)
GO
/****** Object:  View [dbo].[SCOREREAD]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[SCOREREAD]
AS
SELECT mno AS 维修工工号, YEAR(starttime) AS 年份, MONTH(starttime) AS 月份, DATENAME(MONTH, starttime) AS 月份名称, SUM(score) AS 当月总积分, COUNT(*) AS 当月维修单数, AVG(score) 
          AS 当月平均每单积分
FROM   dbo.[ORDER]
GROUP BY mno, YEAR(starttime), MONTH(starttime), DATENAME(MONTH, starttime), mno
GO
/****** Object:  View [dbo].[CLASS_FREQUENCY]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[CLASS_FREQUENCY] AS
SELECT 
    [ORDER].cno AS 维修类别编号,
	COUNT(*) as 保修次数
FROM 
    [ORDER] join [CLASSIFY] on [ORDER].cno=[CLASSIFY].cno
GROUP BY 
    [ORDER].cno
GO
/****** Object:  View [dbo].[ROOM_FREQUENCY]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW	[dbo].[ROOM_FREQUENCY] AS
SELECT 
    rno,
	COUNT(*) as 保修次数
FROM 
    [ORDER]
GROUP BY 
    [ORDER].rno
GO
/****** Object:  Table [dbo].[ADMINISTRATOR]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ADMINISTRATOR](
	[ano] [varchar](8) NOT NULL,
	[aname] [varchar](10) NOT NULL,
	[apwd] [varchar](10) NOT NULL,
	[alink] [varchar](11) NOT NULL,
 CONSTRAINT [PK_ADMINISTRATOR] PRIMARY KEY NONCLUSTERED 
(
	[ano] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MAINTAINER]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MAINTAINER](
	[mno] [varchar](8) NOT NULL,
	[mname] [varchar](10) NOT NULL,
	[mpwd] [varchar](10) NOT NULL,
	[mlink] [varchar](11) NOT NULL,
	[allscore] [int] NOT NULL,
 CONSTRAINT [PK_MAINTAINER] PRIMARY KEY NONCLUSTERED 
(
	[mno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ROOMS]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ROOMS](
	[rno] [varchar](10) NOT NULL,
	[ano] [varchar](8) NULL,
	[address] [varchar](30) NOT NULL,
	[assert] [text] NOT NULL,
 CONSTRAINT [PK_ROOMS] PRIMARY KEY NONCLUSTERED 
(
	[rno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[STUDENT]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[STUDENT](
	[sno] [char](8) NOT NULL,
	[rno] [varchar](10) NULL,
	[sname] [varchar](10) NOT NULL,
	[spwd] [varchar](10) NOT NULL,
	[slink] [varchar](11) NOT NULL,
 CONSTRAINT [PK_STUDENT] PRIMARY KEY NONCLUSTERED 
(
	[sno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [ORDER_FK]    Script Date: 2025/6/11 23:20:36 ******/
CREATE NONCLUSTERED INDEX [ORDER_FK] ON [dbo].[ORDER]
(
	[sno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [ORDER2_FK]    Script Date: 2025/6/11 23:20:36 ******/
CREATE NONCLUSTERED INDEX [ORDER2_FK] ON [dbo].[ORDER]
(
	[mno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [ORDER3_FK]    Script Date: 2025/6/11 23:20:36 ******/
CREATE NONCLUSTERED INDEX [ORDER3_FK] ON [dbo].[ORDER]
(
	[cno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [ORDER4_FK]    Script Date: 2025/6/11 23:20:36 ******/
CREATE NONCLUSTERED INDEX [ORDER4_FK] ON [dbo].[ORDER]
(
	[rno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [checkroom_FK]    Script Date: 2025/6/11 23:20:36 ******/
CREATE NONCLUSTERED INDEX [checkroom_FK] ON [dbo].[ROOMS]
(
	[ano] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [live_FK]    Script Date: 2025/6/11 23:20:36 ******/
CREATE NONCLUSTERED INDEX [live_FK] ON [dbo].[STUDENT]
(
	[rno] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[CLASSIFY] ADD  DEFAULT ((0)) FOR [pay]
GO
ALTER TABLE [dbo].[MAINTAINER] ADD  DEFAULT ((0)) FOR [allscore]
GO
ALTER TABLE [dbo].[ORDER] ADD  DEFAULT ((3)) FOR [score]
GO
ALTER TABLE [dbo].[ORDER]  WITH CHECK ADD  CONSTRAINT [FK_ORDER_ORDER_STUDENT] FOREIGN KEY([sno])
REFERENCES [dbo].[STUDENT] ([sno])
GO
ALTER TABLE [dbo].[ORDER] CHECK CONSTRAINT [FK_ORDER_ORDER_STUDENT]
GO
ALTER TABLE [dbo].[ORDER]  WITH CHECK ADD  CONSTRAINT [FK_ORDER_ORDER2_MAINTAIN] FOREIGN KEY([mno])
REFERENCES [dbo].[MAINTAINER] ([mno])
GO
ALTER TABLE [dbo].[ORDER] CHECK CONSTRAINT [FK_ORDER_ORDER2_MAINTAIN]
GO
ALTER TABLE [dbo].[ORDER]  WITH CHECK ADD  CONSTRAINT [FK_ORDER_ORDER3_CLASSIFY] FOREIGN KEY([cno])
REFERENCES [dbo].[CLASSIFY] ([cno])
GO
ALTER TABLE [dbo].[ORDER] CHECK CONSTRAINT [FK_ORDER_ORDER3_CLASSIFY]
GO
ALTER TABLE [dbo].[ORDER]  WITH CHECK ADD  CONSTRAINT [FK_ORDER_ORDER4_ROOMS] FOREIGN KEY([rno])
REFERENCES [dbo].[ROOMS] ([rno])
GO
ALTER TABLE [dbo].[ORDER] CHECK CONSTRAINT [FK_ORDER_ORDER4_ROOMS]
GO
ALTER TABLE [dbo].[ROOMS]  WITH CHECK ADD  CONSTRAINT [FK_ROOMS_CHECKROOM_ADMINIST] FOREIGN KEY([ano])
REFERENCES [dbo].[ADMINISTRATOR] ([ano])
GO
ALTER TABLE [dbo].[ROOMS] CHECK CONSTRAINT [FK_ROOMS_CHECKROOM_ADMINIST]
GO
ALTER TABLE [dbo].[STUDENT]  WITH CHECK ADD  CONSTRAINT [FK_STUDENT_LIVE_ROOMS] FOREIGN KEY([rno])
REFERENCES [dbo].[ROOMS] ([rno])
GO
ALTER TABLE [dbo].[STUDENT] CHECK CONSTRAINT [FK_STUDENT_LIVE_ROOMS]
GO
ALTER TABLE [dbo].[CLASSIFY]  WITH CHECK ADD  CONSTRAINT [CK_CLASS] CHECK  (([class]='特殊' OR [class]='普通'))
GO
ALTER TABLE [dbo].[CLASSIFY] CHECK CONSTRAINT [CK_CLASS]
GO
/****** Object:  StoredProcedure [dbo].[AddAdministrator]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[AddAdministrator]
@id varchar(8),
@name varchar(10),
@pwd varchar(10),
@slink varchar(11),
@ResultCode INT = 0 OUTPUT,
@ResultMessage NVARCHAR(100) = '' OUTPUT
as
begin
	 SET NOCOUNT ON
	if exists (SELECT 1 FROM ADMINISTRATOR WHERE ano = @id)
    BEGIN
        --不可重复注册
		SET @ResultCode = 0
        SET @ResultMessage = '该工号已注册'
        RETURN
    END
    ELSE
    BEGIN
        insert into ADMINISTRATOR(ano,aname,apwd,alink)
		values (@id,@name,@pwd,@slink)
		SET @ResultCode = 1
        SET @ResultMessage = '注册成功'
    END
end
GO
/****** Object:  StoredProcedure [dbo].[AddClassify]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[AddClassify]
@id varchar(100),
@class char(4),
@content text,
@pay int,
@ResultCode INT = 0 OUTPUT,
@ResultMessage NVARCHAR(100) = '' OUTPUT
as
begin
	 SET NOCOUNT ON
	if exists (SELECT 1 FROM CLASSIFY WHERE cno = @id)
    BEGIN
        --不可重复注册
		SET @ResultCode = 0
        SET @ResultMessage = '该编号已存在'
        RETURN
    END
    ELSE
    BEGIN
        insert into CLASSIFY(cno,class,ccontent,pay)
		values (@id,@class,@content,@pay)
		SET @ResultCode = 1
        SET @ResultMessage = '新增分类成功'
    END
end
GO
/****** Object:  StoredProcedure [dbo].[AddMaintainer]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[AddMaintainer]
@id varchar(8),
@name varchar(10),
@pwd varchar(10),
@link varchar(11),
@ResultCode INT = 0 OUTPUT,
@ResultMessage NVARCHAR(100) = '' OUTPUT
as
begin
	 SET NOCOUNT ON
	if exists (SELECT 1 FROM MAINTAINER WHERE mno = @id)
    BEGIN
        --不可重复注册
		SET @ResultCode = 0
        SET @ResultMessage = '该工号的维修员已存在'
        RETURN
    END
    ELSE
    BEGIN
        insert into MAINTAINER(mno,mname,mpwd,mlink)
		values (@id,@name,@pwd,@link)
		SET @ResultCode = 1
        SET @ResultMessage = '新增维修员成功'
    END
end
GO
/****** Object:  StoredProcedure [dbo].[AddRoom]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[AddRoom]
@id varchar(10),
@master varchar(8),
@address varchar(30),
@assert text,
@ResultCode INT = 0 OUTPUT,
@ResultMessage NVARCHAR(100) = '' OUTPUT
as
begin
	 SET NOCOUNT ON
	if exists (SELECT 1 FROM ROOMS WHERE rno = @id)
    BEGIN
        --不可重复注册
		SET @ResultCode = 0
        SET @ResultMessage = '该宿舍已存在'
        RETURN
    END
    ELSE
    BEGIN
        insert into ROOMS(rno,ano,address,assert)
		values (@id,@master,@address,@assert)
		SET @ResultCode = 1
        SET @ResultMessage = '新增宿舍成功'
    END
end
GO
/****** Object:  StoredProcedure [dbo].[AddStudent]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[AddStudent]
@id char(8),
@rno varchar(10),
@name varchar(10),
@pwd varchar(10),
@slink varchar(11),
@ResultCode INT = 0 OUTPUT,
@ResultMessage NVARCHAR(100) = '' OUTPUT
as
begin
	 SET NOCOUNT ON
	if exists (SELECT 1 FROM STUDENT WHERE sno = @id)
    BEGIN
        --不可重复注册
		SET @ResultCode = 0
        SET @ResultMessage = '该学号已注册'
        RETURN
    END
    ELSE
    BEGIN
        insert into STUDENT (sno,rno,sname,spwd,slink)
		values (@id,@rno,@name,@pwd,@slink)
		SET @ResultCode = 1
        SET @ResultMessage = '注册成功'
    END
end
GO
/****** Object:  StoredProcedure [dbo].[ModifyStatus]    Script Date: 2025/6/11 23:20:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[ModifyStatus]
@status int,
@id bigint,
@ResultCode INT = 0 OUTPUT,
@ResultMessage NVARCHAR(100) = '' OUTPUT
as
begin
    SET NOCOUNT ON
    
    BEGIN TRY
        -- 参数验证
        IF (@status < 0 OR @status > 3)
        BEGIN
            SET @ResultCode = 0  -- 参数错误
            SET @ResultMessage = '状态码错误'
            RETURN
        END
        
        -- 获取当前状态
        DECLARE @currentStatus INT
        SELECT @currentStatus = status FROM [ORDER] WHERE ono = @id
        
        -- 状态流转验证
        IF (@status < @currentStatus)
        BEGIN
            SET @ResultCode = 1  -- 状态不可回退
            SET @ResultMessage = '状态不可回退'
            RETURN
        END
        
        -- 更新状态
        BEGIN TRANSACTION
            UPDATE [ORDER]
            SET status = @status
            WHERE ono = @id
            
            SET @ResultCode = 2  -- 成功
            SET @ResultMessage = '订单状态更新成功'
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION
            
        SET @ResultCode = 99  -- 系统错误
        SET @ResultMessage = ERROR_MESSAGE()
    END CATCH
end
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[26] 2[14] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "CLASSIFY"
            Begin Extent = 
               Top = 12
               Left = 76
               Bottom = 254
               Right = 298
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "ORDER"
            Begin Extent = 
               Top = 0
               Left = 751
               Bottom = 426
               Right = 1416
            End
            DisplayFlags = 280
            TopColumn = 2
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'BILL'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'BILL'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[28] 2[23] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "ORDER"
            Begin Extent = 
               Top = 12
               Left = 76
               Bottom = 404
               Right = 320
            End
            DisplayFlags = 280
            TopColumn = 1
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 12
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'SCOREREAD'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'SCOREREAD'
GO
USE [master]
GO
ALTER DATABASE [SchoolMaintainance] SET  READ_WRITE 
GO
