# EXECUTE LINUX OS COMMANDS
Different functions to execute different types of operations in Linux operating system shell.
1. Enter any Linux OS command
2. Execute signal
3. Custom function 1
4. Custom function 2
5. Make a directory
6. Change process priority
7. Logout

## Instructions to start the application
1. Clone (download) the repository
2. Run `python3 main.py` in shell

## Application preview

```python
====================================================
 DOBRO DOSAO RUNNER!
====================================================
 
Vrijeme i Datum: 07:56:15 3 29/06/2022 
OS Naziv: Linux 
OS Verzija: #32~20.04.1-Ubuntu SMP Thu May 26 10:53:08 UTC 2022 
Radni Direktorij: /home/runner/Project 

====================================================
 GLAVNI IZBORNIK 
====================================================

1 – Unos naredbe
2 – Unos signala
3 – Izabrani brojevi
4 – Oduzimanje kvadrata
5 – Stvori direktorij
6 – Promjeni prioritet trenutnog procesa
odjavi ili zavrsi – Zavrsetak izvodenja programa

(Izaberite broj jedne od ponudenih stavki glavnog izbornika...)
```

```python
================================================================================
 1 - UNOS NAREDBE 
================================================================================
 
(Unesite zeljenu naredbu...)

[runner@1123748b342b]$ ls -la

(Izvodenje procesa DIJETE sa PID-om 257...)
 
--------------------------------------------------------------------------------

total 36
drwxr-xr-x 1 runner runner   148 Jun 14 09:22 .
drwxrwxrwx 1 runner runner   118 Aug 24 08:21 ..
drwxr-xr-x 1 runner runner    12 Oct 12  2021 .cache
drwxr-xr-x 1 runner runner    34 Nov 30  2021 .config
drwxr-xr-x 1 runner runner   184 Jun 13 20:30 .git
-rw-r--r-- 1 runner runner 16804 Jun 14 09:22 main.py
-rw-r--r-- 1 runner runner  3667 Jun  5 17:44 poetry.lock
-rw-r--r-- 1 runner runner   329 Jun  5 17:44 pyproject.toml
-rw-r--r-- 1 runner runner  3211 May 27 14:01 .replit
-rw-r--r-- 1 runner runner   403 Jun  5 17:43 replit.nix
drwxr-xr-x 1 runner runner    20 Aug 24 08:22 .upm
drwxr-xr-x 1 runner runner    56 Oct 26  2021 venv

--------------------------------------------------------------------------------
 
(Izvodi se proces RODITELJ - PID Dijeteta: 257, Izlazni status: 0...)

================================================================================
  (Izvodenje naredbe je izvrseno USPJESNO!)  
  (Povratak u glavni izbornik...)  
================================================================================
```

```python
================================================================================
 2 - UNOS SIGNALA 
================================================================================
 
(Unesite zeljenu naredbu...)

[runner@1123748b342b]$ usr2
Broj signala SIGUSR2 je: 12
Stvorena je nova datoteka stog.txt.
```

```shell
~$ cat stog.txt
<frame at 0x7ff9f37b33c0, file 'main.py', line 214, code F2Main_enter_signal>
```

```python
================================================================================
 5 - Stvori direktorij 
================================================================================
 
(Unesite zeljenu naredbu...)

[runner@1123748b342b]$ ../folder         
Nadredeni direktorij: /home/runner 
Vlasnik objekta je: runner [1000] 

Ispis sadrzaja direktorija:
.profile
.bashrc
.bash_logout
.nix-channels
.nix-profile
.nix-defexpr
.cache
.cargo
.m2
.npm
.config
Operating-Systems-College-Project
stog.txt
folder

================================================================================
  (Direktorij je stvoren USPJESNO!)  
  (Povratak u glavni izbornik...)  
================================================================================
```

```python
================================================================================
 6. Ispisi tablicu procesa 
================================================================================
 
(Unesite zeljenu naredbu...)

[runner@1123748b342b]$ 10
╒═════════════════╤═════════════╤═════════════╤════════════╤═══════════════╕
│  Naziv procesa  │   Proces ID │   Prioritet │   Niceness │   Korisnik ID │
╞═════════════════╪═════════════╪═════════════╪════════════╪═══════════════╡
│ Proces roditelj │          53 │          20 │          0 │          1000 │
├─────────────────┼─────────────┼─────────────┼────────────┼───────────────┤
│ Proces trenutni │         385 │          20 │          0 │          1000 │
╘═════════════════╧═════════════╧═════════════╧════════════╧═══════════════╛
╒═════════════════╤═════════════╤═════════════╤════════════╤═══════════════╕
│  Naziv procesa  │   Proces ID │   Prioritet │   Niceness │   Korisnik ID │
╞═════════════════╪═════════════╪═════════════╪════════════╪═══════════════╡
│ Proces roditelj │          53 │          20 │          0 │          1000 │
├─────────────────┼─────────────┼─────────────┼────────────┼───────────────┤
│ Proces trenutni │         385 │          30 │         10 │          1000 │
╘═════════════════╧═════════════╧═════════════╧════════════╧═══════════════╛
```

```shell
~$ cat .hist_data
5
../folder
6
10
2
usr2
odjavi
```
