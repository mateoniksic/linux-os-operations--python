"""
========================================================================
Kratki uvod i upute:
========================================================================
Za pokretanje skripte potrebno je instalirati module:
1. NUMPY: pip install numpy
2. TABULATE: pip install tabulate

Skripta se pokrece u shell-u koristeci naredbu: python3 main.py
------------------------------------------------------------------------

Ako u komentaru nije naveden dio s argumentima ili povratnom vrijednosti
znaci da funkcija ne prima argumente i/ili ne vraca vrijednost.
------------------------------------------------------------------------

F[1-6]Main_* - naziv funkcije sadrzi broj implementirane funkcionalnosti
F[1-6]Helper_* - pomocna funkciju koja se izvrsava u F[1-6]Main_*

main() - glavna funkcija koja se pokrece i preko nje (glavnog izbornika)
se pristupa drugim funkcijama F[1-6]Main_* i preko njih F[1-6]Helper_*.
"""
import threading as th
import signal as sig
import getpass as gp
import tabulate as tab
import numpy as np
import pwd
import time
import os
import errno

USERNAME = gp.getuser()
PC_NAME = os.uname()[1]
USER_PC_NAME = ('\033[0;95;1m\n[' 
				+ USERNAME + '@' + PC_NAME 
				+ ']$\033[0m ')

HIST_DATA = []
MAX_HIST_DATA = 30

TEXT_DECOR_DASH = ('\n' + '-' * 80 + '\n')
TEXT_DECOR_EQUAL = ('\n' + '=' * 80 + '\n')

def print_msg_success(msg):
	"""
	Ispisuje poruku o uspjehu.
	
	Argumenti:
	msg -- "Uspjesno izvodenje", Poruka o uspjehu
	"""
	print(TEXT_DECOR_EQUAL, '\033[0;37;1;42m (' + msg + ') \033[0m',
		  '\n  (Povratak u glavni izbornik...) ', TEXT_DECOR_EQUAL)
	
def print_msg_failure(msg):
	"""
	Ispisuje poruku o neuspjehu.
	
	Argumenti:
	msg -- "Neuspjesno izvodenje", Poruka o neuspjehu
	"""
	print(TEXT_DECOR_EQUAL,
	  '\033[0;37;1;41m (' + msg + ') \033[0m',
	  '\n  (Povratak u glavni izbornik...) ', TEXT_DECOR_EQUAL)
	
def return_user_input(title):
	"""
	Prikazuje naslov ekrana na kojem se korisnik nalazi,
	omogucava unos naredbe korisnika,
	sprema naredbu korisnika u listu HIST_DATA,
	pritisak tipke ENTER ponovno pokrece prikaz poruke za unos naredbe
	
	Argumenti:
	title -- "1 - UNOS NAREDBE", Naslov prikazanog ekrana
	
	Vraća:
	Unos korisnika
	"""
	user_input_error = 0
	
	while True:
		os.system('clear')
	
		print(TEXT_DECOR_EQUAL, title, TEXT_DECOR_EQUAL,
			  '\n(Unesite zeljenu naredbu...)')
	
		if user_input_error != 0:
			print('(Vas unos nije ispravan ili je prazan [{}]...)'.format(user_input_error))
	
		user_input = input(USER_PC_NAME)
		HIST_DATA.append(user_input)
	
		if user_input != '':
			return user_input
			break
		else:
			user_input_error += 1
			continue
	
		user_input_error = 0

