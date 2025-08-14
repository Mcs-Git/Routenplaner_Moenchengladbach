import osmnx as ox
from osmnx import routing
import os
import matplotlib.pyplot as plt

# Setze nicht-interaktives Backend, um matplotlib-Warnungen in headless-Umgebungen zu vermeiden
import matplotlib
matplotlib.use("Agg")

def load_map():
    """
    Lädt das Straßennetz von Mönchengladbach.

    Falls die Datei noch nicht existiert, wird das Straßennetz mithilfe von OSM heruntergeladen
    und im Verzeichnis 'graph/' als GraphML-Datei gespeichert.

    Returns:
        networkx.MultiDiGraph: Der geladene Straßengraph.
    """
    filepath = "graph/moenchengladbach.graphml"

    if not os.path.exists(filepath):
        G = ox.graph_from_place("Mönchengladbach, Germany", network_type="drive")
        ox.save_graphml(G, filepath=filepath, encoding="utf-8")
    else:
        G = ox.load_graphml(filepath)

    return G

def get_map():
    """
    Lädt den Straßengraph und ergänzt ihn um realistische Durchschnittsgeschwindigkeiten
    sowie daraus berechnete Reisezeiten.

    Returns:
        networkx.MultiDiGraph: Der erweiterte Graph mit 'speed_kph' und 'travel_time'-Attributen.
    """
    G = load_map()
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    return G

def find_route(source, destination):
    """
    Findet die schnellste Route zwischen zwei geografischen Punkten.

    Args:
        source (tuple): Startpunkt (Longitude, Latitude).
        destination (tuple): Zielpunkt (Longitude, Latitude).

    Returns:
        list: Eine Liste von Knoten-IDs, die den Pfad beschreiben.

    Raises:
        ValueError: Wenn keine Route gefunden wird.
    """
    G = get_map()

    orig = ox.distance.nearest_nodes(G, X=source[0], Y=source[1])
    dest = ox.distance.nearest_nodes(G, X=destination[0], Y=destination[1])

    route = routing.shortest_path(G, orig, dest, weight="travel_time")

    if not route or len(route) < 2:
        raise ValueError("Keine gültige Route gefunden.")

    return route

def get_total_travel_time(source, destination):
    """
    Berechnet die ungefähre Reisezeit und Entfernung einer Route.

    Die Route wird zusätzlich als SVG visualisiert und gespeichert.

    Args:
        source (tuple): Startkoordinaten (lon, lat).
        destination (tuple): Zielkoordinaten (lon, lat).

    Returns:
        tuple: Reisezeit in Minuten (float), Distanz in Kilometern (float).

    Raises:
        ValueError: Wenn die berechnete Route leer ist.
    """
    G = get_map()
    route = find_route(source, destination)

    route_gdf = ox.routing.route_to_gdf(G, route, weight="travel_time")

    if route_gdf.empty:
        raise ValueError("Die Route enthält keine Kanten.")

    route_length = route_gdf["length"].sum()         # in Metern
    route_time = route_gdf["travel_time"].sum()      # in Sekunden

    total_travel_time = (route_time * 1.3) / 60       # Minuten
    total_travel_distance = route_length / 1000       # Kilometer

    save_graph_route(source, destination, G, route)

    return total_travel_time, total_travel_distance

def save_graph_route(source, destination, G, route):
    """
    Zeichnet und speichert die Route als SVG-Datei inklusive Start- und Zielmarkern.

    Args:
        source (tuple): Startkoordinaten (lon, lat).
        destination (tuple): Zielkoordinaten (lon, lat).
        G (networkx.MultiDiGraph): Der Graph mit Knoten und Kanten.
        route (list): Liste von Knoten-IDs, die die Route darstellen.
    """
    fig, ax = ox.plot_graph_route(
        G,
        route,
        node_size=0,
        route_color="#1A5D41",
        route_linewidth=3,
        bgcolor="#D9E8D3",
        edge_color="#A5C79B",
        edge_linewidth=0.8,
        show=False,
        close=False
    )

    start_node = ox.distance.nearest_nodes(G, X=source[0], Y=source[1])
    end_node = ox.distance.nearest_nodes(G, X=destination[0], Y=destination[1])

    x_start, y_start = G.nodes[start_node]['x'], G.nodes[start_node]['y']
    x_end, y_end = G.nodes[end_node]['x'], G.nodes[end_node]['y']

    ax.scatter(x_start, y_start, c="#FFFFFF", edgecolors="#1A5D41", s=70, zorder=5, linewidth=2, label="Start", marker="o")
    ax.scatter(x_end, y_end, c="#FFFFFF", edgecolors="#1A5D41", s=70, zorder=5, linewidth=2, label="Ziel", marker="X")

    ax.legend(loc="lower right", fontsize=12, labelcolor="#1A5D41", facecolor="#D9E8D3", edgecolor="#D9E8D3")

    fig.savefig("static/graph/route_plot.svg", dpi=300)
    plt.close(fig)

def input_check(source, destination):
    """
    Überprüft die Benutzereingabe auf korrekte Struktur und Typkonvertierbarkeit.

    Args:
        source (list): Liste mit zwei Strings (Koordinaten für Startpunkt).
        destination (list): Liste mit zwei Strings (Koordinaten für Zielpunkt).

    Returns:
        tuple: (Koordinaten Startpunkt, Koordinaten Zielpunkt, Bool ob gültig).
    """
    if len(source) == 2 and len(destination) == 2:
        try:
            source_coordinates = tuple(map(float, source))
            destination_coordinates = tuple(map(float, destination))
            return source_coordinates, destination_coordinates, True
        except ValueError:
            return None, None, False
    return None, None, False
