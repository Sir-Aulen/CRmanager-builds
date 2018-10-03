import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

###Static Variables###
CURR_VERS = 'v1'
settingsFile = 'UserPrefs'

battlesTop = '''-min-value="0" data-max-value="1" style="background-color: rgb(251, 244, 248);">0.44</td>
</tr>

'''
battlesBot = '<fthfoot style="display: table-footer-group; border-spacing:'
collectTop = '''ound-color: rgb(226, 240, 208);">1918</td>
</tr>

'''
collectData = '''
</td>
<td class="right aligned colorize" data-sort-value="'''

###Input Defs###
def TagInput(message):
    inp = input(message)

    if inp[0] == '#':
        return inp[1:]
    return inp
def IntInput(message):
    inp = input(message)

    if inp in DEBUG_COMMANDS:
        DebugCommands(inp)
        return
    
    x = True
    while x:
        try:
            inp = int(inp)
            break
        except ValueError:
            inp = input('Please enter a number: ')

    return inp
def FloatInput(message):
    inp = input(message)

    if inp in DEBUG_COMMANDS:
        DebugCommands(inp)
        return
    
    x = True
    while x:
        try:
            inp = float(inp)
            break
        except ValueError:
            inp = input('Please enter a number: ')
            
    return inp
DEBUG_COMMANDS = ['View Data', 'Delete Settings', 'View Settings']
def DebugCommands(inp):
    global dataList, settings
    
    if inp == 'View Data':
        print()
        print(dataList)
    if inp == 'Delete Settings':
        with open(settingsFile, 'w') as f:
            f.write('')
    if inp == 'View Settings':
        print()
        print(settings)
        
###Get Data###
dataList = []
def CheckData():
    global dataList
    
    driver = webdriver.Chrome()
    driver.get(settings[0])
    source = driver.find_element_by_id('page_content').get_attribute('innerHTML')
    driver.close()

    d_battles = source[source.find(battlesTop)+97:source.find(battlesBot)]
    d_collect = source[source.find(collectTop)+50:]

    currName = ''
    for i in range(len(d_battles)):                 #Get battle data
        if d_battles[i:i+11] == 'data-name="':
            ii = i + 11
            x = ''
            name = ''
            while x != '"':
                name += x
                x = d_battles[ii:ii+1]
                ii+=1
            dataList.append([name, 0, 0, 0, 0])    #[name, war wins, war attacks, win percentage, cards collected]
            currName = name
        if d_battles[i:i+14] == 'cw-war-win.png':
            for ii in dataList:
                if ii[0] == name:
                    ii[1] += 1
                    ii[2] += 1
        if d_battles[i:i+15] == 'cw-war-loss.png':
            for ii in dataList:
                if ii[0] == name:
                    ii[2] += 1                    

    for i in range(len(d_collect)):                 #Get Collection day data
        if d_collect[i:i+11] == 'data-name="':
            ii = i + 11
            x = ''
            name = ''
            while x != '"':
                name += x
                x = d_collect[ii:ii+1]
                ii+=1
            currName = name
        if d_collect[i:i+59] == collectData:
            ii = i + 59
            x = ''
            numb = ''
            while x != '"':
                numb += x
                x = d_collect[ii:ii+1]
                ii+=1
            for ii in dataList:
                if ii[0] == name:
                    ii[4] = float(numb)

    for i in range(len(dataList)):  #Set the percent of battles won for the data
        if (dataList[i][2] > 0):
            dataList[i][3] = dataList[i][1] / dataList[i][2] * 100
        else:
            dataList[i][3] = 0

