class FakeGist:
    def __init__(self):
        self.comment = None

    def create_comment(self, comment):
        self.comment = comment