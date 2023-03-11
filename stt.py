import vosk
import sys
import sounddevice as sd
import queue
import json
import config




model = vosk.Model("model")
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback, player, fuzz, tts, alias):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        
        call = 0
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                
                callback(json.loads(rec.Result())["text"])
                call = 0
                
 
            elif call == 0:
                
                mas = eval(rec.PartialResult().strip())
                

                if mas['partial'].startswith(alias):
                    call = 1
                    

                    player.setVolume(15)
                     
                    tts.play()
                        
                    
                            
                
    
                    

                    
            
