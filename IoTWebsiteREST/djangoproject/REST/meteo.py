import requests

class PrevisioneMeteo:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.variables =  "temperature_2m,wind_speed_10m,precipitation,cloudcover,weathercode"
        self.model = "icon-eu"
        self.weather_dict = {0: "Cielo sereno", 1: "Prevalentemente sereno", 2: "Parzialmente nuvoloso", 3: "Nuvoloso", 45: "Nebbia", 48: "Nebbia con brina", 51: "Pioviggine leggera", 53: "Pioviggine moderata", 55: "Pioviggine intensa", 56: "Pioviggine gelata leggera", 57: "Pioviggine gelata intensa", 61: "Pioggia debole", 63: "Pioggia moderata", 65: "Pioggia forte", 66: "Pioggia gelata leggera", 67: "Pioggia gelata forte", 71: "Neve debole", 73: "Neve moderata", 75: "Neve forte", 77: "Granuli di neve", 80: "Rovesci di pioggia deboli", 81: "Rovesci di pioggia moderati", 82: "Rovesci di pioggia violenti", 85: "Rovesci di neve deboli", 86: "Rovesci di neve forti", 95: "Temporale debole o moderato", 96: "Temporale con grandine leggera", 99: "Temporale con grandine forte"}
        
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly={self.variables}&model={self.model}"
        self.response = requests.get(self.url)
        #print(self.response.json())
        if self.response.status_code == 200:
            self.data = self.response.json()
        else:
            print(f"Si è verificato un errore: {self.response.status_code}")
            self.data = None

    def get_info(self, date, hour):             # meteo relativo specifica data e ora
        if self.data is not None:
            time = f"{date}T{hour}"
            if time in self.data["hourly"]["time"]:
                index = self.data["hourly"]["time"].index(time)
                
                temp = self.data["hourly"]["temperature_2m"][index]
                wind = self.data["hourly"]["wind_speed_10m"][index]
                rain = self.data["hourly"]["precipitation"][index]
                cloud = self.data["hourly"]["cloudcover"][index]
                weather = self.data["hourly"]["weathercode"][index]

                return {"temp": temp, "wind": wind, "rain": rain, "cloud": cloud, "weather" :self.weather_dict[weather]}
            else:
                #print(f"La data e l'ora specificate non sono disponibili")
                return None
        else:
            print(f"Non è possibile ottenere le informazioni meteo")
            return None
    def get_rain(self, date, hour):
        info = self.get_info(date, hour)
        if info is not None:
            return info["rain"]
        else:
            return None