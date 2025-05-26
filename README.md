# ipv4_subnet_calc
Subnetting calculator, shows new subnets after changing subnet mask / prefix

# installation:

- clone repository

- open your terminal
- navigate to the project directory

```
cd /path/to/your/project
```

## _create a virtual enviroment (optional)_

```
python -m venv myenv
```

- _activate your virtual enviroment (optional)_
_Windows:_

```
myenv\Scripts\activate
```

_Linux / macOS:_

```
source myenv/bin/activate
```

## install requirements
```
pip install -r requirements.txt
```

# run app:

- _make sure your enviroment is activated (optional)_

in your terminal:

```
streamlit run app.py
```    

The webui should run in your browser

## close app:

- while your app is running navigate to your open terminal (the one you started the app with)
    - ctrl + c
    - the process should shut down
    _(you can also end your python process via windows taskmanager or kill <pid> on Linux)_

- close browser window