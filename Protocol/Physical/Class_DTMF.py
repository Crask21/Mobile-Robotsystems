import numpy as np
import matplotlib.pyplot as plt
#import sounddevice as sd
import pygame 
import time
from random import randrange
import threading
import wave


def CharListToInt(list):
    hex_dict = {
            '0' : 0x0,
            '1' : 0x1,
            '2' : 0x2,
            '3' : 0x3,
            '4' : 0x4,
            '5' : 0x5,
            '6' : 0x6,
            '7' : 0x7,
            '8' : 0x8,
            '9' : 0x9,
            'a' : 0xA,
            'b' : 0xB,
            'c' : 0xC,
            'd' : 0xD,
            'e' : 0xE,
            'f' : 0xF
            }
        
    res =  []
    for i in range(len(list)):
        res.append(hex_dict[list[i][-1]])
    
    return res


class SEND:

    def __init__(data, fs, amplitude, p_fade, baud, syn, sound_media = 'PyGame', mono=False):

        # DTMF setup
        data.fs = fs
        data.amplitude = amplitude
        data.p_fade = p_fade

        # User setting variables
        data.baud = baud
        data.duration = 1/baud
        data.sound_media = sound_media
        data.sync = syn

        data.mono = mono
        
        
       
        data.FFT = []

        # Initialize DMTF tone list
        data.dtmf = []
        data.DTMF_init()

    def setBaud(data,baud):
        data.baud = baud
        data.duration = 1/baud
        data.DTMF_init()
    
    def setFade(data, fade):
        data.p_fade = fade
        data.DTMF_init()

# 
    def silentDTMF(data,mute = False,dur = 2):
            silence = data.makeSIN(1,dur,2,2,data.fs,0.4)
            
            if not mute: 
                data.play_PyGame(silence,data.mono)
            return silence

# Send package of hexi decimals
    def send_package(data, pack, mute = True,plot = False, save_wav = False):
        
        package = [0,0,0,0,0,0,*pack,0,0,0,0,0]

        data.soundwave = np.arange(0,1)
        
        if mute:
            package = data.synchroniazation(data.sync) + package
            #data.silentDTMF()
            #print(package)

        if plot:
            package = pack

        # Convert package into sound array
        for hex in package:
            #data.soundwave = [*data.soundwave, *data.dtmf[hex]]
            data.soundwave = np.concatenate((data.soundwave,data.dtmf[hex]))

            # Delete end spike
            data.soundwave[-1] = 0

        #data.soundwave = [*data.silentDTMF(mute=True),*data.soundwave]

        if data.sound_media == 'PyGame':
            # Play through PyGame
            #data.silentDTMF(dur=0.5)
            data.play_PyGame(data.soundwave, data.mono)

            # Play through Sounddevice
        elif data.sound_media == 'SD':
            data.play_SD(data.soundwave)
        
        if save_wav:
            data.savewav(data.soundwave)


# Plot the package as DTMF tones
    def plot_last_package(data, dur = False, custom = False,curve='o', xlabel = "Time", ylabel="Amplitude",title="DTMF 0x0 sampled at 44100Hz"):

        package_size = round(len(data.soundwave)/data.fs/data.duration)
        
        time = np.arange(0, data.duration * package_size, 1/data.fs) if not dur else np.arange(0, dur , 1/data.fs)
        

        for ig in range((len(data.soundwave) - len(time))):
            data.soundwave = np.delete(data.soundwave,-1)
        #data.soundwave = np.delete(data.soundwave,-1)

        
        if custom:
            data.soundwave = 5000 * np.sin(2*np.pi*1209*time) + 5000 * np.sin(2*np.pi*697*time)

        plt.plot(time,data.soundwave,curve)#'r--' 'o'
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()


# Plot fft
    def plot_fft(data):

        package_size = round(len(data.FFT)/data.fs/data.duration)

        time = np.arange(0, data.duration * package_size, 1/data.fs)
        #data.FFT = np.delete(data.FFT,-1)

        plt.plot(data.FFT,'r--')
        plt.ylabel('some numbers')
        plt.show()
    
        
# Make a DTMF tone
    def makeDTMF(data,freq1,freq2):
        amplitude = data.amplitude
        dur = 1/data.baud
        f_sample = data.fs
        percentage_fade= data.p_fade

        # Turn frequencies into functions 
        time = np.arange(0, dur, 1/f_sample)
        xi = amplitude * np.sin(2*np.pi*freq2*time) + amplitude * np.sin(2*np.pi*freq1*time)   
        
        # Fadeeeeeee #
        number_of_faded_points = int(percentage_fade * f_sample)
        if percentage_fade > 1:
            number_of_faded_points = int(percentage_fade/100 * dur * f_sample)

        fade = np.linspace(0,1,num=number_of_faded_points)
        fade_end = np.linspace(1,0,num=number_of_faded_points)

        data.FFT.append(np.fft.fft(xi))

        for j in range(number_of_faded_points):
            xi[j] = xi[j] * fade[j]

        #print(xi[-1*number_of_faded_points:])

        for j in np.arange(-1*number_of_faded_points,-1):    
            xi[j] = xi[j] * fade_end[j]

        #print(xi[-1*number_of_faded_points:-1])

        # Fadeeeeeee #
        


        return xi

