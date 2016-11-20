class ManagementHandler(object):
    """Management Api Operations Handler (e.g. Queue, Exchange)"""

    def __init__(self, http_client):
        self.http_client = http_client
