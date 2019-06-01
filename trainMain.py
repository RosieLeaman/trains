# the command needed for script is /Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import sys
import traceback

import pygame
import random
import math

windowSizeX = 800
windowSizeY = 500

pygame.init()
window = pygame.display.set_mode((windowSizeX,windowSizeY))

pygame.display.set_caption('Train excitement')

screen = pygame.display.get_surface()
font = pygame.font.SysFont('courier',15,True)

# some other variables
edgeX = 50
edgeY = 50
detailsWidth = 300
worldRect = pygame.Rect(edgeX,edgeY,windowSizeX-2*edgeX-detailsWidth,windowSizeY-2*edgeY)
detailsRect = pygame.Rect(worldRect.topright[0] + edgeX,worldRect.topright[1],detailsWidth,windowSizeY-2*edgeY)

# text display functions

# THIS MUST BE PASSED A STRING FOR TEXT IT DOES NOT CHECK
def drawText(screen,font,text,pos,colour):
    a = font.render(text,True,colour)
    screen.blit(a,pos)

def breakTextIntoPieces(text,font,maxWidth):
    # breaks text into pieces that will fit inside maxWidth for displaying
    size = font.size(text)
    numChars = len(text)

    pieces = ['']

    # split the text into words
    words = text.split()

    totalLen = 0
    currentPiece = 0

    if len(words) == 0:
        return []

    pieces[0] = words[0]

    for i in words[1:]:
        # before we add the next word
        proposedNext = pieces[currentPiece]+' '+i
        nextSize = font.size(proposedNext)

        if nextSize[0] > maxWidth:
            # the proposed addition is too long. Shift to next line.
            currentPiece = currentPiece + 1
            pieces.append(i)
            size = font.size(pieces[currentPiece])

            totalLen = totalLen + size[0]

        else:
            # the proposed addition will fit
            totalLen = nextSize[0]
            pieces[currentPiece] = proposedNext

    return pieces

def drawLongText(text,screen,font,pos,maxWidth,lineHeight):
    textPieces = breakTextIntoPieces(text,font,maxWidth)
    newPos = pos
    for i in textPieces:
        drawText(screen,font,i,newPos,(0,0,0))
        newPos = (newPos[0],newPos[1] + lineHeight)

    return newPos # return the final position so we can place later text appropriately

boyNames = ['Andy','Andrew','Albert','Alex','Alexander','Arthur','Anthony','Ant',
            'Bob','Brian','Brennan','Brendan','Bart','Bartholomew','Bertie',
            'Chris','Christopher','Colin','Charles','Charlie','Connor','Carl','Christian',
            'David','Dave','Darren','Drew','Dom','Dominic','Dennis',
            'Edgar','Ewan','Earl','Edward','Eddie',
            'Francis','Frank','Fred','Frederic',
            'Greg','Gary','Gazza','George',
            'Harry','Harold','Horace','Henry','Howard',
            'Ian','Ivan',
            'Jason','Justin','John','Jon','Josh','Joshua','Jim','Jerry',
            'Kenneth','Ken','Karl','Kieran',
            'Louis','Lewis','Liam','Leo','Luke','Laurence','Larry','Les',
            'Mike','Michael','Mark','Malcolm','Mo','Max',
            'Nathan','Nicholas','Nick','Norman','Navid',
            'Oscar','Oli','Ollie','Oliver','Owen',
            'Pete','Peter','Pedro','Paul','Patrick','Pat'
            'Quentin',
            'Robert','Richard','Rich','Rick','Robin','Ron','Ronald','Rowan',
            'Sam','Samuel','Sammy','Sebastian','Sebastien','Seamus','Simon','Stuart','Seb',
            'Thomas','Tom','Tommy','Timothy','Tim','Tristan','Tristram','Tony',
            'Ulysses',
            'Victor','Victoire','Vince','Vincent',
            'William','Will','Wes',
            'Xavier',
            'Yves',
            'Zack','Zachary','Zacharias']

girlNames = ['Andrea','Alison','Amy','Amelia','Arwen','Abigail','Abbie','Alice',
             'Barbara','Barb','Bethany','Bethan',
             'Chloe','Christel','Crystal','Carmen','Connie','Catherine','Cath',
             'Deirdre','Dorothy','Dot','Dottie','Denise',
             'Emily','Em','Emma','Emilia','Elsie','Elizabeth','Eleanor','Elinor','Ellen','Elena',
             'Frances','Florence','Flo','Flossie',
             'Gabrielle','Gabby','Georgina','Georgie','Greta','Gloria',
             'Hannah','Hannie','Hattie','Harriet','Helen','Helena','Hazel','Hortense','Henrietta',
             'Irene','Irena','Isabel','Isabella','Izzy','Issy',
             'Jenny','Jenna','Jen','Jemima',
             'Katherine','Kath','Kathy','Kat','Krystal','Karen',
             'Lizzy','Lizzie','Louise','Lacey','Liz','Lauren','Laura',
             'Mirjam','Miriam','Marnie','Margaret','Meg','Maggie','Mags','Martha','Maisy','Molly','Millie','Millicent','Mildred',
             'Nicole','Nicola','Nicky','Naomi','Nellie','Nell',
             'Olive','Olave',
             'Penelope','Penny','Polly','Petunia','Poppy','Peggy',
             'Rosie','Ros','Rosalyn','Rosalind','Rose','Rosa','Roberta',
             'Sally','Susan','Sandy','Sandra','Shelley','Sophie','Soph','Stella','Sue',
             'Tessa','Teresa','Terese','Tracy','Tracey','Tina','Tory',
             'Vanessa','Victoria','Vicky',
             'Wilhelmina','Wanda',
             'Yvonne','Yvette',
             'Zara']

