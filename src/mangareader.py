from bs4 import BeautifulSoup
import requests

class Mangareader:
	def __init__(self) -> None:
		self.parent_url = "https://mangareader.tv"
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.results  = {
			"status": None,
			"results": []
		}
	def search(self, query:str):
		try:
			formattedQuery = query.replace(" ", "+")
			url = f"{self.proxy_url}{self.parent_url}/search/?w={formattedQuery}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("#ares > div > table > tbody > tr")

			for items in cards:
				tempContent = {}	
				tempContent["title"] = items.find("a").get_text()
				tempContent["id"] = items.find("a").get("href").split("/")[2]
				tempContent["image"] = f"{self.parent_url}{items.find('div', class_='d56').get('data-src')}"
				tempContent["chapters"] = items.find("div", class_="d58").get_text().split(" ")[0]
				tempContent["status"] = items.find("div", class_="d58").get_text().rsplit(" ")[3]
				tempContent["genres"] = items.find("div", class_="d60").get_text().replace("\n", "").replace(" ", "").split(",")[:-1]
				self.results["results"].append(tempContent)

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

	def info(self, id:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/manga/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			tempContent = {}
			tempContent["image"] = f"{self.parent_url}{soup.select_one('#main > div.d14 > div > div.d37 > div.d38 > img').get('src')}"
			tempContent["title"] = soup.select_one("#main > div.d14 > div > div.d37 > div.d39 > div.d40").get_text()
			tempContent["status"] = soup.select_one("#main > div.d14 > div > div.d37 > div.d39 > table > tbody > tr:nth-child(4) > td:nth-child(2)").get_text()
			tempContent["author"] = soup.select_one("#main > div.d14 > div > div.d37 > div.d39 > table > tbody > tr:nth-child(5) > td:nth-child(2)").get_text().strip().split(",")[0]

			genresSelector = soup.select("#main > div.d14 > div > div.d37 > div.d39 > table > tbody > tr:nth-child(7) > td:nth-child(2) > a")
			tempContent["genres"] = ", ".join(i.get_text() for i in genresSelector)

			chapterList = []
			chapterSelector = soup.select("#main > div.d14 > div > table > tbody > tr > td > a")
			for items in chapterSelector:
				tempChapter = {}
				tempChapter["title"] = items.get_text().strip()
				tempChapter["id"] = items.get("href").split("/", 1)[1]
				chapterList.append(tempChapter)

			tempContent["chapters"] = chapterList
			self.results["results"] = tempContent
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results
		
	def pages(self, id: str):
		try:
			url = f"{self.parent_url}/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			imgSelectors = soup.select("#ib > div > img")
			images = [i.get("data-src") for i in imgSelectors]

			self.results["results"] = images
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results
		
	def latest(self, genre: str = ""):
		try:
			url = f"{self.parent_url}/genre/{genre}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("#main > div.d14 > div > div.d38 > div.d39 > table > tbody > tr")

			for card in cards:
				tempContent = {}
				tempContent["title"] = card.find("div", class_="d42").find("a").get_text()
				tempContent["id"] = card.find("div", class_="d42").find("a").get("href").split("/")[2]
				tempContent["image"] = f"{self.parent_url}{card.find('div', class_='d41').get('data-src')}"
				tempContent["author"] = card.find("div", class_="d43").get_text().strip().replace("\n", "").split(",")[:-1]
				tempContent["chapters"] = card.find("div", class_="d44").get_text().strip().split(" ")[0].replace("\xa0", " ")
				tempContent["status"] = card.find("div", class_="d44").get_text().strip().split(" ")[-1][1:-1]
				tempContent["genres"] = card.find("div", class_="d46").get_text().strip().replace(" ", "").replace("\n", " ").split(",")[:-1]
				self.results["results"].append(tempContent)
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results
		