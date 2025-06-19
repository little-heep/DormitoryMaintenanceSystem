import re
import tkinter as tk
from tkinter import ttk, messagebox
from code.controllers.student_controller import StudentController
from code.tools.databasetools import db_student_update, db_all_room


class StudentUI:
    def __init__(self, controller, current_student):
        self.current_student = current_student
        self.student_controller = controller
        self.root = tk.Tk()
        self.root.title("学生宿舍维修系统")
        self.root.geometry("550x550")
        self.root.configure(bg="#f0f8ff")

        # 初始化样式和界面
        self.setup_style()
        self.create_main_interface()
        self.root.mainloop()

    def setup_style(self):
        """配置全局样式"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab',
                        font=('微软雅黑', 10, 'bold'),
                        padding=[15, 5],
                        background="#e1f5fe")
        style.configure('TButton',
                        font=('微软雅黑', 10),
                        background="#4CAF50",
                        foreground="white",
                        borderwidth=0)  # 无边框按钮
        style.map('TButton',
                  background=[('active', '#45a049')])
        style.configure('TFrame',
                        background="#f0f8ff")  # 主背景色
        style.configure('TLabelframe',
                        background="#fdffeb",
                        font=('微软雅黑', 10))
        style.configure('TLabelframe.Label',
                        background="#fdffeb",
                        foreground="#1565C0")
        style.configure('TEntry',
                        fieldbackground="white")  # 输入框白色背景
        style.configure('Custom.TRadiobutton',
                             background='#fdffeb',
                             foreground='black',
                             font=('微软雅黑', 10))

    def create_main_interface(self):
        """创建主界面"""
        # 顶部标题
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(header_frame,
                  text="🏠 学生宿舍维修系统",
                  font=('微软雅黑', 16, 'bold'),
                  foreground="#0D47A1",
                  background="#f0f8ff").pack(pady=10)

        # 标签页控件
        self.tab_control = ttk.Notebook(self.root)
        self.setup_report_tab()  # 报修上报
        self.setup_query_tab()  # 订单查询
        self.setup_feedback_tab()  # 维修反馈
        self.setup_info_tab()  # 个人信息
        self.tab_control.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    # =================== 报修上报模块 ===================
    def setup_report_tab(self):
        self.frame_report = ttk.Frame(self.tab_control, style='TFrame')

        # 标题和表单框架
        ttk.Label(self.frame_report,
                  text="📝 维修报修",
                  font=('微软雅黑', 12, 'bold'),
                  foreground="#1565C0",
                  background="#f0f8ff").pack(pady=(10, 20))

        form_frame = ttk.LabelFrame(self.frame_report,
                                    text="填写报修信息",
                                    style='TLabelframe')
        form_frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(form_frame,
                  text="🏠 宿舍号:",
                  background="#fdffeb").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        # 从数据库获取当前学生的宿舍号作为默认值
        student_dorm = self.current_student.mo
        self.dorm_var = tk.StringVar(value=student_dorm)

        # 创建Combobox并设置自动补全
        self.combo_dorm = ttk.Combobox(form_frame,
                                       textvariable=self.dorm_var,
                                       width=30,
                                       style='TCombobox')
        self.combo_dorm.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 问题类型选择
        ttk.Label(form_frame,
                  text="🔧 问题类型:",
                  background="#fdffeb").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # 创建分类和具体问题的选择框
        self.class_var = tk.StringVar()
        self.content_var = tk.StringVar()
        self.pay_var = tk.StringVar(value="0")  # 存储支付金额

        # 分类选择框
        class_frame = ttk.Frame(form_frame)
        class_frame.grid(row=1, column=1, padx=5, pady=5,sticky="w")

        ttk.Radiobutton(class_frame, text="普通", variable=self.class_var,
                        value="普通", command=self.update_content_options,
                        style='Custom.TRadiobutton').pack(side="left")

        ttk.Radiobutton(class_frame, text="特殊", variable=self.class_var,
                        value="特殊", command=self.update_content_options,
                        style='Custom.TRadiobutton').pack(side="left")

        # 具体问题选择框
        ttk.Label(form_frame,
                  text="🔍 具体问题:",
                  background="#fdffeb").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.content_combobox = ttk.Combobox(form_frame, textvariable=self.content_var, width=30)
        self.content_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # 初始化分类为"普通"
        self.class_var.set("普通")
        self.update_content_options()

        # 4. 新增问题详情 (放在最后)
        ttk.Label(form_frame,
                  text="📝 问题详情以及预约时间:",
                  background="#fdffeb").grid(row=3, column=0, padx=5, pady=5, sticky="ne")

        self.entry_details = tk.Text(form_frame, width=30, height=4, wrap="word")
        self.entry_details.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # 提交按钮
        ttk.Button(self.frame_report,
                   text="📤 提交报修",
                   command=self.submit_report,
                   style='TButton').pack(pady=20)

        self.tab_control.add(self.frame_report, text="报修上报")

    def update_content_options(self):
        """根据选择的分类更新具体问题选项"""
        if self.class_var.get() == "普通":
            options = [
                ("空调维修", "A001", "0"),
                ("衣柜维修", "A002", "0"),
                ("修灯泡", "A003", "5"),
                ("修门", "A004", "0")
            ]
        else:
            options = [
                ("通厕所", "B001", "10"),
                ("修水管", "B002", "3")
            ]

        # 更新下拉框选项
        self.content_combobox['values'] = [opt[0] for opt in options]
        self.content_options_map = {opt[0]: (opt[1], opt[2]) for opt in options}
        self.content_combobox.current(0)

    def show_payment_popup(self, amount):
        """显示支付弹窗"""
        popup = tk.Toplevel(self.root)
        popup.title("支付维修费用")
        popup.geometry("300x200")
        popup.resizable(False, False)

        ttk.Label(popup, text=f"本次维修需支付: ¥{amount}", font=('微软雅黑', 12)).pack(pady=20)

        # 支付按钮
        ttk.Button(popup, text="确认支付",
                   command=lambda: self.process_payment(popup, amount)).pack(pady=10)

        # 取消按钮
        ttk.Button(popup, text="取消支付",
                   command=popup.destroy).pack(pady=10)

    def process_payment(self, popup, amount):
        """处理支付逻辑"""
        # 这里可以添加实际的支付处理逻辑
        popup.destroy()
        messagebox.showinfo("支付成功", f"已成功支付¥{amount}元", parent=self.root)
        self.clear_input_fields()

    def submit_report(self):
        """处理报修提交"""
        try:
            # 获取输入数据

            content = self.content_var.get().strip()
            dorm=self.current_student.mo
            detail=self.entry_details.get("1.0",tk.END).strip()
            # 验证输入

            if not content:
                raise ValueError("请选择具体问题")

            # 获取cno和支付金额
            cno, pay_amount = self.content_options_map.get(content, (None, "0"))
            if not cno:
                raise ValueError("无法识别问题类型")

            # 提交报修
            success, message = self.student_controller.report_issue(
                self.current_student.sno,
                dorm,
                detail,
                cno
            )

            if not success:
                raise RuntimeError(f"报修失败: {message}")

            # 如果需要支付，显示支付弹窗
            if pay_amount != "0":
                self.show_payment_popup(pay_amount)
            else:
                messagebox.showinfo("成功", "报修成功，维修工已自动分配！", parent=self.root)
                self.clear_input_fields()

        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def clear_input_fields(self):
        """清空输入框"""

        self.class_var.set("普通")
        self.update_content_options()
    # =================== 订单查询模块 ===================
    def setup_query_tab(self):
        self.frame_query = ttk.Frame(self.tab_control, style='TFrame')

        # 使用网格布局管理器
        self.frame_query.grid_rowconfigure(1, weight=1)
        self.frame_query.grid_columnconfigure(0, weight=1)

        # 标题
        ttk.Label(self.frame_query,
                  text="📋 维修订单查询",
                  font=('微软雅黑', 12, 'bold'),
                  foreground="#1565C0",
                  background="#f0f8ff").grid(row=0, column=0, pady=(10, 15), sticky="ew")

        # 创建包含Treeview和Scrollbar的容器
        tree_container = ttk.Frame(self.frame_query)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=10)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        cols = ("订单号", "宿舍", "问题", "状态", "报修时间")
        self.tree = ttk.Treeview(tree_container,
                                 columns=cols,
                                 show='headings',
                                 selectmode="browse")

        # 配置列 - 自动调整列宽
        col_widths = {"订单号": 80, "宿舍": 80, "问题": 200, "状态": 80, "报修时间": 120}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor="center", stretch=True)

        # 自动调整列宽的函数
        def auto_resize_columns(event):
            # 获取Treeview的当前宽度
            tree_width = self.tree.winfo_width()
            # 计算总列宽
            total_width = sum(col_widths.values())
            # 计算每列应该占的比例
            for col in cols:
                self.tree.column(col, width=int(col_widths[col] / total_width * tree_width))

        # 绑定窗口大小变化事件
        self.tree.bind("<Configure>", auto_resize_columns)

        # 滚动条
        scrollbar = ttk.Scrollbar(tree_container,
                                  orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 使用网格布局Treeview和Scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 刷新按钮容器
        button_frame = ttk.Frame(self.frame_query)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame,
                   text="🔄 刷新订单",
                   command=self.refresh_query,
                   style='TButton').pack(pady=10)

        self.tab_control.add(self.frame_query, text="订单查询")
        self.refresh_query()

    def refresh_query(self):
        """刷新订单数据"""
        try:
            # 清空现有数据
            self.tree.delete(*self.tree.get_children())

            # 获取新数据
            orders = self.student_controller.query_orders(self.current_student.sno)
            print(orders)
            if not orders:
                raise ValueError("没有查询到维修订单")

            # 填充数据
            status_map = {0: "待处理", 1: "已分配", 2: "已完成", 3: "已评价"}
            for order in orders:
                if order.sno == self.current_student.sno:
                    status = status_map.get(order.status, "未知状态")
                    self.tree.insert("", "end", values=(
                    order.ono, order.mo, order.ocontent, status, order.starttime
                ))

            # 自动调整列宽
            self.tree.event_generate("<Configure>")

        except Exception as e:
            messagebox.showwarning("提示", str(e), parent=self.root)

    # =================== 维修反馈模块 ===================
    def setup_feedback_tab(self):
        self.frame_feedback = ttk.Frame(self.tab_control, style='TFrame')

        # 标题和表单
        ttk.Label(self.frame_feedback,
                  text="⭐ 维修评价",
                  font=('微软雅黑', 12, 'bold'),
                  foreground="#1565C0",
                  background="#f0f8ff").pack(pady=(10, 20))

        form_frame = ttk.LabelFrame(self.frame_feedback,
                                    text="填写评价信息",
                                    style='TLabelframe')
        form_frame.pack(padx=20, pady=10, fill="x")

        # 表单元素
        ttk.Label(form_frame,
                  text="📋 订单号:",
                  background="#fdffeb").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_order = ttk.Entry(form_frame, width=30, style='TEntry')
        self.entry_order.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame,
                  text="⭐ 评分 (1-5):",
                  background="#fdffeb").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_score = ttk.Entry(form_frame, width=30, style='TEntry')
        self.entry_score.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame,
                  text="💬 评价内容:",
                  background="#fdffeb").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        self.entry_comment = tk.Text(form_frame, width=40, height=8, bg="white")
        self.entry_comment.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # 提交按钮
        ttk.Button(self.frame_feedback,
                   text="📤 提交评价",
                   command=self.sub_feedback,
                   style='TButton').pack(pady=20)

        self.tab_control.add(self.frame_feedback, text="维修反馈")

    def sub_feedback(self):
        """处理评价提交"""
        try:
            # 验证输入
            oid = int(self.entry_order.get())
            rating = int(self.entry_score.get())
            if not 1 <= rating <= 5:
                raise ValueError("评分必须在1-5之间")

            comment = self.entry_comment.get("1.0", tk.END).strip()
            if not comment:
                raise ValueError("请填写评价内容")
            # 提交评价
            if not self.student_controller.submit_feedback(order_id=oid, rating=rating, comment=comment):
                raise RuntimeError("提交评价失败，请检查订单号是否正确")

            # 清空表单
            self.entry_order.delete(0, tk.END)
            self.entry_score.delete(0, tk.END)
            self.entry_comment.delete("1.0", tk.END)
            messagebox.showinfo("成功", "感谢您的反馈！", parent=self.root)

        except ValueError as e:
            messagebox.showerror("输入错误", str(e), parent=self.root)
        except Exception as e:
            messagebox.showerror("提交失败", str(e), parent=self.root)

    # =================== 个人信息模块 ===================
    def setup_info_tab(self):
        self.frame_info = ttk.Frame(self.tab_control, style='TFrame')

        # 创建四个彩色标题框
        self.create_info_headers()

        # 当前信息显示
        self.setup_current_info_section()

        # 信息修改区域
        self.setup_modify_section()

        self.tab_control.add(self.frame_info, text="个人信息")
        self.load_info()

    def create_info_headers(self):
        """创建四个彩色标题框"""
        headers_frame = tk.Frame(self.frame_info, bg="#fdffeb")
        headers_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # 四个不同颜色的标题框
        header_colors = ["#FF7043", "#42A5F5", "#66BB6A", "#AB47BC"]
        header_texts = ["👤 基本信息", "📱 联系方式", "🏠 宿舍信息", "🔒 安全设置"]
        header_icons = ["👤", "📱", "🏠", "🔒"]

        for i in range(4):
            header = tk.Frame(headers_frame,
                              bg=header_colors[i],
                              height=30,
                              relief=tk.RAISED,
                              bd=1)
            header.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0 if i == 3 else 2, 0))

            tk.Label(header,
                     text=f"{header_icons[i]} {header_texts[i].split(' ')[1]}",
                     font=('微软雅黑', 10, 'bold'),
                     bg=header_colors[i],
                     fg="white").pack(pady=5)

    def setup_current_info_section(self):
        """当前信息显示区域"""
        current_info_frame = ttk.LabelFrame(self.frame_info,
                                            text="当前信息",
                                            style='TLabelframe')
        current_info_frame.pack(padx=20, pady=10, fill="x")

        # 初始化信息变量
        self.info_vars = {
            "姓名": tk.StringVar(value="加载中..."),
            "学号": tk.StringVar(value=self.current_student.sno),
            "宿舍号": tk.StringVar(value="加载中..."),
            "联系方式": tk.StringVar(value="加载中...")
        }

        # 创建只读信息显示
        fields = ["姓名", "学号", "宿舍号", "联系方式"]
        icons = ["👤", "🆔", "🏠", "📱"]

        for row, (field, icon) in enumerate(zip(fields, icons)):
            ttk.Label(current_info_frame,
                      text=f"{icon} {field}:",
                      background="#fdffeb").grid(row=row, column=0, padx=5, pady=5, sticky="e")

            ttk.Entry(current_info_frame,
                      textvariable=self.info_vars[field],
                      state='readonly',
                      width=25,
                      style='TEntry').grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def setup_modify_section(self):
        """信息修改区域"""
        modify_frame = ttk.LabelFrame(self.frame_info,
                                      text="修改信息",
                                      style='TLabelframe')
        modify_frame.pack(padx=20, pady=10, fill="x")

        # 修改联系方式
        ttk.Label(modify_frame,
                  text="📱 新联系方式:",
                  background="#fdffeb").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.phone_entry = ttk.Entry(modify_frame, width=25, style='TEntry')
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 修改宿舍号
        ttk.Label(modify_frame,
                  text="🏠 新宿舍号:",
                  background="#fdffeb").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.dorm_entry = ttk.Entry(modify_frame, width=25, style='TEntry')
        self.dorm_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # 修改密码
        ttk.Label(modify_frame,
                  text="🔑 新密码:",
                  background="#fdffeb").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.new_pw = ttk.Entry(modify_frame, show='*', width=25, style='TEntry')
        self.new_pw.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # 保存按钮
        ttk.Button(self.frame_info,
                   text="💾 保存修改",
                   command=self.save_info,
                   style='TButton').pack(pady=20)

    def load_info(self):
        """安全加载个人信息"""
        try:
            # 检查学生对象有效性
            if not hasattr(self, 'current_student') or not getattr(self.current_student, 'sno', None):
                raise ValueError("学生信息未初始化")

            # 执行查询
            info = self.student_controller.get_personal_info(self.current_student.sno)
            if not info or len(info) < 3:
                raise ValueError("获取的信息不完整")

            # 更新UI
            self.info_vars["姓名"].set(info[0] or "未知")
            self.info_vars["宿舍号"].set(info[1] or "未知")
            self.info_vars["联系方式"].set(info[2] or "未知")

        except Exception as e:
            messagebox.showerror("加载失败", f"无法加载个人信息: {str(e)}", parent=self.root)
            # 设置默认值防止UI显示异常
            self.info_vars["姓名"].set("未知")
            self.info_vars["宿舍号"].set("未知")
            self.info_vars["联系方式"].set("未知")

    def save_info(self):
        """安全保存个人信息修改"""
        try:
            # 验证学生信息
            if not hasattr(self, 'current_student') or not getattr(self.current_student, 'sno', None):
                raise ValueError("无效的学生会话")

            # 获取输入
            phone = self.phone_entry.get().strip()
            password = self.new_pw.get().strip()
            dorm = self.dorm_entry.get().strip()

            # 检查是否有修改
            if not any([phone, password, dorm]):
                messagebox.showwarning("提示", "没有检测到要修改的信息", parent=self.root)
                return

            # 执行更新
            success = True
            updated_fields = []

            if phone:
                linkpattern = r'^1[3-9]\d{9}$'
                if not re.match(linkpattern, phone):
                    messagebox.showerror("联系方式错误📞", "联系方式应为11位中国式电话号码！")
                    return
                if db_student_update(self.student_controller.db_conn, 2, phone, self.current_student.sno):
                    updated_fields.append("联系方式")
                    self.info_vars["联系方式"].set(phone)
                    self.phone_entry.delete(0, tk.END)
                else:
                    success = False

            if dorm:
                romlis = db_all_room(self.student_controller.db_conn)
                exi = False
                for i in romlis:
                    if dorm == i.mo:
                        exi = True
                        break
                if not exi:
                    messagebox.showerror("宿舍号错误🏠", "宿舍号不存在！")
                    return
                if db_student_update(self.student_controller.db_conn, 1, dorm, self.current_student.sno):
                    updated_fields.append("宿舍号")
                    self.info_vars["宿舍号"].set(dorm)
                    self.dorm_entry.delete(0, tk.END)
                else:
                    success = False

            if password:
                pwdpattern = r'^(?=.*[0-9])(?=.*[a-zA-Z])[a-zA-Z0-9]{6,10}$'
                if not re.match(pwdpattern, password):
                    messagebox.showerror("密码错误🔒", "密码应为包含数字和字母的6-10位字符串")
                    return
                if db_student_update(self.student_controller.db_conn, 0, password, self.current_student.sno):
                    updated_fields.append("密码")
                    self.new_pw.delete(0, tk.END)
                else:
                    success = False

            # 显示结果
            if success:
                msg = "更新成功" + (f": {', '.join(updated_fields)}" if updated_fields else "")
                messagebox.showinfo("成功", msg, parent=self.root)
            else:
                messagebox.showerror("错误", "部分信息更新失败，请重试", parent=self.root)

        except Exception as e:
            messagebox.showerror("系统错误", f"保存过程中发生错误:\n{str(e)}", parent=self.root)