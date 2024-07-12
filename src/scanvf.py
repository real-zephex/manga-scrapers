from bs4 import BeautifulSoup
import requests
import html

class Scanvf:
	def __init__(self) -> None:
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.parent_url = "https://scanvf.org"
		self.results  = {
			"status": "",
			"results": []
		}
	
	def search(self, query:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/search?q={query}"
			response = requests.get(url)
			content = html.unescape(response.json()) # search page didn't have a separate page 
			self.results["status"] = response.status_code
			soup = BeautifulSoup(content, "html.parser")

			cards = soup.select("div.container-fluid > div.row > div > div.series")

			for card in cards:
				tempContent = {}
				tempContent["id"] = card.find("div", class_="last-series-details").find("a").get("href").split("/")[2]
				tempContent["image"] = card.find("div", class_="last-series-details").find("a").find("div", class_="position-relative").find("div", class_="series-img-wrapper").find("img").get("data-src")
				tempContent["title"] = card.find("div", class_="justify-content-center").find("a", class_="link-series").find("h3").get_text()

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

			content = {}
			content["image"] = soup.select_one("body > main > div > div > div > div:nth-child(1) > div.col-12.col-md-auto > div > img").get("src")
			
			infoSelector = soup.select_one("body > main > div > div > div > div:nth-child(1) > div.col-12.col-md > div > div")
			content["title"] = infoSelector.find("div", class_="col-12 mb-4 align-self-center").find("div", class_="d-flex justify-content-between").find("h1").get_text()
			content["description"] = infoSelector.find("div", class_="col-12 mb-4").find("p").get_text()
			
			endContentSelector = soup.select_one("body > main > div > div > div > div:nth-child(1) > div.col-12.col-lg-3.mt-4.mt-lg-0 > div")
			content["author"] = ", ".join(i.get_text() for i in endContentSelector.find("div", class_="col-6 col-md-12 mb-4").find_all("div"))
			content["genres"] = ", ".join(i.get_text() for i in endContentSelector.find_all("div", class_="col-6 col-md-12 mb-4")[1].find_all("div"))

			chapterSelector = soup.select("body > main > div > div > div > div.row.list-books > div > div > div")
			chapters = []

			for chapter in chapterSelector:
				tempChapter = {}
				tempChapter["id"] = chapter.find("a").get("href").split("/")[2]
				tempChapter["title"] = chapter.find("a").find("div").find("h5").get_text().replace("\n", " ")
				chapters.append(tempChapter)
			content["chapters"] = chapters

			self.results["results"] = content
			return self.results
			
		except Exception as e:
			self.results["results"] = e
			return self.results
	
	def pages(self, id:str):
		try:
			for i in range(1, 1000):

				url = f"{self.proxy_url}{self.parent_url}/scan/{id}/{str(i)}"
				response = requests.get(url)
				self.results["status"] = response.status_code
				soup = BeautifulSoup(response.content, "html.parser")

				imageSelector = soup.select_one("body > main > div > div > div > div > div.col.text-center.book-page > img")
				infoPageChecker = soup.select_one("body > main > div > div > div > div:nth-child(1) > div.col-12.col-md > div > div > div:nth-child(3) > p")

				if imageSelector:
					self.results["results"].append(imageSelector.get("src"))
				elif infoPageChecker:
					break

			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results