surnames = ['Anderson','Anders','Andrew','Andrews','Abbot','Abbott','Abbot','Abbotson','Atkinson',
            'Broughley','Briarley','Benson','Beshley','Bottley','Brown','Browett','Brindle','Burns','Baker','Ball','Brockes','Bennett','Bennet','Banner','Bradshaw',
            'Christian','Carlson','Carlsen','Colley','Chandler','Colin','Collins','Collinson','Cooper','Corbyn','Cobbold','Curry','Cohen','Creaghan','Chesney','Chester',
            'Derrick','Dobson','Dentley','Dent','Deightley','Downs','Dabner','Day','Deigh','Dodd','Doddson','Davies','Docker',
            'Edwinson','Edwardson','Elley','Ellinson','Ebb','Evans','Eggerton','Elliott',
            'Francis','Feltchley','Fauntley','Frimley','French','Ford','Furniss',
            'George','Garrison','Gaunt','Grey','Gray','Gordon','Gentle','Gentley','Greer','Gardener','Gardiner','Green','Goold','Gould','Granger','German','Greenslade','Greening','Godfrey',
            'Hooper','Harrison','Howard','Hoppit','Hacker','Horton','Hunt','Hunter','Hammond','Hancock','Hamilton','Hutton','Harryman','Hughes',
            'Ivanson','Inman',
            'Johnson','Jotter','Jute','Jordan','Jones','Joiner','Jack','Jackson','Jenson','Jenkins',
            'Karlsen','Karling','Karlin','Kooper','Kingson','King','Kerr',
            'Laurence','Larson','Lampard','Leaman','Leeman','Lehmann',
            'Malcolm','Martin','May','Mason','Miner','Moore',
            'North','Norton','Norman','Naylor',
            'Oatley','Oakley','Owens','Owen','O\'Connor','Oliver','O\'Reilly',
            'Phillips','Philips','Philson','Potter','Parker','Parkinson','Painter','Pinter','Primrose','Priest','Priestley','Patterson','Pence','Posner','Pitt','Pitts','Portman','Porter',
            'Quentin','Quilter','Quirrel',
            'Roberts','Robertson','Richards','Richardson','Rowan','Reader','Rendell','Reardon-Smith','Robinson','Rayner','Rainer','Renner','Rusbridger','Rawnsley','Rees','Rowson','Ryan','Rudd',
            'Stephenson','Stevenson','Stuart','Scuffell','Scollitt','Spencer','Stewart','Sabbagh','Scott','Slater',
            'Tebbs','Thomas','Thompson','Teller','Tellitt','Titheridge','Thorpe','Taylor',
            'Underson',
            'Varley',
            'Williamson','Williams','Walker','Watkins','Watkinson','Wyatt','Wellington','Weasley','West','Whorley','Wooldridge','Watson','Wiseman',
            'Yenley','Yateley','Young']

# town name bits

townNameExtraStarts = ['North','East','South','West',
                       'Great','Little','Greater',
                       'Old','New']

townNameEndsWeighted = ['ton','ton','ton','ton','ton','ton','ton','ton','ton','ton','ton','ton','ton',
                        'town','town','town',
                        'ham','ham','ham','ham','ham','ham','ham','ham','ham','ham','ham','ham',
                        'ley','ley','ley','ley','ley','ley','ley','ley','ley','ley',
                        'leigh','leigh','leigh','leigh','leigh','leigh',
                        'lay','lay','lay','lay','lay','lay','lay',
                        'er','er','er','er',
                        'chester','chester','chester','chester',
                        'burgh','burgh','burgh','burgh',
                        'ber','ber','ber','ber','ber',
                        'bury','bury','bury','bury',
                        'den','den',
                        'bley',
                        'sham',
                        'run',
                        'brough','brough',
                        'top','top',
                        'ten',
                        'low','low','low','low',
                        'tor','tor',
                        'lea','lea',
                        'ville',
                        'hamble',
                        'burg',
                        'borough','borough','borough','borough',
                        'field','field','field','field','field','field','field',
                        'fell','fell','fell',
                        'wood','wood','wood','wood','wood','wood','wood','wood',
                        'shor',
                        'shore','shore','shore',
                        'shot','shot','shot','shot',
                        'hampton','hampton','hampton',
                        'hill','hill','hill','hill','hill','hill','hill',
                        'cester','cester','cester','cester',
                        'church','church','church','church',
                        'bridge','bridge','bridge','bridge','bridge',
                        'ford','ford','ford','ford','ford',
                        'forth','forth','forth',
                        'wark','wark',
                        'worth','worth','worth',
                        'fort',
                        'edge','edge','edge',
                        'port','port','port',
                        'ness','ness','ness',
                        'pool','pool','pool','pool','pool',
                        'stoke',
                        'cave','cave']

townNameStarts = ['Act','Ad','Af','Ag','Ail','Ain','Al','All','Ald','Am','An','Ap','Ar','Art','As','At','Att','Arn',
                  'Bad','Back','Bag','Ban','Bat','Bran','Bed','Beg','Bel','Ben','Ber','Best','Bet','Bin','Big','Bit','Bog','Bon','Bot','Bott','Bud','Bug','Bun','Butt','But','Bur',
                  'Castle','Cad','Cag','Cal','Call','Cam','Can','Cap','Car','Cas','Cat','Cave','Cor','Cran','Corn','Com','Cosh','Cust','Church','Chur','Chor','Chatt','Chat','Chin','Cran','Craw','Crow',
                  'Dab','Den','Del','Don','Dun','Dell','Dent',
                  'En','Ell','El','Em','Edg','Egg','Eg','End','Ent',
                  'Far','Farm','Farn','Fen','Fenn','Fern','Frim','Flash','Fast','Fett',
                  'Gor','Gon','Gunn','Gun','Gen','Garth','Got','Gott','Gut',
                  'Ham','Har','Hen','Han','Hor','Hors','Hat','Hath','Hutt',
                  'In','Inn','Ir','Ith',
                  'Jack','Jar',
                  'King','Kin','Kis','Ken','Ker','Kerr','Knut','Kirk',
                  'Leam','Len','Lem','Lon','Lun','Lud','Low','Lell','Len','Lesh',
                  'Mid','Mud','Mun','Mis','Mist','Must','Mount','Mumm','Ming','Man','Main','Mat','Map'
                  'Narn','Nor','Nan','Nus','Nes','Nur','Nutt','Not','Nat',
                  'On','Or','Os','Ost','Out',
                  'Pun','Penn','Pin','Pip','Pup','Pell','Peg','Pag','Pad','Pat','Path',
                  'Quen','Quin',
                  'Rus','Red','Run','Rel','Rough','Ren','Rash','Rast','Ret','Rat','Rit',
                  'Shrew','Shell','Sel','South','Shaf','Ship','Sten','Set','Sat',
                  'Tan','Tun','Ton','Taun','Taunt','Trent','Tent','Turn','Tom','Teff','Test','Tesh','Tat',
                  'Ven','Van','Vin',
                  'Wen','Wilm','Won','Wans',
                  'Yard','Yor','Yar','Yarn','Yen','Yat']

townNameMiddles = ['an','al','all','aller','am','aigh','ang','alm',
                   'er','en','ee','eigh',
                   'ie','in','ing','igh',
                   'on','out',
                   'un',
                   'cas','cash',
                   'don','dun','deigh',
                   'ee','eth','edge',
                   'fer','fur','fern','fen','figh',
                   'get',
                   'high','hot',
                   'ker','kerr','kes','kel',
                   'mar','marn','mon','min','mun','men','mes',
                   'nan','nun','non','nonner','ning',
                   'per','pert','port','por','pun','pin','pen','ping','pang','paing',
                   'ren','run','ring','rug','rough',
                   'top','topper','tupper','tup','tip','tiller','ter',
                   'son','sur','ser','sir','stil','sten','stan',
                   'wen','win','win','wan']

