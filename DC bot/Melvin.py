
import discord
from discord import app_commands
import os
import colorama
import random
from colorama import Fore
import asyncio
import time
from discord import ui
from keyboard import write

filename = "Melvin.py"

blackjack_data = {}

# Proměnné na ruletu:
cervena_cisla = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
suda_cisla = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
row_1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
row_2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
row_3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

#Proměné pro blackjack:
blackjack_karty = [
    "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "10♠", "J♠", "Q♠", "K♠", "A♠",
    "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "10♥", "J♥", "Q♥", "K♥", "A♥",
    "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "10♦", "J♦", "Q♦", "K♦", "A♦",
    "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "10♣", "J♣", "Q♣", "K♣", "A♣"
]


# Nastavení Discord bota
intents = discord.Intents.default()
intents.message_content = True

# Nastavení knihovny colorama
RESET = colorama.Style.RESET_ALL
CYAN = colorama.Fore.CYAN + colorama.Style.BRIGHT
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
red = Fore.RED
cyan = Fore.CYAN


def vypis(uzivatel, prikaz, server):
    print(
        green + f"Uživatel" + yellow + f" {uzivatel}" + green + " použil příkaz:" + yellow + f" {prikaz} " + green + "na serveru: " + yellow + f"{server}")


def coiny(potrebne_coiny, uzivatel):
    with open("balance.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith(f"{uzivatel}:"):
            user_coiny = float(line.split(':')[1])
            if user_coiny >= potrebne_coiny:
                return True, user_coiny
            else:
                return False, user_coiny
    return False, 0  # Uživatel nenalezen


def hrablackjack(uzivatel):
    pouzite_karty = []
    karty_v_ruce = []
    karta = random.choice(blackjack_karty)
    pouzite_karty.append(karta)
    zprava = f"OK dealer má v ruce jednu neznámou kartu🃏 a {karta}. Ty máš v ruce: "

    for _ in range(2):
        while True:
            karta = random.choice(blackjack_karty)
            if karta not in pouzite_karty:
                pouzite_karty.append(karta)
                karty_v_ruce.append(karta)
                break

    zprava += " ".join(karty_v_ruce)

    blackjack_data[uzivatel] = {
        'zprava': zprava,
        'pouzite_karty': pouzite_karty,
        'karty_v_ruce': karty_v_ruce
    }

    return zprava, pouzite_karty, karty_v_ruce


def soucet(karty_v_ruce):
    hodnoty = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 11
    }
    celkem = 0
    esa = 0

    for karta in karty_v_ruce.split():
        hodnota = karta[:-1]  # Odstraníme symbol barvy
        if hodnota == 'A':
            esa += 1
        else:
            celkem += hodnoty[hodnota]

    for _ in range(esa):
        if celkem + 11 <= 21:
            celkem += 11
        else:
            celkem += 1

    return celkem


def ruletahra(bet, coins):
    nahoda = random.randint(0, 36)
    if bet.lower() == "red":
        if nahoda in cervena_cisla:
            return float(coins), nahoda
        else:
            return -float(coins), nahoda
    elif bet.lower() == "black":
        if nahoda not in cervena_cisla and nahoda != 0:
            return float(coins), nahoda
        else:
            return -float(coins), nahoda
    elif bet.lower() in "even pair":
        if nahoda in suda_cisla:
            return float(coins), nahoda
        else:
            return -float(coins), nahoda
    elif bet.lower() in "odd impair":
        if nahoda not in suda_cisla and nahoda != 0:
            return float(coins), nahoda
        else:
            return -float(coins), nahoda
    elif bet.lower() == "row 1":
        if nahoda in row_1:
            return float(coins) * 2, nahoda
        else:
            return -float(coins), nahoda
    elif bet.lower() == "row 2":
        if nahoda in row_2:
            return float(coins) * 2, nahoda
        else:
            return -float(coins), nahoda
    elif bet.lower() == "row 3":
        if nahoda in row_3:
            return float(coins) * 2, nahoda
        else:
            return -float(coins), nahoda
    else:
        try:
            bet_number = int(bet)
            if bet_number == nahoda:
                return float(coins) * 35, nahoda
            else:
                return -float(coins), nahoda
        except ValueError:
            return "0", nahoda  # Neplatná sázka


