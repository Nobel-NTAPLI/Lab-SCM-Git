import urllib.request
import json
import ipaddress
import sys


def download_aws_ip_set():
    """Downloads the AWS IP range JSON file and returns it as a dictionary."""
    aws_ip_range_url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
    with urllib.request.urlopen(aws_ip_range_url) as url:
        aws_ip_range_data = json.load(url)
    return aws_ip_range_data['prefixes']


# Find ip given IP belongs to any AWS Service
def find_aws_ip(aws_ip_range_data, ip_to_find):
    """Finds the AWS IP range that contains the given IP address and enriches it with the total number of IPs."""
    results = []
    target_ip = ipaddress.ip_address(ip_to_find)

    for prefix in aws_ip_range_data:
        if 'ip_prefix' in prefix:
            network = ipaddress.ip_network(prefix['ip_prefix'])
            if target_ip in network:
                # On crée une copie du dictionnaire pour y ajouter le nombre total d'IPs en français
                prefix_info = prefix.copy()
                prefix_info['nombre_adresses'] = network.num_addresses
                results.append(prefix_info)

    return results


def feature_min_max(prefix):
    """
    Retourne la première et la dernière adresse IP
    d'une plage réseau AWS.
    """
    network = ipaddress.ip_network(prefix['ip_prefix'])

    first_ip = network.network_address
    last_ip = network.broadcast_address

    return {
        "first_ip": str(first_ip),
        "last_ip": str(last_ip)
    }




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Utilisation : python3 awsip.py <adresse_ip>")
        sys.exit(1)

    ip_to_find = sys.argv[1]

    aws_ranges = download_aws_ip_set()
    results = find_aws_ip(aws_ranges, ip_to_find)

    for prefix in results:
        prefix.update(feature_min_max(prefix))

    print(json.dumps(results, indent=2))
