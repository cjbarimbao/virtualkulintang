import pygame
import time

pygame.mixer.pre_init()
pygame.init()
sig = pygame.mixer.Sound("Mgd_Kulintangan_301_P1_N0_S1.wav")
start = time.time()
channel = sig.play()
while channel.get_busy():
    pygame.time.wait(100)
end = time.time()
print("Execution time: ", end - start)