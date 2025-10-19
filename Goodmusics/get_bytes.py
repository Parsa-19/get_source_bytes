import requests
import concurrent.futures
import json
import urllib.request

def read_urls() -> list:
	with open('goodmusics_downloads.txt', 'r') as file:
		return file.readlines()


class ByteExtractingActions(object):

	def __init__(self):
		self.total_bytes = 0

	def get_total_bytes(self):
		return self.total_bytes

	def add_to_total_bytes(self, byte):
		self.total_bytes += byte

	def remove_successful_byte_extracted_url(self, url):
		with open('goodmusics_downloads.txt', '') as f:
			pass

	def write_to_corrupt_status_urls(self, url):
		with open('corrupt_status_urls.txt', 'a') as f:
			f.write(url + '\n')

	def write_to_corrupt_byte_urls(self, url, corrupt_byte):
		with open('corrupt_byte_urls.txt', 'a') as f:
			f.write(f'{url}\t->  {corrupt_byte}\n')

	def extraction_procedure(self, url):
		''' <psudo-code>
		try:
			make request
			extract Byte
			total_bytes += byte
			remove the successfull byte extracted url from source file 

		except: 
			write the total_byte to destination bytes file
			log the url
			write the url response to the interupted_response file 
			(should guid me how to start the script on the rest of the urls)
		'''

		url = url[:-1] # remove the \n
		print(url)

		resp = requests.get(url, stream=True)
		if resp.status_code != 200:
			self.write_to_corrupt_status_urls(url) # to make request on it later
		print(resp.status_code)

		byte = resp.headers.get('Content-Length')
		if not byte:
			self.write_to_corrupt_byte_urls(url, byte)
			return 0
		byte = int(byte)
		print(byte)
		
		self.add_to_total_bytes(byte)

		# self.remove_successful_byte_extracted_url(url)



def main(MAX_THREADS):

	urls = read_urls()
	urls = urls[:1]
	byte_man = ByteExtractingActions()

	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
		list(executor.map(byte_man.extraction_procedure, urls))



if __name__ == '__main__':
	'''
	consider when running the script from the scratch:
	remove data in these files:
		- corrupt_byte_urls.txt
		- corrupt_status_urls.txt
	by each successfull byte extraction from url; that url will be removed from the "goodmusics_downloads.txt" so refill it from the "downloads_links_backup"
	the result is in total_bytes.txt so empty that as well too.
	'''	
	main(MAX_THREADS=8)