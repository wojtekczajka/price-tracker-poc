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

## to run app:
```bash
python3 -m venv myvenv # optionally (I recommend :p) create a virtual environment
pip3 install -r requirements.txt
uvicorn main:app --reload
```
