from coinbase.wallet.client import Client
import requests

def get_info(market, p):
	res={}
	market=market.lower()
	pair=p
	
	print "Load pair %s for %s" % (market, p)
	
	if market=='wex':
		r = requests.get('https://wex.nz/api/3/ticker/%s'% pair)
		res=r.json()
		res=res[pair]
		return res['buy'], res['sell']
	
	if market=='bitstamp':
		# Bloked https://eais.rkn.gov.ru/
		pair=pair.replace('_', '')
		q="http://www.bitstamp.net/api/v2/ticker/%s/" % pair
		print q
		r = requests.get(q, verify=False)
		print r.text
		#res=r.json()
	
	if market=='bitfinex':
		pair=pair.replace('_', '')
		r = requests.get("https://api.bitfinex.com/v1/pubticker/%s" % pair)
		res=r.json()
		return res['ask'], res['bid']
		
	if market=='poloniex':
		pair=pair.upper()
		
		pair=pair[4:]+'_'+pair[:3]

		r = requests.get("https://poloniex.com/public?command=returnTicker")
		res=r.json()
		res=res[pair]
		
		return res['lowestAsk'], res['highestBid']

	print market, p, res['buy'], res['buy']
	#print market,  p, res['buy'], res['sell']


markets=['wex','bitfinex',  'poloniex']
pairs=['ltc_btc', 'eth_btc',  'bch_btc']

btc_amount=1
#pair='ltc_btc'

for pair in pairs:
	for m in markets:
		buy, sell=get_info(m, pair)
		buy, sell=float(buy), float(sell)
		
		for m2 in markets:
			if m!=m2:
				buy2, sell2=get_info(m2, pair)
				buy2, sell2=float(buy2), float(sell2)
				
				diff_per=round(buy2/sell,2)
				print 'FROM ', m, '(', sell, ')', '=>', m2, '(', buy2, ') Different %', diff_per
				