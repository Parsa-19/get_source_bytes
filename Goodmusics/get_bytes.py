import requests
import concurrent.futures
import json
import urllib.request
import time




class ReadFiles(object):

	def read_urls_as_list(self) -> list:
		with open('goodmusics_downloads.txt', 'r') as file:
			return file.readlines()

	def get_source_file_str(self):
		with open('goodmusics_downloads.txt', 'r') as f:
			return f.read()


class ByteExtractingActions(ReadFiles):

	def __init__(self):
		'''
		A variable for each file to store and write 
		in their corresponding files at the end
		'''
		self.total_bytes = 0
		self.source_file_str = self.get_source_file_str()
		self.corrupt_status_urls = []
		self.corrupt_byte_urls = []

		self.counter = 0

	def get_total_bytes(self):
		return self.total_bytes

	def add_to_total_bytes(self, byte):
		self.total_bytes += byte

	def remove_url_from_source_str(self, url):	
		self.source_file_str = self.source_file_str.replace(url+'\n', '')
	
	def get_source_file_str_instance_variable(self):
		return self.source_file_str

	def add_url_to_corrupt_status_urls(self, url):
		self.corrupt_status_urls.append(url)

	def add_url_to_corrupt_byte_urls(self, url):
		self.corrupt_byte_urls.append(url)

	def prettified_url_report(self, url, byte):
		print(f'''{'_'*80}
({self.counter})- {byte} \t {url}
			''')


	def extraction_procedure(self, url):
		''' <psudo>
		try:
			make request
			extract Byte
			total_bytes += byte
			remove the successfull byte extracted url from source file

			log everything
		
		except:  
			shows the exception and continue getting bytes

		finally:
			write the total_byte to [total_bytes.txt]
		'''

		url = url[:-1] # remove the \n

		resp = requests.get(url, stream=True)
		if resp.status_code != 200:
			self.add_url_to_corrupt_status_urls(url)
			self.remove_url_from_source_str(url)
			return 0

		byte = resp.headers.get('Content-Length')
		if not byte:
			url_with_byte_str = f'{url} -> {byte}'
			self.add_url_to_corrupt_byte_urls(url_with_byte_str)
			self.remove_url_from_source_str(url)
			return 0

		byte = int(byte)
		self.add_to_total_bytes(byte)
		self.remove_url_from_source_str(url)
		self.prettified_url_report(url, byte)
		self.counter += 1 
		time.sleep(2)
		
	def get_resault(self):
		return {
			'total_bytes': self.total_bytes, 
			'source_file_str': self.source_file_str, 
			'corrupt_status_urls': self.corrupt_status_urls, 
			'corrupt_byte_urls': self.corrupt_byte_urls
		}

class WriteFiles():

	def write_result(self, result):	
		self.write_source_file_str_to_its_actuall_file(result['source_file_str'])
		self.write_total_bytes_to_its_actual_file(result['total_bytes'])
		self.write_corrupt_status_urls_to_its_actual_file(result['corrupt_status_urls'])
		self.write_corrupt_byte_urls_to_its_actual_file(result['corrupt_byte_urls'])

	
	def write_corrupt_status_urls_to_its_actual_file(self, corrupt_status_urls):
		corrupt_status_urls = '\n'.join(corrupt_status_urls)
		with open('corrupt_status_urls.txt', 'a') as f:
			f.write(corrupt_status_urls)
		
	def write_corrupt_byte_urls_to_its_actual_file(self, corrupt_byte_urls):
		corrupt_byte_urls = '\n'.join(corrupt_byte_urls)
		with open('corrupt_byte_urls.txt', 'a') as f:
			f.write(corrupt_byte_urls)

	def write_total_bytes_to_its_actual_file(self, total_bytes):
		total_bytes = str(total_bytes)
		with open('total_bytes.txt', 'a') as f:
			f.write(total_bytes + '\n')

	def write_source_file_str_to_its_actuall_file(self, source_file_str): 
		with open('goodmusics_downloads.txt', 'w') as f:
			f.write(source_file_str)




def main(MAX_THREADS):

	reader = ReadFiles()
	writer = WriteFiles()
	byte_man = ByteExtractingActions()

	urls = reader.read_urls_as_list()

	

	# try:
	# 	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
	# 		list(executor.map(byte_man.extraction_procedure, urls))

	# except Exception as e:
	# 	print(f"\n[$]PARSA[$] main def exception:\n{e}\n")

	# finally:
	# 	result = byte_man.get_resault()
	# 	writer.write_result(result)


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