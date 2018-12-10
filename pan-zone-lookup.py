#!/usr/bin/env python

import urllib
import urllib2
import ssl
import argparse
import re
import xml.etree.ElementTree as ET
import sys
import os


def api_request(url, values):

    data = urllib.urlencode(values)
    context = ssl._create_unverified_context()

    try:
        request = urllib2.Request(url, data)
        return urllib2.urlopen(request, context=context).read()

    except urllib2.URLError:
        print("\n\033[1;31;40m[Error] : Connecting to "+url+". Check IP address.\033[0m")
        return None

def parse_response_code(api_response):

  response = re.search(r"<response status=(.*)><result>",api_response)
  response_string = response.group(1)

  if response_string != '"'+"success"+'"':
    print "\n\033[1;31;40m[Error] : The Firewall was not able to execute the API request."
    print "Reponse :"+str(response_string)+'\n',
    sys.exit(0)

def get_zone(firewall_ip,destination_ip,api_key):

  try:
    url = "https://{ip}/api".format(ip=firewall_ip)
    api_call = {'type': 'op', 'Key': api_key, 'cmd': '<test><routing><fib-lookup><ip>'+destination_ip+'</ip><virtual-router>core0</virtual-router></fib-lookup></routing></test>'}
    api_response = api_request(url,api_call)
    parse_response_code(api_response)
    
    root = ET.fromstring(api_response)
    for leaf in root.iter():		 		 	
		if leaf.tag == "interface":		 	
			interface = leaf.text
			
    api_call = {'type': 'op', 'Key': api_key, 'cmd': '<show><interface>'+interface+'</interface></show>'}
    api_response = api_request(url,api_call)
    parse_response_code(api_response)
	
    root = ET.fromstring(api_response)
    for leaf in root.iter():		 		 	
		if leaf.tag == "zone":		 	
			zone = leaf.text
			print zone
	
  except:
    print("\n\033[1;31;40m[Error] : Cannot run the API call on firewall "+firewall_ip+"\033[0m\n")
    sys.exit(0)

if __name__ == '__main__':	

  usage = 'pan-route-lookup-simple -fi <firewall ip or DNS> -ip <ip_for_zone_lookup>' 
 
  parser = argparse.ArgumentParser(usage=usage)
  parser.add_argument('-fi', action='store',required=True, help='Firewall FQDN/IP')
  parser.add_argument('-ip', action='store',required=True, help='Host IP where Zone lookup is required')
  results = parser.parse_args()
  
  firewall_ip	=  results.fi
  api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"	
  destination_ip= results.ip
  url = "https://{ip}/api".format(ip=firewall_ip)
  
  get_zone(firewall_ip,destination_ip,api_key)
  