riverNames = ['Alder','Arn','Allwater',
              'Burnswater',
              'Ere','Ell','Ellstream',
              'Forth','Forswater',
              'Gee','Gure','Garn',
              'Howe','Haw',
              'Ille','Irley','Iser',
              'Kerrswater',
              'Lee','Loo','Lurn','Lell','Lightwater','Lack',
              'Mum','Murn','Morsley','Murkwater','Mill','Malwater',
              'Nouse','Nen',
              'Ouse','Ort','Orble',
              'Pell','Plie','Porl',
              'Rue','Ree','Reff','Runn',
              'Sten','Stor',
              'Thames','Tees','Trent','Tell',
              'Use','Ure',
              'Vail','Vornt',
              'Wye','Waye','Went',
              'Yellowater','Yarl']

def convertMinToHourMin(time):
    hour = str(int(time/60))
    min = str(time % 60)

    if time % 60 < 10:
        min = '0'+min

    time = hour + ':' + min

    return time

def makeRandomTownName():
    townName = ''
    a = random.random()
    b = random.random()

    if a < 0.15:
        # we add an adjective
        townName = townName + random.choice(townNameExtraStarts) + ' '

    if b <= 0.3:
        # a beginning and an end
        beginning = random.choice(townNameStarts)
        end = random.choice(townNameEndsWeighted)
        if end[0] == beginning[-1]:
            end = end[1:]
        newPart = beginning + end
        townName = townName + newPart

    elif b > 0.3 and b <= 0.45:
        # a beginning a middle and an end
        beginning = random.choice(townNameStarts)
        middle = random.choice(townNameMiddles)
        if middle[0] == beginning[-1]:
            middle = middle[1:]
        end = random.choice(townNameEndsWeighted)
        if end[0] == middle[-1]:
            end = end[1:]
        newPart = beginning + middle + end
        if len(newPart) > 12:
            newPart = middle + end
            newPart = newPart.capitalize()

        townName = townName + newPart

    elif b > 0.45 and b <= 0.65:
        # a beginning and a middle
        beginning = random.choice(townNameStarts)
        middle = random.choice(townNameMiddles)
        if middle[0] == beginning[-1]:
            middle = middle[1:]
        newPart = beginning + middle

        townName = townName + newPart

    else:
        # a middle and an end
        middle = random.choice(townNameMiddles)
        end = random.choice(townNameEndsWeighted)
        if end[0] == middle[-1]:
            end = end[1:]
        newPart = middle + end
        newPart = newPart.capitalize()

        townName = townName + newPart

    if a >= 0.92:
        # it gets an on river
        townName = townName + ' on ' + random.choice(riverNames)

    return townName

# we need to produce some towns
class Town():
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size # in 1000s
        if self.size <= 100:
            self.displaySize = 6
        elif self.size <= 600:
            self.displaySize = 10
        else:
            self.displaySize = 14

        self.connections = []

        self.name = makeRandomTownName()

        self.rect = pygame.Rect(self.x-self.displaySize,self.y-self.displaySize,2*self.displaySize,2*self.displaySize)

        self.visitingServices = []

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if other == None:
            return False
        return (self.x, self.y) == (other.x, other.y)

    def displaySelf(self,screen):
        pygame.draw.circle(screen,(200,50,0),(self.x,self.y),self.displaySize,0)
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.displaySize,1)

    def displaySelfHighlighted(self,screen,colour):
        pygame.draw.circle(screen,colour,(self.x,self.y),self.displaySize,0)
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.displaySize,1)

    def displayDetails(self,screen,font,pos):
        drawText(screen,font,self.name,pos,(0,0,0))

        sizeText = 'Size: {}'.format(self.size)
        drawText(screen,font,sizeText,(pos[0],pos[1]+30),(0,0,0))

    def displayRoutes(self,screen):
        for i in self.connections:
            pygame.draw.line(screen,(0,0,0),(self.x,self.y),(i.x,i.y),2)

    def isNot(self,otherTown):
        if self.x != otherTown.x and self.y != otherTown.y:
            return True
        else:
            return False

    def isConnectedTo(self,otherTown):
        if otherTown in self.connections:
            return True
        else:
            return False

    def findRouteTo(self,otherTown,townList,useDistance):
        # doin a kinda dijkstra
        unvisitedTowns = list(townList)

        dists = {}
        prevs = {}
        for i in unvisitedTowns:
            prevs[i] = None
            if i != self:
                dists[i] = 10000000
            else:
                dists[i] = 0

        while len(unvisitedTowns) > 0:
            # we find the town with the smallest distance
            minDist = 100000000
            minTown = None
            for i in unvisitedTowns:
                if dists[i] < minDist:
                    minTown = i
                    minDist = dists[i]

            for i in minTown.connections:
                if i in unvisitedTowns:
                    # we have not decided this one yet so see if we have a better
                    if useDistance == False:
                        # if we just care about connectedness
                        prospectiveDist = dists[minTown] + 1
                    else:
                        # if we care about distance
                        distBetween = math.sqrt((minTown.x-i.x)**2 + (minTown.y-i.y)**2)
                        prospectiveDist = dists[minTown] + distBetween

                    if prospectiveDist < dists[i]:
                        dists[i] = prospectiveDist
                        prevs[i] = minTown

            unvisitedTowns.remove(minTown)
            if minTown == otherTown:
                break

        if prevs[otherTown] != None:
            route = [otherTown]
            current = otherTown
            while self not in route:
                current = prevs[current]
                route.insert(0,current)

            return route
        else:
            return False

def plotADijkstra(townList,screen):
    choice1 = random.choice(townList)
    choice2 = random.choice(townList)

    route = choice1.findRouteTo(choice2,townList,True)

    if route != False:
        for i in range(0,len(route)-1):
            pygame.draw.line(screen,(255,0,0),(route[i].x,route[i].y),(route[i+1].x,route[i+1].y),2)

