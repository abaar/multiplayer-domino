class Player:
    def __init__(self, name):
        self.name = name
        self.kartu = {}
        self.turn = "Zero"
        self.poin = 0

    def addCard(self, card):
        if isinstance(card, Card):
            self.index = card.randomCard()
            self.kartu[self.index] = card.name[self.index]

    def throwCard(self, index):
        if index in self.kartu:
            del self.kartu[index]


class Card:
    def __init__(self):
        # Buat mengetahui kartu mana saja yang sudah dipakai
        self.card = list()
        # Untuk menamai kartu
        self.name = {
            "00": [0, 0],
            "01": [0, 1],
            "02": [0, 2],
            "03": [0, 3],
            "04": [0, 4],
            "05": [0, 5],
            "06": [0, 6],
            "11": [1, 1],
            "12": [1, 2],
            "13": [1, 3],
            "14": [1, 4],
            "15": [1, 5],
            "16": [1, 6],
            "22": [2, 2],
            "23": [2, 3],
            "24": [2, 4],
            "25": [2, 5],
            "26": [2, 6],
            "33": [3, 3],
            "34": [3, 4],
            "35": [3, 5],
            "36": [3, 6],
            "44": [4, 4],
            "45": [4, 5],
            "46": [4, 6],
            "55": [5, 5],
            "56": [5, 6],
            "66": [6, 6]
        }
        # Untuk mengetahui kartu mana saja yang ada di meja
        self.ready = list()
        # Untuk mengetahui jumlah kartu yang sudah keluar
        self.jumlah = 0

    # Fungsi untuk merandom kartu yang akan dibagikan
    def randomCard(self):
        from random import randint

        while True:
            self.value1 = randint(0, 6)
            self.value2 = -1
            while self.value2 < self.value1:
                self.value2 = randint(0, 6)
            self.kartu = str(self.value1) + str(self.value2)
            if self.kartu not in self.card:
                self.card.append(self.kartu)
                break
        self.jumlah += 1
        return self.kartu

    # Fungsi untuk mengetahui kartu mana saja yang ada di meja
    def inTable(self, dict):
        if len(self.ready) == 0:
            for d in dict:
                self.ready.append(d)
        else:
            if dict[0] == self.ready[0]:
                self.ready.remove(dict[0])
                self.ready.insert(0, dict[1])
            elif dict[1] == self.ready[0]:
                self.ready.remove(dict[1])
                self.ready.insert(0, dict[0])
            elif dict[0] == self.ready[1]:
                self.ready.remove(dict[0])
                self.ready.insert(1, dict[1])
            elif dict[1] == self.ready[1]:
                self.ready.remove(dict[1])
                self.ready.insert(1, dict[0])
        print "Kartu yang tersedia di meja " + str(self.ready[0]) + " " + str(self.ready[1])

    # Untuk me-return True or False kartu ready yang ada di table
    def readyInTable(self, dict):
        if len(self.ready) == 0:
            return True
        else:
            for d in dict:
                if d in self.ready:
                    return True
            print "Anda harus memasukan kartu yang tersedia di meja"
            print "Kartu yang tersedia di meja " + str(self.ready[0]) + " " + str(self.ready[1])
            return False


