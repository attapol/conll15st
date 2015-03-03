"""CONLL Shared Task 2015 System output validator

It verifies that each line is 
1) a well-formed json and readable by json.loads
2) a relation json looks similar to the one given in the training set
"""
import argparse
import json 
import sys

RELATION_TYPES = ['Explicit', 'Implicit', 'AltLex', 'EntRel', 'NoRel']
SENSES = ['Temporal.Asynchronous.Precedence',
		'Temporal.Asynchronous.Succession', 
		'Temporal.Synchrony', 
		'Contingency.Cause.Reason',
		'Contingency.Cause.Result',
		'Contingency.Condition', 
		'Comparison.Contrast',
		'Comparison.Concession',
		'Expansion.Conjunction',
		'Expansion.Instantiation',
		'Expansion.Restatement',
		'Expansion.Alternative',
		'Expansion.Alternative.Chosen alternative',
		'Expansion.Exception',
		'EntRel',
		]

def validate_file(file_name):
	lines = open(file_name)
	all_correct = True
	for i, line in enumerate(lines):
		try:
			print 'Validating line %s' % (i+1)
			relation = json.loads(line)
			check_type(relation)	
			check_sense(relation)
			check_args(relation)
			check_connective(relation)
		except Exception as e:
			sys.stderr.write('Line %s %s\n' % ((i+1), e))
			all_correct = False
	return all_correct

def validate_relation_list(relation_list):
	all_correct = True
	for i, relation in enumerate(relation_list):
		try:
			check_type(relation)	
			check_sense(relation)
			check_args(relation)
			check_connective(relation)
		except Exception as e:
			sys.stderr.write('Relation %s %s\n' % (i, e))
			all_correct = False
	return all_correct
	
def check_type(relation):
	if 'Type' not in relation:
		raise ValueError('Field \'Type\' is required but not found')
	relation_type = relation['Type']
	if relation_type not in RELATION_TYPES:
		raise ValueError('Invalid type of %s' % relation_type)
	if relation_type == 'NoRel':
		raise ValueError('NoRel should be removed as it is treated as a negative example')


def check_sense(relation):
	if 'Sense' not in relation:
		raise ValueError('Field \'Sense\' is required but not found')
	senses = relation['Sense']
	if not isinstance(senses, list): 
		raise TypeError('Sense field must a list of one element')
	if len(senses) > 1: 
		raise TypeError('Sense field must a list of one element. Got %s' % len(senses))
	sense = senses[0]
	if sense not in SENSES:
		raise ValueError('Invalid sense of %s' % sense)
	
def check_args(relation):
	if 'Arg1' not in relation:
		raise ValueError('Field \'Arg1\' is required but not found')
	else:
		check_span(relation['Arg1'])
	if 'Arg2' not in relation:
		raise ValueError('Field \'Arg2\' is required but not found')
	else:
		check_span(relation['Arg2'])

def check_connective(relation):
	if 'Connective' not in relation:
		raise ValueError('Field \'Connective\' is required but not found')
	else:
		check_span(relation['Connective'])

def check_span(span):
	if 'TokenList' not in span:
		raise ValueError('Field \'TokenList\' is required but not found')
	if not isinstance(span['TokenList'], list): 
		raise TypeError('TokenList field must a list of token indices')

if __name__ == '__main__':
	parser = argparse.ArgumentParser('System output format validator')
	parser.add_argument('system_output_file')
	args = parser.parse_args()
	validate_file(args.system_output_file)
