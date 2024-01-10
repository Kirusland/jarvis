import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "names": ('джарвис'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('сейчас времени', 'который час'),
        "joke": ('расскажи анекдот')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["names"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['names']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Ошибка распозновния голоса!")
    except sr.RequestError as e:
        print("[log] Провверьте интернет соединение!")
    except sr.WaitTimeoutError:
        print("[log] Микрофон не подключен или не работает!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))


    elif cmd == 'joke':
        # рассказать анекдот
        speak("Пока не умею рассказывать анекдоты")

    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
# voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[4].id)

# forced cmd test
#speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

speak("Добрый день, сэр")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop