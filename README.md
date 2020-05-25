# Dash
Aplikacja przedstawiająca za pomocą frameworku dash, coroczne dane zbierane przez stronę stackoverflow
 
# Instalacja

## Wymagania
Do prawidłowego uruchomienia aplikacji wymagane jest zainstalowanie i skonfigurowanie [docker-a](https://www.docker.com/) oraz  [docker-compose](https://docs.docker.com/compose/install/).

## Instalacja/uruchomienie aplikacji

Aby zainstalować i uruchomić aplikacje należy wpisać w terminalu:
```
docker-compose pull
docker-compose build
docker-compose up
```
lub w skrócie
```
docker-compose up --build
```
aplikacja uruchomi się na porcie 8000.

###Aktualizacja istniejącej instancji
jeżeli kod się zmienił należy przebudować app image
```bash
git pull
docker-compose up --build
```
Po uruchomieniu powyższej komendy aplikacja automatycznie pobierze wymagane obrazy oraz zbuduje z kodu nowy obraz backendu.