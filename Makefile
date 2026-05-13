MDBOOK := $(shell which mdbook 2>/dev/null || echo ~/.cargo/bin/mdbook)
PORT   := 8765

.PHONY: docs test watch serve clean help

docs:   ## Build the user-guide docs (src/ → docs/)
	$(MDBOOK) build

test:   ## Compile-check every rust fence in the user-guide (T145 gate)
	$(MDBOOK) test

watch:  ## Rebuild docs automatically on every .md change
	$(MDBOOK) watch

serve:  ## Start a local HTTP server at http://localhost:8765
	@echo "Serving at http://localhost:$(PORT)"
	python3 -m http.server $(PORT)

clean:  ## Delete generated docs/
	$(MDBOOK) clean

help:   ## Show available commands
	@grep -E '^[a-z]+:.*##' Makefile | awk -F'##' '{printf "  \033[33m%-8s\033[0m %s\n", $$1, $$2}'
