lint:
	-codespell
	-ruff clean
	-ruff check . --fix
	-ruff format .
update:
	-uv lock --upgrade
	-uv sync
	-pre-commit autoupdate
sec:
	-safety scan --apply-fixes
	-bandit -r .
	-gitleaks dir . --verbose --report-format=json --report-path=gitleaks-report.json
test:
	-coverage run -m pytest
	-coverage html --directory coverage/html
	-coverage report
commit-check:
	-commitizen check
bump:
	-commitizen bump --yes
changelog:
	-commitizen changelog