def F1Main_enter_command():
	"""
	Omogucuje korisniku da unese odredenu naredbu,
	naredba se moze sastojati od 0 ili vise parametara i argumenata,
	ako naredba nije unesena u roku prikazuje se poruka o zavrsetku unosa,
	unos naredbe cal s parnim mjesecom prikazuje kalendara u formatu za UK,
	prikaz glavnog izbornika nakon izvodenja naredbe ili isteka vremena
	"""
	user_input = return_user_input("1 - UNOS NAREDBE")
	
	commands = user_input.split()
	
	pid = os.fork()
	
	if pid == 0:
		print('\n(Izvodenje procesa DIJETE sa PID-om {}...)\n'.format(os.getpid()), TEXT_DECOR_DASH)
	
		if (commands[0] == 'cal' 
			and len(commands) == 3 
			and int(commands[1]) % 2 == 0):
			print('\nNaredba CAL - PARNI MJESEC - Format UK\n')
			os.execvpe(commands[0], commands, {'LANG': 'en_GB.UTF-8', 'LC_TIME': 'en_GB.UTF-8'})
		else:
			os.execvp(commands[0], commands)
	
	else:
		pid_child, exit_status_child = os.wait()
		print(TEXT_DECOR_DASH, 
			  '\n(Izvodi se proces RODITELJ - PID Dijeteta: {}, Izlazni status: {}...)'
			  .format(pid_child, exit_status_child))
	
		if exit_status_child == 0:
			print_msg_success('Izvodenje naredbe je izvrseno USPJESNO!')
		else:
			print_msg_failure('Izvodenje naredbe je izvrseno NEUSPJESNO!')
	
	time.sleep(6)
	return

def F2Helper_signal_handler(signal_number, frame):
	"""
	Definira kako ce se signal obraditi,prvo se prikaze ime i broj signala,
	zatim se vrijednost varijable frame pohrani u datoteku "stog.txt".
	
	Argumenti:
	signal_number -- "SIGUSR2", Signal koji je poslan
	frame -- "<frame at 0x7f2dc20cf040, file 'main.py', line 193, code enter_signal>", Okvir signala
	"""
	print('Broj signala {} je: {}\nStvorena je nova datoteka stog.txt.\n'
		  .format(sig.Signals(signal_number).name, signal_number))
	save_file([str(frame)], 'stog.txt')
	return

def F2Helper_validate_signal(signal_to_validate):
	"""
	Funkcija prvo formatira vrijednost string varijable signal_to_validate tj.
	signala kojeg treba provjeriti na nacin da prvo pretvori sva mala slova
	u velika te ukloni substring SIG ako postoji te kao rezultat ostaje skraceni
	naziv signala kojem se pridruzuje string SIG na pocetak kako bi se dobio
	puni naziv signala koji se usporeduje sa listom dozvoljenih signala.
	Prikuplja se popis svih dostupnih ispravnih signala te sprema u prociscenu
	listu, dodaje se signal	SIGUSR2 teprovjerava ako se proslijedeni signal nalazi
	u listi dostupnih i ispravnih signala.
	
	Argumenti:
	signal_to_validate -- "SIGINT", Signal kojeg je potrebno provjeriti
	
	Vraća:
	1 - Ako je signal ispravan
	0 - Ako signal nije ispravan
	"""
	signal_to_validate = 'SIG' + str(signal_to_validate.upper().replace('SIG','')) 
	valid_signals = list(sig.valid_signals())[0:9] + list(sig.valid_signals())[20:]
	valid_signals_clean = ['SIGUSR2']

	for signal in valid_signals:
		if 'Signals.' in str(signal):
			signal_clean = str(signal).replace('Signals.', '')
			valid_signals_clean.append(signal_clean)

	for signal in valid_signals_clean:
			if signal_to_validate == signal:
				return signal
	
	return 0

def F2Main_enter_signal():
	"""
	Omogucuje korisniku da unese (puni ili skraceni) naziv signala
	namjenjen trenutnom procesu. Nepoznati naziv signala javlja
	poruku o pogresnom unosu koji se ponavlja dok se ne unese ispravan.
	Ignoriraju se signali s identifikatorima u rasponu od 10 do 20,
	svi drugi signali se obraduju kako je zadano (eng. default).
	Signali ABRT ili USR2 javljaju poruku o zaprimljenom signalu,
	redni broj signala te zapisuju stanje stoga procesa u datoteku.
	Nakon obavijesti o stvorenoj datoteci prikazuje se glavni izbornik.
	"""
	os.system('clear')

	process_id = os.getpid()

	while True:
		user_input = F2Helper_validate_signal(return_user_input('2 - UNOS SIGNALA'))
		if (user_input):
			break
		else:
			print_msg_failure('Uneseni signal nije ispravan ili je identifikator u rasponu od [10-20].')
			time.sleep(3)
		
	if 'ABRT' in user_input or 'USR2' in user_input:
		sig.signal(int(sig.Signals[user_input].value), F2Helper_signal_handler)
		os.kill(process_id, int(sig.Signals[user_input].value))
	else:
		sig.signal(int(sig.Signals[user_input].value), sig.SIG_DFL)
		os.kill(process_id, int(sig.Signals[user_input].value))

	time.sleep(6)
	return

