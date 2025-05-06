from base import Player

player = Player("Goredawn the Gladiator")

player.connect()
while True:
    player.take_turn(input('Player:'))
