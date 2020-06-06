# ansible2siteconf
ansible Konfiguration zu site.conf Generator


## Vorbereitung

Abhängigkeit:

```bash
sudo apt install python3-venv
```

Repository clonen

```bash
git clone --recursive git@github.com:Neanderfunk/ansible2siteconf.git

cd ansible2siteconf

# If you already have cloned a repository and now want to load it’s submodules you have to use submodule update.
git submodule update --init
```


venv einrichten

```bash
python3 -m venv .venv/

source .venv/bin/activate

```

Python Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```


## Benutzung

```bash
./generate.py
```

Die `site.conf` Dateien werden im Ordner `out` generiert.
