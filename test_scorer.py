import json
import scorer

def convert_to_output(relation_dict):
	new_relation = {}
	new_relation['DocID'] = relation_dict['DocID']
	new_relation['Type'] = relation_dict['Type']
	new_relation['Sense'] = relation_dict['Sense']

	new_relation['Arg1'] = {}
	new_relation['Arg1']['TokenList'] = [x[2] for x in relation_dict['Arg1']['TokenList']]
	new_relation['Arg2'] = {}
	new_relation['Arg2']['TokenList'] = [x[2] for x in relation_dict['Arg2']['TokenList']]
	new_relation['Connective'] = {}
	new_relation['Connective']['TokenList'] = []
	if 'TokenList' in relation_dict['Connective']:
		new_relation['Connective']['TokenList'] = [x[2] for x in relation_dict['Connective']['TokenList']]
	return new_relation

def main():
	"""Test the scorer

	There are 29 gold relations.
	We corrupt 5 relations and remove 1. 
	Precision = (29 - 6) / 28 = 0.8214
	Recall = (29 - 6) / 29 = 0.7931
	F1 = 2 * (0.8214 * 0.7931) / (0.8214 + 0.7931) = 0.8070
	"""
	relations = [json.loads(x) for x in open('tutorial/pdtb_trial_data.json')]
	output_relations = [convert_to_output(x) for x in relations]
	output_relations[1]['Connective']['TokenList'] = [0]
	output_relations[3]['Arg1']['TokenList'].pop(4)
	output_relations[4]['Arg2']['TokenList'].pop(4)
	output_relations[5]['Arg2']['TokenList'].pop(4)
	output_relations[6]['Sense'] = [u'Contingency.Condition'] # This will hurt sense recall
	output_relations.pop(0) # This will hurt all precision
	scorer.evaluate(relations, output_relations)
	return output_relations

if __name__ == '__main__':
	main()
