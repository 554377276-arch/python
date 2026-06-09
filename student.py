class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def update_score(self, new_score):
        self.score = new_score

    def __str__(self):
        return f"姓名:{self.name}, 成绩:{self.score}"