SHELL=/bin/bash

install:
	echo "Creating a virtual environment and installing the necessary packages to use the program. Please wait..."
	python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt
	echo "Setup succeeded. You can now run the program with 'make run'. You can also uninstall the program at any time with 'make clean'."

run:
	source env/bin/activate && python3 analyzer.py

clean:
	echo "Removing the installed packages and the virtual environment. Please wait..."
	rm -rf env && pyclean .
	echo "Removal of the installed packages and the virtual environment succeeded."
	
