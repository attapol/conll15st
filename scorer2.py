"""CONLL Shared Task 2015 Scorer

"""
import argparse
import json

from scorer import evaluate

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Evaluate system's output against the gold standard")
	parser.add_argument('gold', help='Gold standard file')
	parser.add_argument('predicted', help='System output file')
	args = parser.parse_args()
	gold_list = [json.loads(x) for x in open(args.gold)]
	predicted_list = [json.loads(x) for x in open(args.predicted)]

	print 'Evaluation for all discourse relations'
	evaluate(gold_list, predicted_list)

	print 'Evaluation for explicit discourse relations only'
	explicit_gold_list = [x for x in gold_list if x['Type'] == 'Explicit']
	explicit_predicted_list = [x for x in predicted_list if x['Type'] == 'Explicit']
	evaluate(explicit_gold_list, explicit_predicted_list)

	print 'Evaluation for non-explicit discourse relations only (Implicit, EntRel, AltLex)'
	non_explicit_gold_list = [x for x in gold_list if x['Type'] != 'Explicit']
	non_explicit_predicted_list = [x for x in predicted_list if x['Type'] != 'Explicit']
	evaluate(non_explicit_gold_list, non_explicit_predicted_list)