class MainDrawGame:
    # Inisialisasi untuk memindahkan semua class yang diluar menjadi di atribut dalam class
    def __init__(self, player, jmlplayer, card):
        self.jmlplayer = jmlplayer
        self.player = {}
        for p in range(jmlplayer):
            if isinstance(player[p], Player):
                self.player[p] = player[p]
        if isinstance(card, Card):
            self.card = card
        self.nilai = list()
        self.index = 0
        self.turn = 1
        self.turnindex = 0
        self.draw = 0
        self.bergerak = jmlplayer

    def firstDraw(self):
        # Jika jumlah player 2 maka berdasarkan peraturan domino, dibagi 7 kartu
        if self.jmlplayer == 2:
            for _ in range(7):
                for p in range(self.jmlplayer):
                    self.player[p].addCard(self.card)
        # Jika jumlah player 3-4 maka berdasarkan peraturan domino, dibagi 5 kartu
        else:
            for _ in range(5):
                for p in range(self.jmlplayer):
                    self.player[p].addCard(self.card)

    def firstTurn(self):
        for p in range(self.jmlplayer):
            if "66" in self.player[p].kartu:
                self.nilai.append(6)
            elif "55" in self.player[p].kartu:
                self.nilai.append(5)
            elif "44" in self.player[p].kartu:
                self.nilai.append(4)
            elif "33" in self.player[p].kartu:
                self.nilai.append(3)
            elif "22" in self.player[p].kartu:
                self.nilai.append(2)
            elif "11" in self.player[p].kartu:
                self.nilai.append(1)
            elif "00" in self.player[p].kartu:
                self.nilai.append(0)
            else:
                self.nilai.append(-1)

        # Untuk mengetahui index ke berapa yang memiliki nilai terbesar
        self.index = self.nilai.index(max(self.nilai))

    def drawCard(self):
        # Untuk mengecek apakah kartu di player ada di meja
        # Untuk giliran pertama dikarenakan tidak ada kartu di meja, maka tidak akan masuk ke for ini
        for r in self.card.ready:
            for k in self.player[self.index].kartu.values():
                if r in k:
                    self.draw = 0
                    break
                self.draw = 1
            if self.draw == 0:
                break

        # Jika kartu di player tidak ada di meja maka return True
        if self.draw == 1:
            # Jika jumlah kartu yang sudah keluar = 28, maka tidak dapat draw lagi
            if self.card.jumlah == 28:
                print "Kartu di meja sudah habis"
                self.bergerak -= 1
                return True
            else:
                self.player[self.index].addCard(self.card)
                return True
        # Jika kartu diplayer ada di meja maka return False
        else:
            return False

    def inGame(self):
        # Game akan terus berjalan hingga kartu habis atau sudah ada pemenangnya
        while True:
            print "TURN " + str(self.turn)
            # Cek dulu kartu di player ada di meja atau tidak
            if self.drawCard():
                print "Kartu di tangan tidak memiliki titik yang sama dengan di meja, giliran dilewat"
            else:
                print self.player[self.index].name + " Has Card -> " + str(self.player[self.index].kartu)
                print "Your Turn..."
                while True:
                    dot = raw_input()
                    # Jika yang diinputkan ada di player
                    if dot in self.player[self.index].kartu:
                        print self.player[self.index].name + " Have Choose " + str(
                            self.player[self.index].kartu[dot]) + " Card"
                        # Jika kartu yang diinputkan player ada di table
                        if self.card.readyInTable(self.player[self.index].kartu[dot]):
                            self.card.inTable(self.player[self.index].kartu[dot])
                            self.player[self.index].throwCard(dot)
                            break
                    else:
                        print "Masukan kartu yang kamu miliki saja..."

            print self.player[self.index].name + " Has Card -> " + str(self.player[self.index].kartu)

            # Jika ada kartu dari player yang habis
            if len(self.player[self.index].kartu) == 0:
                self.result("Bergerak")
                print self.player[self.index].name + " Win This Round"
                print "Kamu mendapat poin " + str(self.player[self.index].poin)
                return self.index, self.player[self.index].poin
            # Jika tidak ada yang bisa bergerak
            if self.bergerak == 0:
                print "Sudah tidak ada yang bisa bergerak"
                self.result("Tidak Bisa")
                print self.player[self.index].name + " Win This Round"
                print "Kamu mendapat poin " + str(self.player[self.index].poin)
                return self.index, self.player[self.index].poin

            # Untuk looping ketika sudah player 4 balik ke player 1
            self.index += 1
            if self.index == self.jmlplayer:
                self.index = 0

            # Untuk pertambahan TURN
            self.turnindex += 1
            if self.turnindex == self.jmlplayer:
                self.turnindex = 0
                self.turn += 1

    def result(self, penanda):
        # Kalau sudah tidak ada yang bisa bergerak
        # Maka akan dinilai dahulu poin terkecil dari setiap player untuk ditentukan siapa pemenangnya
        if penanda == "Tidak Bisa":
            self.poin = list()
            for p in range(self.jmlplayer):
                for arr in self.player[p].kartu.values():
                    for point in arr:
                        self.poin.append(point)
            self.index = self.poin.index(min(self.poin))
        # Jika sudah didapatkan pemenangnya maka akan dinilai poin yang dia peroleh
        for p in range(self.jmlplayer):
            if self.player[p].name != self.player[self.index].name:
                for arr in self.player[p].kartu.values():
                    for point in arr:
                        self.player[self.index].poin += point


def main():
    print "Select Room"
    print "1. Custom\t2. Quick"
    room = input()
    if room == 1:
        print "Select Number of Player"
        print "2 Player\t3 Player\t4 Player"
        jmlplayer = input()
        print "Select Your Goal"
        print "100\t150\t200"
        goal = input()
        # Inisiaslisasi setiap player mempunyai poin 0
        poin = list()
        for _ in range(jmlplayer):
            poin.append(0)

        while True:
            player = {}
            for p in range(jmlplayer):
                name = "Player "+str(p+1)
                player[p] = Player(name)
            card = Card()
            game = MainDrawGame(player, jmlplayer, card)
            game.firstDraw()
            game.firstTurn()
            result = game.inGame()
            poin[result[0]] += result[1]
            for p in range(jmlplayer):
                print player[p].name + " Has Poin -> " + str(poin[p])

            if poin[result[0]] > goal:
                print "The winner is " + player[result[0]].name
                break
    else:
        print "Searching room..."


if __name__ == "__main__":
    main()
