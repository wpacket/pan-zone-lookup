# pan-get-device-state
As far as I can see there is not easy way on PanOS to get the zone for a given IP address.
The script will connect to the firewall and provide the security zone for a given IP.
## How to Run it
First make sure to generate an API_KEY and put it in the api_key variable ( in the script ).
API key can be retrieved via the following URL https://firewall_ip/api/?type=keygen&user=username&password=password 
```
pan-route-lookup -fi <firewall ip or DNS> -ip <ip_for_zone_lookup>
```

## Example
```
# python pan-zone-lookup.py -fi 192.168.1.254 -ip 8.8.8.8
The IP 8.8.8.8 is connected to the Zone L3-Untrust
```

