class ExceptionVulnerabilityManagement(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ExceptionFindingsExcepted(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
