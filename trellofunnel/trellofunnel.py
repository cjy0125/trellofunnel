# Library for parsing Trello json and filter out unwanted items
import ijson
import time
import datetime
import types

class trellofunnel():
    def __init__(self, file):
        self.file = file
        self.reload()

    def reload(self):
        with open(self.file) as f:
            obj = ijson.items(f, '')
            self.rawdata = list(obj)[0]
            self.members = self.rawdata.pop('members', None)
            self.cards = self.rawdata.pop('cards', None)
            self.labels = self.rawdata.pop('labels', None)
            self.lists = self.rawdata.pop('lists', None)
            self.normalizeDateLastActivity()
            self.updateListsMapping()
            self.updateLabelsMapping()

    def normalizeDateLastActivity(self):
        for i in range(len(self.cards)):
            self.cards[i]['dateLastActivity'] = self.timeToTimstamp(self.cards[i]['dateLastActivity'])

    def timeToTimstamp(self, timestr):
        return time.mktime(datetime.datetime.strptime(timestr[:19], "%Y-%m-%dT%H:%M:%S").timetuple())

    def viewCardsByKeys(self, keys):
        for i in range(len(self.cards)):
            output = ''
            for j in keys:
                if j == 'labels':
                    output = '{}\t'.format(output)
                    for k in range(len((self.cards[i][j]))):
                        output = '{}[{}]'.format(output, self.cards[i][j][k]['name'])
                elif j == 'idList':
                    output = '{}\t{}'.format(output, self.mapLists.get(self.cards[i][j]))
                else:
                    output = '{}\t{}'.format(output, self.cards[i][j])
            print output

    def cardsFilterByLabels(self, filter):
        pass

    def cardsFilterByMembers(self, filter):
        pass

    def cardsFilterByList(self, listId):
        for i in reversed(range(len(self.cards))):
            if self.cards[i]['idList'] != listId:
                self.cards.pop(i)

    def cardsFilterByClosed(self, boolean = False):
        for i in reversed(range(len(self.cards))):
            if self.cards[i]['closed'] != boolean:
                self.cards.pop(i)

    def cardsFilterByLastUpdateDate(self, days):
        # 86400 = 60*60*24 sec
        threshold = time.time() - days * 86400
        for i in reversed(range(len(self.cards))):
            if self.cards[i]['dateLastActivity'] < threshold:
                self.cards.pop(i)

    def updateListsMapping(self):
        self.mapLists = {}
        for i in self.lists:
            self.mapLists[i['id']] = i['name']

    def updateLabelsMapping(self):
        self.mapLabels = {}
        for i in self.labels:
            self.mapLabels[i['id']] = i['name']