def ban_check(uzivatel):
    try:
        with open('blacklist.txt', 'r') as file:
            obsah = file.read()
            for line in obsah.splitlines():
                if line.startswith(f"{uzivatel}:"):
                    ban_do = int(line.split(':')[1])
                    if time.time() < ban_do:
                        return "ano", ban_do
                    else:
                        return "ne", None
            return "ne", None  # Uživatel není v blacklistu
    except FileNotFoundError:
        return "ne", None  # Soubor neexistuje


# Vyčištění konzole a výpis úvodní hlavičky
os.system("cls")
print(blue + "====================================================================")
print(blue + "                               Melvin                               ")
print(blue + "====================================================================")


# Definice klienta Discord bota
class MelvinClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()



client = MelvinClient()


# Event při připojení bota
@client.event
async def on_ready():
    print(green + f'{client.user} se úspěšně připojil k Discordu!' + RESET)


# Příkaz /help
@client.tree.command(name="help", description="Zobrazí nápovědu a seznam příkazů")
async def help(interaction: discord.Interaction):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, "/help", server)
    help_text = """
    🐱 Čau jsem Melvin, nejvíc useless BOT na celým discordu.

    Co umím:
    /help - zobrazí tuhle nápovědu
    /ruleta - zahraj si ruletu o coiny (bet může být even, odd, row 1, row 2, row 3, red, black,)
    /work - Tento příkaz ti zakáže gemblit na 2h ale dá ti 1000🪙
    /start - dá ti na začátek 1000🪙
    /balance - zobrazí kolik máš coinů🪙
    """
    await interaction.response.send_message(help_text)


# Příkaz /ruleta
@client.tree.command(name="ruleta", description="Napiš: /ruleta [na co vsázíš] [počet coinů]")
async def ruleta(interaction: discord.Interaction, bet: str, coins: float):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, f"/ruleta {bet} {coins}", server)
    ban_status, _ = ban_check(uzivatel)

    if coins <= 0:
        await interaction.response.send_message("Musíš vsadit kladnou částku.")
        return

    if ban_status == "ne":
        dostatek, user_coiny = coiny(coins, uzivatel)
        if dostatek:
            if coins > user_coiny:
                coins = user_coiny  # Vsadit všechny peníze
            vyhra, nahoda = ruletahra(bet, coins)
            if vyhra == "0":
                await interaction.response.send_message(
                    f"Neplatná sázka. Zkus to znovu s platnou sázkou. Můžeš vsadit na:\n"
                    f"- Barvu: red, black\n"
                    f"- Sudá/lichá čísla: even, odd\n"
                    f"- Řady: row 1, row 2, row 3\n"
                    f"- Konkrétní číslo: 0-36")
            else:
                new_balance = round(user_coiny + vyhra, 2)
                with open('balance.txt', 'r') as file:
                    lines = file.readlines()
                with open('balance.txt', 'w') as file:
                    for line in lines:
                        if line.startswith(f"{uzivatel}:"):
                            file.write(f"{uzivatel}:{new_balance}\n")
                        else:
                            file.write(line)
                if vyhra > 0:
                    await interaction.response.send_message(
                        f"🤑🤑🤑Vyhrál jsi {vyhra}🪙, protože padlo číslo: {nahoda}, už jsem ti je přičetl na účet, teď máš proto {new_balance}🪙.🤑🤑🤑")
                else:
                    await interaction.response.send_message(
                        f"Bohužel jsi prohrál😿, protože padlo číslo: {nahoda}. Odečetl jsem ti {abs(vyhra)}🪙 z účtu, teď máš proto na účtě {new_balance}🪙.")
        else:
            await interaction.response.send_message(
                f"Nemáš dostatek coinů. Tvůj aktuální zůstatek je {round(user_coiny, 2)}🪙.")
    else:
        await interaction.response.send_message("Je mi líto, ale momentálně nemůžeš gamblit 😿")


