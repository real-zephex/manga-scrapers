from bs4 import BeautifulSoup
import requests

class Mangaworld:
	def __init__(self) -> None:
		self.parent_url = "https://www.mangaworld.ac"
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.results  = {
			"status": None,
			"results": []
		}

	def search(self, query:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/archive?keyword={query}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cardSelector = soup.select("body > div.container > div > div > div.comics-grid > div.entry")

			for card in cardSelector:
				tempContent = {}
				tempContent["title"] = card.find("div", class_="content").find("p", class_="name").get_text()
				tempContent["id"]  =card.find("a", class_="thumb position-relative").get("href").split("/", 3)[3]
				tempContent["image"] = card.find("a", class_="thumb position-relative").find("img").get("src")
				tempContent["type"] = card.find("div", class_="content").find("div", class_="genre").find("a").get_text()
				tempContent["author"] = card.find("div", class_="content").find("div", class_="author").find("a").get_text()
				tempContent["status"] = card.find("div", class_="content").find("div", class_="status").find("a").get_text()
				tempContent["artist"] = card.find("div", class_="content").find("div", class_="artist").find("a").get_text()
				tempContent["genres"] = ", ".join(i.get_text() for i in card.find("div", class_="content").find("div", class_="genres").find_all("a"))
				
				self.results["results"].append(tempContent)
			
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

	def info(self, id:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			content = {}
			infoPaneSelector = soup.select_one("#manga-page > div > div > div.col-sm-12.col-md-8.col-xl-9 > div > div:nth-child(1) > div.has-shadow.comic-info.d-block.d-sm-flex > div.info")
			content["title"] = infoPaneSelector.find("h1", class_="name bigger").get_text()
			content["alt-titles"] = infoPaneSelector.find("div", class_="meta-data").find("div", class_="col-12").get_text().split(": ", 1)[1].strip()
			content["image"] = soup.select_one("#manga-page > div > div > div.col-sm-12.col-md-8.col-xl-9 > div > div:nth-child(1) > div.has-shadow.comic-info.d-block.d-sm-flex > div.thumb.mb-3.text-center > img").get("src")
			content["type"] = infoPaneSelector.find("div", class_="meta-data").find_all("div", class_="col-12 col-md-6")[2].find("a").get_text()
			content["description"] = soup.select_one("#noidungm").get_text()
			content["status"] = infoPaneSelector.find("div", class_="meta-data").find_all("div", class_="col-12 col-md-6")[3].find("a").get_text()
			content["author"] = infoPaneSelector.find("div", class_="meta-data").find("div", class_="col-12 col-md-6").find("a").get_text()
			content["artist"] = infoPaneSelector.find("div", class_="meta-data").find_all("div", class_="col-12 col-md-6")[1].find("a").get_text()
			content["genres"] = ", ".join(i.get_text() for i in infoPaneSelector.find("div", class_="meta-data").find_all("div", class_="col-12")[1].find_all("a"))

			chapterSelector = soup.select("#chapterList > div.chapters-wrapper.py-2.pl-0 > div > div.volume-chapters.pl-2 > div.chapter")
			if len(chapterSelector) == 0:
				chapterSelector = soup.select("#chapterList > div.chapters-wrapper.py-2.pl-0 > div")
			chapter = []
			
			for item in chapterSelector:
				tempChapter = {}
				tempChapter["id"] = item.find("a", class_="chap").get("href").split("/", 3)[3]
				tempChapter["title"] = item.find("a", class_="chap").get("title")
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

			imagesSelector = soup.select("#page > img")
			for i in imagesSelector:
				self.results["results"].append(i.get("src"))
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

print(Mangaworld().info("manga/1941/omniscient-reader-s-viewpoint"))