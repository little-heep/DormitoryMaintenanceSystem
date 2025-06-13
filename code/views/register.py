import tkinter as tk
from tkinter import messagebox
from code.views.login import LoginApp
from code.models.structs import *
from code.tools.databasetools import *

class RegisterPage:
    def __init__(self,db):
        self.root = tk.Tk()
        self.root.title("维修系统 - 注册")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self._setup_ui()

        # 初始化数据库连接
        self.conn = db

    def _setup_ui(self):
        """创建注册界面控件"""
        # 设置主窗口背景色 - 改为更柔和的蓝色背景
        self.root.configure(bg="#e6f2ff")

        # 主框架 - 改为白色背景，增加圆角边框
        main_frame = tk.Frame(self.root, bg="white", padx=20, pady=20,
                              relief="groove", bd=2)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # 标题 - 改为深蓝色
        tk.Label(main_frame, text="宿舍维修系统注册",
                 font=("Microsoft YaHei", 16, "bold"),
                 bg="white", fg="#1a5fb4").grid(row=0, column=0, pady=(0, 20), columnspan=2)

        # 身份选择
        tk.Label(main_frame, text="身份:",
                 font=("Microsoft YaHei", 10),
                 bg="white", fg="#555").grid(row=1, column=0, sticky="w", pady=(0, 5))

        self.role_var = tk.StringVar(value="学生")  # 默认值
        roles = ["学生", "维修工", "管理员"]

        # 美化下拉菜单
        role_menu = tk.OptionMenu(main_frame, self.role_var, *roles, command=self.toggle_dormitory_field)
        role_menu.config(font=("Microsoft YaHei", 10),
                         bg="white", fg="#333",
                         relief="solid", bd=1,
                         highlightthickness=0,
                         activebackground="#e6f2ff",
                         activeforeground="#1a5fb4")
        role_menu["menu"].config(bg="white", fg="#333",
                                 activebackground="#e6f2ff",
                                 activeforeground="#1a5fb4",
                                 font=("Microsoft YaHei", 10))
        role_menu.grid(row=1, column=1, sticky="ew", pady=(0, 15))

        # 账号
        tk.Label(main_frame, text="账号:",
                 font=("Microsoft YaHei", 10),
                 bg="white", fg="#555").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.entry_username = self.create_entry(main_frame)
        self.entry_username.grid(row=2, column=1, ipady=5, ipadx=10, pady=(0, 15), sticky="ew")

        # 姓名
        tk.Label(main_frame, text="姓名:",
                 font=("Microsoft YaHei", 10),
                 bg="white", fg="#555").grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.entry_name = self.create_entry(main_frame)
        self.entry_name.grid(row=3, column=1, ipady=5, ipadx=10, pady=(0, 15), sticky="ew")

        # 密码
        tk.Label(main_frame, text="密码:",
                 font=("Microsoft YaHei", 10),
                 bg="white", fg="#555").grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.entry_password = self.create_entry(main_frame,show="*")
        self.entry_password.grid(row=4, column=1, ipady=5, ipadx=10, pady=(0, 15), sticky="ew")

        # 确认密码
        tk.Label(main_frame, text="确认密码:",
                 font=("Microsoft YaHei", 10),
                 bg="white", fg="#555").grid(row=5, column=0, sticky="w", pady=(0, 5))
        self.entry_confirm_password = self.create_entry(main_frame,show="*")
        self.entry_confirm_password.grid(row=5, column=1, ipady=5, ipadx=10, pady=(0, 15), sticky="ew")

        # 联系方式
        tk.Label(main_frame, text="联系方式:",
                 font=("Microsoft YaHei", 10),
                 bg="white", fg="#555").grid(row=6, column=0, sticky="w", pady=(0, 5))
        self.entry_contact = self.create_entry(main_frame)
        self.entry_contact.grid(row=6, column=1, ipady=5, ipadx=10, pady=(0, 15), sticky="ew")

        # 宿舍号 (初始显示)
        self.dorm_label = tk.Label(main_frame, text="宿舍号:",
                                   font=("Microsoft YaHei", 10),
                                   bg="white", fg="#555")
        self.dorm_label.grid(row=7, column=0, sticky="w", pady=(0, 5))

        self.entry_dormitory = self.create_entry(main_frame)
        self.entry_dormitory.grid(row=7, column=1, ipady=5, ipadx=10, pady=(0, 20), sticky="ew")

        # 注册按钮 - 改为蓝色按钮
        register_btn = tk.Button(main_frame, text="注册", command=self.register_user,
                                 font=("Microsoft YaHei", 10, "bold"),
                                 bg="#3C873D", fg="white",
                                 activebackground="#0d4b8c",
                                 activeforeground="white",
                                 relief="flat",
                                 padx=20, pady=5)
        register_btn.grid(row=8, column=0, columnspan=2, pady=(0, 10))

        # 返回登录
        back_frame = tk.Frame(main_frame, bg="white")
        back_frame.grid(row=9, column=0, columnspan=2)

        tk.Label(back_frame, text="已有账号？",
                 font=("Microsoft YaHei", 9),
                 bg="white", fg="#777").pack(side="left")
        login_link = tk.Label(back_frame, text="返回登录",
                              font=("Microsoft YaHei", 9, "underline"),
                              bg="white", fg="#1a5fb4", cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.return_to_login())

        # 调整列权重使内容居中
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def create_entry(self, parent,show=None):
        """创建统一风格的输入框"""
        entry = tk.Entry(parent,
                         font=("Microsoft YaHei", 10),
                         bd=1, relief="solid",
                         highlightthickness=1,
                         highlightcolor="#1a5fb4",
                         highlightbackground="#ddd",
                         show=show)
        return entry

    def toggle_dormitory_field(self, role):
        """根据选择的身份显示/隐藏宿舍号字段"""
        if role == "学生":
            self.dorm_label.grid()
            self.entry_dormitory.grid()
        else:
            self.dorm_label.grid_remove()
            self.entry_dormitory.grid_remove()

    def register_user(self):
        role = self.role_var.get()
        """注册用户逻辑"""
        if role == "学生":
            stu = Student(
            sno=self.entry_username.get().strip(),  # 学号 (PK, 8位字符)
            mo=self.entry_dormitory.get().strip() if role == "学生" else "", # 房间号 (FK, 可为空)
            sname=self.entry_name.get().strip(),  # 学生姓名
            spwd=self.entry_password.get(), # 学生密码
            slink=self.entry_contact.get().strip() # 学生联系方式
            )
        elif role == "维修工":
            mai = Maintainer(
            mno=self.entry_username.get().strip(),  # 维护人员编号 (PK)
            mname= self.entry_name.get().strip(), # 维护人员姓名
            mpwd=self.entry_password.get(),  # 维护人员密码
            mlink= self.entry_contact.get().strip(), # 维护人员联系方式
            allscore=0 # 总评分
            )
        elif role == "管理员":
            adm = Administrator(
            ano=self.entry_username.get().strip(),   # 管理员编号 (PK)
            aname= self.entry_name.get().strip(),  # 管理员姓名
            apwd=self.entry_password.get(),  # 管理员密码
            alink= self.entry_contact.get().strip()  # 管理员联系方式
            )

        # 获取表单数据
        username = self.entry_username.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        contact = self.entry_contact.get().strip()
        role = self.role_var.get()
        dormitory = self.entry_dormitory.get().strip() if role == "学生" else ""

        # 验证表单
        if not all([username, name, password, confirm_password, contact]):
            messagebox.showerror("错误", "请填写所有必填字段！")
            return

        if password != confirm_password:
            messagebox.showerror("错误", "两次输入的密码不一致！")
            return

        if role == "学生" and not dormitory:
            messagebox.showerror("错误", "请填写宿舍号！")
            return

        # 保存到数据库
        if role == "学生":
            code,_=db_add_student(self.conn,stu)
            if code == 1:
                messagebox.showinfo("注册成功","欢迎登录")
            else:
                messagebox.showinfo("注册失败")
        elif role == "管理员":
            code, _ = db_add_administor(self.conn, adm)
            if code == 1:
                messagebox.showinfo("注册成功", "欢迎登录")
            else:
                messagebox.showinfo("注册失败")
        elif role == "维修工":
            code, _ = db_add_maintainer(self.conn, mai)
            if code == 1:
                messagebox.showinfo("注册成功", "欢迎登录")
            else:
                messagebox.showinfo("注册失败")



    def return_to_login(self):
        self.root.destroy()  # 销毁主窗口
        LoginApp(self.conn)

    def run(self):
        """启动应用"""
        self.root.mainloop()