class Service():
    def __init__(self,route):
        self.route = route
        self.routePieceTimes = self.timesToNextStation()
        self.routeStartTimes = self.chooseStartTimes(self.route,self.routePieceTimes)

        self.routeReverse = list(route)
        self.routeReverse.reverse()
        self.routePieceTimesReverse = self.timesToNextStation()
        self.routeStartTimesReverse = self.chooseStartTimes(self.routeReverse,self.routePieceTimesReverse)

        # attach this service to that station
        for i in route:
            i.visitingServices.append(self)

    def displaySelf(self,screen,colour):
        for i in range(0,len(self.route)-1):
            pygame.draw.line(screen,colour,(self.route[i].x,self.route[i].y),(self.route[i+1].x,self.route[i+1].y),2)

    def displayWrittenRoute(self,screen,font,pos,lineHeight):
        newPos = pos
        for i in range(0,len(self.route)):
            drawText(screen,font,self.route[i].name,newPos,(0,0,0))
            newPos = (newPos[0],newPos[1] + lineHeight)

    def displayWrittenRouteWithTimes(self,screen,font,pos,lineHeight):
        newPos = pos
        time = self.routeStartTimes[0]
        for i in range(0,len(self.route)):
            text = convertMinToHourMin(time) + '     ' + self.route[i].name
            if i < len(self.route)-1:
                time = time + self.routePieceTimes[i]

            drawText(screen,font,text,newPos,(0,0,0))
            newPos = (newPos[0],newPos[1] + lineHeight)

        return newPos

    def displayTrainDepartureTimes(self,stationIndex,reverseFlag,screen,font,pos,maxWidth,lineHeight):
        if reverseFlag == False:
            text = 'Trains depart {} at '.format(self.route[stationIndex].name)
            for i in self.routeStartTimes:
                text = text + convertMinToHourMin(i) + ', '
        else:
            text = 'Trains depart {} at '.format(self.routeReverse[stationIndex].name)
            for i in self.routeStartTimesReverse:
                text = text + convertMinToHourMin(i) + ', '

        drawLongText(text,screen,font,pos,maxWidth,lineHeight)
        pass

    def getRemainingRouteFrom(self,town):
        remainingRoute = []
        startAdding = False
        for i in self.route:
            if startAdding == True:
                remainingRoute.append(i)
            if i == town:
                startAdding = True

        return remainingRoute

    def getRemainingRouteFromReverse(self,town):
        remainingRoute = []
        startAdding = False
        for i in self.routeReverse:
            if startAdding == True:
                remainingRoute.append(i)
            if i == town:
                startAdding = True

        return remainingRoute

    def getRouteUpTo(self,town):
        routeUpTo = []
        for i in self.route:
            routeUpTo.append(i)
            if i == town:
                break
        return routeUpTo

    def getRouteUpToReverse(self,town):
        routeUpTo = []
        for i in self.routeReverse:
            routeUpTo.append(i)
            if i == town:
                break
        return routeUpTo

    def timesToNextStation(self):
        times = [0 for x in range(0,len(self.route)-1)]
        # time is based on distance.
        for i in range(0,len(times)):
            dist = math.sqrt((self.route[i].x - self.route[i+1].x)**2 + (self.route[i].y - self.route[i+1].y)**2)
            times[i] = int(0.5*dist)

        return times

    def getTimeBetweenStations(self,station1,station2):
        # note that these must be ordered correctly.
        time = 0
        counting = False
        for i in range(0,len(self.route)-1):
            if counting == True:
                time = time + self.routePieceTimes[i]

            if self.route[i] == station1:
                counting = True
            if self.route[i] == station2:
                break

        return time

    def getTimeBetweenStationsReverse(self,station1,station2):
        # note that these must be ordered correctly.
        time = 0
        counting = False
        for i in range(0,len(self.routeReverse)-1):
            if counting == True:
                time = time + self.routePieceTimesReverse[i]

            if self.routeReverse[i] == station1:
                counting = True
            if self.routeReverse[i] == station2:
                break

        return time

    def chooseStartTimes(self,route,routePieceTimes):
        totalRouteTime = 0
        for i in routePieceTimes:
            totalRouteTime = totalRouteTime + i

        # choose starting time
        if route[0].size < 300:
            firstTrainTime = random.randint(400,500)
        else:
            firstTrainTime = random.randint(300,450)

        # choose ending time
        if route[0].size < 300:
            endTrainTime = random.randint(1260,1380)
        else:
            endTrainTime = random.randint(1350,1440)

        # work out how many trains we have per day

        numTrainsPerDay = int((endTrainTime-firstTrainTime-totalRouteTime)/60)

        startTimes = [firstTrainTime + 60*i for i in range(0,numTrainsPerDay)]

        return startTimes

