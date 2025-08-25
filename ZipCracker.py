import zipfile
import itertools
import string
import time
from multiprocessing import Pool, cpu_count

# ==== Einstellungen ====
ZIP_PATH      = "gg.zip"
TARGET_MEMBER = "secret.txt"   # None -> erste Datei im Archiv wählen
CHARSET       = string.ascii_lowercase + string.digits   # a-z0-9
MIN_LEN       = 1
MAX_LEN       = 6
BATCH_SIZE    = 2000
WORKERS       = max(1, cpu_count() - 1)

# ---- globale Variablen für Worker (per Initializer gesetzt) ----
_ZPATH = None
_MEMBER = None


def init_worker(zpath, member):
    global _ZPATH, _MEMBER
    _ZPATH = zpath
    _MEMBER = member


def batched(iterable, n):
    """Iteriere über iterable in Blöcken der Größe n."""
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch


def iter_candidates(charset, min_len, max_len):
    for L in range(min_len, max_len + 1):
        # lexikografische Reihenfolge; bei Bedarf Reihenfolge ändern
        for tup in itertools.product(charset, repeat=L):
            yield "".join(tup)


def iter_candidates_from_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip()
            if w:
                yield w


def worker_try_batch(batch):
    """
    Öffnet das ZIP einmal und testet alle Passwörter im Batch.
    Verifiziert per 1-Byte-Read (schnell). Gibt Treffer oder None zurück.
    """
    try:
        with zipfile.ZipFile(_ZPATH) as z:
            for pw in batch:
                pwb = pw.encode("utf-8", errors="ignore")
                try:
                    with z.open(_MEMBER, "r", pwd=pwb) as fp:
                        # 1 Byte reicht, um das Passwort zu validieren
                        fp.read(1)
                    return pw  # Treffer!
                except (RuntimeError, zipfile.BadZipFile, KeyError):
                    # falsches Passwort oder CRC-Fehler => weiter
                    continue
                except NotImplementedError:
                    # Wahrscheinlich AES-ZIP -> zipfile kann das nicht
                    return "__AES_NOT_SUPPORTED__"
    except FileNotFoundError:
        return "__ZIP_NOT_FOUND__"
    return None


def main():
    # Ziel-Datei im Archiv bestimmen
    try:
        with zipfile.ZipFile(ZIP_PATH) as z:
            names = z.namelist()
    except FileNotFoundError:
        print(f"[!] ZIP nicht gefunden: {ZIP_PATH}")
        return
    except zipfile.BadZipFile:
        print("[!] Defektes ZIP.")
        return

    member = TARGET_MEMBER if (TARGET_MEMBER and TARGET_MEMBER in names) else (names[0] if names else None)
    if not member:
        print("[!] ZIP ist leer.")
        return
    print(f"[*] Ziel-Datei: {member}")

    # Kandidatenquelle: Brute-Force – oder hier stattdessen iter_candidates_from_file('common.txt')
    candidates = iter_candidates(CHARSET, MIN_LEN, MAX_LEN)

    t0 = time.time()
    tried = 0
    found = None

    with Pool(processes=WORKERS, initializer=init_worker, initargs=(ZIP_PATH, member)) as pool:
        for result in pool.imap_unordered(worker_try_batch, batched(candidates, BATCH_SIZE), chunksize=1):
            tried += BATCH_SIZE
            # Fortschritt ausgeben (optional)
            if tried % (BATCH_SIZE * 10) == 0:
                dt = time.time() - t0
                rate = tried / max(dt, 1e-6)
                print(f"[.] Versuche ~{tried:,} | {rate:,.0f} pw/s")

            if result:
                if result == "__AES_NOT_SUPPORTED__":
                    print("[!] Dieses ZIP nutzt wahrscheinlich AES-Verschlüsselung. "
                          "Die Python-Stdlib kann das nicht. Nutze 'pyzipper' oder erstelle das ZIP mit ZipCrypto.")
                    pool.terminate()
                    break
                if result == "__ZIP_NOT_FOUND__":
                    print("[!] ZIP nicht gefunden.")
                    pool.terminate()
                    break
                found = result
                print(f"[+] Passwort gefunden: '{found}'")
                pool.terminate()
                break

    dt = time.time() - t0
    if found:
        print(f"[✓] Dauer: {dt:.1f}s  | grob getestete Kandidaten: ~{tried:,}")
        # Optional: extrahieren
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extract(member, pwd=found.encode())
            print(f"[+] '{member}' extrahiert.")
    else:
        print(f"[-] Kein Passwort im Suchraum gefunden. Dauer: {dt:.1f}s  | ~{tried:,} Versuche")


if __name__ == "__main__":
    main()
