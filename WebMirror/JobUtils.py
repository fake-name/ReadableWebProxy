


def buildjob(
			module,
			call,
			dispatchKey,
			jobid,
			args                 = [],
			kwargs               = {},
			additionalData       = None,
			postDelay            = 0,
			unique_id            = None,
			early_ack            = False,
			serialize            = False,
			response_routing_key = False,
		):

	if response_routing_key is None:
		response_routing_key = 'response'
	job = {
			'call'                 : call,
			'module'               : module,
			'args'                 : args,
			'kwargs'               : kwargs,
			'extradat'             : additionalData,
			'jobid'                : jobid,
			'dispatch_key'         : dispatchKey,
			'postDelay'            : postDelay,
			'serialize'            : serialize,
			'response_routing_key' : response_routing_key,
			'early_ack'            : early_ack,
			# 'response_routing_key' : 'lowrate_response' if serialize else 'response'
		}

	if unique_id is not None:
		job['unique_id'] = unique_id
	return job

