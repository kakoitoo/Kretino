import torch
import sounddevice as sd
import time
import threading
import simpleaudio as simple_audio 
 
filename = 'ok.wav' 

def play():
    wave_object = simple_audio.WaveObject.from_wave_file(filename) 
    play_object = wave_object.play() 
    play_object.wait_done()

torch._C._jit_set_profiling_mode(False)


language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000 
speaker = 'aidar' 
put_accent = True
put_yo = True
device = device = "cuda"
text = "Скибиди йес йес йес йес"

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


# воспроизводим

def aplay():
    threading.Thread(target = play).start()
    

def va_speak(what: str):
    threading.Thread(target = va_speak_th, args=(what, )).start()

def va_speak_th(what: str):
    try:
        audio = model.apply_tts(text=what+"..",
                                speaker=speaker,
                                sample_rate=sample_rate,
                                put_accent=put_accent,
                                put_yo=put_yo)

        sd.play(audio, sample_rate * 1.05)
        time.sleep((len(audio) / sample_rate) + 0.5)
        sd.stop()
    except Exception as e:
        print("Ашипка:", e)




audio = model.apply_tts(text=text+"..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)
                            
va_speak(text)