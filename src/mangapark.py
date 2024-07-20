from bs4 import BeautifulSoup
import requests
import json
import re

class Mangapark:
	def __init__(self) -> None:
		self.parent_url = "https://mangapark.net"
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.results  = {
			"status": None,
			"results": []
		}
		self.pattern = r"https:\/\/xfs-n\d+\.xfspp\.com\/comic\/\d+\/[a-zA-Z0-9]+\/[a-f0-9]+\/\d+_\d+_\d+_\d+\.(?:webp|jpeg)"
		self.pattern_two = r"https:\/\/xfs-n\d+\.xfspp\.com\/comic\/\d+\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+\/\d+_[a-zA-Z0-9]+_\d+_\d+\.(?:webp|jpeg)"
		self.pattern_three = r"https:\/\/xfs-n\d+\.xfspp\.com\/comic\/\d+\/images+\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+_\d+_\d+_\d+\.(?:webp|jpeg|jpg)"
		

	def search(self, query:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/search?word={query}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cardSelector = soup.select("#app-wrapper > main > div.grid.gap-5.grid-cols-1.border-t.border-t-base-200.pt-5 > div")

			for card in cardSelector:
				tempContent = {}
				tempContent["title"] = card.find("h3", class_="font-bold space-x-1").get_text()
				tempContent["image"] = card.find("div", class_="shrink-0 basis-20 md:basis-24").find("div", class_="group relative w-full").find("a").find("img").get("src")
				tempContent["id"] = card.find("h3", class_="font-bold space-x-1").find("a", class_="link-hover link-pri").get("href").split("/")[2]
				try:
					tempContent["authors"] = card.find("div", attrs={"q:key": "6N_0"}).get_text()
				except:
					tempContent["authors"] = "?"
				self.results["results"].append(tempContent)
			
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results
		
	def info(self, id:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/title/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			content = {}
			content["image"] = soup.select_one("#app-wrapper > main > div.flex.flex-col > div.flex > div.w-24 > img").get("src")

			headerSection = soup.select_one("#app-wrapper > main > div.flex.flex-col > div.mt-3 > div.space-y-2.hidden")
			content["title"] = headerSection.find("h3").get_text()
			try:
				content["altTitle"] = ", ".join(i.get_text() for i in headerSection.find("div", attrs={"q:key": "tz_2"}).find_all("span") if i.get_text() != " / ")
			except:
				content["altTitle"] = "?"
			content["author"] = ", ".join(i.get_text() for i in headerSection.find("div", attrs={"q:key": "tz_4"}).find_all("a"))

			middleSection = soup.select_one("#app-wrapper > main > div.flex.flex-col > div.mt-3 > div:nth-child(2)")
			content["genres"] = " ".join(i.get_text() for i in middleSection.find("div", attrs={"q:key": "30_2"}).find_all("span"))
			content["status"] = middleSection.find("div", attrs={"q:key": "Yn_8"}).find("span", attrs={"q:key": "Yn_5"}).get_text()

			content["description"] = " ".join(i.get_text() for i in soup.select_one("#app-wrapper > main > div.flex.flex-col > div.mt-3 > div > div > div.overflow-y-hidden.max-h-28 > div:nth-child(1) > react-island > div").find_all("div"))

			chapterSelector = soup.select("#app-wrapper > main > div:nth-child(5) > div:nth-child(2) > div > div > div > div.space-x-1")
			chapters = []

			for chapter in chapterSelector:
				tempChapter = {}
				tempChapter["id"] = chapter.find("a").get("href").split("/", 2)[2]
				tempChapter["title"] = chapter.find("a").get_text()
				chapters.append(tempChapter)
			
			content["chapters"] = chapters[::-1]

			self.results["results"] = content
			return self.results
		

		except Exception as e:
			self.results["results"] = e
			return self.results
		
	def pages(self, id:str):
		try:
			url = f"{self.proxy_url}{self.parent_url}/title/{id}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			scriptTags = soup.find_all("script")
			jsonify = json.loads(scriptTags[-4].text)			
			pages = []
			
			for i in jsonify["objs"]:
				try:
					if re.match(self.pattern, i) or re.match(self.pattern_two, i) or re.match(self.pattern_three, i):
						pages.append(i)
				except:
					pass
			self.results["results"] = pages
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results

	def latest(self, page:str = "1"):
		try:
			url = f"{self.proxy_url}{self.parent_url}/latest/{page}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cardSelector = soup.select("#app-wrapper > main > div > div.space-y-5 > div.grid.gap-5.grid-cols-1.border-t.border-t-base-200.pt-3 > div")

			for card in cardSelector:
				content = {}
				content["image"] = card.find("img").get("src")
				content["title"] = card.find("div", class_="pl-3 grow flex flex-col space-y-1 group").find("h3").get_text()
				content["id"] = card.find("div", class_="pl-3 grow flex flex-col space-y-1 group").find("h3").find("a").get("href").split("/")[2]
				content["chapterReleased"] = card.find("div", attrs={"q:key": "R7_8"}).find("span").find("a").get_text()
				self.results["results"].append(content)
			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results

