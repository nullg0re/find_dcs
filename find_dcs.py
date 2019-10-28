#!/usr/bin/python3
import dns.resolver
import sys

def a_lookup(record):
	ip = ""
	answers = dns.resolver.query(record,'A')
	for ip in answers:
		return ip

def get_dnsServers(domain):
	dnsServers = {}
	answers = dns.resolver.query(domain, 'NS')
	for record in answers:
		record = str(record).strip('.')
		dnsServers[record] = a_lookup(record)
	return dnsServers

def srv_lookup(domain, dnsServers, type):
	if type == 'dc':
		srv_record = f"_ldap._tcp.dc._msdcs.{domain}"
		dcs = {}
		records = []
		for k,v in dnsServers.items():
			dnsServer = str(v)
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = [dnsServer]
			try:
				answers = my_resolver.query(srv_record, 'SRV')
				for data in answers:
					dc = str(data).split(' ')[3].strip('.')
					if dc not in dcs:
						dcs[dc] = a_lookup(dc)
			except Exception as e:
				continue
		return dcs

	elif type == 'exchange':
		srv_record = f"_autodiscover._tcp.{domain}"
		exchanges = {}
		records = []
		for k,v in dnsServers.items():
			dnsServer = str(v)
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = [dnsServer]
			try:
				answers = my_resolver.query(srv_record, 'SRV')
				for data in answers:
					exchange = str(data).split(' ')[3].strip()
					if exchange not in exchanges:
						exchanges[exchange] = a_lookup(exchange)
			except Exception as e:
				continue

		return exchanges

	elif type == 'sql':
		srv_record = f"_sql._tcp.{domain}"
		sqls = {}
		records = []
		for k,v in dnsServers.items():
			dnsServer = str(v)
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = [dnsServer]
			try:
				answers = my_resolver.query(srv_record,'SRV')
				for data in answers:
					sql = str(data).split(' ')[3].strip()
					if sql not in sqls:
						sqls[sql] = a_lookup(sql)
			except Exception as e:
				continue

		return sqls

	elif type == 'gc':
		srv_record = f"_ldap._tcp.gc._msdcs.{domain}"
		gcs = {}
		records = []
		for k,v in dnsServers.items():
			dnsServer = str(v)
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = [dnsServer]
			try:
				answers = my_resolver.query(srv_record, 'SRV')
				for data in answers:
					gc = str(data).split(' ')[3].strip()
					if gc not in gcs:
						gcs[gc] = a_lookup(gc)
			except Exception as e:
				continue
		return gcs

def main():
	if len(sys.argv) != 2:
		print(f"[+] Usage: {sys.argv[0]} <domain>")
		exit()

	domain = sys.argv[1]

	print('[*] Getting DNS Servers...')
	dnsServers = get_dnsServers(domain)

	print("[*] Getting Domain Controllers and Exchange Servers...")
	types = ['dc','exchange','sql','gc']
	for type in types:
		if type == 'dc':
			print("[+] Domain Controllers:")
			dcs = srv_lookup(domain, dnsServers, type)
			for k,v in dcs.items():
				print(f"[+] {k}  :  {v}")
		elif type == 'exchange':
			print("[+] Exchange Servers:")
			exchanges = srv_lookup(domain, dnsServers, type)
			for k,v in exchanges.items():
				print(f"[+] {k}  :  {v}")
		elif type == 'sql':
			print("[+] SQL Servers:")
			sqls = srv_lookup(domain, dnsServers, type)
			for k,v in sqls.items():
				print(f"[+] {k}  :  {v}")
		elif type == 'gc':
			print("[+] Global Catalog Servers:")
			gcs = srv_lookup(domain, dnsServers, type)
			for k,v in sqls.items():
				print(f"[+] {k}  :  {v}")


	print("[+] Happy Hunting! Good Luck")


if __name__ == '__main__':
	main()

