import pyodbc
from typing import Optional, List , Tuple

from code.models.structs import (
    Administrator,
    Classify,
    Maintainer,
    Order,
    Rooms,
    Student
)
import code.tools.databasetools as dbtools


class AdminController:
    ##################### 用户管理 ###################

    def add_student(self, db: pyodbc.Connection, sno: str, mo: Optional[str], sname: str, spwd: str, slink: str):
        new_student = Student(sno=sno, mo=mo, sname=sname, spwd=spwd, slink=slink)
        res,err=dbtools.db_add_student(db, new_student)
        if res == -1:
            print("添加学生失败")
            return -1,err
        else:
            print("添加学生成功")
            return 0,""

    def add_maintainer(self, db: pyodbc.Connection, mno: str, mname: str, mpwd: str, mlink: str):
        new_maintainer = Maintainer(mno=mno, mname=mname, mpwd=mpwd, mlink=mlink,allscore=0)
        res,err=dbtools.db_add_maintainer(db, new_maintainer)
        if res == -1:
            print("添加维修员失败")
            return -1,err
        else:
            print("添加维修员成功")
            return 0,""

    def add_administor(self, db: pyodbc.Connection, ano: str, aname: str, apwd: str, alink: str):
        new_administrator = Administrator(ano=ano, aname=aname, apwd=apwd, alink=alink)
        res,err=dbtools.db_add_administor(db, new_administrator)
        if res == -1:
            print("添加管理员失败")
            return -1,err
        else:
            print("添加管理员成功")
            return 0,""

    def delete_student(self, db: pyodbc.Connection, sno: str):
        try:
            dbtools.db_del_student(db, sno)
            print("删除学生成功")
        except Exception as e:
            print(f"删除学生失败: {e}")

    def delete_maintainer(self, db: pyodbc.Connection, mno: str):
        try:
            dbtools.db_del_maintainer(db, mno)
            print("删除维修员成功")
        except Exception as e:
            print(f"删除维修员失败: {e}")

    def delete_administor(self, db: pyodbc.Connection, ano: str):
        try:
            dbtools.db_del_administor(db, ano)
            print("删除管理员成功")
        except Exception as e:
            print(f"删除管理员失败: {e}")

    def change_student_pwd(self, db: pyodbc.Connection, sno: str, new_pwd: str):
        cl = 0
        try:
            dbtools.db_student_update(db, cl, new_pwd, sno)
            print("修改学生密码成功")
        except Exception as e:
            print(f"修改学生密码失败: {e}")

    def change_student_room(self, db: pyodbc.Connection, sno: str, rno: str):
        cl = 1
        try:
            dbtools.db_student_update(db, cl, rno, sno)
            print("修改学生宿舍成功")
        except Exception as e:
            print(f"修改学生宿舍失败: {e}")

    def change_student_slink(self, db: pyodbc.Connection, sno: str, new_slink: str):
        cl = 3
        try:
            dbtools.db_student_update(db, cl, new_slink, sno)
            print("修改学生联系方式成功")
        except Exception as e:
            print(f"修改学生联系方式失败: {e}")

    def change_maintainer_pwd(self, db: pyodbc.Connection, mno: str, new_pwd: str):
        cl = 0
        try:
            dbtools.db_worker_admin_updatepwd(db, cl, new_pwd, mno)
            print("修改维修员密码成功")
        except Exception as e:
            print(f"修改维修员密码失败: {e}")

    def change_admin_pwd(self, db: pyodbc.Connection, ano: str, new_pwd: str):
        cl = 1
        try:
            dbtools.db_worker_admin_updatepwd(db, cl, new_pwd, ano)
            print("修改管理员密码成功")
        except Exception as e:
            print(f"修改管理员密码失败: {e}")

    def change_maintainer_link(self, db: pyodbc.Connection, mno: str, new_mlink: str):
        cl = 0
        try:
            dbtools.db_worker_admin_updatelink(db, cl, new_mlink, mno)
            print("修改维修员联系方式成功")
        except Exception as e:
            print(f"修改维修员联系方式失败: {e}")

    def change_admin_link(self, db: pyodbc.Connection, ano: str, new_alink: str):
        cl = 1
        try:
            dbtools.db_worker_admin_updatelink(db, cl, new_alink, ano)
            print("修改管理员联系方式成功")
        except Exception as e:
            print(f"修改管理员联系方式失败: {e}")


    ##################### 查询相关 ###################

    def list_all_maintainers(self, db: pyodbc.Connection) -> List[Maintainer]:
        '''
        获取所有维修员信息
        '''
        return dbtools.db_all_worker(db)

    def get_maintainer_by_id(self, db: pyodbc.Connection, mno: str) -> Optional[Maintainer]:

        return dbtools.db_worker_by_id(db, mno)

    def list_all_students(self, db: pyodbc.Connection) -> List[Student]:
        return dbtools.db_all_student(db)

    def get_student_by_id(self, db: pyodbc.Connection, sno: str) -> Optional[Student]:
        return dbtools.db_student_by_id(db, sno)

    def list_all_admins(self, db: pyodbc.Connection) -> List[Administrator]:
        try:
            cursor = db.cursor()
            sql = "SELECT ano,aname,apwd,alink FROM ADMINISTRATOR"
            cursor.execute(sql)
            results = cursor.fetchall()

            admins = []
            for row in results:
                admin = Administrator(ano=row[0], aname=row[1], apwd=row[2], alink=row[3])
                admins.append(admin)
            return admins
        except Exception as e:
            print("获取管理员列表失败", e)
            return []

    def get_admin_by_id(self, db: pyodbc.Connection, ano: str) -> Optional[Administrator]:
        return dbtools.db_admin_by_id(db, ano)

    def get_worker_score(self, db: pyodbc.Connection) -> List[Tuple[str, int, int, str, int, int, int]]:
        """
        查询维修工积分统计视图
        :param db: 数据库连接
        :return: 返回一个列表，包含元组(工号, 年份, 月份, 月份名称, 总积分, 维修单数, 平均积分)
        """
        return dbtools.db_worker_scores(db)

    def get_income_by_month(self, db: pyodbc.Connection) -> List[Tuple[int, int, int]]:
        """
        查询维修工积分统计视图
        :param db: 数据库连接
        :return: 返回一个列表，包含元组(年份，月份，总收入)
        """
        return dbtools.db_month_icome(db)


    ##################### 分类与订单 ###################

    def list_all_classify(self, db: pyodbc.Connection) -> List[Classify]:
        return dbtools.db_all_classify(db)

    def get_classify_frequency(self, db: pyodbc.Connection) -> List[Tuple[str, int]]:
        """
        查询维修统计视图
        :param db: 数据库连接
        :return: 返回一个列表，包含元组(维修类别编号, 保修次数)
        """
        return dbtools.db_class_frequency(db)

    def get_room_frequency(self, db: pyodbc.Connection) -> List[Tuple[str, int]]:
        '''
        查询宿舍统计视图
        :param db: 数据库连接
        :return: 返回一个列表，包含元组(宿舍编号, 宿舍次数)
        '''
        return dbtools.db_room_frequency(db)

    def list_all_orders(self, db: pyodbc.Connection) -> List[Order]:
        return dbtools.db_all_order(db)

    def change_order_score(self, db: pyodbc.Connection, ono: str, score: int, comment: str):
        '''
        修改订单评分
        :param db: 数据库连接
        :param ono: 订单编号
        :param score: 评分
        :param comment: 评价内容
        '''
        return dbtools.db_order_updatescore(db, score, comment, ono)

    def change_order_time(self, db: pyodbc.Connection, ono: str, new_time: str):
        '''
        :param db: 数据库连接
        :param ono: 订单编号
        :param new_time: 新的完成时间
        '''
        return dbtools.db_order_updatetime(db, new_time,ono)

    def change_order_status(self, db: pyodbc.Connection, ono: str, status: str):
        '''
        :param db: 数据库连接
        :param ono: 订单编号
        :param status: 新的订单状态
        '''
        return dbtools.db_order_updatestatus(db,status ,ono)

    ##################### 宿舍管理 ###################

    def list_all_rooms(self, db: pyodbc.Connection) -> List[Rooms]:
        '''
        获取所有宿舍信息
        :param db: 数据库连接
        :return: 宿舍列表
        '''
        try:
            cursor = db.cursor()
            sql = "SELECT rno,ano,address,assert FROM ROOMS"
            cursor.execute(sql)
            results = cursor.fetchall()

            rooms = []
            for row in results:
                room = Rooms(mo=row[0], ano=row[1], address=row[2], assert_=row[3])
                rooms.append(room)
            return rooms
        except Exception as e:
            print("获取宿舍列表失败", e)
            return []

    
    def add_room(self, db: pyodbc.Connection, rno: str, ano: str, address: str, assert_: str):
        '''
        添加宿舍
        :param db: 数据库连接
        :param rno: 宿舍编号
        :param ano: 管理员编号
        :param address: 宿舍地址
        :param assert_: 宿舍资产
        '''
        new_room = Rooms(mo=rno, ano=ano, address=address, assert_=assert_)
        try:
            dbtools.db_add_room(db, new_room)
            print("添加宿舍成功")
        except Exception as e:
            print(f"添加宿舍失败: {e}")

    def delete_room(self, db: pyodbc.Connection, rno: str):
        '''
        删除宿舍
        :param db: 数据库连接
        :param rno: 宿舍编号
        '''
        try:
            dbtools.db_del_room(db, rno)
            print("删除宿舍成功")
        except Exception as e:
            print(f"删除宿舍失败: {e}")


"""
AdminController 功能总结:
-----------------------
1. 用户管理 (14个方法)
   - 学生管理: 添加/删除/修改密码/宿舍/联系方式
   - 维修员管理: 添加/删除/修改密码/联系方式
   - 管理员管理: 添加/删除/修改密码/联系方式

2. 查询统计 (8个方法)
   - 获取所有/单个学生/维修员/管理员信息
   - 维修员积分统计
   - 月度收入统计

3. 分类与订单管理 (7个方法)
   - 维修类别管理
   - 订单管理: 获取所有订单/修改评分/完成时间/状态
   - 维修频率统计

4. 宿舍管理 (2个方法)
   - 获取所有宿舍信息
   - 添加宿舍
   - 删除宿舍
"""
