from code.controllers.maintainer_controller import MaintenanceController
from code.models.structs import Maintainer
from code.tools.databasetools import db_init
from code.views.maintainer_ui import MaintenanceUI
import tkinter as tk

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


    # 测试代码
    #如果判断是维修工登录成功，创建维修工ui界面，创建代码如下,不需要的话记得注释掉，不要影响测试
    root = tk.Tk()
    current_maintainer = Maintainer(
        mno="201002",
        mname="黄钟",
        mpwd="zhong122",
        mlink="12345678102",
        allscore=6
    )
    # 创建控制器实例
    controller = MaintenanceController(current_maintainer,db)
    # 创建UI实例
    app = MaintenanceUI(root, controller)
    root.mainloop()



    db.close()
