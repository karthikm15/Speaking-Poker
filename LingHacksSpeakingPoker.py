'''
Mar 30-31, 2019
@authors: suryajasper, adityamittal, karthikmittal
'''
import random
from collections import OrderedDict
import speech_recognition as sr
import os

def Voice():
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            #r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, 5)
            except:
                print("Please try again")
        t = ''
        try:
            t = r.recognize_google(audio)
            print(t)
            return t
        except:
            print("Sorry, I didn't quite catch that.")
            os.system("say try speaking louder")
            continue
        if (t == 'stop'):
            print("done")
            break
    return input()
    
class computer:
  currentIndex = 0
  pot = 0
  def __init__(self, dictionary, cards, suits, availableMoney, money, alterations, current, currentIndex, individualCurrent, pot):
    self.dictionary = dictionary
    self.cards = cards
    self.suits = suits
    self.availableMoney = availableMoney
    self.money = money
    self.alterations = alterations
    self.current = current
    self.individualCurrent = individualCurrent
    self.firstRun = True

  def Turn(self):
    if self.firstRun:
      for card, suit in self.dictionary.items():
        self.cards.append(card)
        self.suits.append(suit)
      self.firstRun = False
    self.cards.sort()
    self.suits.sort()
    for i in range(len(self.cards)):
        self.cards[i] = self.cards[i]%13 + 1
    #print(self.cards)
    #print("ind", self.individualCurrent, "static", computer.currentIndex, self.current)
    #print(1, "ind", self.individualCurrent, "static", computer.currentIndex, self.current)
    if self.individualCurrent < computer.currentIndex:
      self.Raise(computer.currentIndex-self.individualCurrent, False)
      #print(2, "ind", self.individualCurrent, "static", computer.currentIndex, self.current)
      return True, computer.currentIndex
    if (len(self.cards) == 2):
      if (self.cards[0] == self.cards[1]):
        self.Raise(1, True)
      if (self.cards[0]%13+1 > 10) or (self.cards[1]%13+1 > 10):
          chance = random.randint(0,10)
          if (chance <= 5):
              self.Raise(1, True)
              return True, computer.currentIndex
      elif (random.randint(0,20) == 20):
        self.Fold()
      else:
        self.Call()
    if (len(self.cards) >= 5):
      #Royal Flush
      tempList = self.cards
      tempList.reverse()
      if tempList[0] == 14 and tempList[1] == 13 and tempList[2] == 12 and tempList[3] == 11 and tempList[4] == 10:
        self.Raise(5, True)
        return True, computer.currentIndex
      #Straight
      straightnum = 0
      maxstraight = 0
      for i in range(len(self.cards)):
        if i == 0:
          straightnum = 1
          continue
        if self.cards[i] == self.cards[i-1] +1:
          straightnum +=1 
          if (straightnum > maxstraight):
            maxstraight = straightnum
        else:
          straightnum = 0
      if maxstraight == 5:
        self.Raise(5, True)
        return True, computer.currentIndex
      elif (self.cardsLeft() >= (5-maxstraight)):
        self.Raise(1, True)
        return True, computer.currentIndex
      #four in a row
      similar = []
      maxSimilar = 0
      sim = 0
      for i in range(len(self.cards)):
        if i == 0:
          similar.append(self.cards[i])
          maxSimilar = 1
          continue
        if self.cards[i] == similar[similar.count-1]:
          similar.append(self.cards[i])
          sim += 1
          if (sim > maxSimilar):
            maxSimilar = similar
        else:
          sim = 0
      if maxSimilar == 4:
        self.Raise(2, True)
        return True, computer.currentIndex
      #Flush
      flush = 0 
      maxflush = 0
      for i in range(len(self.suits)):
        if i == 0:
          flush += 1
          continue
        if self.suits[i] == self.suits[i-1]:
          flush += 1
          if flush > maxflush:
              maxflush = flush
        else:
          flush = 0
            
      if flush == 5:
        self.Raise(5, True)
        return True, computer.currentIndex
      elif self.cardsLeft() >= (5-maxflush):
        self.Raise(1, True)
        return True, computer.currentIndex
      
      #three of a kind
      if maxSimilar == 3:
        self.Raise(1, True)
        return True, computer.currentIndex
      #two of a kind
      if maxSimilar == 2:
        self.Call()
    return False, computer.currentIndex

  def Fold(self):
      print("one of your opponents has folded")
      os.system("say 'one of your opponents has folded'")
      return
  def cardsLeft(self):
      return 7-len(self.cards)
  def Raise(self, num, started):
    try:
      #os.system("say one of your opponents is raising the bet to" + str(self.money[computer.currentIndex+num]))
      print("one of your opponents is raising the bet to ", self.money[computer.currentIndex+num])
      self.pot += money[computer.currentIndex+num]
      if (started == True):
        computer.currentIndex += num
        #print("We are raising currentIndex to ", computer.currentIndex)
      self.individualCurrent = computer.currentIndex
      self.current = self.money[computer.currentIndex]
      self.availableMoney -= current
    except IndexError:
      self.pot += self.money[len(self.money)-1]
      computer.currentIndex = len(self.money)-1
      self.current = self.money[computer.currentIndex]
    finally:
      self.alterations += 1
  def Call(self):
    print("one of your opponents is calling")
    #os.system("say one of your opponents is calling")
    self.pot += self.current
    self.alterations += 1

