# Library for parsing Trello json and filter out unwanted items
import json
import time
import datetime
import requests

class trellofunnel():
    """This is a simple python class to filter Trello cards by keys,
and the data source is an exported JSON from Trello.\n"""
    def __init__(self, **kwargs):
        if 'file' in kwargs:
            self.loadFromFile(kwargs.get('file'))
        else :
            self.loadFromTrello(kwargs)

    def __parseCards(self, strRawdata):
        self.rawdata = json.loads(strRawdata)
        self.members = self.rawdata.pop('members', None)
        self.cards = self.rawdata.pop('cards', None)
        self.labels = self.rawdata.pop('labels', None)
        self.lists = self.rawdata.pop('lists', None)
        self.__normalizeDateLastActivity()
        self.updateListsMapping()
        self.updateLabelsMapping()

    def __normalizeDateLastActivity(self):
        for i in range(len(self.cards)):
            self.cards[i]['dateLastActivity'] = self.__timeToTimstamp(self.cards[i]['dateLastActivity'])

    def __timeToTimstamp(self, timestr):
        return time.mktime(datetime.datetime.strptime(timestr[:19], "%Y-%m-%dT%H:%M:%S").timetuple())

    def getTrelloToken(self, user, password):
        r = requests.get('https://trello.com')
        dsc = r.cookies.get_dict()['dsc']

        payload = {'method': 'password', 'factors[user]': user, 'factors[password]': password}
        r = requests.post('https://trello.com/1/authentication', data = payload, cookies={'dsc':dsc})
        code = json.loads(r.text)['code']

        payload = {'dsc': dsc, 'authentication': code}
        r = requests.post('https://trello.com/1/authorization/session', data = payload, cookies={'dsc':dsc})
        cookies = r.cookies.get_dict()
        return cookies['token']

    def loadFromFile(self, file):
        """Load JSON from file\nArgs:\n\tfile (str) : file path"""
        with open(file) as f:
            self.__parseCards(f.read())

    def loadFromTrello(self, kwargs):
        """Load JSON from Trello online\nArgs:\n\tuser (str)\n\tpassword (str)\n\turl (str): JSON download path"""
        token = self.getTrelloToken(user = kwargs.get('user'), password = kwargs.get('password'))
        r = requests.get(url = kwargs.get('url'), cookies = {'token' : token})
        self.__parseCards(r.text)

    def viewCardsByKeys(self, keys):
        """Get the view of remaining cards\nArgs:\n\tkeys array(str) : fields what you want to show
Return:\n\tstr : a string for each fields of remaining cards"""
        result = ''
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
            result = '{}\n{}'.format(result, output)
        return result

    def cardsFilterByLabels(self, labels):
        """Filter cards by name of label\nArgs:\n\tlabels array(str): array of label names\n"""
        for i in reversed(range(len(self.cards))):
            dropFlag = True
            for label in self.cards[i]['labels']:
                if self.mapLabels[label['id']] in labels:
                    dropFlag = False
                    break
            if dropFlag == True:
                self.cards.pop(i)

    def cardsFilterByMembers(self, filter):
        """TBD"""
        pass

    def cardsFilterByList(self, listId):
        """Filter cards by ID of list\nArgs:\n\tlistId str : refer self.mapLists to get listId\n"""
        for i in reversed(range(len(self.cards))):
            if self.cards[i]['idList'] != listId:
                self.cards.pop(i)

    def cardsFilterByClosed(self, boolean = False):
        """Filter cards by closed flag, default would filter out closed cards.
Args:\n\tboolean (bool) : Flag only available for True/False\n"""
        for i in reversed(range(len(self.cards))):
            if self.cards[i]['closed'] != boolean:
                self.cards.pop(i)

    def cardsFilterByLastUpdateDate(self, days):
        """Filter cards by activate in recent n days\nArgs:\n\tdays (int) : number of days\n"""
        threshold = time.time() - days * 86400  # 86400 = 60*60*24 sec
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

if __name__ == '__main__':
    pass
