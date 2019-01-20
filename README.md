# Targeting Model Harvest
Python application that can interact with Google Ads through the Google AdWords API.

## Getting started End users
1. Extract the app (executable/.exe) and data folder. Keep these two together, since the app relies on this folder.
2. Double click the app and start using it.

For instructions on how certain things work, please consult the `docs` folder in the repository.

---

## Getting started Developers
1. Check if Python is installed by opening a cmd window (press start and type `cmd`) and typing `python`.
If you see Python and its version number you are good to go. If it says `'python' is not recognized...` then you need to install python first. To do so, follow the part of [this guide](https://www.howtogeek.com/197947/how-to-install-python-on-windows/) that install python 3.
2. After installing python there is one more thing to install, namely `pipenv`. This handy little package manages all our dependencies and makes it easy to install. To do so go back to the cmd window and type `pip install pipenv`.
3. The next step is cloning (or downloading the ZIP) [the repository](https://bitbucket.org/harvest_digital/projectharvest/src/master/). When downloading a ZIP extract it to a location of your choice.
4. Now go back to the cmd window and go the location of the repository on your machine using `cd`. Do not enter the folder `harvest_app`.
5. Now run the command `pipenv lock`. This command generates a `Pipfile.lock`, which handles all dependencies for the app.
6. Now run the command `pipenv install` to install all dependencies of this application.
7. Lastly you have to run the command `pipenv shell` to activate the virtual environment and happy coding :).

For more information on installing pipenv read the [pipenv documentation here](https://pipenv.readthedocs.io/en/latest/install/).
For more information on using pipenv use this [handy guide](https://realpython.com/pipenv-guide/).

---

### Packaging
To package this app into an executable, first open a command prompt and move to `NAME_OF_FOLDER/harvest_app/` using `cd`. Once inside make sure that the virtual environment is activated by using the command `pipenv shell`. Now use the command `pyinstaller guiMain.spec`. This command will create a new executable in place of the previous one.

### Setup googleads.yaml file
This file has to be in `data/config file API/`. In case it is not there or you lost the file, head to [the GitHub repository](https://github.com/googleads/googleads-python-lib/blob/master/googleads.yaml) of the python client library. Then copy the content of the file `googleads.yaml` and paste it in a (new) file with the same name in the `data/config file API/` folder.
The following fields of this file have to be filled in:
* `developer_token`
* `client_customer_id`(optional, but recommended)
* `client_id`
* `client_secret`
* `refresh_token`

The developer token has to be approved within Google Ads. To apply for basic access, head to the API centre in Google Ads and follow those steps.
The client customer ID does not have to be filled in, but it is recommended to use the ID of a MCC account.
To get a client id and client secret, follow [these steps](https://developers.google.com/adwords/api/docs/guides/first-api-call#set_up_oauth2_authentication).
To get a refresh token, follow [this guide](https://github.com/googleads/googleads-python-lib/wiki/API-access-using-own-credentials-(installed-application-flow)#step-2---setting-up-the-client-library)

### Change AdWords MCC client ID
To change the MCC client ID that is used when calling the API, go to the `config.txt` file in `data > config file API`. In this file just change the ID within qoutes to the ID you wish to use.
For example, `client_ID_to_use: '7548889362'` to `client_ID_to_use: 'YOUR_ID'`

### Data files
This app defaults to a folder called 'data' when loading CSV or excel files. The app can load these files from any location, but when pressing the clear widgets button, will always default to a folder called data. It is thus easier to save the files you wish to use in this folder.

For instructions on how to use each page, please consult the instructions file in the docs folder.
