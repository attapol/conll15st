import json
import sys
from scorer import evaluate
from validator import validate_relation_list

def write_proto_text(key, value, f):
	f.write('measure {\n key: "%s" \n value: "%s"\n}\n' % (key ,round(value, 4)))

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

	write_proto_text('Parser precision', precision, output_file)
	write_proto_text('Parser recall', recall, output_file)
	write_proto_text('Parser f1', f1, output_file)

	p, r, f = connective_cm.get_prf('yes')
	write_proto_text('Explicit connective precision', p, output_file)
	write_proto_text('Explicit connective recall', r, output_file)
	write_proto_text('Explicit connective f1', f, output_file)

	p, r, f = arg1_cm.get_prf('yes')
	write_proto_text('Arg1 extraction precision', p, output_file)
	write_proto_text('Arg1 extraction recall', r, output_file)
	write_proto_text('Arg1 extraction f1', f, output_file)

	p, r, f = arg2_cm.get_prf('yes')
	write_proto_text('Arg2 extraction precision', p, output_file)
	write_proto_text('Arg2 extraction recall', r, output_file)
	write_proto_text('Arg2 extraction f1', f, output_file)

	p, r, f = rel_arg_cm.get_prf('yes')
	write_proto_text('Arg 1 Arg2 extraction precision', p, output_file)
	write_proto_text('Arg 1 Arg2 extraction recall', r, output_file)
	write_proto_text('Arg 1 Arg2 extraction f1', f, output_file)

	p, r, f = sense_cm.compute_average_prf()
	write_proto_text('Sense precision', p, output_file)
	write_proto_text('Sense recall', r, output_file)
	write_proto_text('Sense f1', f, output_file)

	output_file.close()

