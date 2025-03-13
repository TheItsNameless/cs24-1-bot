*Ein wilder Bot der Seminargruppe CS24-1 erscheint…*

# Development

Ganz einfach:

1. Clone das Repo
2. Erstelle eine venv mit `python3 -m venv venv` oder dem Tool, dass deine IDE mitbringt.
3. Installiere alle Pakete aus `requirements.txt` und `torch.requirements.txt` mit `python3 -m pip install -r requirements.txt` (bzw. `python3 -m pip install -r requirements.txt`).
4. Erstelle einen Testbot auf der [Discord Developers Seite](https://discord.com/developers)
5. Kopiere die `EXAMPLE.env` Datei und nenne sie in `.env` um. Fülle die Werte aus.
6. Richte die Datenbank ein. Befolge [diese Anleitung](#Datenbank-Einrichtung).
7. Starte den Bot, indem du die `main.py` Datei mittels `python3 main.py` ausführst.

# Datenbank Einrichtung
1. Zunächst musst du das Tortoise-CLI tool `aerich` installieren. Führe dazu `python3 -m pip install aerich` aus.

> Der Nachfolgende Schritt sollte **nicht** erneut ausgeführt werden müssen, da bereits Migrationen vorhanden sind!
2. Sollten keine Migrations in `/migrations` vorhanden sein, führe zunächst `aerich init-db` aus, um die Datenbank zu initialisieren. **Dies muss nur beim ersten Mal gemacht werden.**

> Dieser Schritt ist **notwendig**!
3. Führe `aerich upgrade` aus, um die Datenbank auf die neueste Version zu bringen.

# Änderungen am Datenmodel

Solltest du Änderungen an den Daten vornehmen, die in der Datenbank gespeichert werden, musst du die Datenbankmigrationen aktualisieren.

1. Führe `aerich migrate --name=<name der migration>` aus, um eine neue Migration zu erstellen.
2. Führe `aerich upgrade` aus, um die Datenbank auf den neuesten Stand zu bringen.
