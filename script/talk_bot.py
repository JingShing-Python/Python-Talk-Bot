# detect voice
import speech_recognition
# generate voice
from pygame import mixer
import tempfile
from gtts import gTTS

# time
from datetime import datetime
from time import sleep

class Talk_Bot:
    def __init__(self, mode = 'voice1'):
        # speaker init
        mixer.init()
        # mode: voice1, voice2, text
        self.mode = mode
        # recognizer init    
        self.recognizer = speech_recognition.Recognizer()
        self.master = None

    def line_speaker(self, texts,lang='zh-tw'):
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=texts,lang=lang)
            tts.save("{}.mp3".format(fp.name))
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play()
        print(texts)

    def listener(self):
        if self.mode == 'voice1':
            result = None
            while(result == None):
                with speech_recognition.Microphone() as source:
                    # recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                try:
                    result = self.recognizer.recognize_google(audio,language = 'zh-tw')
                except:
                    continue
            print(result)
            return result
        elif self.mode == 'text':
            result = input()
            return result

    def order_manage(self):
        self.line_speaker('您好，很高興為您服務，請問要做些甚麼？')
        while(1):
            order_line = self.listener()

            # 問好
            if '你好' in order_line:
                self.line_speaker('你好。')
                if self.master!=None:
                    self.line_speaker('我的'+self.master)
            
            # 我的名字是
            elif '我的名字是' in order_line or '我是' in order_line:
                self.master=order_line.split('是')[-1]
                self.line_speaker('你就是我的Master嗎？'+self.master)

            # 有什麼吃的？
            elif '吃的' in order_line:
                eat_count = 0
                self.line_speaker('想吃飯還是麵？')
                while(eat_count<2):
                    order_line = self.listener()
                    if '飯' in order_line:
                        self.line_speaker('我們沒有飯')
                        eat_count+=1
                    elif '麵' in order_line:
                        self.line_speaker('我們沒有麵')
                        eat_count+=1
                    else:
                        self.line_speaker('我們沒有這個')
                self.line_speaker('我們有水餃')
                continue

            # 機率論
            elif '機率' in order_line:
                self.line_speaker('請描述你所要計算的機率問題。講完後請說我說完了')
                while(not '完' in order_line):
                    order_line = self.listener()
                self.line_speaker('請問所求為會發生還是不會發生的機率？')
                order_line = self.listener()
                while(not '會' in order_line):
                    order_line = self.listener()
                if '不會' in order_line:
                    self.line_speaker('二分之一')
                else:
                    self.line_speaker('二分之一')

            # 問時間，幾點了
            elif ('時間' in order_line) or ('幾點' in order_line):
                now = datetime.now()
                res_text = '現在時間是 %d 點 %d 分 %d 秒' % (now.hour, now.minute, now.second)
                self.line_speaker(res_text)

            # 離開
            elif '離開' in order_line or '結束' in order_line:
                self.line_speaker('很高興為您服務，很期待您下次光顧。')
                sleep(6)
                break
            
            # not any option upper
            else:
                self.line_speaker('不好意思，請再說一次。')
            
    def __call__(self):
        self.order_manage()

if __name__ == '__main__':
    talk_bot = Talk_Bot('text')
    talk_bot()