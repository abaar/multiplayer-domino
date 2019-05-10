class Player:
    def __init__(self, name):
        self.name = name
        self.kartu = {}

    def addCard(self, card):
        if isinstance(card, Card):
            self.index = card.randomCard()
            self.kartu[self.index] = card.name[self.index]

class Card:
    # Buat mengetahui kartu mana saja yang sudah dipakai
    card = list()

    def __init__(self):
        self.name = {
            "00": [0,0],
            "01": [0,1],
            "02": [0,2],
            "03": [0,3],
            "04": [0,4],
            "05": [0,5],
            "06": [0,6],
            "11": [1,1],
            "12": [1,2],
            "13": [1,3],
            "14": [1,4],
            "15": [1,5],
            "16": [1,6],
            "22": [2,2],
            "23": [2,3],
            "24": [2,4],
            "25": [2,5],
            "26": [2,6],
            "33": [3,3],
            "34": [3,4],
            "35": [3,5],
            "36": [3,6],
            "44": [4,4],
            "45": [4,5],
            "46": [4,6],
            "55": [5,5],
            "56": [5,6],
            "66": [6,6]
        }

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
        return self.kartu


class MainDrawGame:
    # Inisialisasi untuk memindahkan semua class yang diluar menjadi di atribut dalam class
    def __init__(self, player, jmlplayer, goal, card):
        self.jmlplayer = jmlplayer
        self.goal = goal
        self.player = {}
        for p in range(jmlplayer):
            if isinstance(player[p],Player):
                self.player[p] = player[p]
        if isinstance(card, Card):
            self.card = card

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

    def inGame(self):
        # Game akan terus berjalan hingga kartu habis
        while True:
            # Dimulai dari player 1
            for p in range(self.jmlplayer):
                print self.player[p].name + " Has Card -> " + str(self.player[p].kartu)
            break

def main():
    print "Select Room"
    print "1. Custom\t2. Quick"
    room = input()
    if room == 1:
        print "Select Game"
        print "1. Draw Game\t2. Block Game"
        game = input()

        print "Select Number of Player"
        print "2 Player\t3 Player\t4 Player"
        jmlplayer = input()

        player = {}
        for p in range(jmlplayer):
            name = "Player "+str(p+1)
            player[p] = Player(name)

        print "Select Your Goal"
        print "1. 100\t2. 150\t3. 200"
        goal = input()

        card = Card()
        if game == 1:
            game = MainDrawGame(player, jmlplayer, goal, card)
            game.firstDraw()
            game.inGame()
            # game.result()

        else:
            print "Game belum dibuat..."

    else:
        print "Searching room..."


if __name__ == "__main__":
    main()