class Passenger():
    def __init__(self,townList):
        a = random.random()
        if a < 0.5:
            self.name = random.choice(boyNames)
        else:
            self.name = random.choice(girlNames)
        self.surname = random.choice(surnames)

        self.homeTown = random.choice(townList)

        possibleDestinations = list(townList)
        possibleDestinations.remove(self.homeTown)
        self.destination = random.choice(possibleDestinations)

        print('got to find a service for this passenger')
        b = self.findServicesTaken()
        if b == False:
            self.identifiedService = False
            print('oops')
        else:
            self.identifiedService = True

        self.opinion = random.random()

    def findServicesTaken(self):
        # first see if there is a direct service from where we want to go from to destination
        print('--- finding service ---')
        print('Going from {} to {}'.format(self.homeTown.name,self.destination.name))
        print('Available services at {} are:'.format(self.homeTown.name))
        count = 0

        for service in self.homeTown.visitingServices:
            # first check one way on route
            print('--- Service {} ---'.format(count))
            count = count + 1

            remainingRoute = service.getRemainingRouteFrom(self.homeTown)


            if self.destination in remainingRoute:
                self.serviceTaken = [service]
                self.wayStations = [self.homeTown, self.destination]

                serviceTime = random.choice(service.routeStartTimes)

                serviceTime = serviceTime + service.getTimeBetweenStations(service.route[0],self.homeTown)

                endTime = serviceTime + service.getTimeBetweenStations(self.homeTown,self.destination)

                self.stationTimes = [serviceTime,endTime]

                return True

            # then check the other
            remainingRoute = service.getRemainingRouteFromReverse(self.homeTown)

            if self.destination in remainingRoute:
                self.serviceTaken = [service]
                self.wayStations = [self.homeTown, self.destination]

                serviceTime = random.choice(service.routeStartTimesReverse)

                serviceTime = serviceTime + service.getTimeBetweenStationsReverse(service.route[0],self.homeTown)

                endTime = serviceTime + service.getTimeBetweenStationsReverse(self.homeTown,self.destination)

                self.stationTimes = [serviceTime,endTime]

                return True

        print('--- No direct connection found ---')
        # what if we didnt find one?? We will have to change.
        for service in self.homeTown.visitingServices:
            remainingRoute = service.getRemainingRouteFrom(self.homeTown)
            for town in remainingRoute:
                print('---')
                print('Trying to see if we can find a route from {} to {}'.format(town.name,self.destination.name))
                print('Available services at {} are:'.format(town.name))
                count = 0
                for service2 in town.visitingServices:
                    print('--- Service {} ---'.format(count))
                    count = count + 1

                    remainingRoute = service2.getRemainingRouteFrom(town)

                    if self.destination in remainingRoute:
                        self.serviceTaken = [service,service2]
                        self.wayStations = [self.homeTown,town,self.destination]

                        serviceTime = random.choice(service.routeStartTimes[0:3])
                        serviceTime = serviceTime + service.getTimeBetweenStations(service.route[0],self.homeTown)

                        arrivalIntermediate = serviceTime + service.getTimeBetweenStations(self.homeTown,town)

                        # get the time at the intermediate station
                        for i in range(0,len(service2.route)):
                            timeAtIntermediate = service2.routeStartTimes[i] + service2.getTimeBetweenStations(service2.route[0],town)
                            if timeAtIntermediate > arrivalIntermediate:
                                break

                        timeAtEnd = timeAtIntermediate + service2.getTimeBetweenStations(town,self.destination)

                        self.stationTimes = [serviceTime, arrivalIntermediate , timeAtEnd]

                        return True
                    # and check reverse
                    remainingRoute = service2.getRemainingRouteFromReverse(town)
                    print(' reversed ')
                    for j in service2.routeReverse:
                        print(j.name)

                    print('The route from {} is '.format(town.name))
                    for j in remainingRoute:
                        print(j.name)


                    if self.destination in remainingRoute:
                        self.serviceTaken = [service,service2]
                        self.wayStations = [self.homeTown,town,self.destination]

                        serviceTime = random.choice(service.routeStartTimesReverse[0:3])
                        serviceTime = serviceTime + service.getTimeBetweenStationsReverse(service.route[0],self.homeTown)

                        arrivalIntermediate = serviceTime + service.getTimeBetweenStationsReverse(self.homeTown,town)

                        # get the time at the intermediate station
                        for i in range(0,len(service2.route)):
                            timeAtIntermediate = service2.routeStartTimes[i] + service2.getTimeBetweenStationsReverse(service2.route[0],town)
                            if timeAtIntermediate > arrivalIntermediate:
                                break

                        timeAtEnd = timeAtIntermediate + service2.getTimeBetweenStationsReverse(town,self.destination)

                        self.stationTimes = [serviceTime, arrivalIntermediate , timeAtEnd]

                        return True

            # check the other way too
            remainingRoute = service.getRemainingRouteFromReverse(self.homeTown)
            for town in remainingRoute:
                for service2 in town.visitingServices:
                    remainingRoute = service.getRemainingRouteFrom(town)
                    if self.destination in remainingRoute:
                        self.serviceTaken = [service,service2]
                        self.wayStations = [self.homeTown,town,self.destination]

                        serviceTime = random.choice(service.routeStartTimes[0:3])
                        serviceTime = serviceTime + service.getTimeBetweenStations(service.route[0],self.homeTown)

                        arrivalIntermediate = serviceTime + service.getTimeBetweenStations(self.homeTown,town)

                        # get the time at the intermediate station
                        for i in range(0,len(service2.route)):
                            timeAtIntermediate = service2.routeStartTimes[i] + service2.getTimeBetweenStations(service2.route[0],town)
                            if timeAtIntermediate > arrivalIntermediate:
                                break

                        timeAtEnd = timeAtIntermediate + service2.getTimeBetweenStations(town,self.destination)

                        self.stationTimes = [serviceTime, arrivalIntermediate , timeAtEnd]

                        return True
                    # and check reverse
                    remainingRoute = service.getRemainingRouteFromReverse(town)
                    if self.destination in remainingRoute:
                        self.serviceTaken = [service,service2]
                        self.wayStations = [self.homeTown,town,self.destination]

                        serviceTime = random.choice(service.routeStartTimesReverse[0:3])
                        serviceTime = serviceTime + service.getTimeBetweenStationsReverse(service.route[0],self.homeTown)

                        arrivalIntermediate = serviceTime + service.getTimeBetweenStationsReverse(self.homeTown,town)

                        # get the time at the intermediate station
                        for i in range(0,len(service2.route)):
                            timeAtIntermediate = service2.routeStartTimes[i] + service2.getTimeBetweenStationsReverse(service2.route[0],town)
                            if timeAtIntermediate > arrivalIntermediate:
                                break

                        timeAtEnd = timeAtIntermediate + service2.getTimeBetweenStationsReverse(town,self.destination)

                        self.stationTimes = [serviceTime, arrivalIntermediate , timeAtEnd]

                        return True

        return False

