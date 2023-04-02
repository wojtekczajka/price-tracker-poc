# price-tracker-poc

> To download front end repo
```bash
git submodule update --init --recursive
```

> To update submodule to the **main** branch
```bash
cd price-tracker-front
git switch main && git pull
cd ..
git add price-tracker-front
git commit -m "submodule pulled"
git push
```

## to run backend app:
```bash
python3 -m venv myvenv # optionally (I recommend :p) create a virtual environment
source myvenv/bin/activate
pip3 install -r requirements.txt
uvicorn backend_app.main:app --reload
```

## user
```
login: user
password: user
```
