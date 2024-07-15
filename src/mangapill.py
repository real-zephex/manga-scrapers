from bs4 import BeautifulSoup
import requests

class Mangapill:
	def __init__(self) -> None:
		self.proxy_url = "https://sup-proxy.zephex0-f6c.workers.dev/api-text?url="
		self.parent_url = "https://mangapill.com"
		self.results  = {
			"status": "",
			"results": []
		}

	def search(self, query: str):
		try:
			newQuery = query.replace(" ", "+")
			url = f"{self.proxy_url}{self.parent_url}/search?q={newQuery}"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")

			cards = soup.select("body > div.container.py-3 > div.my-3.grid.justify-end.gap-3.grid-cols-2 > div")

			for items in cards:
				tempContent = {}
				tempContent["id"] = items.find("a", class_="relative block").get("href").split("/", 1)[1]
				tempContent["title"] = items.find("div", class_="mt-3 font-black leading-tight line-clamp-2").get_text()
				try:
					tempContent["subheading"] = items.find("div", class_="line-clamp-2 text-xs text-secondary mt-1").get_text()
				except:
					tempContent["subheading"] = "?"
				tempContent["image"] = items.find("a", class_="relative block").find("figure").find("img").get("data-src") # MARK: Referer is required
				genresSelector = items.find("div", class_="flex flex-wrap gap-1 mt-1").find_all("div")
				tempContent["type"] = genresSelector[0].get_text()
				tempContent["year"] = genresSelector[1].get_text()
				tempContent["status"] = genresSelector[2].get_text()
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

			tempContent = {}
			tempContent["image"] = soup.select_one("body > div.container > div.flex.flex-col > div.text-transparent.flex-shrink-0.w-60.h-80.relative.rounded.bg-card.mr-3.mb-3 > img").get("data-src")
			tempContent["title"] = soup.select_one("body > div.container > div.flex.flex-col > div.flex.flex-col > div:nth-child(1) > h1").get_text()
			tempContent["description"] = soup.select_one("body > div.container > div.flex.flex-col > div.flex.flex-col > div:nth-child(2) > p").get_text()
			tempContent["type"] = soup.select_one("body > div.container > div.flex.flex-col > div.flex.flex-col > div.grid.grid-cols-1 > div:nth-child(1) > div").get_text()
			tempContent["status"] = soup.select_one("body > div.container > div.flex.flex-col > div.flex.flex-col > div.grid.grid-cols-1 > div:nth-child(2) > div").get_text()
			tempContent["year"] = soup.select_one("body > div.container > div.flex.flex-col > div.flex.flex-col > div.grid.grid-cols-1 > div:nth-child(3) > div").get_text()

			genresSelector = soup.select("body > div.container > div.flex.flex-col > div.flex.flex-col > div:nth-child(4) > a")
			tempContent["genres"] = [i.get_text() for i in genresSelector]

			chapterSelector = soup.select("#chapters > div > a")
			chapters = []
			for items in chapterSelector:
				tempChapters = {}
				tempChapters["title"] = items.get_text()
				tempChapters["id"] = items.get("href").split("/", 1)[1]
				chapters.append(tempChapters)
			tempContent["chapters"] = chapters[::-1]

			self.results["results"] = tempContent
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

			imageSelector = soup.select("body > div > chapter-page > div > div.relative.bg-card.flex.justify-center.items-center > picture > img")
			self.results["results"] = [i.get("data-src") for i in imageSelector]
			return self.results

		except Exception as e:
			self.results["results"] = e
			return self.results	

	def new(self, type:str): # Same as search
		try:
			url = f"{self.proxy_url}{self.parent_url}/mangas/new"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")	

			cards = soup.select("body > div.container.py-3 > div.grid.justify-end.gap-3.grid-cols-2 > div")

			for items in cards:
				tempContent = {}
				tempContent["id"] = items.find("a", class_="relative block").get("href").split("/", 1)[1]
				tempContent["title"] = items.find("div", class_="mt-3 font-black leading-tight line-clamp-2").get_text()
				try:
					tempContent["subheading"] = items.find("div", class_="line-clamp-2 text-xs text-secondary mt-1").get_text()
				except:
					tempContent["subheading"] = "?"
				tempContent["image"] = items.find("a", class_="relative block").find("figure").find("img").get("data-src") # MARK: Referer is required
				genresSelector = items.find("div", class_="flex flex-wrap gap-1 mt-1").find_all("div")
				tempContent["type"] = genresSelector[0].get_text()
				tempContent["year"] = genresSelector[1].get_text()
				tempContent["status"] = genresSelector[2].get_text()
				self.results["results"].append(tempContent)

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results	

	def recent(self): # Same as search
		try:
			url = f"{self.proxy_url}{self.parent_url}/chapters"
			response = requests.get(url)
			self.results["status"] = response.status_code
			soup = BeautifulSoup(response.content, "html.parser")	

			cards = soup.select("body > div.container.py-3 > div.grid.grid-cols-2 > div")

			for items in cards:
				tempContent = {}
				tempContent["id"] = items.find("div", class_="px-1").find("a", class_="mt-1.5 leading-tight text-secondary").get("href").split("/", 1)[1]
				tempContent["image"] = items.find("a").find("figure").find("img").get("data-src")
				tempContent["title"] = items.find("div", class_="px-1").find("a", class_="mt-1.5 leading-tight text-secondary").find("div", class_="line-clamp-2 text-sm font-bold").get_text()
				self.results["results"].append(tempContent)

			return self.results
		except Exception as e:
			self.results["results"] = e
			return self.results	