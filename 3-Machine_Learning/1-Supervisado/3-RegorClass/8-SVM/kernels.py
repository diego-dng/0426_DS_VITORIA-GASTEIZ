import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn import datasets
from sklearn.svm import SVC

# Kernel Lineal
X_lin, y_lin = datasets.make_blobs(
    n_samples=100, centers=2, random_state=42, cluster_std=1.2
)
clf_lin = SVC(kernel="linear")
clf_lin.fit(X_lin, y_lin)

# Kernel Polinómico
X_poly, y_poly = datasets.make_moons(n_samples=100, noise=0.15, random_state=42)
# Usamos un grado 3 con coeficiente para una bonita curva
clf_poly = SVC(kernel="poly", degree=3, coef0=1, C=5)
clf_poly.fit(X_poly, y_poly)

# Kernel RBF
X_rbf, y_rbf = datasets.make_circles(
    n_samples=100, factor=0.3, noise=0.1, random_state=42
)
clf_rbf = SVC(kernel="rbf", gamma=1)
clf_rbf.fit(X_rbf, y_rbf)


def agregar_hiperplano_y_regiones(X, clf, fig, row, col, colorscale_regiones):
    
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
    
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    fig.add_trace(
        go.Contour(
            x=np.linspace(x_min, x_max, 200),
            y=np.linspace(y_min, y_max, 200),
            z=Z,
            showscale=False,
            opacity=0.25,  
            colorscale=colorscale_regiones,
            contours=dict(showlines=False),
            hoverinfo="skip",
            name="Regiones de decisión",
        ),
        row=row, col=col
    )

    fig.add_trace(
        go.Contour(
            x=np.linspace(x_min, x_max, 200),
            y=np.linspace(y_min, y_max, 200),
            z=Z,
            showscale=False,
            contours=dict(showlines=True, start=0, end=0),
            line=dict(color="black", width=3),
            name="Hiperplano (Z=0)"
        ),
        row=row, col=col
    )
    
    fig.add_trace(
        go.Contour(
            x=np.linspace(x_min, x_max, 200),
            y=np.linspace(y_min, y_max, 200),
            z=Z,
            showscale=False,
            contours=dict(showlines=True, start=-1, end=1, size=2),
            line=dict(color="dimgray", width=1.5, dash="dash"),
            name="Márgenes (Z=±1)"
        ),
        row=row, col=col
    )


fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "<b>Kernel Lineal</b><br>Hiperplano Rígido (Línea Recta)",
        "<b>Kernel Polinómico</b><br>Hiperplano Flexible (Curva en 2D)",
        "<b>Kernel RBF (Truco del Kernel)</b><br>El hiperplano es un plano plano (gris) que corta los datos elevados en 3D",
    ),
    specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "scene", "colspan": 2}, None]],
    vertical_spacing=0.18,
)

agregar_hiperplano_y_regiones(X_lin, clf_lin, fig, row=1, col=1, colorscale_regiones="Blues")
fig.add_trace(
    go.Scatter(
        x=X_lin[:, 0], y=X_lin[:, 1],
        mode="markers",
        marker=dict(color=y_lin, colorscale="Viridis", size=10, line=dict(width=1, color="black")),
        name="Datos (Lineal)",
        showlegend=False
    ),
    row=1, col=1
)

agregar_hiperplano_y_regiones(X_poly, clf_poly, fig, row=1, col=2, colorscale_regiones="Plasma")
fig.add_trace(
    go.Scatter(
        x=X_poly[:, 0], y=X_poly[:, 1],
        mode="markers",
        marker=dict(color=y_poly, colorscale="Viridis", size=10, line=dict(width=1, color="black")),
        name="Datos (Poly)",
        showlegend=False
    ),
    row=1, col=2
)


r = np.exp(-(X_rbf[:, 0] ** 2 + X_rbf[:, 1] ** 2))

fig.add_trace(
    go.Scatter3d(
        x=X_rbf[:, 0], y=X_rbf[:, 1], z=r,
        mode="markers",
        marker=dict(color=y_rbf, colorscale="Viridis", size=6, opacity=1, line=dict(width=1, color="black")),
        name="Datos Proyectados",
        showlegend=False
    ),
    row=2, col=1
)

x_plane, y_plane = np.meshgrid(np.linspace(-1.3, 1.3, 10), np.linspace(-1.3, 1.3, 10))
z_plane = np.ones_like(x_plane) * 0.55  # Altura óptima del corte educativo
fig.add_trace(
    go.Surface(
        x=x_plane, y=y_plane, z=z_plane,
        opacity=0.4,
        colorscale="Greys",
        showscale=False,
        name="Hiperplano de separación (Plano Z)"
    ),
    row=2, col=1
)

fig.update_layout(
    title_text="<b>Visualización de Hiperplanos y Kernels en SVM</b>",
    title_font_size=24,
    height=900,
    width=1100,
    template="plotly_white",
    legend=dict(title="Leyenda", x=1.02, y=1),
    scene=dict(
        xaxis_title="Característica X1",
        yaxis_title="Característica X2",
        zaxis_title="Dimensión del Kernel (Z)",
        camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)),
    )
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

print("Generando el cuadro interactivo. Se abrirá en tu navegador automáticamente...")
fig.show()