@client.tree.command(name="start", description="Tento příkaz ti dá 1000🪙 pokud jsi tu nový.")
async def start(interaction: discord.Interaction):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, "/start", server)
    try:
        with open('balance.txt', 'r') as file:
            lines = file.readlines()
        user_exists = any(line.startswith(f"{uzivatel}:") for line in lines)
        if user_exists:
            await interaction.response.send_message("Podle všeho už jsi někdy hrál takže ti coiny nepřičtu 😾")
        else:
            with open('balance.txt', 'a') as file:
                file.write(f"{uzivatel}:1000\n")
            await interaction.response.send_message("🤑Přičetl jsem ti 1000🪙🤑")
    except FileNotFoundError:
        with open('balance.txt', 'w') as file:
            file.write(f"{uzivatel}:1000\n")
        await interaction.response.send_message("🤑Přičetl jsem ti 1000🪙🤑")


@client.tree.command(name="work", description="Tento příkaz ti zakáže gemblit na 2h ale dá ti 1000🪙")
async def work(interaction: discord.Interaction):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, "/work", server)
    try:
        with open('blacklist.txt', 'r') as file:
            obsah = file.read()
            for line in obsah.splitlines():
                if line.startswith(f"{uzivatel}:"):
                    ban_do = int(line.split(':')[1])
                    if time.time() < ban_do:
                        await interaction.response.send_message(
                            f"Jelikož už pracuješ nemohu tě nechat pracovat znovu. Tvůj ban vyprší v {time.ctime(ban_do)}.")
                        return
    except FileNotFoundError:
        pass

    ban_do = int(time.time()) + 2 * 3600  # 8 hodin v sekundách
    with open('blacklist.txt', 'a') as file:
        file.write(f"{uzivatel}:{ban_do}\n")

    try:
        with open('balance.txt', 'r') as file:
            lines = file.readlines()
        user_found = False
        for i, line in enumerate(lines):
            if line.startswith(f'{uzivatel}:'):
                current_balance = float(line.split(':')[1])
                lines[i] = f"{uzivatel}:{current_balance + 1000}\n"
                user_found = True
                break
        if not user_found:
            lines.append(f"{uzivatel}:1000\n")
        with open('balance.txt', 'w') as file:
            file.writelines(lines)
    except FileNotFoundError:
        with open('balance.txt', 'w') as file:
            file.write(f"{uzivatel}:1000\n")

    await interaction.response.send_message(
        f"Začal jsi pracovat, za 2 hodiny ti přičtu 1000🪙. Tvůj ban vyprší v {time.ctime(ban_do)}.")

    # Odstranění uživatele z blacklistu po 8 hodinách
    await asyncio.sleep(2 * 3600)  # 8 hodin v sekundách
    with open('blacklist.txt', 'r') as file:
        lines = file.readlines()
    with open('blacklist.txt', 'w') as file:
        for line in lines:
            if not line.startswith(f"{uzivatel}:"):
                file.write(line)


@client.tree.command(name="balance", description="Tento příkaz ti napíše kolik máš coinů🪙")
async def balance(interaction: discord.Interaction):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, "/balance", server)
    try:
        with open('balance.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(f"{uzivatel}:"):
                    user_coiny = float(line.split(':')[1])
                    await interaction.response.send_message(f"Tvůj aktuální zůstatek je {round(user_coiny, 2)}🪙.")
                    return
        # If the user is not found in the file
        await interaction.response.send_message(
            "Nemáš zatím žádné coiny. Použij příkaz /start pro získání počátečních coinů🪙.")
    except FileNotFoundError:
        await interaction.response.send_message("Soubor s coiny nebyl nalezen. Kontaktuj prosím správce bota.")


@client.tree.command(name="message", description="Tento příkaz může použít jen ockotajny, nebo dandulblack.")
async def message(interaction: discord.Interaction, zprava: str):
        uzivatel = interaction.user.name
        server = interaction.guild.name
        vypis(uzivatel, "/restart", server)
        if uzivatel in "ockotajny dandulblack":
            await interaction.response.send_message(zprava)
        else:
            await interaction.response.send_message("Hele, na tohle nemáš právo😾")




@client.tree.command(name="restart", description="Tento příkaz může použít jen ockotajny, nebo dandulblack.")
async def restart(interaction: discord.Interaction):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, "/restart", server)
    if uzivatel in "ockotajny dandulblack":
        await interaction.response.send_message("Jdu se restartovat👋")
        os.system('start.py')
    else:
        await interaction.response.send_message("Hele, na tohle nemáš právo😾")


