states = open("E:/hashcat/wordlists/states.txt", "r")
nouns = open("C:/Users/roney/Downloads/nouns.txt", "r")
nouns2 = nouns.readlines()
numbers99 = open("numbers99.txt", "w+")
finalOutput = open ("finalOutput.txt", "w+")

if __name__ == '__main__':
    for i in states:
        state = i.strip('\n')
        state = state.lower()
        print(state)
        a = 0
        while a < 15:
            noun = nouns2[a].strip('\n')
            noun = noun.upper()
            print(noun)
            b = 0
            a += 1
            while b <= 99:
                strX = str(b).zfill(2)
                #string2 = str(i.strip('\n')) + str(a.strip('\n')) + strX + "\n"
                string2 = state + noun + strX + "\n"
                print(string2)
                finalOutput.write(string2)
                b += 1