class View():
    def __init__(self,screen,font,worldRect,detailsRect):
        # things needed to display
        self.screen = screen
        self.font = font
        self.lineHeight = 30

        self.worldRect = worldRect
        self.detailsRect = detailsRect

        # town list
        self.townList = None

        # service list
        self.services = None

        # current display mode
        # showing town details
        self.townMode = False
        self.currentTown = None

        # displaying route to
        self.routeMode = False
        self.routeEnds = []
        self.route = []

        # displaying available  services
        self.serviceMode = False
        self.displayedService = None

        # displaying passengers
        self.passengerMode = False
        self.passenger = None

    def resetAllModeVariables(self):
        self.townMode = False
        self.currentTown = None

        self.routeMode = False
        self.routeEnds = []
        self.route = []

        self.serviceMode = False
        self.displayedService = None

        self.passengerMode = False
        self.passenger = None

    def displayView(self):
        screen.fill((200,255,255))

        for i in self.townList:
            i.displaySelf(self.screen)
            i.displayRoutes(self.screen)

        # if we have a current town, display its deets
        if self.townMode == True:
            if self.currentTown != None:
                self.currentTown.displayDetails(self.screen,self.font,self.detailsRect.topleft)

        if self.routeMode == True:
            if len(self.routeEnds) == 0:
                text = 'Choose start of route.'
                drawLongText(text,self.screen,self.font,self.detailsRect.topleft,self.detailsRect.width,self.lineHeight)
            elif len(self.routeEnds) == 1:
                text = 'Choose town to go to from {}.'.format(self.routeEnds[0].name)
                drawLongText(text,self.screen,self.font,self.detailsRect.topleft,self.detailsRect.width,self.lineHeight)
            else:
                # display the text version
                text = 'To go from {} to {}:'.format(self.route[0].name,self.route[-1].name)
                pos = drawLongText(text,self.screen,self.font,self.detailsRect.topleft,self.detailsRect.width,self.lineHeight)

                for i in range(0,len(self.route)):
                    drawText(self.screen,self.font,self.route[i].name,pos,(0,0,0))
                    pos = (pos[0],pos[1] + self.lineHeight)

                    if i < len(self.route)-1:
                        # and draw the route as well here since we loop over it anyway
                        pygame.draw.line(screen,(255,0,0),(self.route[i].x,self.route[i].y),(self.route[i+1].x,self.route[i+1].y),2)

        if self.serviceMode == True:
            self.services[self.displayedService].displaySelf(self.screen,(150,200,50))

            # also display written route
            currentPos = self.services[self.displayedService].displayWrittenRouteWithTimes(self.screen,self.font,self.detailsRect.topleft,self.lineHeight)

            # and display the times it departs initial station
            self.services[self.displayedService].displayTrainDepartureTimes(0,False,self.screen,self.font,currentPos,self.detailsRect.width,self.lineHeight)

        if self.passengerMode == True:
            if self.passenger.identifiedService == True:
                # draw the coloured circles
                town = self.passenger.wayStations[0]
                pygame.draw.circle(screen,(150,0,200),(town.x,town.y),town.displaySize,0)
                pygame.draw.circle(screen,(0,0,0),(town.x,town.y),town.displaySize,1)

                if len(self.passenger.wayStations) == 3:
                    town = self.passenger.wayStations[1]
                    pygame.draw.circle(screen,(0,200,0),(town.x,town.y),town.displaySize,0)
                    pygame.draw.circle(screen,(0,0,0),(town.x,town.y),town.displaySize,1)

                town = self.passenger.wayStations[-1]
                pygame.draw.circle(screen,(50,0,200),(town.x,town.y),town.displaySize,0)
                pygame.draw.circle(screen,(0,0,0),(town.x,town.y),town.displaySize,1)

                # draw the name
                drawText(self.screen,self.font,self.passenger.name+' '+self.passenger.surname,self.detailsRect.topleft,(0,0,0))

                text = 'Travelling from {} to {}.'.format(self.passenger.homeTown.name,self.passenger.destination.name)

                nextPos = (self.detailsRect.topleft[0],self.detailsRect.topleft[1]+self.lineHeight)

                nextPos = drawLongText(text,self.screen,self.font,nextPos,self.detailsRect.width,self.lineHeight)

                text = 'Caught the {} from {}.'.format(convertMinToHourMin(self.passenger.stationTimes[0]),self.passenger.homeTown.name)

                nextPos = drawLongText(text,self.screen,self.font,nextPos,self.detailsRect.width,self.lineHeight)

                if len(self.passenger.wayStations) == 3:
                    text = 'Changed at {} getting the {} to {}.'.format(self.passenger.wayStations[1].name,convertMinToHourMin(self.passenger.stationTimes[1]),self.passenger.serviceTaken[1].route[-1].name)
                    nextPos = drawLongText(text,self.screen,self.font,nextPos,self.detailsRect.width,self.lineHeight)

                text = 'Arrived at {} at {}.'.format(convertMinToHourMin(self.passenger.stationTimes[-1]),self.passenger.destination.name)

                nextPos = drawLongText(text,self.screen,self.font,nextPos,self.detailsRect.width,self.lineHeight)

                if self.passenger.opinion < 0.2:
                    text = 'Had a bad journey. The train they were going to catch was cancelled.'
                elif self.passenger.opinion < 0.8:
                    text = 'Has had an uneventful journey.'
                else:
                    text = 'Has had a good journey.'

                nextPos = drawLongText(text,self.screen,self.font,nextPos,self.detailsRect.width,self.lineHeight)

            else:
                text = 'Awks we couldnt find a route :('
                drawLongText(text,self.screen,self.font,self.detailsRect.topleft,self.detailsRect.width,self.lineHeight)




        pygame.display.flip()

    def makeNewWorld(self,numberTowns):
        # make up some towny bois
        self.townList = makeRandomTowns(10,worldRect.width,worldRect.height,edgeX,edgeY)

        # connect them together
        connectionList = makeAllConnectionsWeighted(self.townList)

        # add extra connections so that we can get places reasonably
        addConnectionsTooFarApart(self.townList,10)

        # get rid of unnecessary connections
        # we do three times, this has always been enough times in past
        reduceTooCloseConnections(self.townList,self.screen)
        reduceTooCloseConnections(self.townList,self.screen)
        reduceTooCloseConnections(self.townList,self.screen)

        # set current view to no view
        self.resetAllModeVariables()

        # add some services LOL
        self.services = makeServicesWeighted(self.townList)

    def switchMode(self,mode):
        if mode == 'town':
            self.resetAllModeVariables()
            self.townMode = True

        elif mode == 'route':
            self.resetAllModeVariables()
            self.routeMode = True

        elif mode == 'service':
            self.resetAllModeVariables()
            self.serviceMode = True
            self.displayedService = 0

        elif mode == 'passenger':
            self.resetAllModeVariables()
            self.passengerMode = True
            self.passenger = Passenger(self.townList)

    def displayTownDetails(self,town):
        self.currentTown = town

    def addToRoute(self,town):
        if len(self.routeEnds) == 0:
            self.routeEnds.append(town)

        elif len(self.routeEnds) == 1:
            self.routeEnds.append(town)
            self.makeRoute()

        else:
            self.routeEnds = [town]

    def makeRoute(self):
        self.route = self.routeEnds[0].findRouteTo(self.routeEnds[1],self.townList,True)

    def changeDisplayedService(self):
        self.displayedService = self.displayedService + 1
        if self.displayedService == len(self.services):
            self.displayedService = 0

        print(self.displayedService)

#####################

def makeRandomTowns(number,xWidth,yWidth,edgeX,edgeY):
    townList = []
    for i in range(0,number):
        tries = 0
        chosen = False
        while chosen == False:
            tries = tries + 1
            xLocation = random.randint(0,xWidth)+edgeX
            yLocation = random.randint(0,yWidth)+edgeY
            # size = random.randint(1,1000)
            size = makeWeightedSizeDistrbn()
            good = 1
            for j in townList:
                if abs(j.x - xLocation) < 24 or abs(j.y-yLocation) < 24:
                    good = 0
            if good == 1:
                chosen = True

        townList.append(Town(xLocation,yLocation,size))

    return townList

def makeWeightedSizeDistrbn():
    # a kinda power law distribution of towns?
    a = random.random()

    return int(999*((-1/3)*math.log(1-a)))+1

def makeTowns(xWidth,yWidth,edgeX,edgeY):
    world = [[random.randint(0,10) for x in range(0,xWidth)] for y in range(0,yWidth)]

    check = False
    count = 0
    while check == False and count <= 100:
        count = count + 1

        newWorld = [[0 for x in range(0,xWidth)] for y in range(0,yWidth)]

        for i in range(0,xWidth):
            for j in range(0,yWidth):
                pass

