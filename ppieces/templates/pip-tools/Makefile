
build-requirements:
	$(info Building requirements...)
	@$(VENV)pip-compile requirements/base.in -o requirements/base.txt
	@$(VENV)pip-compile requirements/development.in -o requirements/development.txt
	@$(VENV)pip-compile requirements/production.in -o requirements/production.txt
	@$(VENV)pip-compile requirements/test.in -o requirements/test.txt

sync-base-requirements:
	$(info Syncing base requirements...)
	@$(VENV)pip-sync requirements/base.txt

sync-dev-requirements:
	$(info Syncing dev requirements...)
	@$(VENV)pip-sync requirements/development.txt

sync-prod-requirements:
	$(info Syncing prod requirements...)
	@$(VENV)pip-sync requirements/production.txt

sync-test-requirements:
	$(info Syncing test requirements...)
	@$(VENV)pip-sync requirements/test.txt
