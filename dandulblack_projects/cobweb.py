import subprocess

def kam_muzu_jit(cil="seznam.cz"):
    vysledek = subprocess.run(["tracert", "-d", cil], capture_output=True, text=True)
    radky = vysledek.stdout.strip().split("\n")[1:]  # přeskočí první řádek
    moznosti = []

    for radek in radky:
        if "Zpoždění" in radek or "nelze" in radek or "vypršel" in radek:
            continue  # přeskočíme timeouty nebo chyby
        casti = radek.split()
        if len(casti) >= 2:
            ip = casti[-1]
            moznosti.append(ip)
    
    print("Kam se můžeš jako paket pohnout:")
    for i, ip in enumerate(moznosti):
        print(f"{i+1}. {ip}")

kam_muzu_jit()