class BlackjackView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
    async def hit(self, button: discord.ui.Button, interaction: discord.Interaction):
        tlacitko = "hit"
        zprava, soucet_karet, karty_v_ruce = blackjack2(tlacitko)
        uzvatel = interaction.user.name

        with open(f"balance.txt", "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(f"{uzvatel}:"):
                user_coiny = float(line.split(':')[1])
                break

        with open("blackjack.txt", "r") as file:
            blackjack_lines = file.readlines()

        for line in blackjack_lines:
            if line.startswith(f"{uzvatel}:"):
                sazka = float(line.split(':')[1])
                break

        if "Bohužel" in zprava:
            user_coiny -= sazka
        elif "Gratuluji" in zprava:
            user_coiny += sazka
        else:
            # Remíza nebo jiný výsledek
            pass

        # Aktualizace balance.txt
        updated_lines = []
        for line in lines:
            if line.startswith(f"{uzvatel}:"):
                updated_lines.append(f"{uzvatel}:{user_coiny}\n")
            else:
                updated_lines.append(line)

        with open(f"balance.txt", "w") as file:
            file.writelines(updated_lines)

        # Přidání informace o coinech do zprávy
        zprava += f"\nVáš aktuální zůstatek: {user_coiny} coinů."

        await interaction.response.send_message(zprava)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary)
    async def stand(self, button: discord.ui.Button, interaction: discord.Interaction):
        tlacitko = "stand"
        zprava, soucet_karet, karty_v_ruce = blackjack2(tlacitko)
        uzvatel = interaction.user.name

        with open(f"balance.txt", "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(f"{uzvatel}:"):
                user_coiny = float(line.split(':')[1])
                break

        with open("blackjack.txt", "r") as file:
            blackjack_lines = file.readlines()

        for line in blackjack_lines:
            if line.startswith(f"{uzvatel}:"):
                sazka = float(line.split(':')[1])
                break

        if "Bohužel" in zprava:
            user_coiny -= sazka
        elif "Gratuluji" in zprava:
            user_coiny += sazka
        else:
            # Remíza nebo jiný výsledek
            pass

        # Aktualizace balance.txt
        updated_lines = []
        for line in lines:
            if line.startswith(f"{uzvatel}:"):
                updated_lines.append(f"{uzvatel}:{user_coiny}\n")
            else:
                updated_lines.append(line)

        with open(f"balance.txt", "w") as file:
            file.writelines(updated_lines)

        # Přidání informace o coinech do zprávy
        zprava += f"\nVáš aktuální zůstatek: {user_coiny} coinů."

        await interaction.response.send_message(zprava)


def blackjack2(tlacitko):
    if tlacitko == "hit":
        with open('zprava.txt', 'r') as file:
            zprava = file.readlines()
        with open('karty_v_ruce.txt', 'r') as file:
            karty_v_ruce = file.readlines()
        with open('pouzite_karty.txt', 'r') as file:
            pouzite_karty = file.readlines()
        while True:
            karta = random.choice(blackjack_karty)
            if karta in pouzite_karty:
                continue
            else:
                pouzite_karty = pouzite_karty + karta
                karty_v_ruce = karty_v_ruce + karta
                zprava = f"{zprava} {karta}"
                soucet_karet = soucet(karty_v_ruce)
                if soucet_karet >= 21:
                    return f"Bohužel ti padla karta {karta}, takže součet tvých karet přesáhl 21, proto prohráváš😿", soucet_karet, karty_v_ruce
                else:
                    return f"{zprava} {karta}", soucet_karet, karty_v_ruce
    elif tlacitko == "stand":
        with open('zprava.txt', 'r') as file:
            zprava = file.read()
        with open('karty_v_ruce.txt', 'r') as file:
            karty_v_ruce = file.read().splitlines()
        with open('pouzite_karty.txt', 'r') as file:
            pouzite_karty = file.read().splitlines()

        while True:
            karta = random.choice(blackjack_karty)
            if karta not in pouzite_karty:
                pouzite_karty.append(karta)
                break

        zprava = zprava.replace("ruce jednu neznámou kartu🃏", f"ruce {karta}")

        with open('zprava.txt', 'w') as file:
            file.write(zprava)
        with open('pouzite_karty.txt', 'w') as file:
            file.write('\n'.join(pouzite_karty))
            karty_dealera = pouzite_karty - karty_v_ruce
        soucet_dealera = soucet(karty_dealera)
        soucetkaret = soucet(karty_v_ruce)
        if soucet_dealera >= soucetkaret:
            zprava = f"Bohužel dealer vyhrál, protože měl karty {karty_dealera} se součtem {soucet_dealera} a ty jsi měl karty {karty_v_ruce} se součtem {soucetkaret}😿"
            return zprava, soucetkaret, karty_v_ruce
        elif soucet_dealera == soucetkaret:
            zprava = f"UFF je to remíza ty i dealer máte součet karet {soucetkaret}"
            return zprava, soucetkaret, karty_v_ruce
        else:
            zprava = f"🤑Gratuluji vahrál jsi s kartamy {karty_v_ruce} se součtem {soucetkaret}, zatím co dealer měl {karty_dealera} se součtem {soucet_dealera}.🤑"
            return zprava, soucetkaret, karty_v_ruce



@client.tree.command(name="blackjack", description="Napiš: /blackjack [počet coinů]")
async def blackjack(interaction: discord.Interaction, coins: float):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, f"/blackjack {coins}", server)
    ban_status, _ = ban_check(uzivatel)
    if coins <= 0:
        await interaction.response.send_message("Musíš vsadit kladnou částku.")
        return

    if ban_status == "ne":
        zprava, pouzite_karty, karty_v_ruce = hrablackjack(uzivatel)
        soucet_karet = soucet(karty_v_ruce)
        zprava = f"{zprava}Součet tvých karet je: {soucet_karet}"
        view = BlackjackView()
        await interaction.response.send_message(zprava, view=view)
    else:
        await interaction.response.send_message("Je mi líto, ale momentálně nemůžeš gamblit 😿")

