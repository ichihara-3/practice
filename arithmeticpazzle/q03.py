# 1..100

def reverse(card):
    return 'back' if card == 'front' else 'front'

def main():
    cards = ['back'] * 100
    for i in range(2, 101):
        for j in range(i-1, 100, i):
            cards[j] = reverse(cards[j])
    print(list(i+1 for i, card in enumerate(cards) if card =='back'))

main()
