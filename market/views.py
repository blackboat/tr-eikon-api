# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import eikon
import urllib
import requests
import json


def index(request):
	app_id = str('CE9D75E3B5ECDE27DC3BDA')
	eikon.set_app_id(app_id)
	# import pdb; pdb.set_trace()
	codes = [str(c) for c in str(urllib.unquote(request.GET.get("codes"))).split(',')]
	start_date = str(request.GET.get("start_date"))
	end_date = str(request.GET.get("end_date"))
	interval = str(request.GET.get("interval"))
	prices = eikon.get_timeseries(codes, fields=[str('Close')], start_date=start_date, end_date=end_date, interval=interval)
	price_list = {p:prices[p].values.tolist() for p in prices}
	dates = [str(row[0]) for row in [t for t in prices.to_records()]]
	price_list['dates'] = dates
	return JsonResponse(price_list)


def realtime(request):
	if request.method == 'POST':
		codes = request.POST.get('codes', None)
		codes = codes.replace(' ', '')
		data_url = 'http://52.87.248.54/update_codes?codes=%s' % codes
		rst = requests.get(data_url)
	else:
		data_url = 'http://52.87.248.54/ric_codes'
		rst = requests.get(data_url)
	ric_codes = json.loads(rst.text)['data']
	ric_codes = [str(code) for code in ric_codes]
	return render(request, 'market/realtime.html', {
		'codes': ric_codes,
	})
