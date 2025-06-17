import tkinter as tk
from tkinter import ttk
from code.controllers.admincontroller import AdminController

class QueryStatsWindow:
    def __init__(self, root, controller: AdminController, db):
        self.root = root
        self.controller = controller
        self.db = db
        self.root.title("查询统计")
        self.root.geometry("900x600")
        root.resizable(False, False) 
        self.root.configure(bg="#f0f8ff")
        
        self._setup_ui()

    def _setup_ui(self):
        """创建查询统计界面"""
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # 使用Notebook分页
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both")

        # 维修员积分统计页
        self.score_frame = tk.Frame(self.notebook, bg="white")
        self._setup_score_ui()
        self.notebook.add(self.score_frame, text="维修员积分")

        # 月度收入统计页
        self.income_frame = tk.Frame(self.notebook, bg="white")
        self._setup_income_ui()
        self.notebook.add(self.income_frame, text="月度收入")

        # 维修类别频率页
        self.class_frame = tk.Frame(self.notebook, bg="white")
        self._setup_class_ui()
        self.notebook.add(self.class_frame, text="维修类别")

        # 宿舍报修频率页
        self.room_frame = tk.Frame(self.notebook, bg="white")
        self._setup_room_ui()
        self.notebook.add(self.room_frame, text="宿舍报修")

    def _setup_score_ui(self):
        """维修员积分统计页面"""
        columns = ("工号", "年份", "月份", "月份名称", "总积分", "维修单数", "平均积分")
        self.score_tree = ttk.Treeview(
            self.score_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.score_tree.heading(col, text=col)
            self.score_tree.column(col, width=100, anchor="center")

        self.score_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_score_list()

    def _setup_income_ui(self):
        """月度收入统计页面"""
        columns = ("年份", "月份", "总收入")
        self.income_tree = ttk.Treeview(
            self.income_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.income_tree.heading(col, text=col)
            self.income_tree.column(col, width=150, anchor="center")

        self.income_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_income_list()

    def _setup_class_ui(self):
        """维修类别频率页面"""
        columns = ("维修类别", "报修次数")
        self.class_tree = ttk.Treeview(
            self.class_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.class_tree.heading(col, text=col)
            self.class_tree.column(col, width=200, anchor="center")

        self.class_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_class_list()

    def _setup_room_ui(self):
        """宿舍报修频率页面"""
        columns = ("宿舍编号", "报修次数")
        self.room_tree = ttk.Treeview(
            self.room_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        for col in columns:
            self.room_tree.heading(col, text=col)
            self.room_tree.column(col, width=200, anchor="center")

        self.room_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_room_list()

    def _refresh_score_list(self):
        """刷新维修员积分列表"""
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        
        scores = self.controller.get_worker_score(self.db)
        for score in scores:
            self.score_tree.insert("", "end", values=score)

    def _refresh_income_list(self):
        """刷新月度收入列表"""
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)
        
        incomes = self.controller.get_income_by_month(self.db)
        for income in incomes:
            self.income_tree.insert("", "end", values=income)

    def _refresh_class_list(self):
        """刷新维修类别列表"""
        for item in self.class_tree.get_children():
            self.class_tree.delete(item)
        
        classes = self.controller.get_classify_frequency(self.db)
        for cls in classes:
            self.class_tree.insert("", "end", values=cls)

    def _refresh_room_list(self):
        """刷新宿舍报修列表"""
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
        
        rooms = self.controller.get_room_frequency(self.db)
        for room in rooms:
            self.room_tree.insert("", "end", values=room)
