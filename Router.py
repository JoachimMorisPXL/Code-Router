import requests
from ncclient import manager
from ncclient.operations import RPCError

# --- Verbindingsinstellingen ---
HOST     = "10.10.10.1"
PORT     = 830
USERNAME = "student"
PASSWORD = "pxl"

# --- GitHub URL (Single Source of Truth) ---
GITHUB_RAW_URL = "https://raw.githubusercontent.com/WoutBormansPXL/code_router/refs/heads/main/conf_router"

def haal_config_op_van_github(url):
    """Haal XML configuratie op uit GitHub."""
    print(f"[*] Config ophalen van: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("[+] Configuratie succesvol gedownload van GitHub.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[-] Fout bij ophalen GitHub configuratie: {e}")
        raise

def deploy_via_netconf(config_xml):
    """Deploy de configuratie via NETCONF (Direct naar running)."""
    print(f"[*] Verbinden met router {HOST} via NETCONF...")
    
    with manager.connect(
        host=HOST, port=PORT,
        username=USERNAME, password=PASSWORD,
        hostkey_verify=False
    ) as m:
        print("[+] Verbonden met de router.")
        
        try:
            # We schrijven direct naar de 'running' datastore omdat
            # de lab-router de 'candidate' functionaliteit niet ondersteunt.
            print("[*] Configuratie direct wegschrijven naar 'running' datastore...")
            m.edit_config(target="running", config=config_xml)
            
            print("[+] SUCCES: Deployment is geslaagd! Configuratie is actief.")
            
        except RPCError as e:
            print(f"[-] Fout in XML configuratie of router weigert: {e.message}")
        except Exception as e:
            print(f"[-] Onverwachte fout tijdens deployment: {e}")

# --- Hoofdprogramma ---
if __name__ == "__main__":
    try:
        xml_payload = haal_config_op_van_github(GITHUB_RAW_URL)
        deploy_via_netconf(xml_payload)
    except Exception:
        print("[-] Script afgebroken.")