# CoNLL 2015 Shared Task - validator and scorer

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


