# find_dcs
Find Domain Controllers and other Sensitive Targets Through DNS Queries

This script quickly finds Domain Controllers, Global Catalogs, SQL Servers, and Exchange Servers through SRV DNS Records.

Things Like DC and GC SRV records are almost guaranteed going to be found in any environment, but SQL servers and Exchange Servers will be a matter of luck.  Who knows.  Good luck!

# Help Menu:
```
# ./find_dcs.py 
[+] Usage: ./find_dcs.py <domain>
```
