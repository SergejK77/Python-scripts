import subprocess
import sys

# CONST #
ENC = "latin1"


def get_PW():
    listi = []
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(ENC)
        print("Ausgabe von 'netsh wlan show profiles':")
    except UnicodeDecodeError as e:
        print(f"Fehler beim Dekodieren der Ausgabe: {e}")
        return listi
    profiles = [line.split(":")[1].strip() for line in data.splitlines() if "Profil fr alle Benutzer" in line]
    ##print("Gefundene Profile:")
    ##print(profiles)

    for i in profiles:
        try:
            results = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profile', i, 'key=clear']
            ).decode(ENC).split('\n')
            ##print(results)
            results = [b.split(":")[1].strip() for b in results if "Schl\x81sselinhalt" in b]
            listi.append(("{:<30}|  {:<}".format(i, results[0] if results else "")))
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Abrufen des Profils {i}: {e}")
            listi.append("{:<30}|  {:<}".format(i, ""))
        except IndexError:
            listi.append("{:<30}|  {:<}".format(i, ""))

    return listi


if __name__ == "__main__":
    passwords = get_PW()
    for password in passwords:
        print(password)