def F3Helper_number_is_prime(number):
	"""
	Provjerava je li broj prost ili nije.
	
	Argumenti:
	number -- "17", Broj koji se provjerava
	
	Vraća:
	False - Broj NIJE prost
	True - Broj JE prost
	"""
	for n in range(2, int(number**0.5) +1):
		if number % n == 0:
			return False
	return True


F3VAR_SUM = 0
F3VAR_ODABRANI_BROJEVI = []
F3VAR_INTERVAL = list(range(0, 2000001))
def F3Helper_chosen_number_sum(lock):
	"""
	Provjerava je li broj iz liste F3VAR_INTERVAL dijeljiv sa 5 i 9,
	ako je zbraja ga u varijabli F3VAR_SUM. Za sve druge brojeve
	provjerava se je li broj prosti te ako je dodaje ga se na kraj
	liste F3VAR_ODABRANI_BROJEVI.
	
	Argumenti:
	lock -- "<unlocked _thread.lock object at 0x7fa6b814cb10>", Lokot
	"""
	lock.acquire()
	global F3VAR_SUM
	global F3VAR_ODABRANI_BROJEVI
	for number in F3VAR_INTERVAL:
		# Ovaj dio ne radi iako bi trebao?
		#if F3Helper_number_is_prime(number):
			#F3VAR_ODABRANI_BROJEVI.append(number)
		if (number % 5 == 0 and number % 9 == 0):
			F3VAR_SUM = F3VAR_SUM + number
	lock.release()
	return

def F3Main_chosen_numbers():
	"""
	U 4 procesne dretve proslijeduje funkciju 
	F3Helper_chosen_number_sum(lock) te ispisuje rezultat
	sume koja se racuna u toj funkciji i 
	proste brojeve iz liste F3VAR_ODABRANI_BROJEVI.
	"""
	os.system('clear')
	print('3 - Izabrani brojevi')
	
	
	print('GLAVNA DRETVA ima PID: {}'.format(os.getpid()))
	lock = th.Lock()
	
	thread1 = th.Thread(target=F3Helper_chosen_number_sum, args=(lock,))
	thread2 = th.Thread(target=F3Helper_chosen_number_sum, args=(lock,))
	thread3 = th.Thread(target=F3Helper_chosen_number_sum, args=(lock,))
	thread4 = th.Thread(target=F3Helper_chosen_number_sum, args=(lock,))
	
	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	
	threads_list = th.enumerate()
	print('\nBroj aktivnih dretvi je {}:'.format(len(threads_list)))
	for thread in threads_list:
		print(thread)
	
	thread1.join()
	thread2.join()
	thread3.join()
	thread4.join()
	
	print('\nPrime brojevi su:\n{}'.format(F3VAR_ODABRANI_BROJEVI))
	
	print('\nZbroj svih brojeva dijeljivih istovremeno sa 5 i 9\nu intervalu [0, 2,000,000] iznosi: {}.'.format(int(F3VAR_SUM)))
	
	time.sleep(6)
	return

def F4Main_square_subtraction():
	"""
	Korisnik unosi pozitivnu cjelobrojvrijednost u rasponu od 1000 do 110,000.
	Provjerava se unesena vrijednost te se od zadanog broja oduzimaju kvadrati
	brojeva u rasponu od 1 do unesene vrijednosti tako da se koriste tri dretve. 
	Ispisuje se ukupno trajanje izvodenja svake dretve, a treca dretva
	ispisuje na zaslon konacan rezultat oduzimanja.
	"""
	os.system('clear')

	print(TEXT_DECOR_EQUAL, '4 - Oduzimanje kvadrata', TEXT_DECOR_EQUAL)
	print_msg_failure('Nazalost funkcionalnost nije dozivjela svoju implementaciju! :( ')
	
	time.sleep(3)
	return

