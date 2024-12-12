PANDOC_OPTS += --variable=theme:Warsaw

%/presentation.pdf: %/presentation.md
	pandoc $(PANDOC_OPTS) --to=beamer --output=$@ $<
