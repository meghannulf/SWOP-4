import requests
import urllib.parse
import argparse

#Example usage:
#python3 query.py -q "select distinct ?Concept where {[] a ?Concept} LIMIT 100"  -f "xml" -o "./out.txt"

parser = argparse.ArgumentParser(description="Python utility to query dbpedia")
parser.add_argument("--format", "-f", help="Format to receive results in", type=str, default="csv", choices=["xml","html","csv","json"])
parser.add_argument("--query", "-q", help="Query to send to dbpedia", type=str, default=None, required=True)
parser.add_argument("--outfile", "-o", help="Path to make the output file", type=str, default=None, required=True)

args = parser.parse_args()


def doQuery(query, format, outfile):
	safeQueryString = urllib.parse.quote_plus(query)
	if format == "json":
		format = "application%2Fsparql-results%2Bjson"
	else:
		format = "text%2F" + format
	res = requests.get("https://dbpedia.org/sparql/?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=" + safeQueryString + "&format=" + format + "&timeout=30000")
	file = open(outfile, "w")
	file.write(res.content.decode("utf-8"))
	file.close()


doQuery(args.query, args.format, args.outfile)
