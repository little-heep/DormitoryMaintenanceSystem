import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, font
from code.controllers.maintainer_controller import MaintenanceController, Order, Maintainer, OrderStatus


class MaintenanceUI:
    def __init__(self, root, controller: MaintenanceController,):

        self.root = root
        self.controller = controller
        self.numundo=0
        self.numdone=0
        self.pending_canvas = None
        self.completed_canvas = None
        self.pending_scrollable_frame = None
        self.completed_scrollable_frame = None
        self.pending_scrollbar = None
        self.completed_scrollbar = None
        self.setup_ui()

        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        """处理窗口大小变化"""
        if event.widget == self.root and hasattr(self, 'pending_canvas') and self.pending_canvas:
            # 更新画布的滚动区域
            self.root.after_idle(self.update_scroll_regions)

    def update_scroll_regions(self):
        """更新滚动区域"""
        if self.pending_canvas and self.pending_scrollable_frame:
            self.pending_canvas.configure(scrollregion=self.pending_canvas.bbox("all"))
        if self.completed_canvas and self.completed_scrollable_frame:
            self.completed_canvas.configure(scrollregion=self.completed_canvas.bbox("all"))

    def setup_ui(self):
        """设置主界面"""
        self.root.title("维修工工作平台")
        self.root.geometry("600x430")  # 增加宽度以容纳两列
        self.root.resizable(True, True)  # 允许调整大小

        # 设置字体
        self.custom_font = font.Font(family="幼圆", size=10)
        self.title_font = font.Font(family="幼圆", size=12, weight="bold")

        # 完整的颜色方案
        self.colors = {
            'primary': '#B2E7FF',
            'primary_dark': '#357ABD',  # 新增
            'primary_light': '#6FA8DC',  # 新增
            'secondary': '#7ED321',
            'accent': '#F5A623',
            'background': '#FDFFEB',
            'card': '#F9FFF8',
            'card_hover': '#F1F3F4',
            'text_primary': '#8FA0FF',
            'text_secondary': '#6C757D',
            'text_light': '#FFFFFF',  # 新增
            'border': '#DEE2E6',
            'success': '#28A745',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'shadow': 'gray85',
            'highlight': '#FF6B6B',
            'info': '#17A2B8'
        }

        # 主容器
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部标题栏
        self.header = tk.Frame(self.main_frame, bg=self.colors['primary'], height=50)
        self.header.pack(fill=tk.X)

        self.title_label = tk.Label(
            self.header,
            text="🔧维修工工作平台",
            font=self.title_font,
            bg=self.colors['text_primary'],
            fg='white'
        )

        # 内容区域
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 底部导航
        self.nav_frame = tk.Frame(self.main_frame, bg=self.colors['border'], height=50)
        self.nav_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.orders_btn = tk.Button(
            self.nav_frame,
            text="📋维修单",
            font=self.custom_font,
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            command=self.show_orders_page
        )
        self.orders_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        self.profile_btn = tk.Button(
            self.nav_frame,
            text="个人信息",
            font=self.custom_font,
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            command=self.show_profile_page
        )
        self.profile_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)

        # 初始化页面
        self.current_page = None
        self.show_orders_page()

    def clear_content(self):
        """清除内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_orders_page(self):
        """显示维修单页面"""
        self.clear_content()
        self.current_page = 'orders'

        # 更新按钮状态
        self.orders_btn.config(bg=self.colors['secondary'])
        self.profile_btn.config(bg=self.colors['primary'])

        # 获取订单数据
        orders = self.controller.get_orders()
        self.numdone= len(orders["completed"])
        self.numundo=len(orders["pending"])

        # 创建左右两个框架
        container = tk.Frame(self.content_frame, bg=self.colors['background'])
        container.pack(fill=tk.BOTH, expand=True)

        # 设置均匀列权重，确保宽度一致
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(2, weight=1)

        # 未完成订单列
        pending_container = tk.Frame(container, bg=self.colors['background'])
        pending_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        tk.Label(
            pending_container,
            text="待完成维修单("+str(self.numundo)+"单)",
            font=self.title_font,
            bg=self.colors['background'],
            fg=self.colors['text_primary']
        ).pack(fill=tk.X, pady=(0, 10))

        # 创建待完成订单的滚动区域
        self.pending_canvas = tk.Canvas(pending_container, bg=self.colors['background'], highlightthickness=0)
        self.pending_scrollbar = ttk.Scrollbar(pending_container, orient="vertical", command=self.pending_canvas.yview)
        self.pending_scrollable_frame = tk.Frame(self.pending_canvas, bg=self.colors['background'])

        # 绑定滚动事件
        self.pending_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.pending_canvas.configure(scrollregion=self.pending_canvas.bbox("all"))
        )

        self.pending_canvas.create_window((0, 0), window=self.pending_scrollable_frame, anchor="nw")
        self.pending_canvas.configure(yscrollcommand=self.pending_scrollbar.set)

        # 布局滚动组件
        self.pending_canvas.pack(side="left", fill="both", expand=True)
        self.pending_scrollbar.pack(side="right", fill="y")

        # 分隔线
        separator = ttk.Separator(container, orient=tk.VERTICAL)
        separator.grid(row=0, column=1, sticky="ns", padx=5)

        # 已完成订单列
        completed_container = tk.Frame(container, bg=self.colors['background'])
        completed_container.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        tk.Label(
            completed_container,
            text="已完成维修单("+str(self.numdone)+"单)",
            font=self.title_font,
            bg=self.colors['background'],
            fg=self.colors['text_primary']
        ).pack(fill=tk.X, pady=(0, 10))

        # 创建已完成订单的滚动区域
        self.completed_canvas = tk.Canvas(completed_container, bg=self.colors['background'], highlightthickness=0)
        self.completed_scrollbar = ttk.Scrollbar(completed_container, orient="vertical",
                                                 command=self.completed_canvas.yview)
        self.completed_scrollable_frame = tk.Frame(self.completed_canvas, bg=self.colors['background'])

        # 绑定滚动事件
        self.completed_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.completed_canvas.configure(scrollregion=self.completed_canvas.bbox("all"))
        )

        self.completed_canvas.create_window((0, 0), window=self.completed_scrollable_frame, anchor="nw")
        self.completed_canvas.configure(yscrollcommand=self.completed_scrollbar.set)

        # 布局滚动组件
        self.completed_canvas.pack(side="left", fill="both", expand=True)
        self.completed_scrollbar.pack(side="right", fill="y")

        # 添加鼠标滚轮支持
        self.bind_mousewheel(self.pending_canvas)
        self.bind_mousewheel(self.completed_canvas)

        # 填充订单数据
        if not orders['pending']:
            tk.Label(
                self.pending_scrollable_frame,
                text="暂无待完成维修单",
                font=self.custom_font,
                bg=self.colors['background'],
                fg=self.colors['text_secondary']
            ).pack(fill=tk.X, pady=20)
        else:
            for order in orders['pending']:
                self.create_order_card(self.pending_scrollable_frame, order, pending=True)

        if not orders['completed']:
            tk.Label(
                self.completed_scrollable_frame,
                text="暂无已完成维修单",
                font=self.custom_font,
                bg=self.colors['background'],
                fg=self.colors['text_secondary']
            ).pack(fill=tk.X, pady=20)
        else:
            for order in orders['completed']:
                self.create_order_card(self.completed_scrollable_frame, order, pending=False)

    def bind_mousewheel(self, canvas):
        """绑定鼠标滚轮事件"""

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

    def create_order_card(self, parent, order: Order, pending: bool):
        """创建订单卡片"""
        # 卡片容器
        card_container = tk.Frame(parent, bg=self.colors['background'])
        card_container.pack(fill=tk.X, pady=(0, 8))

        # 阴影层
        shadow = tk.Frame(
            card_container,
            bg=self.colors['shadow'],
            height=2
        )
        shadow.pack(fill=tk.X, pady=(7, 0))

        card = tk.Frame(
            card_container,
            bg=self.colors['card'],
            padx=15,
            pady=15,
            relief=tk.FLAT,
            bd=0
        )
        card.pack(fill=tk.X, pady=(0, 0))

        # 添加悬停效果
        def on_enter(e):
            card.config(bg=self.colors['card_hover'])

        def on_leave(e):
            card.config(bg=self.colors['card'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # 状态指示器
        status_frame = tk.Frame(card, bg=self.colors['card'])
        status_frame.pack(fill=tk.X, pady=(0, 8))

        status_color = self.colors['warning'] if pending else self.colors['success']
        status_text = "⏳待处理" if pending else "✅已完成"

        tk.Label(
            status_frame,
            text="●",
            font=('Arial', 12),
            fg=status_color,
            bg=self.colors['card']
        ).pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(
            status_frame,
            text=status_text,
            font=self.custom_font,
            fg=status_color,
            bg=self.colors['card']
        ).pack(side=tk.LEFT)

        # 订单基本信息
        info_fields = [
            ("📋维修单号", order.ono),
            ("🛏宿舍号", order.mo),
            ("⏱️报修时间", order.starttime.strftime('%Y-%m-%d %H:%M'))
        ]

        for label_text, value in info_fields:
            info_frame = tk.Frame(card, bg=self.colors['card'])
            info_frame.pack(fill=tk.X, pady=1)

            tk.Label(
                info_frame,
                text=f"{label_text}:",
                font=self.custom_font,
                bg=self.colors['card'],
                fg=self.colors['text_secondary'],
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)

            tk.Label(
                info_frame,
                text=str(value),
                font=self.custom_font,
                bg=self.colors['card'],
                fg=self.colors['text_primary'],
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 问题描述
        desc_frame = tk.Frame(card, bg=self.colors['card'])
        desc_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Label(
            desc_frame,
            text="❓问题描述:",
            font=self.custom_font,
            bg=self.colors['card'],
            fg=self.colors['text_secondary'],
            anchor='w'
        ).pack(anchor='w')

        tk.Label(
            desc_frame,
            text=order.ocontent,
            font=self.custom_font,
            bg=self.colors['card'],
            fg=self.colors['text_secondary'],
            anchor='w',
            wraplength=250,
            justify='left'
        ).pack(fill=tk.X, padx=(10, 0))

        # 根据不同状态显示不同内容
        if pending:
            # 待完成订单 - 显示完成按钮
            btn_frame = tk.Frame(card, bg=self.colors['card'])
            btn_frame.pack(fill=tk.X, pady=(10, 0))

            complete_btn = tk.Button(
                btn_frame,
                text="✓ 确认完成",
                font=self.custom_font,
                bg=self.colors['success'],
                fg='white',
                relief=tk.FLAT,
                cursor='hand2',
                command=lambda o=order, c=card_container: self.complete_order(o, c)
            )
            complete_btn.pack(fill=tk.X)

            # 添加按钮悬停效果
            def btn_enter(e):
                complete_btn.config(bg='#218838')

            def btn_leave(e):
                complete_btn.config(bg=self.colors['success'])

            complete_btn.bind('<Enter>', btn_enter)
            complete_btn.bind('<Leave>', btn_leave)

        else:
            # 已完成订单 - 显示评价信息
            eval_frame = tk.Frame(card, bg=self.colors['card'])
            eval_frame.pack(fill=tk.X, pady=(10, 0))

            if hasattr(order, 'finishtime') and order.finishtime:
                tk.Label(
                    eval_frame,
                    text=f"⏱️完成时间: {order.finishtime.strftime('%Y-%m-%d %H:%M')}",
                    font=self.custom_font,
                    bg=self.colors['card'],
                    fg=self.colors['text_secondary']
                ).pack(fill=tk.X)

            if hasattr(order, 'comment') and order.comment:
                tk.Label(
                    eval_frame,
                    text=f"💯评分: {'★' * order.score}{'☆' * (5 - order.score)}",
                    font=self.custom_font,
                    bg=self.colors['card'],
                    fg=self.colors['highlight']
                ).pack(fill=tk.X)

                tk.Label(
                    eval_frame,
                    text=f"💬评价: {order.comment}",
                    font=self.custom_font,
                    bg=self.colors['card'],
                    fg=self.colors['text_secondary'],
                    wraplength=250,
                    justify='left'
                ).pack(fill=tk.X)
            else:
                tk.Label(
                    eval_frame,
                    text="等待用户评价",
                    font=self.custom_font,
                    bg=self.colors['card'],
                    fg=self.colors['info'],
                    #style='italic'
                ).pack(fill=tk.X)

        return card_container

    def complete_order(self, order: Order, card_widget):
        """完成订单"""
        if messagebox.askyesno("确认", f"确认完成订单 #{order.ono} 吗？"):
            if self.controller.complete_order(order.ono):
                # 从未完成列表移除卡片
                card_widget.destroy()  # 使用 destroy 而不是 pack_forget
                self.numundo-=1
                self.numdone+=1

                # 创建更新后的订单对象
                updated_order = Order(
                    ono=order.ono,
                    sno=order.sno,
                    mno=order.mno,
                    cno=order.cno,
                    mo=order.mo,
                    status=2,
                    ocontent=order.ocontent,
                    starttime=order.starttime,
                    finishtime=datetime.now(),
                    comment=None,
                    score=3
                )

                # 直接添加到已完成列表
                self.add_to_completed_orders(updated_order)
                messagebox.showinfo("成功", "订单状态已更新")
                self.show_orders_page()
            else:
                messagebox.showerror("错误", "更新订单状态失败")

    def add_to_completed_orders(self, order: Order):
        """将订单添加到已完成列表"""
        # 清空已完成区域的空状态提示
        for widget in self.completed_scrollable_frame.winfo_children():
            if isinstance(widget, tk.Label) and "暂无已完成维修单" in widget.cget("text"):
                widget.destroy()

        # 直接在已完成的滚动框架中创建新卡片
        self.create_order_card(self.completed_scrollable_frame, order, pending=False)

        # 更新滚动区域
        self.completed_canvas.update_idletasks()
        self.completed_canvas.configure(scrollregion=self.completed_canvas.bbox("all"))

    def show_profile_page(self):
        """显示个人信息页面"""
        self.clear_content()
        self.current_page = 'profile'

        # 更新导航按钮状态
        self.orders_btn.config(bg=self.colors['primary'])
        self.profile_btn.config(bg=self.colors['secondary'])

        if not self.controller.current_maintainer:
            error_label = tk.Label(
                self.content_frame,
                text="❌ 无法加载个人信息\n请重新登录",
                font=self.title_font,
                bg=self.colors['background'],
                fg=self.colors['danger']
            )
            error_label.pack(expand=True)
            return


        # 创建主容器
        profile_container = tk.Frame(self.content_frame, bg=self.colors['background'])
        profile_container.pack(fill=tk.BOTH, expand=True)

        # 创建个人信息卡片
        profile_card = tk.Frame(
            profile_container,
            bg=self.colors['card'],
            relief=tk.RAISED,
            bd=3,
            padx=30,
            pady=30
        )
        profile_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 创建个人信息表单
        self.create_profile_form(profile_card, self.controller.current_maintainer)

        # 创建修改按钮框架
        button_frame = tk.Frame(profile_card, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # 修改联系方式按钮
        contact_btn = tk.Button(
            button_frame,
            text="📱 修改联系方式",
            font=self.custom_font,
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            command=lambda: self.update_contact()
        )
        contact_btn.pack(side=tk.LEFT, expand=True, padx=5)

        # 修改密码按钮
        password_btn = tk.Button(
            button_frame,
            text="🔑 修改密码",
            font=self.custom_font,
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            command=lambda: self.update_password()
        )
        password_btn.pack(side=tk.LEFT, expand=True, padx=5)

    def create_profile_form(self, parent, maintainer):
        """创建个人信息表单"""
        # 表单标题
        tk.Label(
            parent,
            text="👨‍🔧 个人信息",
            font=('Arial', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text_primary']
        ).pack(anchor='w', pady=(0, 20))

        # 创建信息字段
        fields = [
            ("👤", "姓名", maintainer.mname),
            ("🆔", "工号", maintainer.mno),
            ("📱", "联系方式", maintainer.mlink),
            ("⭐", "总积分", str(maintainer.allscore))
        ]

        for icon, label, value in fields:
            field_frame = tk.Frame(parent, bg=self.colors['card'])
            field_frame.pack(fill=tk.X, pady=8)

            # 标签
            tk.Label(
                field_frame,
                text=f"{icon} {label}:",
                font=self.custom_font,
                bg=self.colors['card'],
                fg=self.colors['text_secondary'],
                width=10,
                anchor='w'
            ).pack(side=tk.LEFT)

            # 值
            tk.Label(
                field_frame,
                text=value,
                font=self.custom_font,
                bg=self.colors['card'],
                fg=self.colors['text_primary'],
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X)

    def update_contact(self):
        """更新联系方式"""
        dialog = tk.Toplevel(self.root)
        dialog.title("修改联系方式")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        # 设置模态
        dialog.transient(self.root)
        dialog.grab_set()

        # 创建表单
        form_frame = tk.Frame(dialog, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="新联系方式:").pack(anchor='w')
        contact_var = tk.StringVar(value=self.controller.current_maintainer.mlink)
        contact_entry = tk.Entry(form_frame, textvariable=contact_var)
        contact_entry.pack(fill=tk.X, pady=(5, 20))

        # 按钮框架
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill=tk.X)

        def save_contact():
            new_contact = contact_var.get()
            if new_contact:
                if self.controller.update_maintainer_link(new_contact):
                    messagebox.showinfo("成功", "联系方式已更新")
                    dialog.destroy()
                    self.controller.current_maintainer.mlink=new_contact
                    self.show_profile_page()  # 刷新页面
                else:
                    messagebox.showerror("错误", "更新失败")
            else:
                messagebox.showwarning("警告", "联系方式不能为空")

        tk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="保存", command=save_contact).pack(side=tk.LEFT, expand=True, padx=5)

    def update_password(self):
        """更新密码"""
        dialog = tk.Toplevel(self.root)
        dialog.title("修改密码")
        dialog.geometry("300x200")
        dialog.resizable(False, False)

        # 设置模态
        dialog.transient(self.root)
        dialog.grab_set()

        # 创建表单
        form_frame = tk.Frame(dialog, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 旧密码
        tk.Label(form_frame, text="旧密码:").pack(anchor='w')
        old_pwd_var = tk.StringVar()
        old_pwd_entry = tk.Entry(form_frame, textvariable=old_pwd_var, show='*')
        old_pwd_entry.pack(fill=tk.X, pady=(5, 10))

        # 新密码
        tk.Label(form_frame, text="新密码:").pack(anchor='w')
        new_pwd_var = tk.StringVar()
        new_pwd_entry = tk.Entry(form_frame, textvariable=new_pwd_var, show='*')
        new_pwd_entry.pack(fill=tk.X, pady=(5, 20))

        # 按钮框架
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill=tk.X)

        def save_password():
            old_pwd = old_pwd_var.get()
            new_pwd = new_pwd_var.get()

            if not old_pwd or not new_pwd:
                messagebox.showwarning("警告", "密码不能为空")
                return

            if self.controller.current_maintainer.mpwd==old_pwd:
                if self.controller.update_maintainer_pwd( new_pwd):
                    messagebox.showinfo("成功", "密码已更新")
                    dialog.destroy()
                    self.controller.current_maintainer.mpwd = new_pwd
                    self.show_profile_page()  # 刷新页面
                else:
                    messagebox.showerror("错误", "更新失败")
            else:
                messagebox.showerror("错误", "旧密码不正确")

        tk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(btn_frame, text="保存", command=save_password).pack(side=tk.LEFT, expand=True, padx=5)
