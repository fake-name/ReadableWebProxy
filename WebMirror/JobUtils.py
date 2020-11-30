


def buildjob(
			module,                          # Select remote function to be invoked.
			call,                            # Select remote function to be invoked.
			dispatchKey,                     # Dispatch key seems to just be roundtripped for the response
			jobid,                           # Round-tripped to response data for job response correlation
			args                 = [],
			kwargs               = {},
			additionalData       = None,     # Round-tripped to response data for job response correlation
			postDelay            = 0,
			unique_id            = None,     # Unique id which can prevent the same host from re-processing a specific
			                                 # job multiple times.
			early_ack            = False,    # Ack job on receipt, rather then after completion. This can be needed for
			                                 # long running jobs so they don't time out and get sent to another client.
			                                 # On the other hand, it can lead to jobs being lost when the marshaller
			                                 # destroys a VM while it's processing a task.
			serialize            = False,    # Serialze jobs by this value
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

