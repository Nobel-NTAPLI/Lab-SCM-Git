import urllib.request
import json
import ipaddress
import sys

from parse_ips import parse_ips
from smallest_subnet import smallest_subnet

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

    # MODE 1 : Calcul du plus petit sous-reseau
    if len(sys.argv) >= 2 and sys.argv[1] == "--subnet":

        try:
            # Recuperation et validation des adresses IP
            ips = parse_ips(sys.argv[2:])

            # Calcul du plus petit sous-reseau
            network = smallest_subnet(ips)

            # Affichage des resultats
            print("\nAdresses IP fournies :")
            for ip in ips:
                print(ip)

            print("\nPlus petit sous-reseau :")
            print(network)

            print("Premiere IP :", network.network_address)
            print("Derniere IP :", network.broadcast_address)

        except ValueError as error:
            print("Erreur :", error)
            sys.exit(1)

    # MODE 2 : Recherche d'une IP dans les plages AWS
    else:

        if len(sys.argv) != 2:
            print("Utilisation :")
            print("  python3 awsip.py <adresse_ip>")
            print("  python3 awsip.py --subnet <ip1> <ip2> ...")
            sys.exit(1)

        ip_to_find = sys.argv[1]

        try:
            aws_ranges = download_aws_ip_set()
            results = find_aws_ip(aws_ranges, ip_to_find)

            for prefix in results:
                prefix.update(feature_min_max(prefix))

            print(json.dumps(results, indent=2))

        except ValueError as error:
            print("Erreur :", error)
            sys.exit(1)

