import time
from subprocess import call

for color in('a', 'e', 'c'): #cycles through different colours
    call('cls', shell=True) #clears the screen
    call('color ' + color, shell=True)
    print('The quick brown fox jumps over the lazy dog.')
    time.sleep(1)

input("\nPress enter to exit. ")
