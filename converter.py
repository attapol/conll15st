from collections import OrderedDict
import sys
import json

def convert_conll(tokens, relations, stream):
	relation_ids = OrderedDict()
	for token in tokens:
		for linker in token[1]['Linkers']:
			role, relation_id = linker.split('_')
			if relation_id not in relation_ids:
				relation_ids[relation_id] = len(relation_id)

	#We will use this to tag the implicit thing to the first arg2
	relation_ids_to_found_arg2 = OrderedDict()
	for k in relation_ids:
		relation_ids_to_found_arg2[k] = False

	for i, token in enumerate(tokens):
		line = []
		line.append(str(i))
		line.append(token[0])
		line.append(token[1]['PartOfSpeech'])
		linker_tuples = [x.split('_') for x in token[1]['Linkers']]
		for k in relation_ids:
			found = False
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
						
					if found:
						line[-1] = line[-1] + '|' + new_info
					else:
						line.append(new_info)
						found = True
			if not found:
				line.append('_')
		stream.write('\t'.join(line))
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


if __name__ == '__main__':
	relation_file, parse_file = sys.argv[1:3]
	parses = json.loads(open(parse_file).read())
	relation_data = open(relation_file).readlines()
	relations = [json.loads(x) for x in relation_data]

	for doc_id, doc in parses.items():
		#doc = parses['wsj_1003']
		output_file = open('%s.pdtb.conll' % doc_id, 'w')
		for s in doc['sentences']:
			tokens = [t for t in s['words']]
			convert_conll(tokens, relations, output_file)