computers = []

#----------------------------------------------------------

while True:
    try:
        while True:
            try:
                print("How many players do you want?")
                os.system("say how many players do you want?")
                numofplayersraw = int(Voice())
                break
            except ValueError:
                print("Please enter an integer between 3 and 9")
                os.system("say Please enter an integer between 3 and 9")
        if (numofplayersraw > 8 or numofplayersraw < 3):
            print("Please enter an integer between 3 and 9")
            os.system("say Please enter an integer between 3 and 9")
            continue
        for i in range(numofplayersraw):
            dictionary1 = {}
            cards1 = []
            suits1 = []
            availableMoney1 = 1000
            money1 = [5, 10, 20, 50, 100]
            alterations1 = 0
            current1 = 10
            currentIndex1 = 0
            individualCurrent1 = currentIndex1
            pot1 = 0
            computers.append(computer(dictionary1, cards1, suits1, availableMoney1, money1, alterations1, current1,currentIndex1, individualCurrent1, pot1))
        break
    except ValueError:
        print("Enter an integer")
        os.system("say Enter an Integer")
players = len(computers)+1
global turn
turn = 1
available = {}
suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
current = 5
global alterations, pot, currentIndex, availableMoney
currentIndex = 0
money = [5, 10, 20, 50, 100]
availableMoney = 1000
alterations = 0
pot = 0
count = 0
for i in suits:
    for j in range(13):
        available[(13*count)+j+1] = i
    count +=1
cards = {}

#----------------------------------------------------------

def Raise1(num):
  print("a player is raising")
  os.system("say You have raised the bet")
  global alterations, pot, currentIndex, availableMoney
  try:
    if alterations > 0:
        computer.pot += money[computer.currentIndex+num]
    computer.currentIndex += num
    current = money[computer.currentIndex]
    availableMoney -= current
    computer.pot -= money[computer.currentIndex-num]
    availableMoney += money[computer.currentIndex-num]
  except IndexError:
    computer.pot += money[len(money)-1]
    computer.currentIndex = len(money)-1
    current = money[computer.currentIndex]
  finally:
    alterations += 1
def Call1():
  print("a player is calling")
  os.system("say You have called")
  global alterations, pot, currentIndex, availableMoney
  computer.pot += money[currentIndex]
  alterations += 1
  availableMoney -= money[currentIndex]
def Fold1():
  exit()

#----------------------------------------------------------

b = list(available.items())
random.shuffle(b)
available = OrderedDict(b)
for i in range(players):
  for j in range(2):
    newkeys = list(available.keys())
    if (i == players-1):
        cards[newkeys[0]] = available[newkeys[0]]
    else:
      computers[i].dictionary[newkeys[0]] = available[newkeys[0]]
      #print("adding vals to computer", i)
    available.pop(newkeys[0])
#print(available)
#print(cards)
availableMoney -= 5
pot += 5
turn += 1
firstRun = True

