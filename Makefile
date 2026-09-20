.PHONY: test paper submission submission-alternatives submission-mm4scireal arxiv-package reproduce reproduce-v3

test:
	python3 -m unittest discover -s tests -v
	node study/test-instrument.cjs
	node inspector/test-core.cjs

paper:
	python3 paper/build_results.py
	cd paper && tectonic main.tex --outdir ../output/pdf
	cp output/pdf/main.pdf output/pdf/delegation-blind-spot-paper.pdf

submission:
	python3 paper/plot_audit_example.py
	tectonic paper/submission/iui-poster.tex --outdir output/pdf

reproduce:
	python3 scripts/unpack_model_artifacts.py
	python3 scripts/reproduce_model_results.py --require-receipts

reproduce-v3:
	python3 scripts/unpack_model_artifacts.py
	python3 scripts/reproduce_v3_results.py

submission-alternatives:
	tectonic paper/submission/chi-poster.tex --outdir output/pdf
	tectonic paper/submission/web-short.tex --outdir output/pdf
	python3 paper/submission/build_visual_poster.py

arxiv-package:
	python3 scripts/package_arxiv.py

submission-mm4scireal:
	tectonic paper/submission/accv-template/mm4scireal.tex --outdir output/pdf
