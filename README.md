# CoNLL 2015 Shared Task - validator and scorers

## Validator
The validator is provided to make sure the discourse parser output is in the right format.
Sample usage:

```
python2.7 validator.py tutorial/pdtb_trial_system_output.json
```

If you would like to see what the error messages look like, try running:
```
python2.7 validator.py tutorial/pdtb_trial_faulty_system_output.json
```

## Scorer
The official scorer for the final evaluation is used to calculate evaluation metrics for argument labeler, connective detection, sense classification, and overall parsing performance.
The output should be validated without any error. The scorer will fail silently if the output is not in the right format or validated.

Sample usage:

```
python2.7 scorer.py tutorial/pdtb_trial_data.json tutorial/pdtb_trial_system_output.json
```

## TIRA scorer
This is the scorer that is used in the TIRA evaluation platform. You should check this out and try to run this offline and see if your parser outputs the right kind of format. 

Sample usage:

First, run your parser on the dataset. We will use the sample parser for now.
```
python2.7 sample_parser.py path/to/conll15-st-03-04-15-dev path/to/model_dir path/to/output_dir
ls -l path/to/output_dir/output.json
```
The system will load the model and other resources from `path/to/model_dir/`. The system output file must be placed in `path/to/outputdir/output.json`

Next, run the TIRA scorer on it. 
```
python2.7 tira_eval.py path/to/conll15-st-03-04-15-dev/ path/to/output_dir path/to/result_dir
```
The evaluation will be done on the gold standard in `path/to/conll15-st-03-04-15-dev/` and the predictions in `path/to/output_dir` and the results will be put in `path/to/result_dir/evaluation.prototext`, which looks like
```
measure {
	 key: "Parser precision"
	  value: "0.0373"
}
measure {
	 key: "Parser recall"
	  value: "0.0418"
}
measure {
	 key: "Parser f1"
	  value: "0.0394"
}
...
```


