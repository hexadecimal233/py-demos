import pygame

from scipy.fft import fft
from scipy.io import wavfile
from scipy import interpolate
import numpy as np

# 音频输入处理~

filename = "D:\\Storage\\projects\\$我的$\\Surfin'\\Surfin' 4.wav"
w, h = 1800, 900  # 窗口大小
rate = 20  # 单次采样长度


samplerate, wav_data = wavfile.read(filename)

sample_delta = int(samplerate / rate * 2)  # 切片长度，x2是因为奈奎斯特频率（说实话这我也不知道是啥先x2再说）
max_freq = int(sample_delta / 2)

mono_data = wav_data[:, 0]


# 音频切片
def get_chopped(chop_start_time: float = 0):  # 毫秒
    chop_start = int(chop_start_time * samplerate / 1000)
    chop_end = chop_start + sample_delta

    # 切割原始采样
    chop = mono_data[chop_start:chop_end]

    # 填充空白，防止绘制时出错
    overread_samples = chop_end - len(mono_data)
    if overread_samples > 0:
        chop = np.pad(chop, (0, overread_samples), mode="constant")

    return chop


# Resample!
def downsample(chop, new_samplerate):
    duration = len(chop) * samplerate

    # 为新音频创建采样时间戳
    time_old = np.linspace(0, duration / samplerate, duration)

    num_downsampled_points = int(duration * new_samplerate / samplerate)
    time_new = np.linspace(0, duration / samplerate, num_downsampled_points)

    # 插值
    interpolator = interpolate.interp1d(time_old, chop)
    downsampled = interpolator(time_new)
    return downsampled


# 可视化频域图
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Audio File Visualizer')

music = pygame.mixer.Sound(filename)
music.play()

total_time = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # 显示逻辑
    chop = get_chopped(total_time)

    # 时域转频率 -- 傅里叶变换
    fft_data = fft(chop)

    # 将FFT系数转换为频率
    frequencies = abs(fft_data) * (1 / samplerate)
    frequencies = frequencies[:max_freq]
    # frequencies0 = downsample(frequencies, w)

    for i in range(0, max_freq - 1):
        j = w * i / max_freq
        pygame.draw.line(screen, (255, 255, 255), (j, h - frequencies[i]), (j, h - frequencies[i + 1]))



    pygame.display.flip()
    total_time += clock.tick(60)  # 60fps

pygame.quit()
