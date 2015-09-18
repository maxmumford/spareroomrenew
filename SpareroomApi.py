import requests
from bs4 import BeautifulSoup

SPAREROOM_LOGIN_URL = "http://www.spareroom.co.uk/flatshare/logon.pl"
SPAREROOM_LISTINGS_URL = "http://www.spareroom.co.uk/flatshare/mylistings.pl"
SPAREROOM_RENEW_URL = "http://www.spareroom.co.uk/flatshare/advert_renew.pl"

class SpareroomApi():
	def __init__(self, email, password):
		self.session = requests.Session()
		self.email = email
		self.password = password

	def login(self):
		login = self.session.post(SPAREROOM_LOGIN_URL, {'email': self.email, 'password': self.password})
		if 'META HTTP-EQUIV="Refresh"' not in login.content:
			raise Exception("Cannot log in")

	def get_advert_listings(self):
		listings = self.session.get(SPAREROOM_LISTINGS_URL)
		if '<span class="advert_id">' not in listings.content:
			raise Exception("Cannot find any advert listings")

		html_soup = BeautifulSoup(listings.content)
		self.advert_ids = [span.get_text() for span in html_soup.find_all('span', {'class' : 'advert_id'})]

		if len(self.advert_ids) == 0:
			raise Exception("No adverts found")

	def renew_all(self):
		for advert_id in self.advert_ids:
			renew = self.session.get(SPAREROOM_RENEW_URL, data={'advert_id': advert_id, 'flatshare_type': 'offered'}, allow_redirects=False)
		return self.advert_ids

	def close(self):
		self.session.close()

email = raw_input('Type your spareroom email: ')
password = raw_input('Type your spareroom password: ')

spareroom_api = SpareroomApi(email, password)
spareroom_api.login()
spareroom_api.get_advert_listings()
advert_ids = spareroom_api.renew_all()
spareroom_api.close()

print "Renewed %s advert(s)" % len(advert_ids)
