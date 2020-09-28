# EbirdTaiwan2020


Setup:
```bash
sudo chmod +x geckodriver
sudo cp geckodriver /usr/bin/
```

## this app requires modification of the source code of django-plotly-dash 1.4.2

this package did not fully support dash (1.14.0) features, but with some modification, I can make them working:

(1) disable showing "updaing" in page title
(2) able to use "prevent_initial_call" in callbacks

search #source_code modification in the dash_wrapper.py file on the top most folder to check how I modify their source code

** copy dash_wrapper.py to replace original one (ex: /venv/lib/python3.7/site-packages/django_plotly_dash/) **


## in server run:
```bash
nohup xxxxx.sh &!
```
Because I am using zsh, I must add ! after the script, otherwise zsh will close this running task when I log out.
