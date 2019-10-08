from pydub import AudioSegment
from matplotlib import pyplot as plt
from numpy.lib import stride_tricks
from scipy import signal

import scipy.io.wavfile as wav
import warnings
import wave
import struct 
import numpy as np


class AudioGenerateService:
    def __init__(self):
        self.audio = []
        self.sample_rate = 44100
        self.freq_array = np.array([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88])
    
    def generic_note(self, freq, duration = 1000, volume = 1.0, octave = 2):
        freq *= octave
        duration  *= 2
        for x in range(int(duration  * (self.sample_rate / 1000.0))):
            self.audio.append(volume * np.sin(2 * np.pi * freq * ( x / self.sample_rate))) 
    
    def generic_silence(self, duration  = 250):
        for x in range(int(duration  * ( self.sample_rate / 1000.0))):
            self.audio.append(.0)
        
    def save_wav(self, file_name):
        wav_file = wave.open(file_name, 'w')
        wav_file.setparams((1, 2, self.sample_rate, len(self.audio), 'NONE', 'not compressed'))
        
        for sample in self.audio:
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))
        
        wav_file.close()
        pass
    
    def call(self):
        freq_array = self.freq_array
        for i in range(2):
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[3], duration = 250, octave = 2)
            self.generic_note(freq=freq_array[5], duration = 350, octave = 2)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[3], duration = 250, octave = 2)
            self.generic_note(freq=freq_array[5], duration = 350, octave = 2)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[1], duration = 150, octave = 1)
            self.generic_note(freq=freq_array[3], duration = 250, octave = 2)
            self.generic_note(freq=freq_array[4], duration = 350, octave = 2)
            self.generic_silence(duration = 250)
        self.save_wav('output.wav')
 
class AudioHistogram:
    def __init__(self):
        self.created_wav = AudioSegment.from_wav('output.wav')
        self.girei_wav = AudioSegment.from_wav('girei.wav')
        pass
        
    def combine(self):
        combine_wav = self.created_wav.overlay(self.girei_wav)
        combine_wav = combine_wav.fade_in(4000).fade_out(4000) 
        combine_wav.export('combine.wav', format = 'wav')
        pass        

    # def create_frequency_spectrogram(self, audioPath):
    #     pass
    #     sampleRate, samples = wav.read(audioPath)
    #     frequencies, times, spectogram = signal.spectrogram(samples, sampleRate)
    #     plt.pcolormesh(times * 1000, frequencies, 10 * np.log10(spectogram))
    #     plt.ylabel('Frequency [Hz]')
    #     plt.xlabel('Time [Ms]')
    #     plt.show()
    #     pass

    # def create_amplitude_spectogramm(self, audioPath):
    #     sample_rate, samples = wav.read(audioPath)

    #     samples = samples / (2. ** 15)
    #     sample_points = float(samples.shape[0])
    #     mono_audio = samples[:, 0]

    #     times = np.arange(0, sample_points, 1) / sample_rate * 1000

    #     plt.plot(times, mono_audio, color='R')
    #     plt.ylabel('Amplitude')
    #     plt.xlabel('Time [ms]')
    #     plt.show()

    def stft(self, sig, frameSize, overlapFac=0.5, window=np.hanning):
        win = window(frameSize)
        hopSize = int(frameSize - np.floor(overlapFac * frameSize))
        
        samples = np.append(sig, np.zeros(int(np.floor(frameSize/2.0))))
        cols = int(np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1)
        samples = np.append(samples, np.zeros(frameSize))
        
        frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
        frames *= win
        
        return np.fft.rfft(frames)    
        
    def logscale_spec(self, spec, sr=44100, factor=20.):
        timebins, freqbins = np.shape(spec)

        scale = np.linspace(0, 1, freqbins) ** factor
        scale *= (freqbins-1)/max(scale)
        scale = np.unique(np.round(scale))
        
        newspec = np.complex128(np.zeros([timebins, len(scale)]))
        for i in range(0, len(scale)):
            if i == len(scale)-1:
                newspec[:,i] = np.sum(spec[:,int(scale[i]):], axis=1)
            else:        
                newspec[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i+1])], axis=1)
        
        allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
        freqs = []
        for i in range(0, len(scale)):
            if i == len(scale)-1:
                freqs += [np.mean(allfreqs[int(scale[i]):])]
            else:
                freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i+1])])]
        
        return newspec, freqs

    def plotstft(self, audiopath, binsize=2**10, plotpath=None, colormap="jet"):
        print(audiopath)
        samplerate, samples = wav.read(audiopath)
        s = self.stft(samples, binsize)
        
        sshow, freq = self.logscale_spec(s, factor=1.0, sr=samplerate)
        ims = 20.*np.log10(np.abs(sshow)/10e-6)
        
        timebins, freqbins = np.shape(ims)
        
        plt.figure(figsize=(15, 7.5))
        plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
        plt.colorbar()

        plt.xlabel("time (s)")
        plt.ylabel("frequency (hz)")
        plt.xlim([0, timebins-1])
        plt.ylim([0, freqbins])

        xlocs = np.float32(np.linspace(0, timebins-1, 5))
        plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
        ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
        plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])
        
        if plotpath:
            plt.savefig(plotpath, bbox_inches="tight")
        else:
            plt.show()
            
        plt.clf()

    def call(self):
        self.plotstft('girei.wav')
        self.plotstft('output.wav')
        self.plotstft('combine.wav')

        pass

    
if __name__ == '__main__':
    # AudioGenerateService().call()
    AudioHistogram().call()
