
from code.tools.databasetools import (db_init)

#测试编码
'''
使用database的函数需要先导入，导包要在最上面
方法一：
    from code.tools.database import connect_db
    # 然后直接调用函数
    result = connect_db()
方法二：
    import code.tools.database as db
    # 使用模块别名调用函数
    connection = db.connect_db()
    data = db.query_data("SELECT * FROM users")
'''


db=db_init()

#操作

db.close()
