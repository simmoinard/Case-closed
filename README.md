# closedcase
Un casier automatique qui gère le prêt de matériel

Installer pyQT5& outils sur Raspberry & Windows :

```bash
#Pour Raspberry : lignes à tester 1 par 1, beaucoup sont inutiles.
sudo apt install python3-pyqt5
sudo apt-get install qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools
sudo apt-get --reinstall install libqt5dbus5 libqt5widgets5 libqt5network5 libqt5gui5 libqt5core5a libdouble-conversion1 libxcb-xinerama0
sudo apt-get install libqt5x11extras5



#Pour Windows
sudo pip install --no-cache-dir pyqt5-tools --user

pyuic5.exe -x file.ui -o ouptut.py
```

Installer QT designer sur Windows :
https://build-system.fman.io/qt-designer-download

Puis les outils pyqt5 (notamment pour transformer l'app en script python)

