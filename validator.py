"""CONLL Shared Task 2015 System output validator

It verifies that each line is 
1) a well-formed json and readable by json.loads
2) a relation json looks like the one given in the training set
"""
import argparse
import json 

RELATION_TYPES = ['Explicit', 'Implicit', 'AltLex', 'EntRel', 'NoRel']
SENSES = ['Temporal.Asynchronous',
		'Temporal.Synchrony', 
		'Contingency.Cause',
		'Contingency.Pragmatic cause', 
		'Contingency.Condition', 
		'Contingency.Pragmatic condition',
		'Comparison.Contrast',
		'Comparison.Pragmatic contrast',
		'Comparison.Concession',
		'Comparison.Pragmatic concession',
		'Expansion.Conjunction',
		'Expansion.Instantiation',
		'Expansion.Restatement',
		'Expansion.Alternative',
		'Expansion.Exception',
		'Expansion.List',
		'EntRel',
		'NoRel']

def validate(file_name):
	lines = open(file_name)
	for i, line in enumerate(lines):
		try:
			relation = json.loads(line)
			check_type(relation)	
			check_sense(relation)
			check_args(relation)
			check_connective(relation)
		except Exception as e:
			print 'Line %s' % i, e

def remove_duplicates(predicted_list):
	to_remove_list = []
	for i in range(len(predicted_list)):
		for j in range(len(predicted_list)):
			if predicted_list[i]['Arg1']['RawText'] == predicted_list[j]['Arg1']['RawText'] and \
					predicted_list[i]['Arg2']['RawText'] == predicted_list[j]['Arg2']['RawText'] and \
					i != j:
				to_remove_list.append(i)
	return [x for i, x in enumerate(predicted_list) if i not in to_remove_list]
	
def check_type(relation):
	if 'Type' not in relation:
		raise ValueError('Field \'Type\' is required but not found')
	relation_type = relation['Type']
	if relation_type not in RELATION_TYPES:
		raise ValueError('Invalid type of %s' % relation_type)


def check_sense(relation):
	if 'Sense' not in relation:
		raise ValueError('Field \'Sense\' is required but not found')
	senses = relation['Sense']
	if not isinstance(senses, list): #or len(senses) != 1:
		raise TypeError('Sense field must a list of one element')
	sense = senses[0]
	if sense not in SENSES:
		raise ValueError('Invalid sense of %s' % sense)
	
def check_args(relation):
	if 'Arg1' not in relation:
		raise ValueError('Field \'Arg1\' is required but not found')
	if 'Arg2' not in relation:
		raise ValueError('Field \'Arg2\' is required but not found')

def check_connective(relation):
	pass

def check_span(span):
	pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser('System output format validator')
	parser.add_argument('system_output_file')
	args = parser.parse_args()
	validate(args.system_output_file)