###Get/Change Settings###
settings = [0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0]
link, m_battles, m_percent, m_collect, e_battles, e_percent, e_collect, useWins, usePercent, useCollect, showReasons, useBucket, b_battles, b_percent, b_collect = settings
def CheckSettings():
    global settings
    global link, m_battles, m_percent, m_collect, e_battles, e_percent, e_collect, b_battles, b_percent, b_collect
    global useWins, usePercent, useCollect, showReason, useBucket
    
    with open(settingsFile, 'a') as f:
        f.close()
    with open(settingsFile, 'r+') as f:
        file = f.read()
        if file == '':
            newFile = ''
            print('|---------------| Initial setup |---------------|')
            print()
            print('What is the tag of the clan you wish to check?')
            tag = TagInput('> ')
            print()
            print('Verifying the clan tag, please allow the program access to chrome')
            input('Press enter to continue')
            checked = False
            while (checked == False):
                link = 'https://royaleapi.com/clan/' + tag + '/war/analytics'
                driver = webdriver.Chrome()
                driver.get(link)
                source = driver.find_element_by_id('page_content').get_attribute('innerHTML')
                
                if ('Please verify that you have entered correctly and try again.') in source:
                    print()
                    print('That clan does not exist. Please enter a valid tag')
                    tag = TagInput('> ')
                else:
                    print()
                    print('***Link verified***')
                    settings[0] = link
                    checked = True
                driver.close()
            print()
            print('The following will deterimine the requirements for ranks in your clan, based on the last 10 wars. These can be changed at any time in the settings')
            print()
            settings[1] = IntInput('What is the minimum requirement for war wins for a member? ')
            settings[2] = FloatInput('What is the minimum requirement of cards collected for a member? ')
            settings[3] = IntInput('What is the minimum requirement for war wins for an elder? ')
            settings[4] = FloatInput('What is the minimum requirement of cards collected for an elder? ')
            settings[5] = True
            settings[7] = True
            print()
            
            SaveSettings()
        else:
            if file[:2] != CURR_VERS:
                if file[:2] == 'ht':
                    settings = file.split('~')

                    link = settings[0]
                    m_battles = int(settings[1])
                    m_collect = float(settings[2])
                    e_battles = int(settings[3])
                    e_collect = float(settings[4])
                                
                    file = 'v1' + str(link) + '~' + str(m_battles) + '~0~' + str(m_collect) + '~' + str(e_battles) + '~0~' + str(e_collect) + '~1~0~1~0~1~0~0~0'
                    f.write(file)

            file = file[2:]
            settings = file.split('~')

            link = settings[0]
            m_battles = int(settings[1])
            m_percent = int(settings[2])
            m_collect = float(settings[3])
            e_battles = int(settings[4])
            e_percent = int(settings[5])
            e_collect = float(settings[6])
            useWins = int(settings[7])
            usePercent = int(settings[8])
            useCollect = int(settings[9])
            useBucket = int(settings[10])
            showReasons = int(settings[11])
            b_battles = int(settings[12])
            b_percent = int(settings[13])
            b_collect = int(settings[14])
            
def ChangeSettings():
    global settings
    global link, m_battles, m_percent, m_collect, e_battles, e_percent, e_collect, b_battles, b_percent, b_collect
    global useWins, usePercent, useCollect, showReasons, useBucket
    
    x = True
    while x:    
        print('|---------------| Settings |---------------|')
        print()
        print('1: Change Clan Tag')
        print('2: Change Requirements')
        print('3: Change Requirement Categories')
        print('4: General Settings')
        print('5: Back')
        inp = int(input('> '))
        print()
        if inp == 5:
            SaveSettings()
            x = False
        elif inp == 1:
            tag = TagInput('What is the new tag? ')
            print()
            checked = False
            while (checked == False):
                link = 'https://royaleapi.com/clan/' + tag + '/war/analytics'
                driver = webdriver.Chrome()
                driver.get(link)
                source = driver.find_element_by_id('page_content').get_attribute('innerHTML')
                
                if ('Please verify that you have entered correctly and try again.') in source:
                    print()
                    print('That clan does not exist. Please enter a valid tag')
                    tag = TagInput('> ')
                else:
                    print()
                    print('***Link verified***')
                    print()
                    settings[0] = link
                    UpdateStatic()
                    checked = True
                driver.close()
        elif inp == 2:
            if useWins:
                print('Previous requirements for members to win ' + str(m_battles) + ' battles and for elders to win ' + str(e_battles) + ' battles')
                m_battles = IntInput('What is the new requirement for members? ')
                e_battles = IntInput('What is the new requirement for elders? ')
                print()
            if usePercent:
                print('Previous requirements for members were to win ' + str(m_percent) + '% of battles and for elders to win ' + str(e_percent) + '% of battles')
                m_percent = IntInput('What is the new requirement for members? ')
                e_percent = IntInput('What is the new requirement for elders? ')
            if useCollect:
                print('Previous requirements for members were to collect ' + str(m_collect) + ' cards and for elders to collect ' + str(e_collect) + ' cards')
                m_collect = IntInput('What is the new requirement for members? ')
                e_collect = IntInput('What is the new requirement for elders? ')
            print()
            SaveSettings()
        elif inp == 3:
            xx = True
            while xx:
                msg = 'Which do you want to change? People are currently being judged on: '
                if useWins:
                    msg += 'total war wins, '
                if usePercent:
                    msg += 'war win percentage, '
                if useCollect:
                    msg += 'total cards collected, '
                print(msg[:-2])
                print('1: Total war wins')
                print('2: War win percentage')
                print('3: Total cards collected')
                print('4: Back')
                inp = IntInput('> ')
                print()
                if inp == 1:
                    useWins = int(not(useWins))
                elif inp == 2:
                    usePercent = int(not(usePercent))
                elif inp == 3:
                    useCollect = int(not(useCollect))
                elif inp == 4:
                    SaveSettings()
                    xx = False
        elif inp == 4:
            xx = True
            while xx:
                print('General Settings:')
                print('1: Show reasons for rank placements (currently ' + str(bool(showReasons)) + ')')
                #print('2: Use ineligible members category - doesn\'t consider certain requirements (currently '  + str(bool(useBucket)) + ')')
                print('2: Back')
                inp = IntInput('> ')
                print()
                if inp == 2:
                    xx = False
                elif inp == 1:
                    showReasons = int(not(showReasons))
