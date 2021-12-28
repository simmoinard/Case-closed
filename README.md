# Case closed
Un casier automatique qui gère le prêt de matériel

Installer pyQT5& outils sur Raspberry & Windows :

```bash
#Pour Raspberry : lignes à tester 1 par 1, beaucoup sont inutiles.
sudo apt install python3-pyqt5
sudo apt-get install qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools
sudo apt-get --reinstall install libqt5dbus5 libqt5widgets5 libqt5network5 libqt5gui5 libqt5core5a libdouble-conversion1 libxcb-xinerama0
sudo apt-get install libqt5x11extras5
```


#Pour Windows
```
sudo pip install --no-cache-dir pyqt5-tools --user
```
La commande suivante transforme le fichier .uien script python, executable depuis le Raspberry (à mettre ensuite au boot du raspberry)
```
pyuic5.exe -x file.ui -o ouptut.py
```

Installer QT designer sur Windows :
https://build-system.fman.io/qt-designer-download

Sur Raspberry : on installe mysql, puis on edite le nouveau mot de passe (Yes à tout)
https://raspberry-pi.fr/installer-serveur-web-raspberry-lamp/

```bash
sudo apt install mariadb-server
sudo mysql_secure_installation
sudo apt install apache2
sudo apt-get install php libapache2-mod-php
sudo apt install phpmyadmin

sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

```

mysql est finalement prêt à être utilisé : 
```

mysql -uroot -p
```


