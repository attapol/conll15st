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

def convert_conll_one_sentence(tokens, sentence_id, global_token_id_offset, relation_ids, relations, stream):

	#We will use this to tag the implicit thing to the first arg2
	relation_ids_to_found_arg2 = OrderedDict()
	for k in relation_ids:
		relation_ids_to_found_arg2[k] = False

	for i, token in enumerate(tokens):
		line = []
		line.append(str(i + global_token_id_offset))
		line.append(str(sentence_id))
		line.append(str(i))

		line.append(token[0])
		line.append(token[1]['PartOfSpeech'])
		linker_tuples = [x.split('_') for x in token[1]['Linkers']]
		
		# Writing information for each relation in this document 
		# One column per relation
		for k in relation_ids:
			found = False # to detect whether the token has multiple roles in the same relation
			for role, relation_id in linker_tuples:
				if k == relation_id:
					relation = relations[int(relation_id)]
					new_info = ''
					if role == 'arg2' and relation['Type'] == 'Implicit' and \
							not relation_ids_to_found_arg2[relation_id]:
						relation_ids_to_found_arg2[relation_id] = True
						new_info += 'arg2|%s|%s' % (relation['Connective']['RawText'],
								','.join(relation['Sense']))
					elif role =='arg2' and relation['Type'] == 'EntRel' and \
							not relation_ids_to_found_arg2[relation_id]:
						relation_ids_to_found_arg2[relation_id] = True
						new_info += 'arg2|EntRel'
					elif role == 'conn' and relation['Type'] == 'AltLex':
						new_info += 'altlex|%s' % ','.join(relation['Sense'])
					elif role == 'conn' and relation['Type'] == 'Explicit':
						new_info += 'conn|%s' % ','.join(relation['Sense'])
					else:
						new_info += role
						
					if found: # multiple roles in the same relation. appending to the same column info
						line[-1] = line[-1] + '|' + new_info
					else:
						line.append(new_info)
						found = True
			# END OF linker tuple loop
			if not found:
				line.append('_')
		# END OF relation_ids loop
		stream.write('\t'.join(line))
		stream.write('\n')
	stream.write('\n')


def convert_input_output(file_name):
	new_relations = []
	for line in open(file_name):
		relation = json.loads(line)
		new_relation = OrderedDict()
		new_relation['Arg1'] = {}
		new_relation['Arg1']['TokenList'] = [x[2] for x in relation['Arg1']['TokenList']]
		new_relation['Arg2'] = {}
		new_relation['Arg2']['TokenList'] = [x[2] for x in relation['Arg2']['TokenList']]
		new_relation['Connective'] = {}
		if relation['Type'] == 'Explicit':
			new_relation['Connective']['TokenList'] = [x[2] for x in relation['Connective']['TokenList']]
		new_relation['Sense'] = relation['Sense']	
		new_relation['DocumentID'] = relation['WSJSection']	
		new_relations.append(new_relation)
	return new_relations

def main(args):
	relation_file, parse_file = args[1:3]
	relation_data = open(relation_file).readlines()
	all_relations = [json.loads(x) for x in relation_data]
	parses = json.loads(open(parse_file).read())

	for doc_id, doc in parses.items():
		token_id_offset = 0
		output_file = open('%s.pdtb.conll' % doc_id, 'w')
		
		# Get all of the revelant relations
		relation_ids = OrderedDict()
		for s in doc['sentences']:
			for token in s['words']:
				for linker in token[1]['Linkers']:
					role, relation_id = linker.split('_')
					if relation_id not in relation_ids:
						relation_ids[relation_id] = len(relation_id)

		for si, s in enumerate(doc['sentences']):
			tokens = []
			for t in s['words']:
				tokens.append(t)
			convert_conll_one_sentence(tokens, si, token_id_offset, relation_ids, all_relations, output_file)
			token_id_offset += len(tokens)


if __name__ == '__main__':
	main(sys.argv)
