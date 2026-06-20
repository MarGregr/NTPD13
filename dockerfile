FROM python:3.9-slim

#Ustawienie katalogu roboczego wewnątrz kontenera
WORKDIR /app

#Kopiowanie pliku z listą zależności
COPY requirements.txt .

#Instalacja bibliotek (bez zapisywania cache, aby obraz był mniejszy)
RUN pip install --no-cache-dir -r requirements.txt

#Kopiowanie reszty plików aplikacji do kontenera
COPY . .

EXPOSE 8000

#Uruchomienie serwera
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]