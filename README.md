# facemask_lock
## Run
1. Create Python 3.6+ venv and installing requirements.txt
```bash
python3 -m venv <ENV_NAME>
source <ENV_NAME>/bin/activate
pip install -r requirements.txt
```
2. Configure IP webcam at main.py line 28.

3. Run main.py in virtual environment.
```bash
python main.py
```

4. Run the following command in the GCP instance with superuser privileges:
```bash
gunicorn -2 4 -b 0.0.0.0:80 main:app
```

4. Go to http://localhost:5000 or http://0.0.0.0:5000 if running on LAN in a device other than server.