def makeSimpleConnections(townList):
    for town1 in townList:
        closest = None
        closestDist = windowSizeX*windowSizeX + windowSizeY*windowSizeY
        for town2 in townList:
            if town2 not in town1.connections:
                dist = (town2.x-town1.x)**2 + (town2.y-town1.y)**2
                if dist < closestDist:
                    closestDist = dist
                    closest = town2

        town1.connections.append(town2)
        town2.connections.append(town1)

    return connectionList

def makeSimpleConnectionsWeighted(townList):
    # order the list by size
    sortedTownList = sorted(townList, key=lambda x: x.size, reverse=True)

    for town1 in townList:
        closest = None
        closestDist = windowSizeX*windowSizeX + windowSizeY*windowSizeY
        for town2 in townList:
            if town2 != town1 and town2 not in town1.connections:
                dist = ((town2.x-town1.x)**2 + (town2.y-town1.y)**2)/(town2.size)
                if dist < closestDist:
                    closestDist = dist
                    closest = town2

        if closest != None:
            town1.connections.append(closest)
            closest.connections.append(town1)


def makeAllConnectionsWeighted(townList):

    makeSimpleConnectionsWeighted(townList)

    # order the list by size
    sortedTownList = sorted(townList, key=lambda x: x.size, reverse=True)

    for town1 in sortedTownList:
        if town1.size >= 100:
            closest = None
            closestDist = windowSizeX*windowSizeX + windowSizeY*windowSizeY
            for town2 in sortedTownList:
                if town2 != town1 and town2 not in town1.connections:
                    dist = ((town2.x-town1.x)**2 + (town2.y-town1.y)**2)/(town2.size**3)
                    if dist < closestDist:
                        route = town1.findRouteTo(town2,townList,False)
                        if route == False:
                            # there is not already a route. So we add
                            closestDist = dist
                            closest = town2


            if closest != None:
                town1.connections.append(closest)
                closest.connections.append(town1)

        if town1.size >= 600:
            # we get a third connection if really big
            closest = None
            closestDist = windowSizeX*windowSizeX + windowSizeY*windowSizeY
            for town2 in sortedTownList:
                if town2 != town1 and town2 not in town1.connections:
                    dist = ((town2.x-town1.x)**2 + (town2.y-town1.y)**2)/(town2.size)
                    if dist < closestDist:
                        route = town1.findRouteTo(town2,townList,False)
                        if route == False:
                            # there is not already a route. So we add
                            closestDist = dist
                            closest = town2

            if closest != None:
                town1.connections.append(closest)
                closest.connections.append(town1)


def reduceTooCloseConnections(townList,screen):
    for town1 in townList:
        for town2 in town1.connections:
            if town2 != town1:
                for nearbyTown in townList:
                    if nearbyTown != town1 and nearbyTown != town2:
                        distance = findDistPointToLine((nearbyTown.x,nearbyTown.y),(town1.x,town1.y),(town2.x,town2.y))
                        if distance != None and distance < 1000:
                            # this line is too close to this town. They should be friends
                            # print('trying to make friends')
                            # print('other town {} {}'.format(nearbyTown.x,nearbyTown.y))
                            #
                            # town1.displaySelfHighlighted(screen,(50,200,0))
                            # town2.displaySelfHighlighted(screen,(50,200,0))
                            # nearbyTown.displaySelfHighlighted(screen,(0,50,200))
                            # pygame.display.flip()

                            # are they already attached?
                            if nearbyTown not in town1.connections:
                                town1.connections.append(nearbyTown)
                                nearbyTown.connections.append(town1)
                            if nearbyTown not in town2.connections:
                                town2.connections.append(nearbyTown)
                                nearbyTown.connections.append(town2)

                            # remove the town1 town 2 connection
                            town1.connections.remove(town2)
                            town2.connections.remove(town1)
                            break

def findDistByRoute(town1,town2,townList):
    route = town1.findRouteTo(town2,townList,False)
    if route != False:
        distByRoute = 0
        for i in range(0,len(route)-1):
            distByRoute = distByRoute + (route[i].x-route[i+1].x)**2+ (route[i].y-route[i+1].y)**2

        return distByRoute
    else:
        return 1000000000

def findClosestPointOnLineTo(point,lineStartPoint,lineEndPoint):
    # see MATLAB code
    newStartPoint = (lineStartPoint[0]-lineEndPoint[0],lineStartPoint[1]-lineEndPoint[1])
    newPoint = (point[0]-lineEndPoint[0],point[1]-lineEndPoint[1])

    # calculate the alpha
    alpha = (newStartPoint[0]*newPoint[0]+newStartPoint[1]*newPoint[1])/(newStartPoint[0]*newStartPoint[0]+newStartPoint[1]*newStartPoint[1])

    # we only actually want it if the point
    nearestPoint = (alpha*newStartPoint[0],alpha*newStartPoint[1])
    nearestPoint = (nearestPoint[0]+lineEndPoint[0],nearestPoint[1]+lineEndPoint[1])

    return nearestPoint


def findDistPointToLine(point,lineStartPoint,lineEndPoint):

    nearestPoint = findClosestPointOnLineTo(point,lineStartPoint,lineEndPoint)

    smallestX = min([lineStartPoint[0],lineEndPoint[0]])
    biggestX = max([lineStartPoint[0],lineEndPoint[0]])
    smallestY = min([lineStartPoint[1],lineEndPoint[1]])
    biggestY = max([lineStartPoint[1],lineEndPoint[1]])

    if nearestPoint[0] > smallestX and nearestPoint[0] < biggestX:
        if nearestPoint[1] > smallestY and nearestPoint[1] < biggestY:
            dist = (nearestPoint[0] - point[0])**2 + (nearestPoint[1] - point[1])**2
        else:
            dist = None
    else:
        dist = None

    return dist

def addConnectionsTooFarApart(townList,limitTimesCrow):
    for town1 in townList:
        if town1.size > 100:
            for town2 in townList:
                if town1 != town2:
                    # find the route distance
                    distByRoute = findDistByRoute(town1,town2,townList)

                    # find crow flies distance

                    distByCrow = (town1.x-town2.x)**2+ (town1.y-town2.y)**2

                    if distByRoute > limitTimesCrow*distByCrow:
                        # add new route
                        town1.connections.append(town2)
                        town2.connections.append(town1)

def findTownConnectionWeightsSimple(town):
    townWeights = {}
    for i in town.connections:
        townWeights[i] = i.size

    return townWeights

def findTownConnectionWeightsDouble(town):
    townWeights = {}
    for i in town.connections:
        townWeights[i] = 2*i.size
        for j in i.connections:
            townWeights[i] = townWeights[i]+j.size

    return townWeights

