# garminHrExporter

## Anleitung

### Vorbedingungen

* python3
* pip3

### Abhängigkeiten installieren

```bash
pip3 install -r requirements
```

### Config.yaml anpassen

```yaml
# The directory where the exported files will be saved
exportDir: ""
# The directory where the Garmin auth token will be saved
tokenDir: ""
zones:
  - name: "1"
    min: 0
    max: 100
  - name: "2"
    min: 100
    max: 120
  - name: "3"
    min: 120
    max: 140
  - name: "4"
    min: 140
    max: 160
  - name: "5"
    min: 160
    max: 9999
```

Setze das `exportDir` auf einen beliebigen Pfad. In dieses Verzeichnis werden alle Daten exportiert.
Setze das `tokenDir` auf einen beliebingen Pfad. In diesem Verzeichnis wird das Garmin Connect Token gespeichert, damit du dich nicht jedes mal neu einloggen musst.
Passe die Herzfrequenzzonen `zones` entsprechend an.

### Ausführen

Der Exported exportiert immer Die Herzfrequenzdaten eines einzelnen Tages. Der Tag kann im ISO Format angegeben werden.
Wird kein Tag angegeben, werden die Daten des aktuellen Tages geladen.

```bash
./garminHrExporter.py 2024-04-16
```

Bei der ersten Verwendung musst du dich mit deinen Garmin Connect Zugangsdaten einloggen.
 