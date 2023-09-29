# Fichero para la creación de los gráficos de la página "Estadísticas" de la web
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.patheffects import withStroke

# Función para generar el gráfico de usuario "Número total de películas y series vistas"
def get_hbar_graph(a, b):
    # Creamos una nuevo gráfico y trazamos los datos
    data = [a, b]
    names = ["Películas", "Series"]

    # Para determinar exactamente donde se posiciona cada barra
    y = [i for i in range(len(names))]

    # Color
    BLUE = "#076fa2"

    fig, ax = plt.subplots(figsize=(6, 3), facecolor="#D6C6D6")
    ax.barh(y, data, height=0.5, align="center", color=BLUE);

    # Personalizamos layout del gráfico
    # Eje x
    ax.xaxis.set_ticks([i for i in range(0,  max(a, b) + 1)])
    ax.xaxis.set_ticklabels([i for i in range(0, max(a, b) + 1)], size=8, fontfamily="sans-serif", fontweight=100)
    ax.xaxis.set_tick_params(labelbottom=True, labeltop=False, length=0)
    ax.set_xlim((0, max(a, b) + 2.5))
    # Eje y
    ax.yaxis.set_visible(False)
    # Ticks y gridlines
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#A8BAC4", lw=1.2)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_lw(1.5)
    # capstyle para que las líneas no vayan más allá del límite especificado
    ax.spines["left"].set_capstyle("butt")
    # Añadimos etiquetas a las barras
    for name, number, y_pos in zip(names, data, y):
        ax.text(
            number + 0.1, y_pos, name,
            color=BLUE, fontfamily="sans-serif", fontsize=13, va="center",
            path_effects=[withStroke(linewidth=6, foreground="#D6C6D6")]
        )
    # Color de fondo
    ax.set_facecolor("#D6C6D6")

    # ajustar el margen del gráfico
    fig.subplots_adjust(left=0.04, right=1, top=0.80, bottom=0.1)

    # Título
    fig.text(0.15, 0.925, "Número total de películas y series vistas",
        fontsize=13, fontweight="bold", fontfamily="sans-serif")

    # Guardamos el gráfico en formato png en el objeto BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return string.decode('utf-8')

# Función para generar el gráfico de usuario "Tiempo total visualizado [horas]"
def get_hbar_graph2(a, b):
    # Creamos una nuevo gráfico y trazamos los datos
    data = [a, b]
    names = ["Películas", "Series"]

    # Para determinar exactamente donde se posiciona cada barra
    y = [i for i in range(len(names))]

    # Color
    BLUE = "#076fa2"

    fig, ax = plt.subplots(figsize=(6, 3), facecolor="#D6C6D6")
    ax.barh(y, data, height=0.5, align="center", color=BLUE);

    # Personalizamos layout del gráfico
    # Eje x
    if max(int(a), int(b)) < 380:
        ax.xaxis.set_ticks([i * 20 for i in range(0, max(int(a), int(b)) + 1)])
        ax.xaxis.set_ticklabels([i * 20 for i in range(0, max(int(a), int(b)) + 1)], size=8, fontfamily="sans-serif",
                                fontweight=100)
        ax.xaxis.set_tick_params(labelbottom=True, labeltop=False, length=0)
        ax.set_xlim((0, max(a, b) + 70))
    else:
        ax.xaxis.set_ticks([i*80 for i in range(0, max(int(a), int(b)) + 1)])
        ax.xaxis.set_ticklabels([i*80 for i in range(0, max(int(a), int(b)) + 1)], size=8, fontfamily="sans-serif",
                                fontweight=100)
        ax.xaxis.set_tick_params(labelbottom=True, labeltop=False, length=0)
        ax.set_xlim((0, max(a, b) + 100))

    # Eje y
    ax.yaxis.set_visible(False)
    # Ticks y gridlines
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#A8BAC4", lw=1.2)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_lw(1.5)
    # capstyle para que las líneas no vayan más allá del límite especificado
    ax.spines["left"].set_capstyle("butt")
    # Añadimos etiquetas a las barras
    for name, number, y_pos in zip(names, data, y):
        ax.text(
            number + 4, y_pos, name,
            color=BLUE, fontfamily="sans-serif", fontsize=13, va="center",
            path_effects=[withStroke(linewidth=6, foreground="#D6C6D6")]
        )

    # ajustar el margen del gráfico
    fig.subplots_adjust(left=0.04, right=1, top=0.80, bottom=0.1)

    # Título
    fig.text(0.2, 0.925, "Tiempo total visualizado [horas]",
        fontsize=13, fontweight="bold", fontfamily="sans-serif")

    # Color de fondo
    ax.set_facecolor("#D6C6D6")

    # Guardamos el gráfico en formato png en el objeto BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return string.decode('utf-8')
