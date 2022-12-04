#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/11/23 11:21 
# @File           : initialize.py
# @IDE            : PyCharm
# @desc           : 简要说明
from core.database import db_getter
from utils.excel.excel_manage import ExcelManage
from application.settings import BASE_DIR, VERSION
import os
from apps.vadmin.auth import models as auth_models
from apps.vadmin.system import models as system_models
from sqlalchemy.sql.schema import Table
import subprocess


class InitializeData:
    """
    初始化数据

    生成步骤：
        1. 读取数据
        2. 获取数据库
        3. 创建数据
    """

    SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts', 'initialize')

    def __init__(self):
        self.sheet_names = []
        self.datas = {}
        self.ex = None
        self.db = None
        self.__serializer_data()
        self.__get_sheet_data()

    @classmethod
    def migrate_model(cls):
        """
        模型迁移映射到数据库
        """
        subprocess.check_call(f'alembic revision --autogenerate -m "{VERSION}"', cwd=BASE_DIR)
        subprocess.check_call('alembic upgrade head', cwd=BASE_DIR)
        print(f"{VERSION} 数据库表迁移完成")

    def __serializer_data(self):
        """
        序列化数据，将excel数据转为python对象
        """
        self.ex = ExcelManage()
        self.ex.open_workbook(os.path.join(self.SCRIPT_DIR, 'data', 'init.xlsx'), read_only=True)
        self.sheet_names = self.ex.get_sheets()

    def __get_sheet_data(self):
        """
        获取工作区数据
        """
        for sheet in self.sheet_names:
            sheet_data = []
            self.ex.open_sheet(sheet)
            headers = self.ex.get_header()
            datas = self.ex.readlines(min_row=2, max_col=len(headers))
            for row in datas:
                sheet_data.append(dict(zip(headers, row)))
            self.datas[sheet] = sheet_data

    async def __generate_data(self, table_name: str, model):
        """
        生成数据

        @params table_name: 表名
        @params model: 数据表模型
        """
        async_session = db_getter()
        db = await async_session.__anext__()
        if isinstance(model, Table):
            for data in self.datas.get(table_name):
                await db.execute(model.insert().values(**data))
        else:
            for data in self.datas.get(table_name):
                db.add(model(**data))
        print(f"{table_name} 表数据已生成")
        await db.flush()
        await db.commit()

    async def generate_menu(self):
        """
        生成菜单数据
        """
        await self.__generate_data("vadmin_auth_menu", auth_models.VadminMenu)

    async def generate_role(self):
        """
        生成角色
        """
        await self.__generate_data("vadmin_auth_role", auth_models.VadminRole)

    async def generate_user(self):
        """
        生成用户
        """
        await self.__generate_data("vadmin_auth_user", auth_models.VadminUser)

    async def generate_user_role(self):
        """
        生成用户
        """
        await self.__generate_data("vadmin_auth_user_roles", auth_models.vadmin_user_roles)

    async def generate_system_tab(self):
        """
        生成系统配置分类数据
        """
        await self.__generate_data("vadmin_system_settings_tab", system_models.VadminSystemSettingsTab)

    async def generate_system_config(self):
        """
        生成系统配置数据
        """
        await self.__generate_data("vadmin_system_settings", system_models.VadminSystemSettings)

    async def generate_dict_type(self):
        """
        生成字典类型数据
        """
        await self.__generate_data("vadmin_system_dict_type", system_models.VadminDictType)

    async def generate_dict_details(self):
        """
        生成字典详情数据
        """
        await self.__generate_data("vadmin_system_dict_details", system_models.VadminDictDetails)

    async def run(self):
        """
        执行初始化工作
        """
        self.migrate_model()
        await self.generate_menu()
        await self.generate_role()
        await self.generate_user()
        await self.generate_user_role()
        await self.generate_system_tab()
        await self.generate_dict_type()
        await self.generate_system_config()
        await self.generate_dict_details()
        print(f"{VERSION} 数据已初始化完成")
