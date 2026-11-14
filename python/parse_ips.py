
import ipaddress


def parse_ips(ip_strings):
    """
    Valide les adresses IP saisies par l'utilisateur.
    Retourne une liste d'adresses IPv4 valides.
    """

    if not ip_strings:
        raise ValueError("Veuillez fournir au moins une adresse IP.")

    validated_ips = []

    for ip in ip_strings:
        try:
            address = ipaddress.IPv4Address(ip)
            validated_ips.append(str(address))
        except ipaddress.AddressValueError:
            raise ValueError(f"Adresse IPv4 invalide : {ip}")

    return validated_ips
