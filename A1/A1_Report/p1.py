def given():
	Given L,
	L = [div, span, p, h1, h2, h3, h4, title, a, strong, em, table,...]
	Procedure extractContent(HTML page P)
		G = extract all tags from P that is in L

		for tag t in G do
			if t has element then
				extractContent(t)
			else
				T.add(t.text content)
			endif
		endfor
	endProcedure