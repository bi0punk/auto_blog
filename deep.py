import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Ejemplo de datos: [(x1, y1, -profundidad1), (x2, y2, -profundidad2), ...]
# Nota: las profundidades son negativas
datos_sismos = [(100, 150, -120), (120, 130, -378), (150, 170, -444)]

# Separar los datos en coordenadas X, Y y profundidades Z (negativas)
x = [punto[0] for punto in datos_sismos]
y = [punto[1] for punto in datos_sismos]
z = [punto[2] for punto in datos_sismos]

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scatter = ax.scatter(x, y, z, c=np.abs(z), cmap='viridis', depthshade=True)

# Añadir etiquetas y título si es necesario
ax.set_xlabel('Coordenada X')
ax.set_ylabel('Coordenada Y')
ax.set_zlabel('Profundidad')
ax.set_title('Profundidad de Sismos')

# Ajustar los límites del eje Z si es necesario
ax.set_zlim(-max(np.abs(z)), 0)

# Mostrar el gráfico
plt.show()
