# eye-blinking-communicator
Implementation of a communicator for non-speakers using eye blink recognition

## Structure
```bash
eye_blink_communicator/
│
├─ data/                  # przykładowe wideo lub dane treningowe
├─ models/                # zapisane modele ML do rozpoznawania mrugnięć
├─ src/
│   ├─ acquisition.py      # moduł akwizycji obrazu
│   ├─ eye_detection.py    # detekcja twarzy i oczu
│   ├─ blink_recognition.py # rozpoznawanie mrugnięć
│   ├─ interpreter.py      # mapowanie mrugnięć na komunikaty
│   ├─ ui.py               # interfejs użytkownika
│   └─ config.py           # konfiguracje systemu
├─ tests/                 # testy jednostkowe
├─ requirements.txt       # zależności
└─ main.py                # punkt startowy programu
```