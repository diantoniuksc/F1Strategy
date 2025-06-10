
# Allow running local scripts for this session (required for activation script)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Create a new virtual environment named 'venv'
python -m venv venv

# (Alternative) Activate the virtual environment (Command Prompt)
venv\Scripts\activate

# Install the fastf1, seaborn, sklearn modules inside the virtual environment
pip install fastf1
pip install seaborn
pip install sklearn
