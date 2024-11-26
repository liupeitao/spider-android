from lamda.client import Device
from pydantic import BaseModel ,Field
from lamda.client import Point
from typing import Optional
import time
from db.models import App



def let_talk_search():
    time.sleep(1)


let_talk_search()



class PhoneNumber(BaseModel):
    phone: str = Field(..., title="phone number", description="phone number")

NAME = "LetsTalk"

INTER_URL_PATTERN = "api.m.jd.com/api"
def get_device():
    d = Device("192.168.9.6")
    return d

class LetTalk_Spider():
    def __init__(self, item:App):
        self.d = get_device()
        print(item)
        pass

    def crawl_chat(self, friend: Optional[str] = None):
        self.d.start_activity(**{'component': 'com.onelab.securecomm/.ui2.view.MainActivity'})
        
    @classmethod
    def check_phone(self, phones: list[PhoneNumber]):
        self.d.start_activity(**{'component': 'com.onelab.securecomm/.ui2.view.AddContactActivity'})    
        time.sleep(2)
        e = self.d(text='电话')
        e.click()
        ele = self.d(text='电话号码')
        ele.set_text(phones[0].phone)

        s_btn = self.d(resourceId="com.onelab.securecomm:id/btnSearchMember")        
        s_btn.click()
        ele.clear_text_field()
    def _chat_tab(self):
        chat_tab = self.d(resourceId="com.onelab.securecomm:id/navigation_chat")
        chat_tab.click()
    def crawl_all_chat(self):
        self.d.start_activity(**{'component': 'com.onelab.securecomm/.ui2.view.MainActivity'})
        self._chat_tab()
        time.sleep(2)
        f = self.d(resourceId="com.onelab.securecomm:id/mainFrame")
        chats_res = []
        for dialog in f.info_of_all_instances():
            p = bounds_to_point(dialog.bounds.top, dialog.bounds.bottom, dialog.bounds.right)
            self.d.click(p)
            time.sleep(2)
            for i in range(3):
                time.sleep(2)
                s = self.ff()
                self.scroll()
                time.sleep(2)
                print(s)
            chats_res.append(s)
            time.sleep(2)
            self.d.start_activity(**{'component': 'com.onelab.securecomm/.ui2.view.MainActivity'})
            time.sleep(1)
        return chats_res

    def scroll(self, step=66):
        self.d().scroll_from_top_to_bottom(step)

    def ttt(self):
        self.d.remove_all_watchers()
        self.d.set_watcher_loop_enabled(True)
        
    def _get_friend_name(self):
        friend_name = self.d(resourceId="com.onelab.securecomm:id/toolbarTitleTxt")
        r = friend_name.get_text()
        return r
    def ff(self):
        friend_name = self._get_friend_name()
        if friend_name is None:
            raise Exception("friend name not found")
        my_message = self.d(resourceId="com.onelab.securecomm:id/textMessageRight")
        timer = self.d(resourceId="com.onelab.securecomm:id/textTimeRight")
        you_message = self.d(resourceId="com.onelab.securecomm:id/textMessageLeft")
        you_timer = self.d(resourceId="com.onelab.securecomm:id/textTimeLeft")

        messages = my_message.info_of_all_instances()
        timers = timer.info_of_all_instances()
        your_messages = you_message.info_of_all_instances()
        your_timers = you_timer.info_of_all_instances()
        result = []
        try:
            for i in range(my_message.count()):
                msg = {}
                m = messages[i].text
                msg['text']=m
                msg['from'] = 'me'
                msg['to'] = friend_name
                try:
                    msg['time'] = timers[i].text
                except Exception:
                    msg['time'] = ""
                print(msg)
                print(friend_name)
                result.append(msg)
        except Exception as e:
            pass
        
        try:
            for i in range(your_messages.count()):
                msg = {}
                m = your_messages[i].text
                msg['text']=m
                msg['from'] = friend_name
                msg['to'] = 'me'
                try:
                    msg['time'] = your_timers[i].text
                except Exception:
                    msg['time'] = ""
                result.append(msg)
        except Exception as e:
            pass
        return result

def bounds_to_point(top, bottom, right):
    return Point(x=int(right/2), y=int((top + bottom) / 2))
