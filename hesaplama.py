import numpy as np

# -------------------------------
# Devre çözüm fonksiyonu
# -------------------------------
def solve_circuit(R1, R2, R3, R4, Ig1, Ig2):
    G1 = 1 / R1
    G2 = 1 / R2
    G3 = 1 / R3
    G4 = 1 / R4

    Y = np.array([
        [G1 + G2, -G2],
        [-G2, G2 + G3 + G4]
    ], dtype=float)

    I = np.array([-Ig1, Ig2], dtype=float)

    v = np.linalg.solve(Y, I)

    return v, Y


# -------------------------------
# Nominal değerler
# -------------------------------
R1 = 25
R2 = 5
R3 = 50
R4 = 75

Ig1 = 12
Ig2 = 16

v_nominal, Y_nominal = solve_circuit(R1, R2, R3, R4, Ig1, Ig2)

print("Nominal Durum")
print(f"v1 = {v_nominal[0]:.4f} V")
print(f"v2 = {v_nominal[1]:.4f} V")


# -------------------------------
# Ig1 değişimi: 12A -> 13A
# -------------------------------
v_Ig1_changed, _ = solve_circuit(R1, R2, R3, R4, 13, Ig2)

print("\nIg1 = 13A Durumu")
print(f"v1 = {v_Ig1_changed[0]:.4f} V")
print(f"v2 = {v_Ig1_changed[1]:.4f} V")


# -------------------------------
# R1 değişimi: %10 artış
# -------------------------------
R1_changed = R1 * 1.10

v_R1_changed, _ = solve_circuit(R1_changed, R2, R3, R4, Ig1, Ig2)

print("\nR1 %10 Artırılmış Durum")
print(f"R1 = {R1_changed:.2f} ohm")
print(f"v1 = {v_R1_changed[0]:.4f} V")
print(f"v2 = {v_R1_changed[1]:.4f} V")


# -------------------------------
# Akım kaynaklarına göre duyarlılık
# -------------------------------
Y_inv = np.linalg.inv(Y_nominal)

dv_dIg1 = Y_inv @ np.array([-1, 0])
dv_dIg2 = Y_inv @ np.array([0, 1])

print("\nAkım Kaynaklarına Göre Duyarlılıklar")
print(f"dv1/dIg1 = {dv_dIg1[0]:.4f}")
print(f"dv2/dIg1 = {dv_dIg1[1]:.4f}")
print(f"dv1/dIg2 = {dv_dIg2[0]:.4f}")
print(f"dv2/dIg2 = {dv_dIg2[1]:.4f}")


# -------------------------------
# Dirençlere göre duyarlılık
# -------------------------------
v = v_nominal.reshape(2, 1)

dY_dR1 = np.array([
    [-1 / R1**2, 0],
    [0, 0]
], dtype=float)

dY_dR2 = np.array([
    [-1 / R2**2, 1 / R2**2],
    [1 / R2**2, -1 / R2**2]
], dtype=float)

dv_dR1 = -Y_inv @ dY_dR1 @ v
dv_dR2 = -Y_inv @ dY_dR2 @ v

print("\nDirençlere Göre Duyarlılıklar")
print(f"dv1/dR1 = {dv_dR1[0, 0]:.4f}")
print(f"dv2/dR1 = {dv_dR1[1, 0]:.4f}")
print(f"dv1/dR2 = {dv_dR2[0, 0]:.4f}")
print(f"dv2/dR2 = {dv_dR2[1, 0]:.4f}")


# -------------------------------
# Sonuç tablosu
# -------------------------------
print("\nSonuç Tablosu")
print("-------------------------------------------")
print("Durum                 v1(V)        v2(V)")
print("-------------------------------------------")
print(f"Nominal              {v_nominal[0]:8.4f}    {v_nominal[1]:8.4f}")
print(f"Ig1 = 13A            {v_Ig1_changed[0]:8.4f}    {v_Ig1_changed[1]:8.4f}")
print(f"R1 = 27.5 ohm        {v_R1_changed[0]:8.4f}    {v_R1_changed[1]:8.4f}")
print("-------------------------------------------")
import matplotlib.pyplot as plt

# -------------------------------
# Grafik 1: Ig1 değişimi
# -------------------------------
labels = ["Nominal", "Ig1 = 13A"]
v1_values = [v_nominal[0], v_Ig1_changed[0]]
v2_values = [v_nominal[1], v_Ig1_changed[1]]

x = np.arange(len(labels))
width = 0.35

plt.figure()
plt.bar(x - width/2, v1_values, width, label="v1")
plt.bar(x + width/2, v2_values, width, label="v2")
plt.xticks(x, labels)
plt.ylabel("Gerilim (V)")
plt.title("Ig1 Akımındaki Değişimin Düğüm Gerilimlerine Etkisi")
plt.legend()
plt.savefig("ig1_degisim_grafigi.png", dpi=300, bbox_inches="tight")
plt.show()


# -------------------------------
# Grafik 2: R1 değişimi
# -------------------------------
labels = ["Nominal", "R1 = 27.5 ohm"]
v1_values = [v_nominal[0], v_R1_changed[0]]
v2_values = [v_nominal[1], v_R1_changed[1]]

x = np.arange(len(labels))

plt.figure()
plt.bar(x - width/2, v1_values, width, label="v1")
plt.bar(x + width/2, v2_values, width, label="v2")
plt.xticks(x, labels)
plt.ylabel("Gerilim (V)")
plt.title("R1 Direncindeki %10 Artışın Düğüm Gerilimlerine Etkisi")
plt.legend()
plt.savefig("r1_degisim_grafigi.png", dpi=300, bbox_inches="tight")
plt.show()