@client.tree.command(name="stop", description="Tento příkaz může použít jen ockotajny, nebo dandulblack.")
async def stop(interaction: discord.Interaction):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, "/stop", server)
    if uzivatel in "ockotajny dandulblack":
        await interaction.response.send_message("Vypínám server👋")
        os.system("shutdown /s /t 0")
        await interaction.response.send_message("Hele, na tohle nemáš právo😾")

@client.tree.command(name="dm", description="Tento příkaz může použít jen ockotajny, nebo dandulblack.")
async def dm(interaction: discord.Interaction):
    if interaction.user.name not in ["ockotajny", "dandulblack"]:
        await interaction.response.send_message("Nemáš oprávnění použít tento příkaz.", ephemeral=True)
        return

    message = (
        "🐱 Čau jsem Melvin, nejvíc useless BOT na celým discordu.\n"
        "Co umím:\n"
        "/help - zobrazí tuhle nápovědu\n"
        "/ruleta - zahraj si ruletu o coiny (bet může být even, odd, row 1, row 2, row 3, red, black,)\n"
        "/work - Tento příkaz ti zakáže gemblit na 2h ale dá ti 1000🪙\n"
        "/start - dá ti na začátek 1000🪙\n"
        "/balance - zobrazí kolik máš coinů🪙"
    )

    try:
        await interaction.user.send(message)
        await interaction.response.send_message("Máš to tam😸.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("Nemohl jsem ti poslat DM. Zkontroluj, zda máš povolené přijímání zpráv.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Nastala chyba při odesílání DM: {str(e)}", ephemeral=True)


import random


def sloty(uzivatel, coins):
    SYMBOLY = {
        'TRESNE': '🍒',
        'CITRON': '🍋',
        'POMERANC': '🍊',
        'HROZNY': '🍇',
        'SEDMICKA': '7️⃣',
        'BAR': 'BAR',
        'ZVON': '🔔',
        'DIAMANT': '💎',
        'WILD': '❓',
        'SCATTER': '⭐'
    }
    vysledek = random.choices(list(SYMBOLY.values()), k=3)

    # Definice multiplikátorů
    MULTIPLIERS = {
        'TRESNE': 2,
        'CITRON': 2,
        'POMERANC': 3,
        'HROZNY': 3,
        'SEDMICKA': 5,
        'BAR': 10,
        'ZVON': 15,
        'DIAMANT': 20,
        'WILD': 25,
        'SCATTER': 50
    }

    # Kontrola výhry
    if len(set(vysledek)) == 1:  # Všechny symboly jsou stejné
        symbol = vysledek[0]
        multiplier = MULTIPLIERS[list(SYMBOLY.keys())[list(SYMBOLY.values()).index(symbol)]]
    elif '❓' in vysledek:  # WILD symbol
        non_wild = [s for s in vysledek if s != '❓']
        if len(set(non_wild)) == 1:
            symbol = non_wild[0]
            multiplier = MULTIPLIERS[list(SYMBOLY.keys())[list(SYMBOLY.values()).index(symbol)]]
        else:
            multiplier = 1
    else:
        multiplier = 0

    return vysledek, multiplier


@client.tree.command(name="slots", description="Napiš: /slots [počet coinů]")
async def slots(interaction: discord.Interaction, coins: float):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, f"/slots {coins}", server)
    ban_status, _ = ban_check(uzivatel)
    if coins <= 0:
        await interaction.response.send_message("Musíš vsadit kladnou částku.")
        return

    if ban_status == "ne":
        vysledek, multiplier = sloty(uzivatel, coins)
        zprava = f"Výsledek: {' '.join(vysledek)}\n"

        if multiplier > 0:
            vyhrana_castka = coins * multiplier
            zprava += f"Gratulujeme! Vyhráváš {vyhrana_castka}🪙 (multiplikátor {multiplier}x)"
            balance(vyhrana_castka, uzivatel)
        else:
            zprava += "Bohužel jsi nevyhrál. Zkus to znovu!"
            vyhrana_castka = coins * multiplier
            balance(vyhrana_castka, uzivatel)

        await interaction.response.send_message(zprava)
    else:
        await interaction.response.send_message("Je mi líto, ale momentálně nemůžeš gamblit 😿")