# Make double sinusoid
    def makeSIN(data,amplitude,dur,freq1,freq2,f_sample, percentage_fade):
         # Turn frequencies into functions 
            time = np.arange(0, dur, 1/f_sample)
            xi = amplitude * np.sin(2*np.pi*freq2*time) + amplitude * np.sin(2*np.pi*freq1*time)   
            
            # Fadeeeeeee #
            number_of_faded_points = int(percentage_fade * f_sample)
            if percentage_fade > 1:
                number_of_faded_points = int((percentage_fade/1000000) / dur * f_sample)

            fade = np.linspace(0,1,num=number_of_faded_points)
            fade_end = np.linspace(1,0,num=number_of_faded_points)

            data.FFT.append(np.fft.fft(xi))

            for j in np.arange(number_of_faded_points):
                xi[j] = xi[j] * fade[j]

            #print(xi[-1*number_of_faded_points:])

            for j in np.arange(-1*number_of_faded_points,-1):    
                xi[j] = xi[j] * fade_end[j]    

            #print(xi[-1*number_of_faded_points:-1])

            # Fadeeeeeee #
            

    
            return xi

# Setup DTMF tones in list
    def DTMF_init(data):


        # DTMF frequencies
        dtmf_freq = [[1209,697], # 0
                    [1336,697],  # 1
                    [1477,697],  # 2
                    [1633,697],  # 3
                    [1209,770],  # 4
                    [1336,770],  # 5
                    [1477,770],  # 6
                    [1633,770],  # 7
                    [1209,852],  # 8
                    [1336,852],  # 9
                    [1477,852],  # A
                    [1633,852],  # B
                    [1209,941],  # C
                    [1336,941],  # D
                    [1477,941],  # E
                    [1633,941]]  # F

        data.dtmf = []

        for i in np.arange(len(dtmf_freq)):
            data.dtmf.append(data.makeDTMF(dtmf_freq[i][0], dtmf_freq[i][1]))

# Save soundwave as soundfile
    def savewav(data, soundwave):
        # open new wave file
        pygame.mixer.init(frequency=data.fs, size=-16, channels=1)

        # Convert list to numpy array
        buffer = np.array(soundwave,dtype=np.int16)

        # Dublicate sound channel for stereo
        buffer = np.repeat(buffer.reshape(len(soundwave), 1), 2, axis = 1)

        # Create sound object
        sound = pygame.sndarray.make_sound(buffer)

        sfile = wave.open('pure_tone.wav', 'w')

        # set the parameters
        sfile.setframerate(data.fs)
        sfile.setnchannels(2)
        sfile.setsampwidth(2)

        # write raw PyGame sound buffer to wave file
        sfile.writeframesraw(sound.get_raw())

        # close file
        sfile.close()

# Play the sound through either PyGame or Sounddevice
    def play_PyGame(data, soundwave, mono = False):
        # Initialize PyGame mixer
        pygame.mixer.init(frequency=data.fs, size=-16, channels=1)

        # Convert list to numpy array
        buffer = np.array(soundwave,dtype=np.int16)

        # Dublicate sound channel for stereo
        if not mono:
            buffer = np.repeat(buffer.reshape(len(soundwave), 1), 2, axis = 1)

        # Create sound object
        sound = pygame.sndarray.make_sound(buffer)

        # Play the sound
        sound.play()

        # Delay for the duration of the sound
        pygame.time.wait(int(sound.get_length() * 1000)) 

    

    # Synchroniazation
    def synchroniazation(data,num, mute = False):
        sync = []
        for i in range(num):
            sync.append(0xA)
            sync.append(0xB)
        sync.append(0xC)
        #sync.append(0xC)
        #data.send_package(sync,mute)
        return sync

        # Create a random package
    def rand_pack(data,num):
        size = 16
        random_data = []
        for i in range(num):
            random_data.append(randrange(size))
        print(random_data)
        return random_data

    def compare(data, original, recieved, compare = True):

        dif = len(recieved) - len(original)

        if len(recieved) > len(original):
                recieved2 = recieved.copy()
                recieved = recieved[:len(recieved) - dif]


        if original == recieved:
            print('100% match')
            print("Original: ",original)
            
            print("Recieved: ",recieved2)
            return 100
        


        elif compare:
            count = 0

            length = len(original) if dif >= 0 else len(recieved)

            for i in range(length):
                if recieved[i] == original[i]:
                    count += 1
            accuracy = count/len(original)*100
            
            print(accuracy,'% match.', len(original) - count, 'errors')
            print('Original:',original)
            print('Recieved:',recieved)
            return accuracy


        else:
            send_count =[]
            for i in range(16):
                send_count.append(original.count(i))

            recieved_count = []
            for i in range(16):
                recieved_count.append(recieved.count(i))

            count = 0
            for i in range(16):
                
                if recieved_count[i] == send_count[i]:
                    count += 1



            print(count/16*100,'% count match. ', count, 'errors')
            print(original)
            print(recieved)
            return count/16*100





## DTMF Settings
#fs = 4000
#amplitude = 15000
#media = 'PyGame' # 'SD'
#fade_P = 0.005
#baud_rate = 1
#syn = 0
## SYNC'
#send=SEND(fs, amplitude, fade_P, baud_rate,syn, media,mono=False)
#
#send.send_package([0,1,0], save_wav=True)
#