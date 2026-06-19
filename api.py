import requests

def get_motivation():
    try:
        res = requests.get("https://api.quotable.io/random")
        data = res.json()
        return data["content"]
    except:
        return "Sigue estudiando, cada esfuerzo cuenta 💪"