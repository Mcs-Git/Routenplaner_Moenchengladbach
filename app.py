from flask import Flask, render_template, request
import route_api
import matplotlib

# Verhindert GUI-Warnungen von Matplotlib beim Betrieb in Flask (kein interaktives Backend)
matplotlib.use('Agg')

# Initialisiere Flask-Anwendung
app = Flask(__name__)


@app.route("/")
def index():
    """
    Startseite der Anwendung: Zeigt das Eingabeformular für Start- und Zielkoordinaten.

    Returns:
        str: Gerenderte HTML-Seite mit dem Eingabeformular.
    """
    return render_template('index.html')


@app.route("/api/route", methods=['POST'])
def route():
    """
    Verarbeitet das Formular zur Routenberechnung.

    Liest Koordinaten aus dem Formular, prüft sie, berechnet Route, Distanz und Reisezeit,
    speichert die Visualisierung, und zeigt die Ergebnisse in einer HTML-Seite an.

    Returns:
        str: Gerenderte HTML-Seite mit Reisedaten oder Fehlermeldung.
    """
    # Koordinaten vom Formular abfragen
    source = request.form.getlist("source")
    destination = request.form.getlist("destination")

    # Eingabe validieren und Koordinaten umwandeln
    source_coordinates, destination_coordinates, is_valid = route_api.input_check(source, destination)

    if is_valid:
        try:
            # Reisedaten berechnen
            travel_time, travel_distance = route_api.get_total_travel_time(source_coordinates, destination_coordinates)

            # Ergebnisse formatieren
            total_travel_time = f"{travel_time:.2f}"  # Minuten
            total_travel_distance = f"{travel_distance:.2f}"  # Kilometer

            # Ergebnis-Seite anzeigen
            return render_template(
                'route.html',
                source=source_coordinates,
                destination=destination_coordinates,
                travel_time=total_travel_time,
                total_distance=total_travel_distance
            )
        except Exception as e:
            # Fehler bei der Berechnung oder im Routing
            return f"Fehler bei der Routenberechnung: {str(e)}", 500
    else:
        # Ungültige Benutzereingabe
        return "Ungültige Eingabe. Bitte geben Sie je zwei gültige Koordinaten ein.", 400


if __name__ == "__main__":
    # Starte lokalen Entwicklungsserver im Debug-Modus
    app.run(debug=True)
