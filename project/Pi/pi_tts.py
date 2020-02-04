# pip install gTTS
# pip install pygame
# Reference Link : https://wikidocs.net/15214
import pygame
from gtts import gTTS
pygame.mixer.init()

text ="경고! 비확인 운전자!"

tts = gTTS(text=text, lang='ko')
tts.save("helloEN.mp3")

music_file = "helloEN.mp3"
freq = 24000    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
bitsize = -16   # signed 16 bit. support 8,-8,16,-16
channels = 1    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)

# default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.load(music_file)
pygame.mixer.music.play()

