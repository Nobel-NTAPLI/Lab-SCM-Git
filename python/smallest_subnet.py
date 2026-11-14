
import ipaddress


def smallest_subnet(ips):
    """
    Trouve le plus petit sous-réseau IPv4
    contenant toutes les adresses fournies.
    """

    if not ips:
        raise ValueError("La liste d'adresses IP est vide.")

    # Conversion des adresses IPv4 en nombres entiers
    addresses = [
        int(ipaddress.IPv4Address(ip))
        for ip in ips
    ]

    # Recherche de la plus petite et grande adresse
    min_ip = min(addresses)
    max_ip = max(addresses)

    # Nombre de bits différents entre les extrêmes
    difference = min_ip ^ max_ip

    # Calcul du préfixe réseau commun
    prefix = 32 - difference.bit_length()

    # Construction du plus petit sous-réseau
    network = ipaddress.ip_network(
        (min_ip, prefix),
        strict=False
    )

    return network
