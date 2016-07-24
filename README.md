# trellofunnel
This is a simple python class which is using to filter out cards by different keys, the data source is exported JSON from Trello.


|function name               | description                        |
-----------------------------|------------------------------------|
|viewCardsByKeys([keys])     | Get valuse for remaining cards       |
|cardsFilterByClosed(boolean)| Filter out closed cards            |
|cardsFilterByLastUpdateDate(int) | Filter out update dated over n days|
|cardsFilterByList(idList)   | Filter by ID of List               | 
|cardsFilterByLabels         | Filter by labels (TBD)             |
|cardsFilterByMembers        | Filter by members (TBD)            |


# Usage example
Use local file /tmp/trello.json
```
>>> from trellofunnel import trellofunnel
>>> o = trellofunnel(file = '/tmp/trello.json')
>>> o.cardsFilterByClosed()
>>> o.cardsFilterByLastUpdateDate(7)
>>> print o.viewCardsByKeys(['idList', 'labels', 'name'])

	ToDo 	[Dev]	Improve the flow
	Doing 	[Ops]	Switch account
	Done 	[Server]	Upgrade package
```

Download JSON from Trello
```
>>> from trellofunnel import trellofunnel
>>> o = trellofunnel(url= 'https://trello.com/b/ruxunrrp.json', user = 'UserAccount', password = 'P@SSw0rd')
>>> o.cardsFilterByClosed()
>>> o.cardsFilterByLastUpdateDate(7)
>>> print o.viewCardsByKeys(['idList', 'labels', 'name'])

    ToDo    [Dev]   Improve the flow
    Doing   [Ops]   Switch account
    Done    [Server]    Upgrade package
```