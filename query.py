import requests
import urllib.parse
import argparse

#Example usage:
#python3 query.py -q "select distinct ?Concept where {[] a ?Concept} LIMIT 100"  -f "xml" -o "./out.txt"

parser = argparse.ArgumentParser(description="Python utility to query dbpedia")
parser.add_argument("--format", "-f", help="Format to receive results in", type=str, default="csv", choices=["csv"])
parser.add_argument("--query", "-q", help="Query to send to dbpedia DO NOT INCLUDE LIMIT OR OFFSET", type=str, default=None, required=True)
parser.add_argument("--outfile", "-o", help="Path to make the output file", type=str, default=None, required=True)
parser.add_argument("--numQueries", "-n", help="Number of queries to send out (we get 10,000 results per query)",type=int, default=1)

args = parser.parse_args()


def doQuery(query, format, outfile):
	safeQueryString = urllib.parse.quote_plus(query)
	print("Executing query: " + query)
	if format == "json":
		format = "application%2Fsparql-results%2Bjson"
	else:
		format = "text%2F" + format
	res = requests.get("https://dbpedia.org/sparql/?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=" + safeQueryString + "&format=" + format + "&timeout=30000")
	file = open(outfile, "w")
	file.write(res.content.decode("utf-8"))
	file.close()


#do all queries
for q in range(args.numQueries):
	doQuery(args.query + " LIMIT 10000 OFFSET " + str(q * 10000), args.format, ".tmp" + str(q) + args.outfile)
	print("Executed query " + str(q+1) + " of " + str(args.numQueries))

outfile = open(args.outfile, "w")

#consolidate results
for q in range(args.numQueries):
	print("Preparing to consolidate file " + str(q+1) + " of " + str(args.numQueries))
	file = open(".tmp" + str(q) + args.outfile, "r")
	
	firstLine = True
	for line in file.readlines():
		if q == 0:
			outfile.write(line)
		if not firstLine:
			outfile.write(line)
		firstLine = False

	file.close()


outfile.close()
