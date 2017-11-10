Algorithm for identifying locations in queries

tokens = tokenize(query)

matches = {}
for token in query:

	if( isCountry(token) == True ):
		matches[token] = 'Country'

	else if( isState(token) == True ):
		matches[token] = 'State'

	else if( isCity(token) == True ):
		matches[token] = 'City'

	else if( isPlace(token) == True ):
		matches[token] = 'Place'