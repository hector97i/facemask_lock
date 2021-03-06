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

4. Run the following command in the GCP instance with root access:
```bash
gunicorn -w 4 -b 0.0.0.0:80 --access-logfile -  main:app 
```

5. Go to http://localhost:5000 or http://0.0.0.0:5000 if running on LAN in a device other than server.


### Options
If you want to run the program using Flask instead of Gunicorn in the GCP instance, run the following command with root access:
```bash
./run_flask_server.sh
```
