import numpy as np
import matplotlib.pyplot as plt

# Données fournies
R = 6.8e3  # Résistance en ohms (6.8 kohm)
C = 2.2e-9  # Capacité en farads (2.2 nF)
Ve = 3  # Tension d'entrée en volts (3 V)
frequences_kHz = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 12, 15, 18, 19, 25, 30, 40, 100, 200, 300, 500, 700, 1000]  # en kHz

# Conversion des fréquences en Hz
frequences_Hz = np.array(frequences_kHz) * 1e3

# Calcul des grandeurs
Vs = []
gain_db = []
dephasage = []

for f in frequences_Hz:
    omega = 2 * np.pi * f
    H = 1 / (1 + 1j * omega * R * C)
    Vs_f = abs(H) * Ve
    Vs.append(Vs_f)
    gain_db.append(20 * np.log10(abs(H)))
    dephasage.append(np.angle(H, deg=True))

# Enregistrement des résultats dans un fichier texte
with open('resultats_filtre_RC.txt', 'w') as file:
    file.write("Fréquence (kHz)\tGain (dB)\tDéphasage (°)\tVs (V)\n")
    for f_kHz, gain, phase, vs in zip(frequences_kHz, gain_db, dephasage, Vs):
        file.write(f"{f_kHz}\t{gain:.2f}\t{phase:.2f}\t{vs:.4f}\n")

# Calcul de la fréquence de coupure
f_coupure = 1 / (2 * np.pi * R * C)
f_coupure_kHz = f_coupure / 1e3  # Convertir en kHz
print(f"La fréquence de coupure est d'environ {f_coupure_kHz:.2f} kHz")

# Tracer les courbes de Bode avec asymptotes
plt.figure(figsize=(14, 10))

# Courbe de gain
plt.subplot(2, 1, 1)
plt.semilogx(frequences_kHz, gain_db, label='Gain (dB)', linewidth=2)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1, label='Asymptote basse fréquence')
plt.axhline(y=-20, xmin=0.5, xmax=1000, color='gray', linestyle='--', linewidth=1)
plt.semilogx([f_coupure_kHz, f_coupure_kHz], [-80, 0], linestyle='--', color='red', label='Fréquence de coupure')
plt.xlabel('Fréquence (kHz)')
plt.ylabel('Gain (dB)')
plt.title('Courbe de Bode - Gain en dB')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Courbe de déphasage
plt.subplot(2, 1, 2)
plt.semilogx(frequences_kHz, dephasage, label='Déphasage (°)', color='orange', linewidth=2)
plt.axhline(y=-45, color='gray', linestyle='--', linewidth=1, label='Asymptote déphasage')
plt.semilogx([f_coupure_kHz, f_coupure_kHz], [-90, 0], linestyle='--', color='red', label='Fréquence de coupure')
plt.xlabel('Fréquence (kHz)')
plt.ylabel('Déphasage (°)')
plt.title('Courbe de Bode - Déphasage')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

plt.tight_layout()
plt.show()

# Tracer Vs en fonction de la fréquence
plt.figure(figsize=(10, 6))
plt.semilogx(frequences_kHz, Vs, label='Vs (V)', linewidth=2)
plt.axvline(x=f_coupure_kHz, color='red', linestyle='--', label='Fréquence de coupure')
plt.xlabel('Fréquence (kHz)')
plt.ylabel('Vs (V)')
plt.title('Tension de sortie Vs en fonction de la fréquence')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.show()
