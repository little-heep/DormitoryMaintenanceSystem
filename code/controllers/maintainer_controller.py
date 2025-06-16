from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List
from enum import Enum
import pyodbc

from code.models.structs import Maintainer, Order
from code.tools.databasetools import (db_all_order, db_order_updatestatus,db_order_updatetime,
                                      db_worker_admin_updatelink,db_worker_admin_updatepwd)


class OrderStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    TALKED = 3

class MaintenanceController:
    def __init__(self, current_maintainer: Maintainer,db_connection: pyodbc.Connection=None):
        """
        初始化控制器

        :param db_connection: 数据库连接对象
        :param current_maintainer: 当前登录的维修员对象
        """
        self.db_conn = db_connection
        self.current_maintainer = current_maintainer

    def get_orders(self) -> Dict[str, List[Order]]:
        """
        获取当前维修员的所有订单，按状态分类

        :return: 包含'pending'和'completed'两个键的字典，分别对应未完成和已完成订单列表
        """

        orders = {
            'pending': [],
            'completed': []
        }

        for row in db_all_order(self.db_conn):
            if row.mno==self.current_maintainer.mno:
                if row.status==1:
                    orders['pending'].append(row)
                else:
                    orders['completed'].append(row)

        return orders

    def complete_order(self, ono: int) -> bool:
        """
        标记订单为已完成

        :param ono: 订单编号
        :return: 是否成功
        """

        rescode,_=db_order_updatestatus(self.db_conn,2,ono)
        if rescode==2 and db_order_updatetime(self.db_conn,datetime.now(),ono):
            return True
        else:
            return False

    def update_maintainer_link(self,newlink):
        if db_worker_admin_updatelink(self.db_conn,0,newlink,self.current_maintainer.mno):
            return True
        else :
            return  False

    def update_maintainer_pwd(self,newpwd):
        if db_worker_admin_updatepwd(self.db_conn,0,newpwd,self.current_maintainer.mno):
            return True
        else:
            return False

