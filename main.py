import requests
from App import App

def main():
    """Bajar los datos de la API"""

    teams = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()

    stadiums = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()

    matches = requests.request("GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()

    app = App()
    app.menu(teams, stadiums, matches)
main()