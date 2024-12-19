import traceback
import pandas as pd
from telethon import TelegramClient
from app.utils.utils import get_display_width
from openpyxl.reader.excel import load_workbook
from telethon.errors import SessionPasswordNeededError
from openpyxl.worksheet.table import Table, TableStyleInfo
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QLineEdit


async def get_telegram_info(api_name, api_id, api_hash, phone_number, proxy=None, parent=None):
    # 创建并连接客户端
    print(api_name, api_id, api_hash, phone_number, proxy)
    client = TelegramClient(api_name, int(api_id), api_hash, proxy=proxy)
    await client.connect()

    if not await client.is_user_authorized():
        # 使用 PyQt 的 QInputDialog 获取验证码
        await client.send_code_request(phone_number)
        text, ok = QInputDialog.getText(parent, '验证码', '请输入验证码:')  # 使用传入的parent
        if not ok:
            QMessageBox.warning(parent, '警告', '未输入验证码，操作取消！')  # 使用传入的parent
            await client.disconnect()
            return
        verification_code = text
        try:
            await client.sign_in(phone_number, verification_code)
        except SessionPasswordNeededError:
            text, ok = QInputDialog.getText(parent, '两步验证', '请输入两步验证密码:', QLineEdit.Password)
            if not ok:
                QMessageBox.warning(parent, '警告', '未输入两步验证密码，操作取消！')
                await client.disconnect()
                return
            password = text
            await client.sign_in(password=password)

    # 获取对话
    groups_and_channels = []
    bots = []

    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            groups_and_channels.append((dialog.entity, '群组', dialog.name))
        elif dialog.is_channel:
            groups_and_channels.append((dialog.entity, '频道', dialog.name))
        elif dialog.entity.bot:
            bots.append((dialog.entity.username, dialog.entity.first_name, dialog.entity.id))

    # 准备导出数据
    group_channel_data = []
    for entity, chat_type, chat_title in groups_and_channels:
        try:
            username = getattr(entity, 'username', None)
            if username:
                invite_link = f"https://t.me/{username}"
            else:
                invite_link = ""
            group_channel_data.append({
                "类型": chat_type,
                "ID": entity.id,
                "名称": chat_title,
                "邀请链接": invite_link
            })
        except Exception:
            print(traceback.format_exc())
            group_channel_data.append({
                "类型": chat_type,
                "ID": entity.id,
                "名称": chat_title,
                "邀请链接": ""
            })

    bot_data = []
    for username, first_name, user_id in bots:
        bot_data.append({
            "用户名": f"@{username}",
            "昵称": first_name,
            "用户ID": user_id
        })

    # 创建DataFrame
    df_groups_channels = pd.DataFrame(group_channel_data)
    df_bots = pd.DataFrame(bot_data)

    # 导出到Excel
    file_path = "telegram_info.xlsx"
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_groups_channels.to_excel(writer, sheet_name="群组和频道", index=False)
        df_bots.to_excel(writer, sheet_name="机器人", index=False)

    # 加载Excel文件并添加筛选功能
    wb = load_workbook(file_path)

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        # 创建表格
        tab = Table(displayName=f"Table_{sheet_name}", ref=ws.dimensions)
        # 添加样式
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False,
            showLastColumn=False, showRowStripes=True, showColumnStripes=True)
        tab.tableStyleInfo = style
        ws.add_table(tab)

        # 自动调整列宽
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    length = get_display_width(cell.value)
                    if length > max_length:
                        max_length = length
                except:
                    print(traceback.format_exc())
                    pass
            adjusted_width = (max_length + 4)
            ws.column_dimensions[column].width = adjusted_width

    wb.save(file_path)
    # 断开客户端
    await client.disconnect()


class ControllerExport:
    def __init__(self, main_controller, ui):
        self.main_controller = main_controller
        self.ui = ui
        self.ui.main_button_clicked_signal.connect(self.on_main_button_clicked)

    async def on_main_button_clicked(self):
        # 检查按钮是否已经在运行
        if self.main_controller.is_main_button_running:
            return
        self.main_controller.is_main_button_running = True

        # 禁用主界面按钮
        self.ui.main_page.main_btn_2.setEnabled(False)
        self.ui.main_page.export_info_label.setText("正在获取数据...")
        self.ui.main_page.export_info_label.setStyleSheet("color: black")

        api_id = self.ui.main_page.id_input.text()
        api_hash = self.ui.main_page.api_hash_input.text()
        phone = self.ui.main_page.phone_input.text()
        try:
            await get_telegram_info(
                f"telegram_info_{phone}", api_id, api_hash, phone,
                self.main_controller.proxy_settings, parent=self.ui
            )  # 传入 self.ui 作为 parent
        except:
            print(traceback.format_exc())
            self.ui.main_page.export_info_label.setText("获取数据失败")
            self.ui.main_page.export_info_label.setStyleSheet("color: red")
            self.ui.main_page.main_btn_2.setEnabled(True)
            self.main_controller.is_main_button_running = False
            return
        # 启用主界面按钮
        self.ui.main_page.export_info_label.setText("获取数据成功")
        self.ui.main_page.export_info_label.setStyleSheet("color: green")
        self.ui.main_page.main_btn_2.setEnabled(True)
        self.main_controller.is_main_button_running = False
