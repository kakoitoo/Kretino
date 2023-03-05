import config
import threading
import time
import stt
import tts
from rapidfuzz import fuzz
import datetime
import chisla
import webbrowser
import musik
from pygame import mixer
mixer.init()

mus = {
    'name': None,
    'author': None,
    'auto':False,
    'track_num': 0,
    'vol': 1.0,
}



print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")

def autoplay():
    global mus
    if not mixer.music.get_busy() and mus['auto'] == True:

        mixer.music.unload()
        mus['track_num'] += 1
        #поиск по имени +- автор

        if mus['name'] != None:
            
            if musik.play(f"{mus['name']} {mus['author'] if mus['author'] != None else ''}", mixer, num = mus['track_num']) == False:
                
                mus['auto'] = False
                mus['track_num'] = 0
            else:
                print(f"Сейчас играет: {mus['name']} {mus['author'] if mus['author'] != None else ''}")


        #поиск только по автору
        elif mus['name'] == None:
            
            if musik.play(mus['author'], mixer, num = mus['track_num'],  a = True) == False:
                mus['auto'] = False
                mus['track_num'] = 0
            else:
                print(f"Сейчас играет: {mus['name']} {mus['author'] if mus['author'] != None else ''}")

def va_respond(voice: str):
    autoplay()
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        
        cmd, text = recognize_cmd(filter_cmd(voice))

        
        execute_cmd(cmd['cmd'], text)


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(text: str):
    rc = {'cmd': '', 'percent': 0}
    if 'поставь' in text or 'включи' in text or 'играй' in text:
        rc['cmd'] = 'startmus' 
        return (rc, text)
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(text, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    if rc['percent'] < 30:
        rc['cmd'] = 'what' 

    return (rc, text)


def execute_cmd(cmd: str, text: str):
    global mus
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "и открывать браузер"
        tts.va_speak(text)
    
    elif cmd == 'i':
        text = "Привет... я подсяду"
        tts.va_speak(text)

    elif cmd == 'what':
        text = "Моя твоя не понимать"
        tts.va_speak(text)

    elif cmd == 'startmus':
        a = text.find('поставь') if text.find('поставь')!= -1 else 999
        b = text.find('играй') if text.find('играй')!= -1 else 999
        c = text.find('включи') if text.find('включи')!= -1 else 999
        z = min(a, b, c)

         
        print(text)
        if text[z] == 'п':
            musAndAuthor = text[z+8:]
        elif text[z] == 'и':
            musAndAuthor = text[z+6:]
        elif text[z] == 'в':
            musAndAuthor = text[z+7:]

        if 'автор' in musAndAuthor:
            z = musAndAuthor.split('автор')
            mus['name'] = z[0]
            if len(z) > 1:
                mus['author'] = 'автор'.join(z[1:])
            else:
                mus['author'] = None


            if mus['name'].strip() == "":
                mus['name'] = None
        else:
            mus['name'] = musAndAuthor
            mus['author'] = None

        

        
        

        

        #перезагрузка если занят
        try:
            if mixer.music.get_busy(): 
                mixer.music.stop() 

            mixer.music.unload()
        except: pass

        #поиск по имени +- автору
        if mus['name'] != None:
            

            if musik.play(f"{mus['name']} {mus['author'] if mus['author'] != None else ''}", mixer, num = mus['track_num']) == False:
                text = "Я ничего не нашел"
                tts.va_speak(text)
            else:
                text = 'Моё сердце бьётся в ритме диско!'
                tts.va_speak(text)
                mus['auto'] = True
                

        #поиск только по автору
        elif mus['name'] == None and mus['author'] != None:
            if musik.play(mus['author'], mixer, num = mus['track_num'],  a = True) == False:
                text = "Я ничего не нашел"
                tts.va_speak(text)
                

            else:
                text = 'Моё сердце бьётся в ритме диско!'
                tts.va_speak(text)
                mus['auto'] = True
                
        
        else:
            text = f"Я не услышал, повтори"
            tts.va_speak(text)


    elif cmd == 'nowplaing':
        if mus['name'] != None:
            text = f"Сейчас играет {mus['author'] if mus['author']!=None else ''} ... {mus['name']}"
            tts.va_speak(text)

        elif mus['author'] != None:
            text = f"Сейчас играет поток {mus['author'] if mus['author']!=None else ''}"
            tts.va_speak(text)

        else:
            text = "Сейчас ничего не играет... Рассказать шутку про глухих?"
            tts.va_speak(text)


    elif cmd == 'royal':
        text = 'О Боже! Что он делает?! Кретино! Тенти остатенти! Дольваре дес культе, дес фрути та дьяволо! Пиодоро апире! Пароле бова вита, дольче вита э финита! Мама мия!' 
        tts.va_speak(text)
        
    elif cmd == 'bb':
        text = 'чэнж дээ воорд ... май фаайнал мээсэдж ... гудбаай' 
        tts.va_speak(text)
        quit()

    elif cmd == 'stopmus':
        
        if mixer.music.get_busy():
            mixer.music.pause()
            mus['auto'] = False
            
        else:
            text = 'Музыка не играет' 
            tts.va_speak(text)


    elif cmd == 'cont':
        
        if not mixer.music.get_busy():
            try:
                mixer.music.unpause()
                mus['auto'] = True
            except:
                text = 'Нечего продолжать' 
                tts.va_speak(text)

        else:
            text = 'Музыка уже играет' 
            tts.va_speak(text)

    elif cmd == 'timer':
        minutes = chisla.anti_chis(text)

        def set_timer(n: int):
            print(f'таймер на {n} минут')
            time.sleep(n*60)
            if mixer.music.get_busy(): mixer.music.pause()
            mixer.music.unload()
            mixer.music.load('timer.mp3')
            mixer.music.play()
        
        threading.Thread(target=set_timer, args=[minutes]).start() if minutes!=0 else 0


    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + chisla.chis(now.hour) + " часов" + chisla.chis(now.minute) + "минут"
        tts.va_speak(text)



    elif cmd == 'open_browser':
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open("http://python.org")

    
    
    
    
    




# начать прослушивание команд
stt.va_listen(va_respond, fuzz, tts, config.VA_ALIAS)