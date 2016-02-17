import random
import logging

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):

	def __init__(self, settings, user_agent='Scrapy'):
		super(RandomUserAgentMiddleware, self).__init__()
		self.user_agent = user_agent

	def process_request(self, request, spider):
		ua = random.choice(self.user_agent_list)
		# ua = "Scrapy/VERSION (+http://scrapy.org)"
		print "*********Current UserAgent: %s*********" %ua
		request.headers.setdefault('User-Agent', ua)

		'''
		the default user_agent_list composes chrome,IE,firefox,Mozilla,
		opera,netscape
		for more user agent strings, you can find it in
		http://www.useragentstring.com/pages/useragentstring.php
		'''

	user_agent_list = [
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
	]