def Choice():
  while True:
    try:
      print ("Your cards are:", end = ' ')
      os.system("say Your cards are")
      gcount = 1
      for key, val in cards.items():
        if gcount == 1:
          print("the", key%13+1, "of", val, end = ' and ')
          os.system("say the " + str(key%13+1) + " of " + str(val) + " and ")
          gcount+=1
          continue
        if gcount == 2:
          print("the", key%13+1, "of", val)
          os.system("say the " + str(key%13+1) + " of " + str(val))
      print("\nEither call, raise, or fold. ")
      os.system("say Say either call, raise, or fold.")
      choice = ''
      while True:
        try:
          choice = Voice()
          if (choice == 'call' or choice == 'fold' or choice == 'raise'):
            break
          else:
            print("Please say call, raise, or fold")
            os.system("say Please say call, raise, or fold")
        except ValueError:
          print("Please say call, raise, or fold")
          os.system("say Please say call, raise, or fold")
      if (choice == 'call'):
        Call1()
        return 0
      elif (choice == 'raise'):
        while True:
          try:
            print("How many places would you like to raise by?")
            os.system("say How many places would you like to raise by?")
            raiseVal = int(Voice())
            if (raiseVal >= 1):
              break
            else:
              print("Please say a number greater than or equal to 1")
              os.system("say Please say a number greater than or equal to 1")
          except ValueError:
            print("Please say a number greater than or equal to 1")
            os.system("say Please say a number greater than or equal to 1")
        if (raiseVal > 0):
          Raise1(raiseVal)
          return currentIndex
        else:
          print("Can't be negative")
          os.system("say the number can't be negative")
      elif (choice == 'fold'):
        Fold1()
        return 0
      else:
        print("Please enter a number between 1 and 3")
        os.system("say Please enter a number between 1 and 3")
    except ValueError:
      print("Must be a positive integer")
      os.system("say Must be a positive integer")

#first round
global raisedMoney, raisedPerson
raisedMoney = []
for i in range(players):
  raisedMoney.append(0)
raisedPerson = players

turn = 1  

#dealing the first three cards on 0 table
dealt = {}
def deal(num):
    global turn
    print("The dealt cards are:")
    for i in range(num):
        newkeys = list(available.keys())
        dealt[newkeys[0]] = available[newkeys[0]]
        available.pop(newkeys[0])
    newKeys = list(dealt.keys())
    for j in range(len(computers)):
        for key, val in dealt.items():
            computers[j].dictionary[key] = val
    os.system("say The dealt cards are")
    for key, val in dealt.items():
        print(key%13+1, "of", val)
        os.system("say " + str(key%13+1) + " of " + str(val))
def Round():
    global turn
    global raisedMoney, raisedPerson
    raisedPerson = players
    #print("there are", len(computers), "computers")
    #print("there are", players, "players")
    turn = 1
    raisedMoney = []
    for i in range(players):
        raisedMoney.append(0)
    while True:
        if (turn == 1):
            raisedMoney[0] = Choice()
            turn += 1
            continue
        elif turn <= players:
            raised, currentIndex = computers[turn-2].Turn()
            current = money[currentIndex]
            raisedMoney[turn-1] = currentIndex
        if turn < raisedPerson:
            turn += 1
        else:
            reverseRaisedMoney = raisedMoney
            reverseRaisedMoney.reverse()
            for i in range(len(reverseRaisedMoney)):
                if i > 0:
                    if reverseRaisedMoney[i] != reverseRaisedMoney[i-1]:
                        raisedPerson = players - i
                        break
            reverseRaisedMoney.reverse()
            #print(raisedPerson)
            if (raisedPerson == players) or (len(set(reverseRaisedMoney)) == 1) or (len(set(reverseRaisedMoney)) == 2) or (2 in reverseRaisedMoney):
                break
            turn = 1
    for i in range(len(computers)):
        computers[i].alterations = 0
        computers[i].currentIndex = 0
        computers[i].individualCurrent = 0
    computer.pot *= players
    print("There is $", computer.pot, "in the pot")
    print("You have $", availableMoney, "available")
    os.system("say There are " + str(computer.pot) + " dollars in the pot")
    os.system("say You have " + str(availableMoney) + " dollars to bet")

for round1 in range(4):
    if (round1 == 0):
        Round()
    elif (round1 == 1):
        print("\nRound 2")
        deal(3)
        Round()
    elif (round1 == 2):
        print("\nRound 3")
        deal(1)
        Round()
    elif (round1 == 3):
        print("\nRound 4")
        deal(1)
        Round()
