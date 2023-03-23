<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=200px src="./app/assets/youtube_replay.png" alt="Project logo"></a>
</p>

<h3 align="center">YouTube Replay</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/cala21/youtube_replay.svg)](https://github.com/cala21/youtube_replay/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/cala21/youtube_replay.svg)](https://github.com/cala21/youtube_replay/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Few lines describing your project.
    <br> 
</p>

## **Table of Contents**

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](docume/TODO.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## **About <a name = "about"></a>**

YouTube Replay is an interactive data visualization tool for YouTube users to get information and useful insights on their YouTube Watch History. It leverages the [Youtube API](https://developers.google.com/youtube/v3/docs) to dynamically analyze the user history with respect to :

* advertisements consumed
* similarity with respect to another user
* affinity to a genre/topic

## **Getting Started <a name = "getting_started"></a>**
This section covers the steps to have a hosting server, backend, and frontend up and running locally. See [deployment](#deployment) for notes on how to deploy the project on the cloud.

### **Setting Up The environment**
Run the following to start the virtual env and install all the required packages
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```

### **Downloading personal youtube history**
Navigate to [Google Takeout](https://takeout.google.com/settings/takeout):

* Create a new export
* Deselect all
* Search for "YouTube and YouTube Music" and select it
* Click on "All youtube data included", deselect all and select "history"
* Click on "Multiple Formats" and select json on History
* Select your preferred method to receive the data and complete the export


### **Starting the local server**
After having started the virtual environment run 
```
python run.py
```
The web application should now be available at the address **http://127.0.0.1:8050/**


## **Usage <a name="usage"></a>**

Add notes about how to use the system.

## **Deployment <a name = "deployment"></a>**

Add additional notes about how to deploy this on a live system.

## **Built Using <a name = "built_using"></a>**

- [Pyhton](https://www.mongodb.com/) - Database

## **Authors <a name = "authors"></a>**

- [Camilla Lambrocco](https://github.com/cala21)
- [Rishabh Berlia](https://github.com/cala21)
- [Christopher Hodge](https://github.com/cala21)
- [Joshua Jalowiec](https://github.com/cala21)
- [David Scott](https://github.com/cala21)


## **Acknowledgements <a name = "acknowledgement"></a>**

- References
