import requests
from bs4 import BeautifulSoup
from transformers import pipeline


class WebContentAggregator:
    def __init__(self):
        self.search_query = ""

    def get_search_query(self):
        self.search_query = input("Enter your search query: ")

    def search_web(self):
        search_results = self.fetch_search_results(self.search_query)
        relevant_info = self.extract_info_from_webpages(search_results)
        curated_content = self.curate_content(relevant_info)
        validated_content = self.validate_sources(curated_content)
        filtered_content = self.filter_results(validated_content)

        return filtered_content

    def fetch_search_results(self, query):
        url = f"https://www.google.com/search?q={query}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        search_results = soup.find_all("div", class_="g")
        return search_results

    def extract_info_from_webpages(self, search_results):
        info_list = []
        for result in search_results:
            title = result.find("h3").text
            summary = result.find("span", class_="st").text
            url = result.find("a")["href"]
            metadata = self.get_metadata(url)

            info = {
                "title": title,
                "summary": summary,
                "url": url,
                "metadata": metadata,
            }
            info_list.append(info)

        return info_list

    def get_metadata(self, url):
        # Fetch metadata for a given URL
        return {}

    def curate_content(self, info_list):
        summarizer = pipeline("summarization")
        for info in info_list:
            content = info["summary"]
            summary = summarizer(content, max_length=100, min_length=20)[
                0]["summary_text"]
            info["summary"] = summary

        return info_list

    def validate_sources(self, curated_content):
        validated_content = []
        for info in curated_content:
            source = info["url"]
            credibility = self.validate_source(source)

            if credibility > 0.8:
                validated_content.append(info)

        return validated_content

    def validate_source(self, source):
        # Validate the credibility of a source website
        return 0.9

    def filter_results(self, validated_content):
        # Apply user-defined filters to the content
        filtered_content = []
        for info in validated_content:
            # Apply filters based on publication date, website authority, and keywords
            filtered_content.append(info)

        return filtered_content


class DownloadManager:
    def download_content(self, content):
        # Implement the functionality to download selected content
        for i, info in enumerate(content, start=1):
            title = info["title"]
            url = info["url"]
            file_name = f"{i}_{title}.txt"

            response = requests.get(url)
            with open(file_name, "wb") as file:
                file.write(response.content)

            print(f"Downloaded {file_name}")


class FeedbackManager:
    def provide_feedback(self, content):
        # Implement the functionality to provide feedback on content quality and relevance
        for i, info in enumerate(content, start=1):
            title = info["title"]
            feedback = input(f"Provide feedback for {title}: ")
            # Save feedback to a database or file


class SearchPreferenceManager:
    def customize_search_preferences(self):
        # Implement the functionality to customize search preferences
        print("Search Preferences:")
        # Allow users to set preferences such as filters, search criteria, etc.


class Dashboard:
    def __init__(self):
        self.content_aggregator = WebContentAggregator()
        self.download_manager = DownloadManager()
        self.feedback_manager = FeedbackManager()
        self.search_preference_manager = SearchPreferenceManager()

    def start(self):
        self.display_welcome_message()
        self.content_aggregator.get_search_query()
        self.display_search_results()
        self.display_dashboard()

    def display_welcome_message(self):
        print("Welcome to the Web Content Aggregator Dashboard!")

    def display_search_results(self):
        search_results = self.content_aggregator.search_web()
        for i, result in enumerate(search_results, start=1):
            print(f"\nResult {i}:")
            print(f"Title: {result['title']}")
            print(f"Summary: {result['summary']}")
            print(f"URL: {result['url']}")

    def display_dashboard(self):
        print("Dashboard options:")
        print("1. Download content")
        print("2. Provide feedback")
        print("3. Customize search preferences")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.download_content()
        elif choice == "2":
            self.provide_feedback()
        elif choice == "3":
            self.customize_search_preferences()
        elif choice == "4":
            print("Exiting...")
        else:
            print("Invalid choice. Please try again.")
            self.display_dashboard()

    def download_content(self):
        search_results = self.content_aggregator.search_web()
        self.download_manager.download_content(search_results)

    def provide_feedback(self):
        search_results = self.content_aggregator.search_web()
        self.feedback_manager.provide_feedback(search_results)

    def customize_search_preferences(self):
        self.search_preference_manager.customize_search_preferences()


dashboard = Dashboard()
dashboard.start()
