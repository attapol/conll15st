import json
import sys
from scorer import evaluate
from validator import validate_relation_list

if __name__ == '__main__':
	input_dataset = sys.argv[1]
	input_run = sys.argv[2]
	output_dir = sys.argv[3]

	gold_relations = [json.loads(x) for x in open('%s/pdtb-data.json' % input_dataset)]
	predicted_relations = [json.loads(x) for x in open('%s/output.json' % input_run)]

	all_correct = validate_relation_list(predicted_relations)
	if not all_correct:
		exit(1)
	connective_cm, arg1_cm, arg2_cm, rel_arg_cm, sense_cm, precision, recall, f1 = \
			evaluate(gold_relations, predicted_relations)  
	output_file = open('evaluation.prototext', 'w')
	r = {}
	r['measure'] = 'precision'
	r['value'] = precision
	output_file.write('%s\n' % json.dumps(r))
	r = {}
	r['measure'] = 'recall'
	r['value'] = recall
	output_file.write('%s\n' % json.dumps(r))
	r = {}
	r['measure'] = 'f1'
	r['value'] = f1
	output_file.write('%s\n' % json.dumps(r))

