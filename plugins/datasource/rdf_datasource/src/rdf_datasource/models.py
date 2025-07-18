class Friend:
    def __init__(self, friend_body: dict) -> None:
        self.id = friend_body["id"]
        self.name = friend_body["name"]
        self.age = friend_body["age"]
        self.gender = friend_body["gender"]
        
    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {self.age}, {self.gender}"
        