''' #Code to find out who won
playerDict = cards
for key, value in dealt.items():
    playerDict[key] = value
#computers.append(computer(playerDict, list(playerDict.keys()), list(playerDict.values())), availableMoney, money, 0, computer.current, computer.currentIndex, 0, pot)
#RoyalFlush
someonewon = False
for i in range( len(computers)):
    cpu = computers[i]
    royalcards = list(cpu.dictionary.keys()).sort()
    print(royalcards)
    royalstartindex = -1
    for i in range(len(royalcards)):
        if royalcards[i] == 10:
            royalstartindex= i
    if royalstartindex == -1:
        continue
    else:
        try:
            if (royalcards[royalindex+1] == 11 and royalcards[royalindex+2] == 12 and royalcards[royalindex+3] == 13 and royalcards[royalindex+4] == 14):
                if (i < len(computers)-1):
                    print("Computer", i+1, "won.")
                else:
                    print("You Won!!!!")
                someonewon = True
                break
        except IndexError:
            continue
#Four of a kind
if (not someonewon):
    for i in range( len(computers)):
        cpu = computers[i]
        foakcards = list(cpu.dictionary.keys()).sort()
        count = 0;
        for i in range(len(foakcards)):
            if i == 0:
                count = 1
                continue
            if foakcards[i] == foakcards[i-1]:
                count+=1
                if (count >= 4):
                    if (i < len(computers)-1):
                        print("Computer", i+1, "won.")
                    else:
                        print("You Won!!!!")
                    someonewon = True
                    break
            else:
                count = 0
#Full House
if (not someonewon):
    for i in range( len(computers)):
        cpu = computers[i]
        fhdict = cpu.dictionary
        fhkeys = list(fhdict.keys()).sort()
        checkedTwo, checkedThree = False, False
        count = 0
        for i in range(len(fhdict)):
            if i == 0:
                count = 1
                continue
            if fhdict[fhkeys[i] == fhkeys[i-1]]:
                count+=1
            else:
                if count == 2:
                    checkedTwo = True
                if count == 3:
                    checkedThree = True
                count = 0
        if checkedTwo and checkedThree:
            if (i < len(computers)-1):
                print("Computer", i+1, "won.")
            else:
                print("You Won!!!!")
            someonewon = True
            break
#Flush
if (not someonewon):
    for i in range( len(computers)):
        cpu = computers[i]
        flushdict = cpu.dictionary
        flushsuits = list(flushdict.values()).sort()
        count = 0
        for i in range(len(flashsuits)):
            if i == 0:
                count = 1
                continue
            else:
                if (flashsuits[i] == flashsuits[i-1]):
                    count+=1
                    if (count >= 5):
                        print("Computer", i +1, "won.")
                        someonewon = True
                        break
                else:
                    count = 0	
                        
#Straight
if (not someonewon):
    for i in range( len(computers)):
        cpu = computers[i]
        straightdict = cpu.dictionary
        straightkeys = list(straightdict.values()).sort()
        count = 0
        for i in range(len(straightkeys)):
            if i == 0:
                count = 1
                continue
            else:
                if (straightkeys[i] == straightkeys[i-1]+1):
                    count+=1
                    if (count >= 5):
                        if (i < len(computers)-1):
                            print("Computer", i+1, "won.")
                        else:
                            print("You Won!!!!")
                        someonewon = True
                        break
                else:
                    count = 0
#Three of a kind
if (not someonewon):
    for i in range( len(computers)):
        cpu = computers[i]
        foakcards = list(cpu.dictionary.keys()).sort()
        count = 0
        maxcount = 0;
        for i in range(len(foakcards)):
            if i == 0:
                count = 1
                maxcount = count
                continue
            if foakcards[i] == foakcards[i-1]:
                count+=1
                if count > maxcount:
                    maxcount = count
            else:
                count = 0
        if (maxcount == 3):
            if (i < len(computers)-1):
                print("Computer", i+1, "won.")
            else:
                print("You Won!!!!")
            someonewon = True
            break
#one pair
if (not someonewon):
    for i in range( len(computers)):
        cpu = computers[i]
        foakcards = list(cpu.dictionary.keys()).sort()
        count = 0;
        maxcount = 0;
        for i in range(len(foakcards)):
            if i == 0:
                count = 1
                maxcount = count
                continue
            if foakcards[i] == foakcards[i-1]:
                count+=1
                if count > maxcount:
                    maxcount = count
            else:
                count = 0
        if (maxcount == 2):
            if (i < len(computers)-1):
                print("Computer", i+1, "won.")
            else:
                print("You Won!!!!")
            someonewon = True
            break
'''