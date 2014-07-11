#!/opt/bin/python2.7
# was --> /usr/bin/env python
# 
import os
import json
import sys
import time
import traceback
import urllib2

TICKER_SITE = 'bitstamp.net'
FULLTICKER = True  # If False then display only the weighted average price
GOXXED = False     # If True then display only some text explaining the latest goxxing (ie. why the ticker ain't working)

class requester():  
    def perform(self):
        res = urllib2.urlopen("https://www.%s/api/ticker/" % TICKER_SITE)
        return json.load(res)

class _BitcoinTicker():
  """ Retrieve ticker data (json format) and convert it to plain html.
  """
  def main(self):
    try:
      print 'Content-type: text/html\n'
      reqr = requester()
      if GOXXED:
        fail_notice = """Ticker disabled. Click <a href="http://winkdex.com/">here</a> for a weighted average of the various exchange prices."""
        data = {'result': '%s' % fail_notice,}
      else:
        data = reqr.perform()
      # bitstamp json eg: {"high": "584.80", "last": "562.96", "timestamp": "1393644880", "bid": "555.04", "volume": "28407.09241400", "low": "535.00", "ask": "562.96"}
      if data['last'] != '':
        last = data['last']
        high = data['high']
        low = data['low']
        vol = data['volume']
        #vwap = data['vwap']
        timestamp = data['timestamp']
        time_tuple = time.gmtime(int(timestamp))
        # display only the integer portion of the volume number
        vol_parts = vol.split('.')
        vol_display = vol
        if len(vol_parts) > 1:
          vol_display = vol_parts[0]
        vol_display = "{:,d}".format(int(vol_display))
        spacer = '&nbsp;&nbsp;&nbsp;&nbsp;'
        if FULLTICKER:
          print 'Last %s%s High %s%s Low %s%s Volume %s BTC%s Bitstamp/USD %s %s'  % (
              last.replace('$','')
            , spacer
            , high.replace('$','')
            , spacer
            , low.replace('$','')
            , spacer
            , vol_display
            , spacer
            , time.strftime('%d %b %H:%M', time_tuple)
            , 'GMT'
          )
        else:
          timestamp = data['timestamp']
          time_tuple = time.gmtime(int(timestamp))
          print '1.00 BTC = %s (Last) as of %s %s' % (data['last'], time.strftime('%d %b %H:%M', time_tuple), 'GMT')
      else:
        print 'Empty response from bitstamp.net API.'
    except Exception, e:
      excName, excArgs, excTb = self.formatExceptionInfo()
      print 'Problem connecting to %s (%s). Please try again.' % (TICKER_SITE, excName)

  def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
      excArgs = exc.__dict__["args"]
    except KeyError:
      excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

if __name__ == '__main__':
  app = _BitcoinTicker()
  app.main()