def F5Main_make_directory():
	"""
	Korisnik unosi apsolutnu ili relativnu adresu direktorija za stvorit.
	Provjerava se tocnost adrese i postojanost objekta istog naziva na adresi.
	Ukoliko direktorij postoji ili je adresa nevaljana korisnik se obavjestava.
	Ako je adresa ispravna i direktorij ne postoji, 
	stvara se  novi direktorij s nacinom pristupa 765 te se ispisuje:
	1. Adresa nadredenog direktorija
	2. Naziv i identifikator vlasnika objekta
	3. Ispis sadrzaja direktorija koji je nadreden objektu
	Funkcija zavrsava izvodenje nakon odredenog vremena povratkom u glavni izbornik.
	"""
	os.system('clear')

	user_input = return_user_input('5 - Stvori direktorij')

	initial_working_directory = os.getcwd()

	#Korisnikov unos razbijamo u listu objekata ['','home','runner','datoteka','']
	path_items = user_input.split('/')

	#Ako korisnik unese samo naziv datoteke npr. 'Datoteka' formatiramo unos da bude './Datoteka'
	if (len(path_items) == 1 
		and path_items[0][0] != '/'):
		user_input = './' + user_input

	#Ako se na kraju liste objekata nalazi karakter / ili '' izbacimo ga
	if (path_items[-1] == '' or
	   	path_items[-1] == '/'):
		path_items.pop()

	#Ako se na pocetku liste objekata nalazi prazan unos izbacimo ga
	if (path_items[0] == ''):
		path_items.pop(0)

	#Adresa direktorija u kojem se stvara datoteka 
	root_path = os.path.dirname(user_input)

	#Pridruzujemo root adresi naziv datoteke zbog provjere ako postoji
	if (os.path.isdir(os.path.join(root_path, path_items[-1]))):
		print_msg_failure('Direktorij koji ste htjeli stvoriti vec POSTOJI...')
		time.sleep(3)
		return
		
	else:
		try:
			os.chdir(root_path)
			os.mkdir(path_items[-1], 765)

			parent_dir = os.getcwd()
			parent_dir_content =os.listdir(parent_dir)
			
			object_owner = pwd.getpwuid(os.stat(path_items[-1]).st_uid).pw_name
			object_owner_id = os.stat(path_items[-1]).st_uid
			
			print('Nadredeni direktorij: {}'.format(os.getcwd()),
			  '\nVlasnik objekta je: {} [{}]'.format(object_owner, object_owner_id), 
			  '\n\nIspis sadrzaja direktorija:')
		
			for item in parent_dir_content:
				print(item)
			
			print_msg_success('Direktorij je stvoren USPJESNO!')
			os.chdir(initial_working_directory)
			
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				print_msg_failure('Adresa koju ste unijeli NIJE ISPRAVNA!')
				os.chdir(initial_working_directory)
				time.sleep(3)
				return
			pass
		
	time.sleep(10)
	return

def F6Helper_print_process_table(user_id, process_id, process_priority,
						parent_process_id, parent_process_priority):
	"""
	Ispisuje tablicu procesa koja sadrzi stupce: naziv procesa, proces ID,
	prioritet, niceness, Korisnik ID.
	
	Argumenti:
	user_id -- "1000", Korisnik ID
	process_id -- "3183", Proces ID trenutnog procesa
	process_priority -- "35", Prioritet trenutnog procesa
	parent_process_id -- "14", Proces ID roditelja
	parent_process_priority -- "20", Prioritet procesa roditelja
	"""
	data = [['Naziv procesa','Proces ID', 'Prioritet', 'Niceness', 'Korisnik ID'],
			['Proces roditelj', parent_process_id, parent_process_priority + 20, parent_process_priority, user_id],
			['Proces trenutni', process_id, process_priority + 20, process_priority, user_id]]
	print(tab.tabulate(data, headers='firstrow', tablefmt='fancy_grid', colalign=("center",)))
	
