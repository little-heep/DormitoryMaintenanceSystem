from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Administrator:
    """管理员表结构体"""
    ano: str       # 管理员编号 (PK)
    aname: str     # 管理员姓名
    apwd: str      # 管理员密码
    alink: str     # 管理员联系方式

@dataclass
class Classify:
    """分类表结构体"""
    cno: str       # 分类编号 (PK)
    class_: str    # 分类类别 (使用class_避免与Python关键字冲突)
    content: str   # 分类内容
    pay: int       # 支付金额

@dataclass
class Maintainer:
    """维护人员表结构体"""
    mno: str       # 维护人员编号 (PK)
    mname: str     # 维护人员姓名
    mpwd: str      # 维护人员密码
    mlink: str     # 维护人员联系方式
    allscore: int  # 总评分

@dataclass
class Order:
    """订单表结构体"""
    ono: int              # 订单编号 (PK) 数据库中是自增的新增订单时不需要考虑这个值
    sno: str               # 学生编号 (FK)
    mno: str               # 维护人员编号 (FK)
    cno: str               # 分类编号 (FK)
    mo: str                # 房间编号 (FK)
    status: int            # 订单状态
    ocontent: str          # 订单内容
    starttime: datetime    # 开始时间
    finishtime: Optional[datetime] == None  # 完成时间（可为空）
    comment: Optional[str] == None          # 评价内容（可为空）
    score: int             # 评分

@dataclass
class Rooms:
    """房间表结构体"""
    mo: str                # 房间编号 (PK)
    ano: Optional[str]     # 管理员编号 (FK, 可为空）
    address: str           # 房间地址
    assert_: str           # 房间资产（使用assert_避免与Python关键字冲突）

@dataclass
class Student:
    """学生表结构体"""
    sno: str           # 学号 (PK, 8位字符)
    mo: Optional[str]  # 房间号 (FK, 可为空)
    sname: str         # 学生姓名
    spwd: str          # 学生密码
    slink: str         # 学生联系方式

'''
创建结构体方法
from dataclasses import dataclass  导包
admin = Administrator(
    ano="A001",
    aname="张三",
    apwd="password123",
    alink="13800138000"
)
创建好了一个管理员结构体 admin.ano调用属性
'''