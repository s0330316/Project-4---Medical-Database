# Project-4---Medical-Database

#### Author: Tamana Zafar (s0330316@stud.uni-frankfurt.de)


## Overview
Import the drug datasets and their side effects from the “Molecular network and polypharmacy data” into a suitable PostgreSQL instance. Use the following URLs: http://snap.stanford.edu/decagon/bio-decagon-mono.tar.gz (single drugs) http://snap.stanford.edu/decagon/bio-decagon-combo.tar.gz (double drugs) http://snap.stanford.edu/decagon/bio-decagon-targets.tar.gz (Drug-target protein associations)
Import the following dataset to match commercial names of the drugs.
https://web.cse.ohio-state.edu/~zhang.10631/bak/ddi/drug_569.txt
Develop a web app where the user selects one or two medicines, get the side effects registered in the DB. Then he could report his own side effects. The history of his access should be saved in the database. Analysis module is required to handle reverse lookup- the user report his own set of side effect symptoms, and the system find the closest prediction of medicines that he could have taken. Write queries to find whether drugs with shared proteins have common side effects.

### Prerequisites

What things you need to install the software and how to install them:

- [Python](https://www.python.org/) (version 3.10)
- [Pip](https://pip.pypa.io/) (package installer for Python)
- Install Django by writing in Terminal: pip install Django


### Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/s0330316/Project-4---Medical-Database.git
   cd Project-4---Medical-Database

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
3. **Activate the virtual environment:**
   ```bash
   On Windows:
   .\venv\Scripts\activate

   On macOS/Linux:
   source venv/bin/activate

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

5. **Run migrations:**
   ```bash
   python manage.py migrate

6. **Create a superuser (optional):**
   ```bash 
   python manage.py createsuperuser

7. **Start the development server:**
   ```bash
   python manage.py runserver
   
   Visit http://127.0.0.1:8000/ in your web browser.
