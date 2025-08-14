# Routenplaner_Moenchengladbach

### **1. Aufgabenstellung**

Ziel war es, ein webbasiertes Tool zur Routenberechnung in **Mönchengladbach** zu erstellen. Die Anwendung sollte folgende Funktionen erfüllen:

* Entgegennahme von **zwei GPS-Koordinaten** (Start- und Zielpunkt)
* Berechnung einer **Autofahrroute** über das **OpenStreetMap-Netzwerk**
* **Ausgabe der Reisezeit und Distanz**
* **Grafische Darstellung** der Route
* **Einmaliges Laden und lokales Speichern** des Straßennetzes von Mönchengladbach zur Entlastung der OSM-API


### **2. Technische Umsetzung**

#### **Frontend (HTML & CSS)**

Zwei HTML-Seiten wurden implementiert:

* `index.html` (Startseite):

  * Eingabeformular für Start- und Zielkoordinaten (Länge und Breite)
  * Nutzerfreundliches Design mit einer Farbanmutung, die an Mönchengladbach angelehnt ist (#1A5D41(**Jagdgrün**), #A5C79B(**Salbeigrün**), #D9E8D3(**Minzweiß**))



Das CSS wurde in zwei Dateien (`style.css` und `route.css`) modular strukturiert und sorgt für ein konsistentes Design.

**Eingabeformular-Vorschau für den Routenplaner:**

![](https://codi.ide3.de/uploads/b9ae698f-bf58-4fee-a4f4-21651ab687a9.png)



#### **Backend (Python & Flask)**

* Die Anwendung basiert auf **Flask** und besteht aus zwei Routen:

  * `/` (**GET**): Gibt die Startseite mit dem Formular aus
  * `/api/route` (**POST**): Verarbeitet das Formular und rendert die Ergebnisseite


* Die Route `/api/route`:


  * Validiert die Eingaben (genau zwei Koordinaten pro Feld)
  * Berechnet über ein externes Modul `route_api.py` die schnellste Route mit Reisezeit und Distanz
  * Speichert die Route als **SVG-Grafik** ab
  * Gibt die Ergebnisse auf einer strukturierten HTML-Seite aus




#### **Routing und Kartendaten (OSMnx)**

Das Modul `route_api.py` enthält die Kernlogik:

* **Graphen-Handling**:

  * Der Straßengraph für "Mönchengladbach, Germany" wird nur **einmal heruntergeladen** (per `ox.graph_from_place`) und als `.graphml` gespeichert.
  * Bei weiteren Zugriffen wird dieser **lokal geladen** (zur Schonung der API).

* **Routing**:

  * OSMnx-Funktion `shortest_path()` wird mit dem Gewicht `travel_time` verwendet.
  * Zusätzliche Annotation der Straßenkanten mit Geschwindigkeitsdaten und Reisezeiten.

* **Visualisierung**:

  * Matplotlib generiert ein SVG mit Route und Markern für Start/Ziel.
  * Das Bild wird im Ordner `static/graph/` gespeichert und auf der Ergebnisseite eingebettet.



### **3. Ergebnis**

Die Web-App erlaubt die schnelle und einfache Berechnung einer Route innerhalb von Mönchengladbach. Die wichtigsten Features sind:

* Benutzerfreundliches UI für GPS-Koordinateneingabe
* Stabile Berechnung über vorab gespeicherten Graph
* Ausgabe von **Reisezeit in Minuten** und **Distanz in Kilometern**
* **Kartenbasierte Visualisierung** im einheitlichen Mönchengladbacher Design

### **Beispieldurchlauf: Mönchengladbach Hbf → Hochschule Niederrhein, Campus Monforts Quartier**

Zur Demonstration wurde als Startpunkt der **Mönchengladbacher Hauptbahnhof** (ca. 6.44613, 51.19649) und als Ziel die **Hochschule Niederrhein, Campus Monforts Quartier** (ca. 6.44186, 51.17923) verwendet.

Die Anwendung berechnete erfolgreich:

* Eine direkte Route innerhalb der Stadt
* Die geschätzte Reisezeit in Minuten
* Die Distanz in Kilometern
* Eine visuelle Darstellung der Strecke mit Start-/Zielmarkern im SVG-Format

Screenshots der Weboberfläche mit den Eingabewerten und der gerenderten Route:

![](https://codi.ide3.de/uploads/3f5c14a3-4a6b-4c08-a821-8c9301bd4db5.png)



![](https://codi.ide3.de/uploads/dd269261-517b-424a-9123-3b5eedf07a5b.png)

