import tkinter as tk
from tkinter import ttk, messagebox
from code.controllers.admincontroller import AdminController
from code.models.structs import Rooms

class DormManagementWindow:
    def __init__(self, root, controller: AdminController, db):
        self.root = root
        self.controller = controller
        self.db = db
        self.root.title("宿舍管理")
        self.root.geometry("800x500")
        root.resizable(False, False) 
        self.root.configure(bg="#f0f8ff")
        
        self._setup_ui()

    def _setup_ui(self):
        """创建宿舍管理界面"""
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # 顶部操作按钮
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame,
                 text="添加宿舍",
                 command=self._add_dorm,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="删除宿舍",
                 command=self._delete_dorm,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        # 宿舍列表
        columns = ("宿舍编号", "管理员编号", "地址", "资产")
        self.dorm_tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.dorm_tree.heading(col, text=col)
            self.dorm_tree.column(col, width=150, anchor="center")

        self.dorm_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_dorm_list()

    def _refresh_dorm_list(self):
        """刷新宿舍列表"""
        for item in self.dorm_tree.get_children():
            self.dorm_tree.delete(item)
        
        # 模拟宿舍数据 - 实际应从数据库获取
        rooms = self.controller.list_all_rooms(self.db)
        
        for room in rooms:
            self.dorm_tree.insert("", "end", values=(room.mo,room.ano, room.address, room.assert_))

    def _add_dorm(self):
        """添加宿舍对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加宿舍")
        dialog.geometry("400x600")
        dialog.resizable(False, False)
        
        tk.Label(dialog, 
                text="添加新宿舍信息",
                font=("Microsoft YaHei", 12)).pack(pady=10)

        # 宿舍编号
        tk.Label(dialog, text="宿舍编号:").pack()
        mo_var = tk.StringVar()
        tk.Entry(dialog, textvariable=mo_var).pack(pady=5)

        # 管理员编号
        tk.Label(dialog, text="管理员编号:").pack()
        ano_var = tk.StringVar()
        tk.Entry(dialog, textvariable=ano_var).pack(pady=5)

        # 地址
        tk.Label(dialog, text="地址:").pack()
        address_var = tk.StringVar()
        tk.Entry(dialog, textvariable=address_var).pack(pady=5)

        # 资产
        tk.Label(dialog, text="资产:").pack()
        assert_var = tk.StringVar()
        tk.Entry(dialog, textvariable=assert_var).pack(pady=5)

        def save_dorm():
            try:
                new_room = Rooms(
                    mo=mo_var.get(),
                    ano=ano_var.get(),
                    address=address_var.get(),
                    assert_=assert_var.get()
                )
                self.controller.add_room(self.db, new_room.mo, new_room.ano, 
                                       new_room.address, new_room.assert_)
                messagebox.showinfo("成功", "宿舍添加成功")
                self._refresh_dorm_list()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加宿舍失败: {e}")

        tk.Button(dialog,
                 text="保存",
                 command=save_dorm,
                 bg="#3C873D",
                 fg="white").pack(pady=20)

    def _delete_dorm(self):
        """删除宿舍"""
        selected = self.dorm_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的宿舍")
            return
        
        mo = self.dorm_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("确认", f"确定要删除宿舍 {mo} 吗？"):
            try:
                self.controller.delete_room(self.db, mo)
                messagebox.showinfo("成功", "宿舍删除成功")
                self._refresh_dorm_list()
            except Exception as e:
                messagebox.showerror("错误", f"删除宿舍失败: {e}")
