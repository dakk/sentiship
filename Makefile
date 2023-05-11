.PHONY: 0 1 2 3 4

all: 0 1 2 3 4

0: 
	python -m rastervision.pipeline.cli run_command ./pipeline-config.json chip

1: 0
	python -m rastervision.pipeline.cli run_command ./pipeline-config.json train

2: 1
	python -m rastervision.pipeline.cli run_command ./pipeline-config.json predict

3: 2
	python -m rastervision.pipeline.cli run_command ./pipeline-config.json eval

4: 3
	python -m rastervision.pipeline.cli run_command ./pipeline-config.json bundle

