from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType

# The defaults headers to be used in requests
headers_ = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'en-US,en;q=0.5',
	'Connection': 'keep-alive',
	'Host':'www.car.gr',
	'Referer':'https://www.google.com/',
	'Sec-Fetch-Dest':'document',
	'Sec-Fetch-Mode':'navigate',
	'Sec-Fetch-Site':'cross-site',
	'Sec-Fetch-User':'?1',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'
}

def user_agent_():
	'''
	Creates a random user agent using different
	software name, operating system and hardware type
	'''
	software_names = [
		SoftwareName.CHROME.value,
		SoftwareName.ANDROID.value,
		SoftwareName.FIREFOX.value,
		SoftwareName.OPERA.value
		]
	operating_systems = [
		OperatingSystem.WINDOWS.value,
		OperatingSystem.LINUX.value,
		OperatingSystem.ANDROID.value,
		OperatingSystem.MAC_OS_X.value,
	] 
	hardware_type = [
		HardwareType.COMPUTER.value,
		HardwareType.MOBILE.value,
		HardwareType.SERVER.value,
	]

	user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, hardware_type=hardware_type, limit=100)
	user_agent = user_agent_rotator.get_random_user_agent()

	return user_agent

