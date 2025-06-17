import tkinter as tk
from tkinter import ttk, messagebox
from code.controllers.admincontroller import AdminController
from code.models.structs import Student, Maintainer, Administrator

class UserManagementWindow:
    def __init__(self, root, controller: AdminController, db):
        self.root = root
        self.controller = controller
        self.db = db
        self.root.title("用户管理")
        self.root.geometry("800x600")
        root.resizable(False, False) 
        self.root.configure(bg="#f0f8ff")
        
        self._setup_ui()

    def _setup_ui(self):
        """创建用户管理界面"""
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # 使用Notebook分页
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both")

        # 学生管理页
        self.student_frame = tk.Frame(self.notebook, bg="white")
        self._setup_student_ui()
        self.notebook.add(self.student_frame, text="学生管理")

        # 维修员管理页
        self.maintainer_frame = tk.Frame(self.notebook, bg="white")
        self._setup_maintainer_ui()
        self.notebook.add(self.maintainer_frame, text="维修员管理")

        # 管理员管理页
        self.admin_frame = tk.Frame(self.notebook, bg="white")
        self._setup_admin_ui()
        self.notebook.add(self.admin_frame, text="管理员管理")

    def _setup_student_ui(self):
        """学生管理页面"""
        # 顶部操作按钮
        btn_frame = tk.Frame(self.student_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame,
                 text="添加学生",
                 command=self._add_student,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="删除学生",
                 command=self._delete_student,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)


        tk.Button(btn_frame,
                 text="修改信息",
                 command=self._change_student_info,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        # 学生列表
        columns = ("学号", "姓名", "宿舍", "联系方式")
        self.student_tree = ttk.Treeview(
            self.student_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=150, anchor="center")

        self.student_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_student_list()

    def _setup_maintainer_ui(self):
        """维修员管理页面"""
        # 顶部操作按钮
        btn_frame = tk.Frame(self.maintainer_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame,
                 text="添加维修员",
                 command=self._add_maintainer,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="删除维修员",
                 command=self._delete_maintainer,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="修改信息",
                 command=self._change_maintainer_info,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        # 维修员列表
        columns = ("工号", "姓名", "联系方式", "总积分")
        self.maintainer_tree = ttk.Treeview(
            self.maintainer_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.maintainer_tree.heading(col, text=col)
            self.maintainer_tree.column(col, width=150, anchor="center")

        self.maintainer_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_maintainer_list()

    def _setup_admin_ui(self):
        """管理员管理页面"""
        # 顶部操作按钮
        btn_frame = tk.Frame(self.admin_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame,
                 text="添加管理员",
                 command=self._add_admin,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="删除管理员",
                 command=self._delete_admin,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="修改信息",
                 command=self._change_admin_info,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        # 管理员列表
        columns = ("管理员号", "姓名", "联系方式")
        self.admin_tree = ttk.Treeview(
            self.admin_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.admin_tree.heading(col, text=col)
            self.admin_tree.column(col, width=150, anchor="center")

        self.admin_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_admin_list()

    def _refresh_student_list(self):
        """刷新学生列表"""
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        students = self.controller.list_all_students(self.db)
        for student in students:
            self.student_tree.insert("", "end", values=(
                student.sno,    # 学号
                student.sname,  # 姓名
                student.rno,  # 宿舍
                student.slink  # 联系方式
            ))

    def _refresh_maintainer_list(self):
        """刷新维修员列表"""
        for item in self.maintainer_tree.get_children():
            self.maintainer_tree.delete(item)
        
        maintainers = self.controller.list_all_maintainers(self.db)
        for maintainer in maintainers:
            self.maintainer_tree.insert("", "end", values=(
                maintainer.mno,
                maintainer.mname,
                maintainer.mlink,
                maintainer.allscore
            ))

    def _refresh_admin_list(self):
        """刷新管理员列表"""
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)
        
        admins = self.controller.list_all_admins(self.db)
        for admin in admins:
            self.admin_tree.insert("", "end", values=(
                admin.ano,
                admin.aname,
                admin.alink
            ))

    def _add_student(self):
        """添加学生对话框
        功能：弹出对话框收集学生信息并添加到数据库
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("添加学生")
        dialog.geometry("400x600")
        dialog.configure(bg="#f0f8ff")
        dialog.resizable(False, False)

        form_frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        tk.Label(form_frame, 
                text="添加新学生",
                font=("Microsoft YaHei", 14, "bold"),
                bg="white").pack(pady=10)

        # 学号
        tk.Label(form_frame, text="学号:", bg="white").pack(anchor="w")
        sno_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=sno_var).pack(fill="x", pady=5)

        # 姓名
        tk.Label(form_frame, text="姓名:", bg="white").pack(anchor="w")
        sname_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=sname_var).pack(fill="x", pady=5)

        # 密码
        tk.Label(form_frame, text="密码:", bg="white").pack(anchor="w")
        spwd_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=spwd_var, show="*").pack(fill="x", pady=5)

        #宿舍
        tk.Label(form_frame, text="宿舍:", bg="white").pack(anchor="w")
        mo_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=mo_var).pack(fill="x", pady=5)

        # 联系方式
        tk.Label(form_frame, text="联系方式:", bg="white").pack(anchor="w")
        slink_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=slink_var).pack(fill="x", pady=5)

        def save_student():
            """保存学生信息到数据库"""
            if self.controller.add_student(
                    self.db,
                    sno_var.get(),
                    mo_var.get(),
                    sname_var.get(),
                    spwd_var.get(),
                    slink_var.get()
            ):
                messagebox.showinfo("成功", "学生添加成功")
                self._refresh_student_list()
                dialog.destroy()
            else:
                messagebox.showerror("错误", f"添加失败: {str()}")


        tk.Button(form_frame,
                text="保存",
                command=save_student,
                bg="#3C873D",
                fg="white",
                padx=20).pack(pady=20)

    def _delete_student(self):
        """删除学生
        功能：删除选中的学生记录
        """
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的学生")
            return
        
        sno = self.student_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("确认", f"确定要删除学号为 {sno} 的学生吗？"):
            if  self.controller.delete_student(self.db, sno):
                messagebox.showinfo("成功", "学生删除成功")
                self._refresh_student_list()
            else:
                messagebox.showerror("错误", f"删除失败: {str}")

    def _add_maintainer(self):
        """添加维修员对话框
        功能：弹出对话框收集维修员信息并添加到数据库
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("添加维修员")
        dialog.geometry("400x600")
        dialog.configure(bg="#f0f8ff")
        dialog.resizable(False, False)

        form_frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        tk.Label(form_frame, 
                text="添加新维修员",
                font=("Microsoft YaHei", 14, "bold"),
                bg="white").pack(pady=10)

        # 工号
        tk.Label(form_frame, text="工号:", bg="white").pack(anchor="w")
        mno_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=mno_var).pack(fill="x", pady=5)

        # 姓名
        tk.Label(form_frame, text="姓名:", bg="white").pack(anchor="w")
        mname_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=mname_var).pack(fill="x", pady=5)

        # 密码
        tk.Label(form_frame, text="密码:", bg="white").pack(anchor="w")
        mpwd_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=mpwd_var, show="*").pack(fill="x", pady=5)

        # 联系方式
        tk.Label(form_frame, text="联系方式:", bg="white").pack(anchor="w")
        mlink_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=mlink_var).pack(fill="x", pady=5)

        def save_maintainer():
            """保存维修员信息到数据库"""

            if self.controller.add_maintainer(
                    self.db,
                    mno_var.get(),
                    mname_var.get(),
                    mpwd_var.get(),
                    mlink_var.get()
                ):
                messagebox.showinfo("成功", "维修员添加成功")
                self._refresh_maintainer_list()
                dialog.destroy()
            else:
                messagebox.showerror("错误", f"添加失败: {str()}")

            tk.Button(form_frame,
                      text="保存",
                      command=save_maintainer,
                      bg="#3C873D",
                      fg="white",
                      padx=20).pack(pady=20)

        tk.Button(form_frame,
              text="保存",
              command=save_maintainer,
              bg="#3C873D",
              fg="white",
              padx=20).pack(pady=20)
    def _delete_maintainer(self):
        """删除维修员
        功能：删除选中的维修员记录
        """
        selected = self.maintainer_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的维修员")
            return
        
        mno = self.maintainer_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("确认", f"确定要删除工号为 {mno} 的维修员吗？"):
            if self.controller.delete_maintainer(self.db, mno):
                messagebox.showinfo("成功", "维修员删除成功")
                self._refresh_maintainer_list()
            else:
                messagebox.showerror("错误", f"删除失败: {str}")

    def _add_admin(self):
        """添加管理员对话框
        功能：弹出对话框收集管理员信息并添加到数据库
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("添加管理员")
        dialog.geometry("400x600")
        dialog.configure(bg="#f0f8ff")
        dialog.resizable(False, False)

        form_frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        tk.Label(form_frame, 
                text="添加新管理员",
                font=("Microsoft YaHei", 14, "bold"),
                bg="white").pack(pady=10)

        # 管理员号
        tk.Label(form_frame, text="管理员号:", bg="white").pack(anchor="w")
        ano_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=ano_var).pack(fill="x", pady=5)

        # 姓名
        tk.Label(form_frame, text="姓名:", bg="white").pack(anchor="w")
        aname_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=aname_var).pack(fill="x", pady=5)

        # 密码
        tk.Label(form_frame, text="密码:", bg="white").pack(anchor="w")
        apwd_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=apwd_var, show="*").pack(fill="x", pady=5)

        # 联系方式
        tk.Label(form_frame, text="联系方式:", bg="white").pack(anchor="w")
        alink_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=alink_var).pack(fill="x", pady=5)

        def save_admin():
            """保存管理员信息到数据库"""
            if self.controller.add_administor(
                    self.db,
                    ano_var.get(),
                    aname_var.get(),
                    apwd_var.get(),
                    alink_var.get()
            ):
                messagebox.showinfo("成功", "管理员添加成功")
                self._refresh_admin_list()
                dialog.destroy()
            else:
                messagebox.showerror("错误", f"添加失败: {str}")

        tk.Button(form_frame,
                  text="保存",
                  command=save_admin,
                  bg="#3C873D",
                  fg="white",
                  padx=20).pack(pady=20)

    def _delete_admin(self):
        """删除管理员
        功能：删除选中的管理员记录
        """
        selected = self.admin_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的管理员")
            return
        
        ano = self.admin_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("确认", f"确定要删除管理员号为 {ano} 的管理员吗？"):
            if self.controller.delete_administor(self.db, ano):
                messagebox.showinfo("成功", "管理员删除成功")
                self._refresh_admin_list()
            else:
                messagebox.showerror("错误", f"删除失败: {str}")

    
    def _change_student_info(self):
        """修改学生信息对话框
        功能：弹出对话框收集修改学生信息并更新数据库
        """
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的学生")
            return
        
        sno = self.student_tree.item(selected[0])["values"][0]
        student = self.controller.get_student_by_id(self.db, sno)

        dialog = tk.Toplevel(self.root)
        dialog.title("修改学生信息")
        dialog.geometry("400x400")
        dialog.configure(bg="#f0f8ff")
        dialog.resizable(False, False)

        form_frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        tk.Label(form_frame, 
                text="修改学生信息",
                font=("Microsoft YaHei", 14, "bold"),
                bg="white").pack(pady=10)

        # 学号
        tk.Label(form_frame, text="密码:", bg="white").pack(anchor="w")
        spwd_var = tk.StringVar(value=student.spwd)
        tk.Entry(form_frame, textvariable=spwd_var, show="*").pack(fill="x", pady=5)

        # 宿舍
        tk.Label(form_frame, text="宿舍:", bg="white").pack(anchor="w")
        mo_var = tk.StringVar(value=student.mo)
        tk.Entry(form_frame, textvariable=mo_var).pack(fill="x", pady=5)

        # 联系方式
        tk.Label(form_frame, text="联系方式:", bg="white").pack(anchor="w")
        slink_var = tk.StringVar(value=student.slink)
        tk.Entry(form_frame, textvariable=slink_var).pack(fill="x", pady=5)

        def save_student():
            """保存修改后的学生信息到数据库"""
            try:
                if spwd_var.get():
                    self.controller.change_student_pwd(self.db, sno, spwd_var.get())
                if mo_var.get():
                    self.controller.change_student_room(self.db, sno, mo_var.get())
                if slink_var.get():
                    self.controller.change_student_slink(self.db, sno, slink_var.get())
            except Exception as e:
                messagebox.showerror("错误", f"修改失败: {str(e)}")
            else:
                messagebox.showinfo("成功", "学生信息修改成功")
                self._refresh_student_list()
                dialog.destroy()

        tk.Button(form_frame,
                text="保存",
                command=save_student,
                bg="#3C873D",
                fg="white",
                padx=20).pack(pady=20)

    def _change_maintainer_info(self):
        """修改维修员信息对话框
        功能：弹出对话框收集修改维修员信息并更新数据库
        """
        selected = self.maintainer_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的维修员")
            return
        
        mno = self.maintainer_tree.item(selected[0])["values"][0]
        maintainer = self.controller.get_maintainer_by_id(self.db, mno)

        dialog = tk.Toplevel(self.root)
        dialog.title("修改维修员信息")
        dialog.geometry("400x400")
        dialog.configure(bg="#f0f8ff")
        dialog.resizable(False, False)

        form_frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        tk.Label(form_frame, 
                text="修改维修员信息",
                font=("Microsoft YaHei", 14, "bold"),
                bg="white").pack(pady=10)

        # 密码
        tk.Label(form_frame, text="密码:", bg="white").pack(anchor="w")
        mpwd_var = tk.StringVar(value=maintainer.mpwd)
        tk.Entry(form_frame, textvariable=mpwd_var, show="*").pack(fill="x", pady=5)

        # 联系方式
        tk.Label(form_frame, text="联系方式:", bg="white").pack(anchor="w")
        mlink_var = tk.StringVar(value=maintainer.mlink)
        tk.Entry(form_frame, textvariable=mlink_var).pack(fill="x", pady=5)


        def save_maintainer():
            """保存修改后的维修员信息到数据库"""
            try:
                if mpwd_var.get():
                    self.controller.change_maintainer_pwd(self.db, mno, mpwd_var.get())
                if mlink_var.get():
                    self.controller.change_maintainer_link(self.db, mno, mlink_var.get())
            except Exception as e:
                messagebox.showerror("错误", f"修改失败: {str(e)}")
            else:
                messagebox.showinfo("成功", "维修员信息修改成功")
                self._refresh_maintainer_list()
                dialog.destroy()

        tk.Button(form_frame,
                text="保存",
                command=save_maintainer,
                bg="#3C873D",
                fg="white",
                padx=20).pack(pady=20)

    def _change_admin_info(self):
        """修改管理员信息对话框
        功能：弹出对话框收集修改管理员信息并更新数据库
        """
        selected = self.admin_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的管理员")
            return
        
        ano = self.admin_tree.item(selected[0])["values"][0]
        admin = self.controller.get_admin_by_id(self.db, ano)

        dialog = tk.Toplevel(self.root)
        dialog.title("修改管理员信息")
        dialog.geometry("400x400")
        dialog.configure(bg="#f0f8ff")
        dialog.resizable(False, False)

        form_frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        tk.Label(form_frame, 
                text="修改管理员信息",
                font=("Microsoft YaHei", 14, "bold"),
                bg="white").pack(pady=10)

        # 密码
        tk.Label(form_frame, text="密码:", bg="white").pack(anchor="w")
        apwd_var = tk.StringVar(value=admin.apwd)
        tk.Entry(form_frame, textvariable=apwd_var, show="*").pack(fill="x", pady=5)

        # 联系方式
        tk.Label(form_frame, text="联系方式:", bg="white").pack(anchor="w")
        alink_var = tk.StringVar(value=admin.alink)
        tk.Entry(form_frame, textvariable=alink_var).pack(fill="x", pady=5)

        def save_admin():
            """保存修改后的管理员信息到数据库"""
            try:
                if apwd_var.get():
                    self.controller.change_admin_pwd(self.db, ano, apwd_var.get())
                if alink_var.get():
                    self.controller.change_admin_link(self.db, ano, alink_var.get())
            except Exception as e:
                messagebox.showerror("错误", f"修改失败: {str(e)}")
            else:
                messagebox.showinfo("成功", "管理员信息修改成功")
                self._refresh_admin_list()
                dialog.destroy()

        tk.Button(form_frame,
                text="保存",
                command=save_admin,
                bg="#3C873D",
                fg="white",
                padx=20).pack(pady=20)


