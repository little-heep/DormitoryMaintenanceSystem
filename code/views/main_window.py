import tkinter as tk
from tkinter import ttk
from code.controllers.admincontroller import AdminController
import code.tools.databasetools as dbtools


class AdminMainWindow:
    def __init__(self, root, controller: AdminController, db):
        self.root = root
        self.controller = controller
        self.db = db
        self.root.title("宿舍维修管理系统 - 管理员")
        self.root.geometry("600x600")
        root.resizable(False, False) 
        self.root.configure(bg="#f0f8ff")
        
        # 跟踪子窗口状态
        self.current_child_window = None
        
        self._setup_ui()

    def _setup_ui(self):
        """创建主界面UI"""
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # 标题
        tk.Label(main_frame,
                text="管理员功能菜单",
                font=("Microsoft YaHei", 18, "bold"),
                bg="white",
                fg="#4169E1").pack(pady=(0, 30))

        # 功能按钮框架
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x")

        # 用户管理按钮
        user_btn = tk.Button(btn_frame,
                            text="用户管理",
                            command=self.open_user_management,
                            font=("Microsoft YaHei", 12),
                            bg="#3C873D",
                            fg="white",
                            activebackground="#3a5fcd",
                            relief="flat",
                            padx=20,
                            pady=10,
                            cursor="hand2")
        user_btn.pack(fill="x", pady=5)

        # 查询统计按钮
        stats_btn = tk.Button(btn_frame,
                            text="查询统计",
                            command=self.open_query_stats,
                            font=("Microsoft YaHei", 12),
                            bg="#3C873D",
                            fg="white",
                            activebackground="#3a5fcd",
                            relief="flat",
                            padx=20,
                            pady=10,
                            cursor="hand2")
        stats_btn.pack(fill="x", pady=5)

        # 订单管理按钮
        order_btn = tk.Button(btn_frame,
                            text="订单管理",
                            command=self.open_order_management,
                            font=("Microsoft YaHei", 12),
                            bg="#3C873D",
                            fg="white",
                            activebackground="#3a5fcd",
                            relief="flat",
                            padx=20,
                            pady=10,
                            cursor="hand2")
        order_btn.pack(fill="x", pady=5)

        # 宿舍管理按钮
        dorm_btn = tk.Button(btn_frame,
                            text="宿舍管理",
                            command=self.open_dorm_management,
                            font=("Microsoft YaHei", 12),
                            bg="#3C873D",
                            fg="white",
                            activebackground="#3a5fcd",
                            relief="flat",
                            padx=20,
                            pady=10,
                            cursor="hand2")
        dorm_btn.pack(fill="x", pady=5)

    def _open_child_window(self, window_class):
        """打开子窗口的通用方法"""
        # 如果已有子窗口，则不再创建
        if self.current_child_window is not None and tk._default_root is not None:
            return
            
        # 隐藏主窗口
        self.root.withdraw()
        
        # 创建子窗口
        child_window = tk.Toplevel(self.root)
        self.current_child_window = child_window
        window_class(child_window, self.controller, self.db)
        
        # 设置关闭回调
        child_window.protocol("WM_DELETE_WINDOW", lambda: self._on_child_close(child_window))
        
        # 设置为模态窗口（可选）
        child_window.grab_set()
        
        # 子窗口关闭时回调
        child_window.bind("<Destroy>", lambda e: self._on_child_close(child_window) if e.widget == child_window else None)

    def _on_child_close(self, child_window):
        """子窗口关闭时的处理"""
        # 确保子窗口存在
        if child_window is not None and tk._default_root is not None:
            # 释放模态窗口
            child_window.grab_release()
            # 销毁子窗口
            child_window.destroy()
        
        # 重置引用
        self.current_child_window = None
        
        # 恢复主窗口
        self.root.deiconify()

    def open_user_management(self):
        """打开用户管理窗口"""
        from code.views.adminview.user_management import UserManagementWindow
        self._open_child_window(UserManagementWindow)

    def open_query_stats(self):
        """打开查询统计窗口"""
        from code.views.adminview.query_stats import QueryStatsWindow
        self._open_child_window(QueryStatsWindow)

    def open_order_management(self):
        """打开订单管理窗口"""
        from code.views.adminview.order_management import OrderManagementWindow
        self._open_child_window(OrderManagementWindow)

    def open_dorm_management(self):
        """打开宿舍管理窗口"""
        from code.views.adminview.dorm_management import DormManagementWindow
        self._open_child_window(DormManagementWindow)