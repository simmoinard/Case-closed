# Case closed
Gerer les emprunts et retours de matériels via un casier connecté.

Il est nécessaire d'installer sur Raspberry : pyqt5 pour l'interface, une base de données mysql (mariadb-server), un serveur (apache) et une interface de visualisation (phpMyAdmin), le langage php.

Installer pyQT5 et ses outils sur Raspberry & Windows :

```bash
#Pour Raspberry : lignes à tester 1 par 1, beaucoup sont inutiles.
sudo apt install python3-pyqt5
sudo apt-get install qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools
sudo apt-get --reinstall install libqt5dbus5 libqt5widgets5 libqt5network5 libqt5gui5 libqt5core5a libdouble-conversion1 libxcb-xinerama0
sudo apt-get install libqt5x11extras5

pip install mysqlclient

python -m pip install mysql-connector-python
```


#Pour Windows
```
sudo pip install --no-cache-dir pyqt5-tools --user
```
La commande suivante transforme le fichier .ui en script python, executable depuis le Raspberry (à mettre ensuite au boot du raspberry)
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
Have just the below in /etc/mysql/my.cnf

[mysqld]
#### Unix socket settings (making localhost work)
user            = mysql
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock

#### TCP Socket settings (making all remote logins work)
port            = 3306
bind-address = 0.0.0.0



mysql est finalement prêt à être utilisé : 
```

mysql -u root -p
```
grant all privileges on *.* to ‘username’@‘%’ identified by ‘password’;

