import tkinter as tk
from tkinter import messagebox
import pyodbc
from code.tools import databasetools as db
import code.views.maintainer_ui
from code.controllers.maintainer_controller import MaintenanceController
from code.models.structs import Maintainer
from code.views.maintainer_ui import MaintenanceUI


class LoginApp:
    def __init__(self,db):
        self.root = tk.Tk()
        self.root.title("宿舍维修管理系统")
        self.root.geometry("400x500")
        self.cnn=db

        # 初始化控件
        self._setup_ui()

    def _setup_ui(self):
        """创建美观的登录界面控件"""
        # 设置主窗口样式
        self.root.configure(bg="#f0f8ff")  # 浅蓝色背景

        # 主框架（增加内边距和阴影效果）
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove", padx=30, pady=30)
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # 标题样式
        tk.Label(main_frame,
                 text="宿舍维修系统登录",
                 font=("Microsoft YaHei", 18, "bold"),
                 bg="white",
                 fg="#4169E1").pack(pady=(0, 25))

        # 账号输入框
        tk.Label(main_frame,
                 text="账号:",
                 font=("Microsoft YaHei", 10),
                 bg="white",
                 fg="#555").pack(anchor="w", pady=(5, 0))

        self.entry_username = tk.Entry(main_frame,
                                       font=("Microsoft YaHei", 10),
                                       bd=1,
                                       relief="solid",
                                       highlightthickness=1,
                                       highlightcolor="#4169E1",
                                       highlightbackground="#ddd")
        self.entry_username.pack(fill="x", pady=(0, 15))

        # 密码输入框
        tk.Label(main_frame,
                 text="密码:",
                 font=("Microsoft YaHei", 10),
                 bg="white",
                 fg="#555").pack(anchor="w", pady=(5, 0))

        self.entry_password = tk.Entry(main_frame,
                                       show="*",
                                       font=("Microsoft YaHei", 10),
                                       bd=1,
                                       relief="solid",
                                       highlightthickness=1,
                                       highlightcolor="#4169E1",
                                       highlightbackground="#ddd")
        self.entry_password.pack(fill="x", pady=(0, 15))

        # 身份选择（美化后的下拉菜单）
        tk.Label(main_frame,
                 text="身份:",
                 font=("Microsoft YaHei", 10),
                 bg="white",
                 fg="#555").pack(anchor="w", pady=(5, 0))

        self.role_var = tk.StringVar(value="学生")

        # 创建自定义样式的OptionMenu
        role_menu = tk.OptionMenu(main_frame, self.role_var, "学生", "维修工", "管理员")
        role_menu.config(font=("Microsoft YaHei", 10),
                         bg="white",
                         fg="#333",
                         activebackground="#e6f2ff",
                         activeforeground="#4169E1",
                         relief="solid",
                         bd=1,
                         highlightthickness=0,
                         padx=8,
                         pady=3)
        role_menu["menu"].config(font=("Microsoft YaHei", 10),
                                 bg="white",
                                 fg="#333",
                                 activebackground="#e6f2ff",
                                 activeforeground="#4169E1",
                                 bd=0)
        role_menu.pack(fill="x", pady=(0, 25))

        # 登录按钮
        login_btn = tk.Button(main_frame,
                              text="登 录",
                              command=self.login_user,
                              font=("Microsoft YaHei", 12, "bold"),
                              bg="#3C873D",
                              fg="white",
                              activebackground="#3a5fcd",
                              activeforeground="white",
                              relief="flat",
                              bd=0,
                              padx=20,
                              pady=8,
                              cursor="hand2")
        login_btn.pack(fill="x", pady=(10, 0))

    def login_user(self):
        """处理登录逻辑"""
        user = self.entry_username.get().strip()
        pwd = self.entry_password.get().strip()
        role = self.role_var.get()

        # 验证输入是否为空
        if not user or not pwd:
            messagebox.showerror("错误", "用户名和密码不能为空！")
            self._clear_password()  # 清空密码框
            return

        table, user_col, pass_col = self._get_table_info(role)
        sql = f"SELECT * FROM {table} WHERE {user_col}=? AND {pass_col}=?"

        try:
            # 确保连接有效
            if not self.cnn:
                if not self.cnn:
                    messagebox.showerror("错误", "数据库连接失败，请稍后再试")
                    return

            cursor = self.cnn.cursor()
            cursor.execute(sql, (user, pwd))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("登录成功", f"欢迎 {role}：{user}")
                self.root.destroy()  # 关闭登录窗口
                self._open_role_ui(role, user)  # 打开对应角色的界面
            else:
                messagebox.showerror("登录失败", "用户名或密码错误！")
                self._clear_password()  # 清空密码框
                self.entry_username.delete(0,tk.END)
                self.entry_username.focus_set()  # 将焦点设置回用户名输入框

        except Exception as e:
            messagebox.showerror("系统错误", f"登录过程中发生错误:\n{str(e)}")
            self._clear_password()  # 清空密码框
        finally:
            # 注意：这里不应该关闭连接，因为可能在其他地方还要使用
            if 'cursor' in locals():
                cursor.close()

    def _clear_password(self):
        """清空密码输入框"""
        self.entry_password.delete(0, tk.END)

    def _get_table_info(self, role):
        """根据身份返回对应的表信息"""
        role_mapping = {
            "学生": ("STUDENT", "sno", "spwd"),
            "维修工": ("MAINTAINER", "mno", "mpwd"),
            "管理员": ("ADMINISTRATOR", "ano", "apwd")
        }
        return role_mapping.get(role, ("UNKNOWN", "", ""))

    def _open_role_ui(self, role, username):
        """跳转到对应身份的界面"""
        if role == "维修工":

                # 使用with语句自动管理连接

                    cursor = self.cnn.cursor()

                    # 更安全的参数化查询
                    cursor.execute("""
                            SELECT mno, mname, mpwd, mlink, allscore 
                            FROM MAINTAINER
                            WHERE mno=?
                        """, (username,))

                    result = cursor.fetchone()

                    if result:
                        # 使用列名访问更安全，不依赖字段顺序
                        current_maintainer = Maintainer(
                            mno=result[0],
                            mname=result[1],
                            mpwd=result[2],
                            mlink=result[3],
                            allscore=result[4]
                        )



                        # 创建新窗口
                        root = tk.Tk()
                        controller = MaintenanceController(current_maintainer, self.cnn)
                        app = MaintenanceUI(root, controller)
                        root.mainloop()
                    else:
                        messagebox.showerror("错误", "该维修工账号不存在")
        # if role == "维修工":
        #     root = tk.Tk()
        #     current_maintainer = Maintainer(
        #         mno=self.entry_username.get(),
        #         mname=,
        #         mpwd="zhong122",
        #         mlink="12345678102",
        #         allscore=6
        #     )
        #     # 创建控制器实例
        #     controller = MaintenanceController(current_maintainer, db)
        #     # 创建UI实例
        #     app = maintainer_ui.MaintenanceUI(root, controller)
        #     root.mainloop()
        # elif role == "学生":
        #     student_ui.open(username)
        # elif role == "管理员":
        #     admin_ui.open(username)




# 使用示例
if __name__ == "__main__":
    app = LoginApp()
    app.run()