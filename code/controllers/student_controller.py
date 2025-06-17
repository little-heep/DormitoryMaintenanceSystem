# controller.py
import random
from datetime import datetime
from code.models.structs import Order
from code.tools.databasetools import db_add_order, db_student_by_id, db_student_update, db_all_order
from tkinter import messagebox


class StudentController:
    def __init__(self,db):
        self.db_conn = db

    #生成新订单
    def report_issue(self, student_id, dorm, content,cno):
        cursor = self.db_conn.cursor()
        print(student_id,dorm,content)
        print(type(student_id),type(dorm),type(content))

        # ---------- 校验宿舍号 ----------
        if not dorm or dorm.strip() == "":
            messagebox.showerror("错误", "宿舍号不能为空")
            return

        try:
            # ---------- 自动分配维修工 ----------
            cursor.execute("SELECT TOP 1 mno FROM MAINTAINER ORDER BY NEWID()")
            maintainer = cursor.fetchone()
            if not maintainer:
                messagebox.showerror("错误", "没有可用的维修工")
                return

            maintainer_id = maintainer[0]

            # ---------- 可选：宿舍号转类型 ----------
            # 如果数据库中 rno 是 INT 类型就取消注释
            # dorm = int(dorm)

            # ---------- 创建订单 ----------
            order = Order(
                ono=0,  # 自增主键
                sno=student_id,
                mno=maintainer_id,
                cno=cno,
                mo=dorm,
                status=1,
                ocontent=content,
                starttime=datetime.now(),
                finishtime=None,
                comment=None,
                score=0
            )

            # ---------- 添加订单到数据库 ----------
            success = db_add_order(self.db_conn, order)
            if success:
                messagebox.showinfo("成功", "报修订单已提交！")
                e="没问题"
                return success ,e
            else:
                messagebox.showerror("失败", "提交失败，请稍后再试。")

        except Exception as e:
            messagebox.showerror("异常", f"发生错误：{e}")
            print(f"[错误] 提交报修订单失败: {e}")
            return success,e
    #查询订单
    def query_orders(self,student_id):
        orders = db_all_order(self.db_conn)
        return orders
    #提交反馈

    def submit_feedback(self,order_id, rating, comment):
        cursor = self.db_conn .cursor()
        cursor.execute("UPDATE [ORDER] SET status = 3, score = ?, comment = ? WHERE ono = ?", (rating, comment, order_id))
        print(2)
        self.db_conn .commit()
        return True

    #获取个人信息
    # 在 StudentController 类中修改方法
    def get_personal_info(self, sno):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT sname, rno, slink FROM STUDENT WHERE sno=?", sno)
            result = cursor.fetchone()
            return result if result else ("未知", "未知", "未知")  # 确保返回可迭代对象
        except Exception as e:
            print("数据库查询失败:", e)
            return ("未知", "未知", "未知")  # 兜底返回值