def balance(vyhrana_castka, uzivatel):
    updated_lines = []
    with open("balance.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith(f"{uzivatel}:"):
            user_coiny = float(line.split(':')[1])
            user_coiny += vyhrana_castka
            updated_lines.append(f"{uzivatel}:{user_coiny}\n")
        else:
            updated_lines.append(line)

    with open("balance.txt", "w") as file:
        file.writelines(updated_lines)

    return


@client.tree.command(name="sloty", description="Napiš: /slots [počet coinů]")
async def slots(interaction: discord.Interaction, coins: float):
    uzivatel = interaction.user.name
    server = interaction.guild.name
    vypis(uzivatel, f"/slots {coins}", server)
    ban_status, _ = ban_check(uzivatel)
    if coins <= 0:
        await interaction.response.send_message("Musíš vsadit kladnou částku.")
        return

    if ban_status == "ne":
        vysledek, multiplier = sloty(uzivatel, coins)
        zprava = f"Výsledek: {' '.join(vysledek)}\n"

        if multiplier > 0:
            vyhrana_castka = coins * multiplier
            zprava += f"Gratulujeme! Vyhráváš {vyhrana_castka}🪙 (multiplikátor {multiplier}x)"
        else:
            zprava += "Bohužel jsi nevyhrál. Zkus to znovu!"
            vyhrana_castka = -coins  # Odečteme vsazenou částku

        new_balance = balance(vyhrana_castka, uzivatel)
        zprava += f"\nTvůj nový zůstatek: {new_balance}🪙"

        await interaction.response.send_message(zprava)
    else:
        await interaction.response.send_message("Je mi líto, ale momentálně nemůžeš gamblit 😿")


client.run('')
