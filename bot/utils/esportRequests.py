import requests

class EsportRequests:
    def __init__(self):
        self.base_url = "https://esports-api.lolesports.com/persisted/gw/"
        self.headers = {
            "Accept": "*/*",
            "Authority": "esports-api.lolesports.com",
            "Origin": "https://lolesports.com",
            "Referer": "https://lolesports.com/",
            "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z",
        }

    def __get(self, route, **params):
        url = self.base_url + route
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        print(url)
        return requests.get(url, headers=self.headers).json()

    def getLeagues(self, language) -> dict:
        return self.__get("getLeagues", hl=language)

    def getSchedules(self, language, leagueId) -> dict:
        return self.__get("getSchedule", hl=language, leagueId=leagueId)