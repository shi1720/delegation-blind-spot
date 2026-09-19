.PHONY: test paper reproduce
test:
	python3 -m unittest discover -s tests -v
	node study/test-instrument.cjs

paper:
	cd paper && tectonic main.tex --outdir ../output/pdf
	cp output/pdf/main.pdf output/pdf/delegation-blind-spot-paper.pdf

reproduce:
	python3 scripts/unpack_model_artifacts.py
	python3 scripts/reproduce_model_results.py --require-receipts
