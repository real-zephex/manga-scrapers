from bs4 import BeautifulSoup
import requests

class Manganato:
	def __init__(self) -> None:
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.parent_url = "https://manganato.com"
		self.chapter_url = "https://chapmanganato.to"
		self.results  = {
			"status": "",
			"results": []
		}

	def search(self, query):
		try:
			url = f"{self.proxy_url}{self.parent_url}/search/story/{query}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-search-story > div")

			for items in cards:
				tempContent = {}
				tempContent["id"] = items.find("a", class_="item-img").get("href").rsplit("/", 1)[1]
				tempContent["title"] = items.find("div", class_="item-right").find("h3").find("a", class_="a-h text-nowrap item-title").get_text()
				tempContent["image"] = items.find("img", class_="img-loading").get("src")
				tempContent["author"] = items.find("span", class_="item-author").get("title")
				tempContent["heading"] = items.find("a")["title"]
				tempContent["updated"] = items.find("span", class_="item-time").get_text().split(":", 1)[1].strip().split(" - ")
				self.results["results"].append(tempContent)

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

	def info(self, id):
		try:
			url = f"{self.proxy_url}{self.chapter_url}/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			tempContent = {}
			tempContent["image"] = soup.select_one("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-info > div.story-info-left > span.info-image > img").get("src")
			infoPanel = soup.select_one("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-info > div.story-info-right")
			tempContent["title"] = infoPanel.find("h1").get_text()
			tempContent["author"] = infoPanel.find("a", class_="a-h").get_text()
			tempContent["status"] = soup.select_one("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-info > div.story-info-right > table > tbody > tr:nth-child(3) > td.table-value").get_text()
			genres = soup.select_one("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-info > div.story-info-right > table > tbody > tr:nth-child(4) > td.table-value").find_all("a", class_="a-h")
			tempContent["genres"] = ", ".join(i.get_text() for i in genres)
			tempContent["description"] = soup.select_one("#panel-story-info-description").get_text().strip().removeprefix("Description :\r\n        ")

			chapters = soup.select("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-chapter-list > ul > li")
			chapDic = []
			for items in chapters:
				tempChap = {}
				tempChap["title"] = items.find("a", class_="chapter-name").get_text()
				tempChap["id"] = items.find("a", class_="chapter-name").get("href").split("https://chapmanganato.to/")[1]
				chapDic.append(tempChap)

			tempContent["chapters"] = chapDic[::-1]

			self.results["results"] = tempContent
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

	def pages(self, id):
		try:
			url = f"{self.proxy_url}{self.chapter_url}/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			images_selector = soup.select("body > div.body-site > div.container-chapter-reader > img")
			images_url = [i.get("src") for i in images_selector]

			self.results["results"] = images_url
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results	

	def latest(self, page: str = 1):
		try:
			url = f"{self.proxy_url}{self.parent_url}/genre-all/{page}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("body > div.body-site > div.container.container-main > div.panel-content-genres > div")
			
			for items in cards:
					tempContent = {}
					tempContent["img"] = items.find("img", class_="img-loading").get("src")
					tempContent["title"] = items.find("div", class_="genres-item-info").find("h3").find("a", class_="genres-item-name").get_text()
					tempContent["id"] = items.find("div", class_="genres-item-info").find("h3").find("a", class_="genres-item-name").get("href").rsplit("/", 1)[1]
					infoSelector = items.select_one("body > div.body-site > div.container.container-main > div.panel-content-genres > div > div > p")
					tempContent["date"] = infoSelector.find("span", class_="genres-item-time").get_text()
					tempContent["author"] = infoSelector.find("span", class_="genres-item-author").get_text()
					tempContent["description"] = items.select_one("body > div.body-site > div.container.container-main > div.panel-content-genres > div > div > div").get_text().strip()
					self.results["results"].append(tempContent)
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results	

	def newest(self, page: str = 1):
		try:
			url = f"{self.proxy_url}{self.parent_url}/genre-all/{page}?type=newest"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("body > div.body-site > div.container.container-main > div.panel-content-genres > div")
			
			for items in cards:
					tempContent = {}
					tempContent["img"] = items.find("img", class_="img-loading").get("src")
					tempContent["title"] = items.find("div", class_="genres-item-info").find("h3").find("a", class_="genres-item-name").get_text()
					tempContent["id"] = items.find("div", class_="genres-item-info").find("h3").find("a", class_="genres-item-name").get("href").rsplit("/", 1)[1]
					infoSelector = items.select_one("body > div.body-site > div.container.container-main > div.panel-content-genres > div > div > p")
					tempContent["date"] = infoSelector.find("span", class_="genres-item-time").get_text()
					tempContent["author"] = infoSelector.find("span", class_="genres-item-author").get_text()
					tempContent["description"] = items.select_one("body > div.body-site > div.container.container-main > div.panel-content-genres > div > div > div").get_text().strip()
					self.results["results"].append(tempContent)
					
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results	

	def hotest(self, page:str = 1):
		try:
			url = f"{self.proxy_url}{self.parent_url}/genre-all/{page}?type=topview"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("body > div.body-site > div.container.container-main > div.panel-content-genres > div")
			
			for items in cards:
					tempContent = {}
					tempContent["img"] = items.find("img", class_="img-loading").get("src")
					tempContent["title"] = items.find("div", class_="genres-item-info").find("h3").find("a", class_="genres-item-name").get_text()
					tempContent["id"] = items.find("div", class_="genres-item-info").find("h3").find("a", class_="genres-item-name").get("href").rsplit("/", 1)[1]
					infoSelector = items.select_one("body > div.body-site > div.container.container-main > div.panel-content-genres > div > div > p")
					tempContent["date"] = infoSelector.find("span", class_="genres-item-time").get_text()
					tempContent["author"] = infoSelector.find("span", class_="genres-item-author").get_text()
					tempContent["description"] = items.select_one("body > div.body-site > div.container.container-main > div.panel-content-genres > div > div > div").get_text().strip()
					self.results["results"].append(tempContent)

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results	


print(Manganato().search("solo leveling"))