# coding: utf8

import datetime

def log_file(msg, path='tmp/ipnlog.txt'):
	with open(path, 'a') as log:
		now = datetime.datetime.now()
		log.write('\n' + msg + '\n')

def write_logs(request):
	message = '-' + 80
	message += '\nIPN Received\n'
	message += 'ARGS:\n' + str(request.args) + '\n'
	message += 'VARS:\n' + str(request.vars) + '\n'
	log_file(message)

def generate_tokens(token_class, amount):
	return float(amount) / 2.5
