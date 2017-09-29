


class WebGetException(Exception):
	pass

class ContentTypeError(WebGetException):
	pass

class ArgumentError(WebGetException):
	pass

class FetchFailureError(WebGetException):
	pass

