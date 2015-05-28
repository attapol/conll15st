""" Convert json format to CoNLL format

"""
from collections import OrderedDict
import sys
import json

def convert_parse_json_to_conll(parse_dict):
	"""Convert parse dictionary (pdtb_parses.json) into conll dictionary

	Example:
		import json
		parses = json.load('./conll15-st-03-04-15-dev/pdtb-parses.json'))
		d = convert_parse_json_to_conll(parses)

	Returns:
		dictionary mapping from doc_id to conll format string
	"""
	doc_id_to_conll_string = {}
	for doc_id, doc in parse_dict.items():
		token_id_offset = 0
		conll_string = ''
		for si, s in enumerate(doc['sentences']):
			tokens = [t for t in s['words']]

			for i, token in enumerate(tokens):
				fields = []
				fields.append(str(i + token_id_offset))
				fields.append(str(si))
				fields.append(str(i))

				fields.append(token[0])
				fields.append(token[1]['PartOfSpeech'])
				conll_string += '\t'.join(fields)
				conll_string += '\n'
			token_id_offset += len(tokens)
			conll_string += '\n'
		doc_id_to_conll_string[doc_id] = conll_string
	return doc_id_to_conll_string
