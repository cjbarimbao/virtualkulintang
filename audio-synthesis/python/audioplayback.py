import pygame
import time
import sounddevice as sd
import soundfile as sf  

pygame.mixer.pre_init()
pygame.init()
sig = pygame.mixer.Sound("Mgd_Kulintangan_301_P1_N0_S1.wav")
start = time.time()
channel = sig.play()
end = time.time()
print("Execution time: ", end - start)


# read wav file using sounddevice
data, samplerate = sf.read('Mgd_Kulintangan_301_P1_N0_S1.wav')
start = time.time()
sd.play(data, samplerate)
end = time.time()
sd.wait()
print("Execution time: ", end - start)