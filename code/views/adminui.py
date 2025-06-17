import tkinter as tk
from code.controllers.admincontroller import AdminController
import pyodbc
from code.views.adminview.main_window import AdminMainWindow
import code.tools.databasetools as dbtools

def admin_system(controller: AdminController, db: pyodbc.Connection):
    root = tk.Tk()
    app = AdminMainWindow(root, controller, db)
    root.mainloop()

    try:
        db.close()
    except:
        pass

if __name__ == '__main__':
    db=dbtools.db_init()
    controller = AdminController()
    admin_system(controller, db)