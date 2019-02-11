FIGDIR := figures
articledeps := article.tex $(wildcard, ../dat/*)

all:
	mkdir -p $(FIGDIR)
	make build

article.makefile: $(articledeps)
	lualatex -shell-escape article.tex

build: article.makefile $(articledeps)
	make -j2 -f article.makefile
	latexmk -bibtex --shell-escape -lualatex