##                elif inp == 2:
##                    useBucket = int(not(useBucket))
def UpdateStatic():
    global settings
    global link, m_battles, m_percent, m_collect, e_battles, e_percent, e_collect, b_battles, b_percent, b_collect
    global useWins, usePercent, useCollect, showReasons, useBucket

    settings =[link, m_battles, m_percent, m_collect, e_battles, e_percent, e_collect, useWins, usePercent, useCollect, showReasons, useBucket, b_battles, b_percent, b_collect]

def SaveSettings():
    global settings

    UpdateStatic()
    with open(settingsFile, 'w') as f:
        newFile = CURR_VERS
        for i in settings:
            newFile += str(i) + '~'
        newFile = newFile[:-1]
        f.write(newFile)

###Check Data###
def CheckRanks():
    rankList = [[],[],[], []]   #0 = kick, 1 = member, 2 = elder, 3 = bucket
    for i in dataList:
        pos = []
        reasonList = []

        if useWins:
            add = 'kick'
            reason = 'won ' + str(i[1]) + ' battles'
            if i[1] > m_battles:
                add = 'member'
                if i[1] > e_battles:
                    add = 'elder'
            pos.append(add)
            reasonList.append(reason)
        if usePercent:
            add = 'kick'
            reason = 'won ' + "{:.2f}".format(i[3]) + '% of battles'
            if i[3] > m_percent:
                add = 'member'
                if i[3] > e_percent:
                    add = 'elder'
            pos.append(add)
            reasonList.append(reason)
        if useCollect:
            add = 'kick'
            reason = 'collected ' + str(i[4]) + ' cards'
            if i[4] > m_collect:
                add = 'member'
                if i[4] > e_collect:
                    add = 'elder'
            pos.append(add)
            reasonList.append(reason)
        kick = 0
        member = 0
        elder = 0
        for ii in pos:
            if ii == 'kick':
                kick += 1
            elif ii == 'member':
                member += 1
            elif ii == 'elder':
                elder += 1

        reasons = '('
        for ii in reasonList:
            reasons += ii + ', '
        reasons = reasons[:-2] + ')'
        
        if kick > 0:
            rankList[0].append([i[0], reasons])
        elif member > 0:
            rankList[1].append([i[0], reasons])
        elif elder > 0:
            rankList[2].append([i[0], reasons])                

    print('\n|---------------| kick the following |---------------|')
    for i in rankList[0]:
        print(i[0] + ' ' + i[1])
    print('\n\n|---------------| the following should be members |---------------|')
    for i in rankList[1]:
        print(i[0] + ' ' + i[1])
    print('\n\n|---------------| the following should be elders |---------------|')
    for i in rankList[2]:
        print(i[0] + ' ' + i[1])

###Run the program###
CheckSettings()
CheckData()
print('|---------------| Welcome to the CR Clan Manager |---------------|')
print()
while True:
    print ('What do you want to do?')
    print('1: Check Ranks')
    print('2: Settings')
    print('3: Credits')
    inp = IntInput('> ')
    print()
    if inp == 1:
        CheckRanks()
        print()
        input('enter to continue ')
        print()
    if inp == 2:
        ChangeSettings()
        print()
    if inp == 3:
        print('Created by Adam Gallina (aka Sir Aulen in CR) for caveman13, using Python3, Selenium, and Chromedriver.')
        print()
