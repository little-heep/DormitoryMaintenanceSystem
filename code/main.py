from code.controllers.maintainer_controller import MaintenanceController
from code.models.structs import Maintainer
from code.tools.databasetools import db_init
from code.views.maintainer_ui import MaintenanceUI
import tkinter as tk

from code.views.register import RegisterPage

#测试编码
'''from code.tools.databasetools import (db_init)
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




#操作
# 创建控制器if __name__ == "__main__":
if __name__ == "__main__":
    db=db_init()
    #注册登录
    app=RegisterPage(db)
    app.run()

    db.close()