def F6Main_change_process_priority():
	"""
	Korisnik mora unesti cjelobrojan pozitivni broj m u rasponu
	od 1 do 19. Ako korisnicki unos nije ispravan korisnik se vraca
	u glavni izbornik. Nakon unosa vrijednosti izvrsavaju se koraci:
	1. Ispis tablice - RODITELJ PROCES, TRENUTNI PROCES koja sadrzi
	stupce - PID, UID, PRIORITET
	2. Prikaz tablice se izvodi m sekundi
	3. Niceness trenutno procesa dobiva vrijednost m
	4. Ponavlja se korak 1. i 2.
	"""
	os.system('clear')
	
	interval = [str(n) for n in list(range(1,20))]
	user_input = return_user_input('6. Ispisi tablicu procesa')

	if not (user_input in interval):
		print_msg_failure( 'Unos nije u intervalu od 1 do 19' )
		time.sleep(3)
		return
	
	user_id = os.getuid()
	
	process_id = os.getpid()
	process_priority = os.getpriority(os.PRIO_PROCESS, process_id)
	
	parent_process_id = os.getppid()
	parent_process_priority = os.getpriority(os.PRIO_PROCESS, parent_process_id)
	
	F6Helper_print_process_table(user_id, process_id, process_priority,
								 parent_process_id, parent_process_priority)

	time.sleep(int(user_input))

	process_priority = os.nice(int(user_input))

	F6Helper_print_process_table(user_id, process_id, process_priority,
								 parent_process_id, parent_process_priority)
	
	time.sleep(int(user_input))
	return

def save_file(file_content, file_name):
	"""
	Sprema datoteku proizvoljnog naziva u kucni direktorij.
	
	Argumenti:
	file_name -- ".hist_data" ili "datoteka.txt", Naziv datoteke i ekstenzija
	file_content -- "HIST_DATA[-MAX_HIST_DATA:]", Lista sa podacima 
	"""
	np.savetxt(os.path.join(os.path.expanduser('~'), file_name),
			   file_content,
			   newline=os.linesep,
			   fmt='%s')

def main():
	"""
	Glavna funkcija koja prikazuje poruku dobrodoslice, trenutno vrijeme i datum,
	naziv i verziju operacijskog sustava te ispisuje radni direktorij.
	Pokrece sucelje glavnog izbornika
	gdje korisnik moze izabrati pokretanje jedne od ponudenih funkcija.
	"""
	os.system('clear')
	
	menu_options = {
		1: 'Unos naredbe',
		2: 'Unos signala',
		3: 'Izabrani brojevi',
		4: 'Oduzimanje kvadrata',
		5: 'Stvori direktorij',
		6: 'Promjeni prioritet trenutnog procesa',
		'odjavi ili zavrsi': 'Zavrsetak izvodenja programa'
	}
	user_input_error = 0
	
	print(TEXT_DECOR_EQUAL, 'DOBRO DOSAO {}!'.format(USERNAME.upper()),
		  TEXT_DECOR_EQUAL, '\nVrijeme i Datum: {}'.format(time.strftime('%H:%M:%S %w %e/%m/%Y', time.localtime())),
		  '\nOS Naziv: {}'.format(os.uname()[0]),
		  '\nOS Verzija: {}'.format(os.uname()[3]),
		  '\nRadni Direktorij: {}'.format(os.getcwd()))
	
	while True:
		print(TEXT_DECOR_EQUAL, 'GLAVNI IZBORNIK', TEXT_DECOR_EQUAL)
		for key in menu_options.keys():
			print(key, '–', menu_options[key])
		print('\n(Izaberite broj jedne od ponudenih stavki glavnog izbornika...)')
	
		if user_input_error != 0:
			print('(Vas unos nije ispravan ili je prazan [{}]...)'.format(user_input_error))
	
		user_input = input(USER_PC_NAME)
		HIST_DATA.append(user_input)
	
		if user_input == '1':
			F1Main_enter_command()
		elif user_input == '2':
			F2Main_enter_signal()
		elif user_input == '3':
			F3Main_chosen_numbers()
		elif user_input == '4':
			F4Main_square_subtraction()
		elif user_input == '5':
			F5Main_make_directory()
		elif user_input == '6':
			F6Main_change_process_priority()
		elif (user_input == 'odjavi' or user_input == 'zavrsi'):
			save_file(HIST_DATA[-MAX_HIST_DATA:], '.hist_data')
			print(TEXT_DECOR_EQUAL,
				  '\033[0;37;1;42m USPJESNO ste se odjavili. \033[0m',
				  '\n  DOVIDENJA {}!'.format(USERNAME.upper()), TEXT_DECOR_EQUAL)
			break
		else:
			user_input_error += 1
			os.system('clear')
			continue
	
		os.system('clear')
		user_input_error = 0

main()