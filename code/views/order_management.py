import tkinter as tk
from tkinter import ttk, messagebox
from code.controllers.admincontroller import AdminController
from code.models.structs import Order

class OrderManagementWindow:
    def __init__(self, root, controller: AdminController, db):
        self.root = root
        self.controller = controller
        self.db = db
        self.root.title("订单管理")
        self.root.geometry("1000x600")
        root.resizable(False, False) 
        self.root.configure(bg="#f0f8ff")
        
        self._setup_ui()

    def _setup_ui(self):
        """创建订单管理界面"""
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # 顶部操作按钮
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame,
                 text="修改评分",
                 command=self._update_score,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="修改时间",
                 command=self._update_time,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        tk.Button(btn_frame,
                 text="修改状态",
                 command=self._update_status,
                 font=("Microsoft YaHei", 10),
                 bg="#3C873D",
                 fg="white").pack(side="left", padx=5)

        # 订单列表
        columns = ("订单号", "学生号", "维修类别", "报修时间", "完成时间", "状态", "评分", "评价")
        self.order_tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        for col in columns:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=120, anchor="center")

        self.order_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_order_list()

    def _refresh_order_list(self):
        """刷新订单列表"""
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        orders = self.controller.list_all_orders(self.db)
        for order in orders:
            self.order_tree.insert("", "end", values=(
                order.ono,
                order.sno,
                order.cno,
                order.starttime,
                order.finishtime,
                order.status,
                order.score,
                order.comment
            ))

    def _update_score(self):
        """修改订单评分"""
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的订单")
            return
        
        order_no = self.order_tree.item(selected[0])["values"][0]
        
        # 创建评分修改对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("修改订单评分")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, 
                text=f"修改订单 {order_no} 的评分",
                font=("Microsoft YaHei", 12)).pack(pady=20)
        
        tk.Label(dialog, text="评分(1-5):").pack()
        score_var = tk.StringVar()
        score_entry = tk.Entry(dialog, textvariable=score_var)
        score_entry.pack(pady=5)
        
        tk.Label(dialog, text="评价:").pack()
        comment_var = tk.StringVar()
        comment_entry = tk.Entry(dialog, textvariable=comment_var)
        comment_entry.pack(pady=5)
        
        def save_changes():
            try:
                score = int(score_var.get())
                if score < 1 or score > 5:
                    raise ValueError
                comment = comment_var.get()
                self.controller.change_order_score(self.db, order_no, score, comment)
                messagebox.showinfo("成功", "订单评分已更新")
                self._refresh_order_list()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "评分必须是1-5的整数")
        
        tk.Button(dialog,
                 text="保存",
                 command=save_changes,
                 bg="#3C873D",
                 fg="white").pack(pady=20)

    def _update_time(self):
        """修改订单完成时间"""
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的订单")
            return
        
        order_no = self.order_tree.item(selected[0])["values"][0]
        
        # 创建时间修改对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("修改完成时间")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        tk.Label(dialog, 
                text=f"修改订单 {order_no} 的完成时间",
                font=("Microsoft YaHei", 12)).pack(pady=20)
        
        tk.Label(dialog, text="完成时间(YYYY-MM-DD HH:MM:SS):").pack()
        time_var = tk.StringVar()
        time_entry = tk.Entry(dialog, textvariable=time_var)
        time_entry.pack(pady=5)
        
        def save_changes():
            new_time = time_var.get()
            try:
                self.controller.change_order_time(self.db, order_no, new_time)
                messagebox.showinfo("成功", "订单完成时间已更新")
                self._refresh_order_list()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"时间格式错误: {e}")
        
        tk.Button(dialog,
                 text="保存",
                 command=save_changes,
                 bg="#3C873D",
                 fg="white").pack(pady=20)

    def _update_status(self):
        """修改订单状态"""
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的订单")
            return
        
        order_no = self.order_tree.item(selected[0])["values"][0]
        current_status = self.order_tree.item(selected[0])["values"][5]
        
        # 创建状态修改对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("修改订单状态")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        tk.Label(dialog, 
                text=f"修改订单 {order_no} 的状态",
                font=("Microsoft YaHei", 12)).pack(pady=20)
        
        status_var = tk.StringVar(value=current_status)
        status_options = ["待处理", "处理中", "已完成", "已取消"]
        
        for status in status_options:
            tk.Radiobutton(dialog,
                          text=status,
                          variable=status_var,
                          value=status).pack(anchor="w")
        
        def save_changes():
            new_status = status_var.get()
            try:
                self.controller.change_order_status(self.db, order_no, new_status)
                messagebox.showinfo("成功", "订单状态已更新")
                self._refresh_order_list()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"状态更新失败: {e}")
        
        tk.Button(dialog,
                 text="保存",
                 command=save_changes,
                 bg="#3C873D",
                 fg="white").pack(pady=20)
