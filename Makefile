.PHONY: requirements
requirements:
	pip install -r requirements.txt

.PHONY: dist
dist: requirements
	pyinstaller --clean -y garminHrExporter.py
