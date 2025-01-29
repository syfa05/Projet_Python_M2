import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
from scipy.signal import stft
"""
# Parameters
Fa = 10  # Frequency of the carrier (Hz)
Fm = 1   # Frequency of modulation (Hz)
Beta = 2 # Modulation index (dimensionless)
T = 5    # Duration of the signal (s)
Fs = 1000 # Sampling frequency (Hz)

# Time vector
t = np.linspace(0, T, int(Fs * T))

# Instantaneous frequency
instantaneous_frequency = Fa + Beta * Fm * np.sin(2 * np.pi * Fm * t)

# Time-frequency representation (TFCT)
plt.figure(figsize=(10, 6))
plt.plot(t, instantaneous_frequency, label="Instantaneous Frequency")
plt.axhline(Fa, color='gray', linestyle='--', label=r"$F_a$ (Carrier Frequency)")
plt.axhline(Fa + Beta * Fm, color='red', linestyle='--', label=r"$F_a + \beta F_m$")
plt.axhline(Fa - Beta * Fm, color='blue', linestyle='--', label=r"$F_a - \beta F_m$")

# Plot aesthetics
plt.title("Time-Frequency Representation of FM Signal")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

# Paramètres
Fs = 1000  # Fréquence d'échantillonnage
T = 2.0    # Durée totale
t = np.linspace(0, T, int(Fs * T))
F1 = 10.0  # Fréquence du cosinus
tau = 1.0  # Instant du saut

# Génération du signal
x1 = np.cos(2 * np.pi * F1 * t)
x1[t >= tau] += 2 * np.cos(2 * np.pi * F1 * t[t >= tau])  # Amplitude triple après tau

# Calcul STFT
f, t_spec, Zxx = stft(x1, fs=Fs, nperseg=256, noverlap=200)

# Affichage
plt.pcolormesh(t_spec, f, np.abs(Zxx), shading='gouraud')
plt.title('TFCT de x₁(t) - Raie à F1 avec saut d\'amplitude')
plt.ylabel('Fréquence [Hz]')
plt.xlabel('Temps [s]')
plt.ylim(0, 20)
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Parameters for x1(t)
F1 = 10  # Frequency of the cosine (Hz)
tau = 2  # Time shift for the step function (s)
T = 5    # Duration of the signal (s)
Fs = 1000 # Sampling frequency (Hz)

# Time vector
t = np.linspace(0, T, int(Fs * T))

# Signal x1(t): Before and after tau
signal_x1 = np.cos(2 * np.pi * F1 * t) + 2 * (t >= tau) * np.cos(2 * np.pi * F1 * t)

# Time-frequency representation (conceptual)
time_segments = np.arange(0, T, 0.1)
frequencies = [F1 if t_i < tau else [0, F1, 2 * F1] for t_i in time_segments]

# Plot the time-frequency representation
plt.figure(figsize=(10, 6))
for i, t_i in enumerate(time_segments):
    if isinstance(frequencies[i], list):
        for freq in frequencies[i]:
            plt.plot([t_i, t_i + 0.1], [freq, freq], color='blue')
    else:
        plt.plot([t_i, t_i + 0.1], [frequencies[i], frequencies[i]], color='blue')

plt.axvline(x=tau, color='red', linestyle='--', label="$t=\\tau$ (Step Change)")
plt.title("Time-Frequency Representation of $x_1(t)$")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Paramètres
Fc = 100.0  # Fréquence porteuse
Fs = 1000  # Fréquence d'échantillonnage
Ffm = 5.0    # Fréquence de modulation
beta = 5.0   # Indice de modulation
T = 2.0      # Durée

t = np.linspace(0, T, int(Fs * T))
phi = 2 * np.pi * Fc * t + beta * np.sin(2 * np.pi * Ffm * t)  # Phase FM
x2 = np.cos(phi)

# Calcul STFT
f, t_spec, Zxx = stft(x2, fs=Fs, nperseg=512, noverlap=450)

# Affichage
plt.pcolormesh(t_spec, f, np.abs(Zxx), shading='gouraud')
plt.title('TFCT de x₂(t) - FM autour de Fc')
plt.ylabel('Fréquence [Hz]')
plt.xlabel('Temps [s]')
plt.ylim(Fc - 20, Fc + 20)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Parameters for x2(t)
Fa = 10  # Frequency of the carrier (Hz)
Fm = 1   # Frequency of modulation (Hz)
Beta = 2 # Modulation index (dimensionless)
T = 5    # Duration of the signal (s)
Fs = 1000 # Sampling frequency (Hz)

# Time vector
t = np.linspace(0, T, int(Fs * T))

# Instantaneous frequency
instantaneous_frequency = Fa + Beta * Fm * np.sin(2 * np.pi * Fm * t)

# Plot the time-frequency representation
plt.figure(figsize=(10, 6))
plt.plot(t, instantaneous_frequency, label="Instantaneous Frequency")
plt.axhline(Fa, color='gray', linestyle='--', label=r"$F_a$ (Carrier Frequency)")
plt.axhline(Fa + Beta * Fm, color='red', linestyle='--', label=r"$F_a + \beta F_m$")
plt.axhline(Fa - Beta * Fm, color='blue', linestyle='--', label=r"$F_a - \beta F_m$")

# Plot aesthetics
plt.title("Time-Frequency Representation of $x_2(t) = \\cos(2\\pi F_a t + \\beta \\sin(2\\pi F_m t))$")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print(mean(instantaneous_frequency))

import numpy as np
import matplotlib.pyplot as plt

# Parameters for x3(t)
Fa = 10   # Frequency of the carrier (Hz)
Fm = 1    # Frequency of modulation (Hz)
Fam = 0.5 # Frequency of amplitude modulation (Hz)
Beta = 2  # Modulation index (dimensionless)
T = 5     # Duration of the signal (s)
Fs = 1000 # Sampling frequency (Hz)

# Time vector
t = np.linspace(0, T, int(Fs * T))

# Instantaneous frequency for the carrier with phase modulation
instantaneous_frequency = Fa + Beta * Fm * np.sin(2 * np.pi * Fm * t)

# Amplitude modulation factor
am_factor = 1 + 0.5 * np.cos(2 * np.pi * Fam * t)

# Plot the time-frequency representation
plt.figure(figsize=(10, 6))
plt.plot(t, instantaneous_frequency * am_factor, label="Instantaneous Frequency with AM")
plt.axhline(Fa, color='gray', linestyle='--', label=r"$F_a$ (Carrier Frequency)")
plt.axhline(Fa + Beta * Fm, color='red', linestyle='--', label=r"$F_a + \beta F_m$")
plt.axhline(Fa - Beta * Fm, color='blue', linestyle='--', label=r"$F_a - \beta F_m$")

# Plot aesthetics
plt.title(r"Time-Frequency Representation of $x_3(t) = [1 + 0.5 \cos(2\pi F_{am} t)] \cos(2\pi F_a t + \beta \sin(2\pi F_m t))$")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Parameters for x1(t)
Fc = 10   # Carrier frequency (Hz)
Fm = 1    # Modulation frequency (Hz)
T = 5     # Duration of the signal (s)
Fs = 1000 # Sampling frequency (Hz)

# Time vector
t = np.linspace(0, T, int(Fs * T))

# Amplitude modulation factor
am_factor = np.abs(1 + 0.5 * np.cos(2 * np.pi * Fm * t))

# Plot the time-frequency representation
plt.figure(figsize=(10, 6))
plt.plot(t, am_factor * Fc, label="Amplitude Modulated Frequency")
plt.axhline(Fc, color='gray', linestyle='--', label="Carrier Frequency (Fc)")
plt.axhline(Fc * (1 + 0.5), color='red', linestyle='--', label="Fc + 0.5")
plt.axhline(Fc * (1 - 0.5), color='blue', linestyle='--', label="Fc - 0.5")

# Plot aesthetics
plt.title("Time-Frequency Representation of x1(t)")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

Fs = 1000  # Fréquence d'échantillonnage
T = 2.0    # Durée
t = np.linspace(0, T, int(Fs * T))
Fm = 5.0   # Fréquence de modulation

# Génération du signal
x1 = 1 + 0.5 * np.cos(2 * np.pi * Fm * t)

# Calcul de la FFT
f = np.fft.fftfreq(len(t), 1/Fs)
X1 = np.fft.fft(x1)
X1_magnitude = np.abs(X1) / len(t)  # Normalisation

# Affichage
plt.plot(f, X1_magnitude)
plt.title("Spectre de x1(t)")
plt.xlabel("Fréquence [Hz]")
plt.ylabel("Amplitude")
plt.xlim(-10, 10)
plt.grid()
plt.show()
"""
import numpy as np
import matplotlib.pyplot as plt

# Parameters for x2(t)
T = 1      # Period of the impulses (s)
duration = 5  # Duration of the signal (s)
Fs = 1000  # Sampling frequency (Hz)

# Time vector
t = np.linspace(0, duration, int(Fs * duration))

# Impulse train
k_values = np.arange(0, duration, T)
impulse_train = np.zeros_like(t)
for k in k_values:
    impulse_train[np.argmin(np.abs(t - k))] = 1  # Mark impulse closest to k/T

# Plot the impulse train
plt.figure(figsize=(10, 6))
plt.stem(t, impulse_train, label="Impulse Train")
plt.title("Time Representation of x2(t) = Σδ(t - k/T)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

