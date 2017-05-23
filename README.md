# pyinstagram

python port of https://github.com/mgp25/Instagram-API
(pyinstagram is a developing alpha... welcome any tests, suggestions and feedbacks.)

# usage
```
$ pip install pyinstagram
$ python
>> from pyinstagram import Instagram
>> instagram = Instagram('<username>', '<password>')
>> instagram.login()
>> ...
```

# development
```
# fork first
git clone https://github.com/<your id>/pyinstagram pyinstgram
cd pyinstagram
virtualenv ve
. ve/bin/activate
pip install -r requiremnet.txt
pip install -r requiremnet-dev.txt
pip install -e .
py.test --cov=pyinstagram tests/
```
