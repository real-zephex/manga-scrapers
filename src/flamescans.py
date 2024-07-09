from bs4 import BeautifulSoup
import requests

class Flamescans:
	def __init__(self) -> None:
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.parent_url = "https://flamecomics.me"
		self.results  = {
			"status": "",
			"results": []
		}
	
	def search(self, query:str):
		try:
			newQuery = query.replace(" ", "+")
			url = f"{self.proxy_url}{self.parent_url}/?s={newQuery}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("div.wrapper > div.postbody > div > div.listupd > div > div")

			for items in cards:
				tempContent = {}
				tempContent["title"] = items.find("a").get("title")
				tempContent["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
				tempContent["image"] = items.find("img", class_="ts-post-image wp-post-image attachment-medium size-medium").get("src")
				tempContent["status"] = items.find("a").find("div", class_="bigor").find("div", class_="extra-info").find("div", class_="imptdt").find("div", class_="status").find("i").get_text()
				self.results["results"].append(tempContent)

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

	def info(self, id:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/series/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			content = {}
			content["image"] = soup.select_one("div.main-info > div.first-half > div.thumb-half > div.thumb > img").get("src")

			infoSelector = soup.select_one("div.main-info > div.first-half > div.info-half")
			content["title"] = infoSelector.find("div", class_="titles").find("h1", class_="entry-title").get_text()
			
			genreSelector = soup.select("div.main-info > div.first-half > div.info-half > div.genres-container > div > span > a")
			content["genres"] = ", ".join(i.get_text() for i in genreSelector).split(", ")

			content["description"] = infoSelector.find("div", class_="summary").find("div", class_="wd-full").find("div", class_="entry-content entry-content-single").get_text().strip()

			moreInfoSelector = soup.select_one("div.main-info > div.second-half > div.left-side > div")
			content["type"] = moreInfoSelector.select_one("div:nth-child(1) > i").get_text()
			content["status"] = moreInfoSelector.select_one("div:nth-child(2) > i").get_text()
			content["year"] = moreInfoSelector.select_one("div:nth-child(3) > i").get_text()
			content["author"] = moreInfoSelector.select_one("div:nth-child(4) > i").get_text()
			content["artist"] = moreInfoSelector.select_one("div:nth-child(5) > i").get_text()
			content["serialization"] = moreInfoSelector.select_one("div:nth-child(6) > i").get_text()

			chapterSelector = soup.select("#chapterlist > ul > li")
			chapter = []
			for chap in chapterSelector:
				tempChapter = {}
				tempChapter["id"] = chap.find("a").get("href").rsplit("/", 2)[-2]
				tempChapter["title"] = chap.find("div", class_="chbox").find("div", class_="eph-num").find("span", class_="chapternum").get_text().strip().replace("\n", " ")
				chapter.append(tempChapter)
			content["chapters"] = chapter[::-1]

			self.results["results"] = content
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results
	
	def pages(self, id:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			imageSelector = soup.select("#readerarea > p > img")
			self.results["results"] = [i.get("src") for i in imageSelector]

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results
	
	def sort(self, type:str = ""):
		try:
			url = f"{self.proxy_url}{self.parent_url}/series/?order={type}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cardsSelector = soup.select("div.wrapper > div.postbody > div.bixbox.seriesearch > div.mrgn > div.listupd > div > div.bsx")

			for items in cardsSelector:
				tempContent = {}
				tempContent["title"] = items.find("a").get("title")
				tempContent["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
				tempContent["image"] = items.find("img", class_="ts-post-image wp-post-image attachment-medium size-medium").get("src")
				tempContent["status"] = items.find("a").find("div", class_="bigor").find("div", class_="extra-info").find("div", class_="imptdt").find("div", class_="status").find("i").get_text()
				self.results["results"].append(tempContent)

			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results