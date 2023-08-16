import numpy as np
import os

# path = r"C:\Users\qcrew\Documents\yabba\waves"
# data = np.load(r"C:\Users\qcrew\Desktop\qcrew\qcrew\config\GRAPE\pi.npz")
# lst = data.files

# QubitI = data["QubitI"]
# QubitQ = data["QubitQ"]

# wave = QubitI + 1j * QubitQ
# print(wave.shape)

# np.savez(os.path.join(path, "waves.npz"), wave=wave )

data2 = np.load("C://Users//qcrew//Documents//yabba//waves//waves.npz")
lst=data2.files
print(np.imag(data2['wave'][0:5]))

# print(data2["wave"])


# r"C:\Users\qcrew\Desktop\qcrew\qcrew\config\GRAPE\pi.npz"