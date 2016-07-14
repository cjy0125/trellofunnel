# trellofunnel
This is a sample class which using to filter out cards by different keys, the data source is exported JSON from Trello.



|function name               | description                        |
-----------------------------|------------------------------------|
|viewCardsByKeys([key])      | Get valuse for remaining cards       |
|cardsFilterByClosed(boolean)| Filter out closed cards            |
|cardsFilterByLastUpdateDate(int) | Filter out update dated over n days|
|cardsFilterByList(idList)   | Filter by ID of List               | 
|cardsFilterByLabels         | Filter by labels (TBD)             |
|cardsFilterByMembers        | Filter by members (TBD)            |


# Sample Usage
```
>>> from trellofunnel import trellofunnel
>>> o = trellofunnel.trellofunnel('/tmp/trello.json')
>>> o.cardsFilterByClosed()
>>> o.cardsFilterByLastUpdateDate(7)
>>> print o.viewCardsByKeys(['idList', 'labels', 'name'])

	ToDo 	  [Dev]	Improve the flow
	Doing 	[Ops]	Switch account
	Done 	  [Server]	Upgrade package
```
