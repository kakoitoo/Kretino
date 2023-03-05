import vosk
import sys
import sounddevice as sd
import queue
import json




model = vosk.Model("model_small")
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback, fuzz, tts, alias):
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
                

                for x in alias:
                    vrt = fuzz.ratio(mas['partial'], x)
                    if vrt > 50:
                        call = 1
                        tts.play()
                        
                        break
                            
                
    
                    

                    
            
