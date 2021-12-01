for the new Ubuntu 20.04 server:
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install mc gcc python3.9 python3.9-venv python3.9-dev
python3.9 -m venv screnv
source screnv/bin/activate
python --version
ssh-keygen
cat .ssh/id_rsa.pub 
git clone git@github.com:stogoff/pricescrapy.git
cd pricescrapy/
pip install --upgrade pip wheel
pip install -r requirements.txt 
mkdir /tmp/uploads
```
* edit file ~/pricescrapy/pricescrapy/pricescrapy/shops.cfg
```
byobu
source ~/screnv/bin/activate
cd ~/pricescrapy/pricescrapy/pricescrapy
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```
 * ctrl-a d
 
``` 
chmod a+x ~/pricescrapy/pricescrapy/pricescrapy/run.sh
~/pricescrapy/pricescrapy/pricescrapy/run.sh

```