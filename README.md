# Spire apartment availability

For logging into UMass SPIRE system and checking for available apartments. Intended to be run on a schedule.

## Installation

Clone the repo. Set up a virtual environment. Install the python dependencies.

    pip install -r requirements.txt

Create a file called `config.yaml` and fill in the blanks:

    user: <YOUR SPIRE USERNAME>
    password: <YOUR SPIRE PASSWORD>
    spire-id: <YOUR SPIRE ID>

Run the script.

    python login.py
