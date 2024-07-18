from bs4 import BeautifulSoup

from dataclasses import dataclass

import lxml

@dataclass
class Experience:
    title: str
    company: str
    location: str
    start_date: str
    end_date: str
    duration: str
    description: str

@dataclass
class Post:
    type: str
    content: str
    likes: int
    comments: int
    link: str

@dataclass
class Education:
    school: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str
    duration: str
    description: str

@dataclass
class LicenseAndCertification:
    name: str
    issuing_organization: str
    issue_date: str
    expiration_date: str
    credential_id: str

@dataclass
class Project:
    name: str
    description: str
    start_date: str
    end_date: str
    duration: str
    link: str

class LinkedInProfileParser:
    '''
    This class is used to parse a LinkedIn profile and extract useful information from it
    Params:
    - url: The URL of the LinkedIn profile
    - html: The HTML of the LinkedIn profile
    '''
    def __init__(self, url: str, html: str):
        self.url: str = url
        self.html: str = html
        self.name: str = ""
        self.headline: str = ""
        self.location: str = ""
        self.about: str = ""
        self.posts: list[Post] = []
        self.experiences: list[Experience] = []
        self.education: list[Education] = []
        self.licenses_and_certifications: list[LicenseAndCertification] = []

        self._parse()

    def _parse(self):
        src = open(self.html, "r", encoding="utf-8").read()

        if src == None or src == "":
            print("Error reading the file")
            return

        # Now using beautiful soup
        soup = BeautifulSoup(src, 'lxml')

        self.name = soup.find("h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words").text.strip()
        # print(f"Name: {self.name}")

        self.headline = soup.find("div", class_="text-body-medium break-words").text.strip()
        # print(f"Headline: {self.headline}")

        self.location = soup.find("span", class_="text-body-small inline t-black--light break-words").text.strip()
        # print(f"Location: {self.location}")

        profile_cards = soup.find_all("section", attrs={"data-view-name": "profile-card"})
        # print(f"Profile Cards: {len(profile_cards)}")

        for profile_card in profile_cards:
            if profile_card.find("div", id="about"):
                self.about = self._parse_about(profile_card)
                # print(f"About: {self.about}")

            elif profile_card.find("div", id="content_collections"):
                self.posts = self._parse_content_collections(profile_card)
                # print(f"Posts: {len(self.posts)}")

            elif profile_card.find("div", id="experience"):
                self.experiences = self._parse_experience(profile_card)
                # print(f"Experiences: {len(self.experiences)}")

            # elif profile_card.find("div", id="education"):
            #     sections["education"] = profile_card

            # elif profile_card.find("div", id="licenses_and_certifications"):
            #     sections["licenses_and_certifications"] = profile_card

            # elif profile_card.find("div", id="projects"):
            #     sections["projects"] = profile_card

            # elif profile_card.find("div", id="skills"):
            #     sections["skills"] = profile_card

            # elif profile_card.find("div", id="languages"):
            #     sections["languages"] = profile_card

    def _parse_about(self, about_section) -> str | None:
        '''
        This function is used to parse the about section of a LinkedIn profile
        Params:
        - about_section: The about section, in html, of the LinkedIn profile
        Returns:
        - The about text content of the LinkedIn, or None if not found
        '''
        return about_section.find("div", class_="display-flex ph5 pv3").text.replace("…see more", "").strip()
    
    def _parse_content_collections(self, content_collections_section) -> list[Post] | None:
        '''
        This function is used to parse the content collections section, or (posts/shares/likes/etc), of a LinkedIn profile.
        Only the recient posts marked as "posted" are parsed.
        Params:
        - content_collections_section: The content collections section, in html, of the LinkedIn profile
        Returns:
        - A list of Post objects, or None if not found
        '''
        posts: list[Post] = []

        recient_posts = content_collections_section.find("ul", class_="display-flex flex-wrap list-style-none justify-space-between")

        recient_posts = recient_posts.find_all("li", class_="profile-creator-shared-feed-update__mini-container")

        for post in recient_posts:
            
            post_type = post.find("span", class_="feed-mini-update-contextual-description__text").text.strip()

            if "posted" not in post_type:
                continue

            post_type = "posted"
            
            post_content = post.find("div", class_="display-flex flex-row").text.replace("…show more", "").strip()
            post_social = post.find("ul", class_="display-flex")

            post_likes = post_social.find_all("li")[0].text.replace(" likes", "").strip()
            post_comments = post_social.find_all("li")[1].text.replace(" comments", "").strip()

            post_link = post.find("a", class_="app-aware-link")["href"]

            posts.append(Post(type=post_type, content=post_content, likes=post_likes, comments=post_comments, link=post_link))

        return posts
    
    def _parse_experience(self, experience_section) -> list[Experience] | None:
        '''
        This function is used to parse the experience section of a LinkedIn profile
        Params:
        - experience_section: The experience section, in html, of the LinkedIn profile
        Returns:
        - A list of Experience objects, or None if not found
        '''
        experiences: list[Experience] = []

        experiences_html = experience_section.find_all("li", class_="artdeco-list__item")

        for experience_html in experiences_html:
            header = experience_html.find("div", class_="display-flex flex-row justify-space-between")

            body = experience_html.find("ul")

            # print(body)

            header_spans = header.find_all("span", class_="visually-hidden")

            tmp = []

            for span in header_spans:
                tmp.append(span.text)

            experiences.append(Experience(
                title=tmp[0] if len(tmp) > 0 else "",
                company=tmp[1] if len(tmp) > 1 else "",
                start_date=tmp[2] if len(tmp) > 2 else "",
                location=tmp[3] if len(tmp) > 3 else "",
                end_date="",
                duration="",
                description=""
            ))

        print(experiences)

        return experiences