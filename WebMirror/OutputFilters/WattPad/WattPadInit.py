
if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()


from settings import WATTPAD_AUTH_CREDS
import logging

logger = logging.getLogger("Main.Wattpad.Authenticator")

def check_logged_in(wg):
	soup = wg.getSoup("https://www.wattpad.com/home")
	uname = soup.find("span", class_='username')
	if uname and WATTPAD_AUTH_CREDS['username'] in uname.get_text():
		return True
	return False

def log_in(wg):
	soup = wg.getSoup("https://www.wattpad.com/login")

	auth = {
		'username' : WATTPAD_AUTH_CREDS['username'],
		'password' : WATTPAD_AUTH_CREDS['password']
	}

	soup = wg.getSoup("https://www.wattpad.com/login?nextUrl=https://www.wattpad.com/home", postData=auth)

	now_logged_in = check_logged_in(wg)
	if not now_logged_in:
		logger.error("ERROR! Login failed!")
	return now_logged_in

def init_call(fetcher):
	assert WATTPAD_AUTH_CREDS
	logger.info("WattPad Initializer called")
	have_login = check_logged_in(fetcher.wg)
	if not have_login:
		have_login = log_in(fetcher.wg)
	logger.info("Is logged in: %s",  have_login)


if __name__ == '__main__':
	from WebMirror.Fetch import ItemFetcher
	import WebMirror.rules
	ruleset = WebMirror.rules.load_rules()
	fetcher = ItemFetcher(ruleset, "http://www.example.org", "http://www.example.org")

