import datetime
import sys
import time

from lamda.client import Device, GrantType
from lamda.const import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QInputDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

d = Device("192.168.9.6")


class LoginThread(QThread):
    log_signal = pyqtSignal(str)
    code_signal = pyqtSignal()

    def __init__(self, phone):
        super().__init__()
        self.phone = phone

    def run(self):
        try:
            app = d.application("org.thunderdog.challegram")
            self.log_signal.emit("===== TgX Login ======")
            self.log_signal.emit("启动TgX")
            self.log_signal.emit(
                f"Phone: {self.phone} , date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
            self.log_signal.emit("重置TGx...")
            app.reset_data()
            self.log_signal.emit("赋予权限， 大约等待10-20s...")
            self.grant_app(app)
            if d(text="Please enter your valid email address.").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)

            elif d(textContains="We've sent an SMS with an").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)

            elif d(textContains="send an SMS").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)

            elif d(textContains="We've sent the code to your email").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)

            elif d(textContains="code to the Telegram app on your other").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)
            elif d(text="Enter your email address").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)

            elif d(textContains="oo many request").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)

            elif d(textContains="Invalid").exists():
                self.log_signal.emit("检测到上次登录失败，重置TgX数据， 大约需要15s")
                app.reset_data()
                self.grant_app(app)
            time.sleep(1)
            d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
            time.sleep(3)
            if d(text="Start Messaging"):
                d(text="Start Messaging").click()
            phone_input = d(resourceId="org.thunderdog.challegram:id/login_phone")
            time.sleep(2)
            phone_input.set_text(self.phone)
            self.log_signal.emit(f"输入手机号 {self.phone}")
            ack = d(resourceId="org.thunderdog.challegram:id/btn_done")
            ack.click()
            time.sleep(6)
            code_input = d(className="android.widget.EditText")
            time.sleep(2)
            if not d(textContains="sent").exists():
                ret_text = ""
                if d(textContains="oo").exists():
                    ret_text = d(textContains="oo many request").get_text()
                elif d(textContains="Invalid").exists():
                    ret_text = d(textContains="Invalid").get_text()
                elif d(textContains="to").exists():
                    ret_text = d(textContains="to").get_text()
                elif d(textContains="your").exists():
                    ret_text = d(textContains="your").get_text()
                self.log_signal.emit(f"失败。 检测到不是输入验证码页面 原因:{ret_text}")
                self.log_signal.emit("即将退出")
                return
            reer = d(textContains="sent").get_text()
            self.log_signal.emit(f"{reer}")
            for i in range(3):
                self.code_signal.emit()
                code = self.wait_for_code()
                code_input.set_text(code)
                self.log_signal.emit(f"输入验证码 {code}")
                time.sleep(2)
                if d(textContains="Invalid code").exists():
                    self.log_signal.emit(f"验证码错误, 请重新输入。失败次数{i+1}/3")
                    continue
                else:
                    d(text="ALLOW").click()
                    break
            self.log_signal.emit("登录成功")
            return
        except Exception as e:
            self.log_signal.emit(f"异常: {str(e)}")
        finally:
            return None

    def grant_app(self, app):
        permissions = [
            "android.permission.CAMERA",
            "android.permission.INTERNET",
            "android.permission.READ_CONTACTS",
            "android.permission.POST_NOTIFICATIONS",
        ]
        for permission in permissions:
            try:
                app.grant(permission, mode=GrantType.GRANT_ALLOW)
            except Exception:
                pass

    def wait_for_code(self):
        self.code_received = None
        while self.code_received is None:
            time.sleep(0.1)
        return self.code_received

    def set_code(self, code):
        self.code_received = code


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Telegram Login")
        self.resize(720, 600)

        self.phone_label = QLabel("Phone Number:", self)
        self.phone_entry = QLineEdit(self)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_entry)
        layout.addWidget(self.login_button)
        layout.addWidget(self.log_text)

        self.setLayout(layout)

    def log(self, message):
        self.log_text.append(message)

    def login(self):
        phone = self.phone_entry.text()
        self.login_thread = LoginThread(phone)
        self.login_thread.log_signal.connect(self.log)
        self.login_thread.code_signal.connect(self.request_code)
        self.login_thread.start()

    def request_code(self):
        code, ok = QInputDialog.getText(self, "验证码", "请输入验证码")
        if ok:
            self.login_thread.set_code(code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
