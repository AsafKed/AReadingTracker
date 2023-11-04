class Book:
    from .Author import Author
    def __init__(self, title: str, authors: [Author], link: str, rating: float, rating_count: int):
        self.title = title
        self.authors = authors
        self.link = link
        self.rating = rating
        self.rating_count = rating_count