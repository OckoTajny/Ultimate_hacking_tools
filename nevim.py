class Zlodej:
    def __init__(self, barva, vek):
        self.barva = barva
        self.vek = vek
    def soud(self):
        if self.barva == "cerna":
            print("POZOR, ZLODEJ!")
        else:
            print("ZLODEJ NENI CERNY, TAKZE JE TO V POHODE")

zlodej1 = Zlodej("cerna", 20)
zlodej2 = Zlodej("modra", 30)

zlodej1.soud()
zlodej2.soud()