def findNextTown(town):
    townWeights = findTownConnectionWeightsSimple(town)

    totalWeight = 0
    cutoffs = [0 for x in range(0,len(town.connections))]
    for i in range(0,len(town.connections)):
        totalWeight = totalWeight + townWeights[town.connections[i]]
        cutoffs[i] = totalWeight

    cutoffs = [cutoffs[j]/cutoffs[-1] for j in range(0,len(town.connections))]

    # roll a random number
    a = random.random()
    for i in range(0,len(cutoffs)):
        if a < cutoffs[i]:
            return town.connections[i]

    return None

def findNextTownWithBans(town,bannedTowns):
    townWeights = findTownConnectionWeightsDouble(town)

    totalWeight = 0
    cutoffs = [0 for x in range(0,len(town.connections))]
    for i in range(0,len(town.connections)):
        if town.connections[i] not in bannedTowns:
            totalWeight = totalWeight + townWeights[town.connections[i]]
        else:
            totalWeight = totalWeight
        cutoffs[i] = totalWeight

    cutoffs = [cutoffs[j]/cutoffs[-1] for j in range(0,len(town.connections))]

    # roll a random number
    a = random.random()
    for i in range(0,len(cutoffs)):
        if a < cutoffs[i]:
            return town.connections[i]

    return None

def makeNewServiceList(town):
    finished = False
    newService = [town]
    currentTown = town
    prevTown = None

    print('---')
    print('Starting from {}'.format(currentTown.name))
    print('---')
    while finished == False:
        # exteeeeend
        print('currently at {}'.format(currentTown.name))
        print('which has {} connections'.format(len(currentTown.connections)))
        if len(currentTown.connections) == 1:
            print('this is the first step')
            # first step
            nextTown = currentTown.connections[0]
            newService.append(nextTown)
            prevTown = currentTown
            currentTown = nextTown

            print('adding {}'.format(nextTown.name))

            # do we stop now?
            if len(nextTown.connections) == 1:
                # we stop if we reached end of line
                finished = True

        elif len(currentTown.connections) == 2:
            print('we only have one option')
            # if we only have one connection in and out, return the one that wasn't our previous
            if prevTown == currentTown.connections[0]:
                # in this case return index 1
                nextTown = currentTown.connections[1]
            else:
                # otherwise its the first index to return
                nextTown = currentTown.connections[0]

            newService.append(nextTown)
            prevTown = currentTown
            currentTown = nextTown

            print('adding {}'.format(nextTown.name))

            # do we stop now?
            if len(nextTown.connections) == 1:
                # we stop if we reached end of line
                finished = True

            # we also stop if we have done a circle
            if nextTown in newService[0:-1]:
                finished = True
        else:
            # if we have any other case we have multiple choices, and have a change of ending
            bannedTowns = [prevTown]
            #bannedTowns = newService[min(0,len(newService)-3):]
            nextTown = findNextTownWithBans(currentTown,newService)

            # if we have been previously we probs don't want to go again
            if nextTown in newService and len(nextTown.connections) <= 2:
                finished = True
            else:
                if nextTown != None:
                    newService.append(nextTown)
                    prevTown = currentTown
                    currentTown = nextTown

                    print('adding {}'.format(nextTown.name))

                    # do we stop now?
                    if len(nextTown.connections) == 1:
                        # we stop if we reached end of line
                        finished = True

                    # also flip if route too long. flip a coin
                    # bias based on size of current town??
                    a = random.random()
                    #if a < nextTown.size/1500:
                    if len(nextTown.connections) > 2 and a < 0.2:
                        finished = True
                else:
                    finished = True

        if len(newService) >= 6 and len(nextTown.connections) > 2:
            if nextTown in newService[0:-1]:
                print('Ending service at {}'.format(currentTown))
                print(len(newService))
                finished = True

    return newService

def makeServicesWeighted(townList):
    # copy the town list so we can delete
    dupeTownList = list(townList)

    serviceList = []

    # first we go through each town with only one entry
    miniTownList = [town for town in townList if len(town.connections) == 1]

    alreadyFinishedEnds = []

    for town in miniTownList:
        if town not in alreadyFinishedEnds:
            newService = makeNewServiceList(town)

            serviceList.append(Service(newService))

            alreadyFinishedEnds.append(town)
            if len(newService[-1].connections) == 1:
                alreadyFinishedEnds.append(newService[-1])

            # we delete so we know that we have at least one service that visits that town
            for i in newService:
                if i in dupeTownList:
                    dupeTownList.remove(i)


    # add a few more random routes. Say 2 more for now
    # for now just sort the list and use the two largest cities
    sortedTownList = sorted(townList, key=lambda x: x.size, reverse=True)

    for town in sortedTownList:
        currentNumRoutes = 0
        for service in serviceList:
            if town in service.route:
                currentNumRoutes = currentNumRoutes + 1

        routeNeeded = False
        if currentNumRoutes < 1 and town.size <= 100:
            # need a route to this town
            routeNeeded = True
        elif currentNumRoutes < 1 and town.size <= 600:
            routeNeeded = True
        elif currentNumRoutes < 2 and town.size <= 1000:
            routeNeeded = True

        if routeNeeded == True:
            # repeat the same but with a different start town
            newService = makeNewServiceList(town)

            serviceList.append(Service(newService))

    return serviceList

####################################

# MAIN LOOP
done = False
count = 0

ourView = View(screen,font,worldRect,detailsRect)

ourView.makeNewWorld(10)

try:
    while done == False:
        count = count + 1
        if count % 1000 == 0:
             ourView.displayView()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                print(event)
                if event.scancode == 36:
                    # enter key
                    # delete current town as we have new towns now
                    ourView.makeNewWorld(10)

                if event.scancode == 17:
                    # key t
                    ourView.switchMode('route')

                if event.scancode == 34:
                    # key i
                    ourView.switchMode('town')

                if event.scancode == 1:
                    # key s
                    ourView.switchMode('service')

                if event.scancode == 35:
                    # key p
                    ourView.switchMode('passenger')

                if event.scancode == 49:
                    # space bar
                    if ourView.serviceMode == True:
                        ourView.changeDisplayedService()

                    elif ourView.passengerMode == True:
                        ourView.passenger = Passenger(ourView.townList)

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.scancode == 53):
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in ourView.townList:
                    if i.rect.collidepoint(event.pos) == True:
                        # we have hit a town. What happens now depends on current mode
                        if ourView.townMode == True:
                            ourView.displayTownDetails(i)

                        if ourView.routeMode == True:
                            ourView.addToRoute(i)


except:
    print('Oops something went wrong')
    traceback.print_exc(file=sys.stdout)
    pygame.quit()
    done = True


pygame.quit()
