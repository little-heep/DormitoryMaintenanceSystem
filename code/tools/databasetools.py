from ..models.structs import (
    Administrator,
    Classify,
    Maintainer,
    Order,
    Rooms,
    Student
)
from typing import List, Optional, Tuple
import pyodbc
from datetime import datetime
#以下所有函数的参数db指一个数据库连接

#数据库初始化,返回一个数据库连接，用于对数据库操作
def db_init():
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={"localhost"};'
        f'DATABASE={"SchoolMaintainance"};'
        f'UID={"sa"};'
        f'PWD={"abc"}'
    )
    try:
        conn = pyodbc.connect(connection_string)
        print("数据库连接成功")
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        raise

#---------------------------------增----------------------------------

#新增订单（学生使用）：传入Order结构体
def db_add_order(db,order:Order):
    """
        新增订单
        :param db: 数据库连接
        :param order: Order对象
        :return: 是否成功
    """
    try:
        cursor = db.cursor()
        sql = """
            INSERT INTO [ORDER] (sno, mno, cno, rno, status, ocontent, starttime)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        cursor.execute(sql, (
            order.sno, order.mno, order.cno, order.mo,
            order.status, order.ocontent, order.starttime
        ))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        db.rollback()
        print(f"新增订单失败: {e}")
        return False

#新增学生
def db_add_student(db,student:Student):
    try:
        cursor = db.cursor()
        # 准备SQL语句，包含输出参数
        sql = """
            DECLARE @ResultCode INT, @ResultMessage NVARCHAR(100);
            EXEC [dbo].[AddStudent] 
            @id = ?, 
            @rno = ?, 
            @name = ?, 
            @pwd = ?, 
            @slink = ?,
            @ResultCode = @ResultCode OUTPUT,
            @ResultMessage = @ResultMessage OUTPUT;
            SELECT @ResultCode AS ResultCode, @ResultMessage AS ResultMessage;
            """

        # 执行存储过程
        cursor.execute(sql,
                       student.sno,
                       student.mo,
                       student.sname,
                       student.spwd,
                       student.slink)

        # 获取输出参数
        result = cursor.fetchone()
        result_code = result.ResultCode
        result_message = result.ResultMessage

        db.commit()
        cursor.close()

        return result_code, result_message

    except pyodbc.Error as e:
        print(f"数据库错误: {e}")
        return -1, f"数据库错误: {str(e)}"
    except Exception as e:
        print(f"一般错误: {e}")
        return -1, f"一般错误: {str(e)}"

#新增维修工
def db_add_maintainer(db,maintainer:Maintainer):
    try:
        cursor = db.cursor()
        # 准备SQL语句，包含输出参数
        sql = """
            DECLARE @ResultCode INT, @ResultMessage NVARCHAR(100);
            EXEC [dbo].[AddMaintainer] 
            @id = ?, 
            @name = ?, 
            @pwd = ?, 
            @link = ?,
            @ResultCode = @ResultCode OUTPUT,
            @ResultMessage = @ResultMessage OUTPUT;
            SELECT @ResultCode AS ResultCode, @ResultMessage AS ResultMessage;
            """

        # 执行存储过程
        cursor.execute(sql,
                       maintainer.mno,
                       maintainer.mname,
                       maintainer.mpwd,
                       maintainer.mlink)

        # 获取输出参数
        result = cursor.fetchone()
        result_code = result.ResultCode
        result_message = result.ResultMessage

        db.commit()
        cursor.close()

        return result_code, result_message

    except pyodbc.Error as e:
        print(f"数据库错误: {e}")
        return -1, f"数据库错误: {str(e)}"
    except Exception as e:
        print(f"一般错误: {e}")
        return -1, f"一般错误: {str(e)}"

#新增管理员
def db_add_administor(db,administer:Administrator):
    try:
        cursor = db.cursor()
        # 准备SQL语句，包含输出参数
        sql = """
            DECLARE @ResultCode INT, @ResultMessage NVARCHAR(100);
            EXEC [dbo].[AddAdministrator] 
            @id = ?, 
            @name = ?, 
            @pwd = ?, 
            @slink = ?,
            @ResultCode = @ResultCode OUTPUT,
            @ResultMessage = @ResultMessage OUTPUT;
            SELECT @ResultCode AS ResultCode, @ResultMessage AS ResultMessage;
            """

        # 执行存储过程
        cursor.execute(sql,
                       administer.ano,
                       administer.aname,
                       administer.apwd,
                       administer.alink)

        # 获取输出参数
        result = cursor.fetchone()
        result_code = result.ResultCode
        result_message = result.ResultMessage

        db.commit()
        cursor.close()

        return result_code, result_message

    except pyodbc.Error as e:
        print(f"数据库错误: {e}")
        return -1, f"数据库错误: {str(e)}"
    except Exception as e:
        print(f"一般错误: {e}")
        return -1, f"一般错误: {str(e)}"

#新增宿舍
def db_add_room(db,room:Rooms):
    try:
        cursor = db.cursor()
        # 准备SQL语句，包含输出参数
        sql = """
            DECLARE @ResultCode INT, @ResultMessage NVARCHAR(100);
            EXEC [dbo].[AddRoom] 
            @id = ?, 
            @master = ?, 
            @address = ?, 
            @assert = ?, 
            @ResultCode = @ResultCode OUTPUT,
            @ResultMessage = @ResultMessage OUTPUT;
            SELECT @ResultCode AS ResultCode, @ResultMessage AS ResultMessage;
            """

        # 执行存储过程
        cursor.execute(sql,
                       room.mo,
                       room.ano,
                       room.address,
                       room.assert_)

        # 获取输出参数
        result = cursor.fetchone()
        result_code = result.ResultCode
        result_message = result.ResultMessage

        db.commit()
        cursor.close()

        return result_code, result_message

    except pyodbc.Error as e:
        print(f"数据库错误: {e}")
        return -1, f"数据库错误: {str(e)}"
    except Exception as e:
        print(f"一般错误: {e}")
        return -1, f"一般错误: {str(e)}"

#新增报修类别
def db_add_classify(db,cla:Classify):
    try:
        cursor = db.cursor()
        # 准备SQL语句，包含输出参数
        sql = """
            DECLARE @ResultCode INT, @ResultMessage NVARCHAR(100);
            EXEC [dbo].[AddClassify] 
            @id = ?, 
            @class = ?, 
            @content = ?, 
            @pay = ?,
            @ResultCode = @ResultCode OUTPUT,
            @ResultMessage = @ResultMessage OUTPUT;
            SELECT @ResultCode AS ResultCode, @ResultMessage AS ResultMessage;
            """

        # 执行存储过程
        cursor.execute(sql,
                       cla.cno,
                       cla.class_,
                       cla.content,
                       cla.pay)

        # 获取输出参数
        result = cursor.fetchone()
        result_code = result.ResultCode
        result_message = result.ResultMessage

        db.commit()
        cursor.close()

        return result_code, result_message

    except pyodbc.Error as e:
        print(f"数据库错误: {e}")
        return -1, f"数据库错误: {str(e)}"
    except Exception as e:
        print(f"一般错误: {e}")
        return -1, f"一般错误: {str(e)}"

#-------------------------删--------------------------------

#删除订单
def db_del_order(db, ono: int):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM [ORDER] WHERE ono = ?"
        cursor.execute(sql, (ono,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"删除订单失败: {e}")
        return False

#删除学生
def db_del_student(db, sno: str):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM STUDENT WHERE sno = ?"
        cursor.execute(sql, (sno,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"删除学生失败: {e}")
        return False

#删除维修工
def db_del_maintainer(db, mno: str):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM MAINTAINER WHERE mno = ?"
        cursor.execute(sql, (mno,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"删除维修工失败: {e}")
        return False

#删除管理员
def db_del_administer(db, ano: str):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM ADMINISTRATOR WHERE ano = ?"
        cursor.execute(sql, (ano,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"删除管理员失败: {e}")
        return False

#删除宿舍
def db_del_room(db, mo: str):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM ROOMS WHERE rno = ?"
        cursor.execute(sql, (mo,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"删除宿舍失败: {e}")
        return False

#删除报修类别
def db_del_classify(db, cno: str):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM CLASSIFY WHERE cno = ?"
        cursor.execute(sql, (cno,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"删除报修类别失败: {e}")
        return False


#------------------------------------改---------------------------

#修改学生密码或宿舍，修改密码cl=0 detail=新密码，修改宿舍cl=1 detail=新宿舍号，修改联系方式cl=2 detail=新联系方式
def db_student_update(db,cl,detail,sid):
    try:
        cursor = db.cursor()
        if cl == 0:  # 修改密码
            sql = "UPDATE STUDENT SET spwd = ? WHERE sno = ?"
        elif cl == 1:  # 修改宿舍
            sql = "UPDATE STUDENT SET rno = ? WHERE sno = ?"
        elif cl == 2:  # 修改联系方式
            sql = "UPDATE STUDENT SET slink = ? WHERE sno = ?"
        else:
            return False

        cursor.execute(sql, (detail, sid))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"修改学生信息失败: {e}")
        return False

#修改维修工或管理员密码，维修工则cl=0，管理员则cl=1
def db_worker_admin_updatepwd(db,cl,pwd,id):
    try:
        cursor = db.cursor()
        if cl == 0:  # 维修工
            sql = "UPDATE MAINTAINER SET mpwd = ? WHERE mno = ?"
        elif cl == 1:  # 管理员
            sql = "UPDATE ADMINISTRATOR SET apwd = ? WHERE ano = ?"
        else:
            return False

        cursor.execute(sql, (pwd, id))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"修改密码失败: {e}")
        return False

#修改维修工或管理员联系方式，维修工则cl=0，管理员则cl=1
def db_worker_admin_updatelink(db, cl: int, link: str, id: str):
    try:
        cursor = db.cursor()
        if cl == 0:  # 维修工
            sql = "UPDATE MAINTAINER SET mlink = ? WHERE mno = ?"
        elif cl == 1:  # 管理员
            sql = "UPDATE ADMINISTRATOR SET alink = ? WHERE ano = ?"
        else:
            return False

        cursor.execute(sql, (link, id))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"修改联系方式失败: {e}")
        return False


# 修改订单的评分score和评论comment
def db_order_updatescore(db, score: int, comment: str, ono: int):
    try:
        cursor = db.cursor()
        sql = "UPDATE [ORDER] SET score = ?, comment = ? WHERE ono = ?"
        cursor.execute(sql, (score, comment, ono))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"修改订单评分失败: {e}")
        return False


# 修改订单的完成时间
def db_order_updatetime(db, finish_time: datetime, ono: int):
    try:
        cursor = db.cursor()
        sql = "UPDATE [ORDER] SET finishtime = ? WHERE ono = ?"
        cursor.execute(sql, (finish_time, ono))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"修改订单完成时间失败: {e}")
        return False

def db_order_updatestatus(db,status:int,orderid:int):
    try:
        cursor = db.cursor()
        # 准备SQL语句，包含输出参数
        sql = """
            DECLARE @ResultCode INT, @ResultMessage NVARCHAR(100);
            EXEC [dbo].[ModifyStatus] 
            @status = ?, 
            @id = ?,
            @ResultCode = @ResultCode OUTPUT,
            @ResultMessage = @ResultMessage OUTPUT;
            SELECT @ResultCode AS ResultCode, @ResultMessage AS ResultMessage;
            """

        # 执行存储过程
        cursor.execute(sql,status,orderid)

        # 获取输出参数
        result = cursor.fetchone()
        result_code = result.ResultCode
        result_message = result.ResultMessage

        db.commit()
        cursor.close()

        return result_code, result_message

    except pyodbc.Error as e:
        print(f"数据库错误: {e}")
        return -1, f"数据库错误: {str(e)}"
    except Exception as e:
        print(f"一般错误: {e}")
        return -1, f"一般错误: {str(e)}"


#--------------------------------查------------------------------------
#查询所有学生
def db_all_student(db) -> List[Student]:
    try:
        cursor = db.cursor()
        sql = "SELECT sno, rno, sname, spwd, slink FROM STUDENT"
        cursor.execute(sql)
        results = cursor.fetchall()

        students = []
        for row in results:
            student = Student(
                sno=row[0],
                rno=row[1],
                sname=row[2],
                spwd=row[3],
                slink=row[4]
            )
            students.append(student)
        return students
    except Exception as e:
        print(f"查询所有学生失败: {e}")
        return []

#按照学号查询学生信息
def db_student_by_id(db, sno: str) -> Optional[Student]:
    try:
        cursor = db.cursor()
        sql = "SELECT sno, rno, sname, spwd, slink FROM STUDENT WHERE sno = ?"
        cursor.execute(sql, (sno,))
        row = cursor.fetchone()

        if row:
            return Student(
                sno=row[0],
                rno=row[1],
                sname=row[2],
                spwd=row[3],
                slink=row[4]
            )
        return None
    except Exception as e:
        print(f"按学号查询学生失败: {e}")
        return None

#查询所有维修工
def db_all_worker(db) -> List[Maintainer]:
    try:
        cursor = db.cursor()
        sql = "SELECT mno, mname, mpwd, mlink, allscore FROM MAINTAINER"
        cursor.execute(sql)
        results = cursor.fetchall()

        maintainers = []
        for row in results:
            maintainer = Maintainer(
                mno=row[0],
                mname=row[1],
                mpwd=row[2],
                mlink=row[3],
                allscore=row[4]
            )
            maintainers.append(maintainer)
        return maintainers
    except Exception as e:
        print(f"查询所有维修工失败: {e}")
        return []


# 按照工号查询维修工信息
def db_worker_by_id(db, mno: str) -> Optional[Maintainer]:
    try:
        cursor = db.cursor()
        sql = "SELECT mno, mname, mpwd, mlink, allscore FROM MAINTAINER WHERE mno = ?"
        cursor.execute(sql, (mno,))
        row = cursor.fetchone()

        if row:
            return Maintainer(
                mno=row[0],
                mname=row[1],
                mpwd=row[2],
                mlink=row[3],
                allscore=row[4]
            )
        return None
    except Exception as e:
        print(f"按工号查询维修工失败: {e}")
        return None


# 按照工号查询管理员信息
def db_admin_by_id(db, ano: str) -> Optional[Administrator]:
    try:
        cursor = db.cursor()
        sql = "SELECT ano, aname, apwd, alink FROM ADMINISTRATOR WHERE ano = ?"
        cursor.execute(sql, (ano,))
        row = cursor.fetchone()

        if row:
            return Administrator(
                ano=row[0],
                aname=row[1],
                apwd=row[2],
                alink=row[3]
            )
        return None
    except Exception as e:
        print(f"按工号查询管理员失败: {e}")
        return None


# 查询所有分类信息
def db_all_classify(db) -> List[Classify]:
    try:
        cursor = db.cursor()
        sql = "SELECT cno, class, ccontent, pay FROM CLASSIFY"
        cursor.execute(sql)
        results = cursor.fetchall()

        classifies = []
        for row in results:
            classify = Classify(
                cno=row[0],
                class_=row[1],
                content=row[2],
                pay=row[3]
            )
            classifies.append(classify)
        return classifies
    except Exception as e:
        print(f"查询所有分类信息失败: {e}")
        return []


# 查询所有订单
def db_all_order(db) -> List[Order]:
    try:
        cursor = db.cursor()
        sql = "SELECT ono, sno, mno, cno, rno, status, ocontent, starttime, finishtime, comment, score FROM [ORDER]"
        cursor.execute(sql)
        results = cursor.fetchall()

        orders = []
        for row in results:
            order = Order(
                ono=row[0],
                sno=row[1],
                mno=row[2],
                cno=row[3],
                mo=row[4],
                status=row[5],
                ocontent=row[6],
                starttime=row[7],
                finishtime=row[8],
                comment=row[9],
                score=row[10]
            )
            orders.append(order)
        return orders
    except Exception as e:
        print(f"查询所有订单失败: {e}")
        return []

#查询各类报修类别的频率
def db_class_frequency(db) -> List[Tuple[str, int]]:
    """
    查询维修统计视图
    :param db: 数据库连接
    :return: 返回一个列表，包含元组(维修类别编号, 保修次数)
    """
    try:
        cursor = db.cursor()
        # 直接查询视图，就像查询普通表一样
        sql = "SELECT 维修类别编号, 保修次数 FROM [dbo].[CLASS_FREQUENCY]"
        cursor.execute(sql)
        results = cursor.fetchall()

        return [(row[0], row[1]) for row in results]

    except Exception as e:
        print(f"查询维修统计视图失败: {e}")
        return []

#查询各宿舍报修的频率
def db_room_frequency(db) -> List[Tuple[str, int]]:
    """
    查询维修统计视图
    :param db: 数据库连接
    :return: 返回一个列表，包含元组(宿舍号, 保修次数)
    """
    try:
        cursor = db.cursor()
        # 直接查询视图，就像查询普通表一样
        sql = "SELECT rno, 保修次数 FROM ROOM_FREQUENCY"
        cursor.execute(sql)
        results = cursor.fetchall()

        return [(row[0], row[1]) for row in results]

    except Exception as e:
        print(f"查询维修统计视图失败: {e}")
        return []

#查询每月每个维修工的积分情况
def db_worker_scores(db) -> List[Tuple[str, int, int, str, int, int, int]]:
    """
    查询维修工积分统计视图
    :param db: 数据库连接
    :return: 返回一个列表，包含元组(工号, 年份, 月份, 月份名称, 总积分, 维修单数, 平均积分)
    """
    try:
        cursor = db.cursor()
        # 查询维修工积分统计视图
        sql = """
        SELECT 维修工工号, 年份, 月份, 月份名称, 当月总积分, 当月维修单数, 当月平均每单积分 
        FROM SCOREREAD
        ORDER BY 维修工工号, 年份, 月份
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        return [
            (row.维修工工号, row.年份, row.月份, row.月份名称,
             row.当月总积分, row.当月维修单数, row.当月平均每单积分)
            for row in results
        ]

    except Exception as e:
        print(f"查询维修工积分统计视图失败: {e}")
        return []

#统计每个月收入情况
def db_month_icome(db) -> List[Tuple[int, int, int]]:
    """
    查询维修工积分统计视图
    :param db: 数据库连接
    :return: 返回一个列表，包含元组(年份，月份，总收入)
    """
    try:
        cursor = db.cursor()
        # 查询每月收入统计视图
        sql = """
            SELECT year(o.starttime) AS y, month(o.starttime) AS m,SUM(c.pay) AS monthly_revenue
            FROM [ORDER] o JOIN CLASSIFY c ON o.cno = c.cno
            GROUP BY YEAR(o.starttime), MONTH(o.starttime), DATENAME(MONTH, o.starttime)
            ORDER BY YEAR(o.starttime), MONTH(o.starttime);
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        return [(row.y, row.m, row.monthly_revenue) for row in results]

    except Exception as e:
        print(f"收入统计失败: {e}")
        return []