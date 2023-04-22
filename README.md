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
The web application should now be available at the address **http://127.0.0.1:8080/**


## **Usage <a name="usage"></a>**

Add notes about how to use the system.

## **Deployment <a name = "deployment"></a>**

Add additional notes about how to deploy this on a live system.

The following steps are to deploy this Dash application to GCP. If your app doesn't work locally, you should fix that first as it won't work on GCP (even if you pray real hard). If it works locally, but it doesn't deploy, the majority of the time it will be due to the `app.yaml` file.

##### Step 1: Make a Project on GCP
> Skip this step if the project is already created by a team member.

Using the CLI or the Console Interface online (which we use below), create a new project with a suitable project name (here we call it `youtubereplay-project`).

##### Step 2: Make Yourself the Owner of Project

> Skip this step if the project is already created by a team member. Ask them to add you as a contributor to be able to deploy.

Make sure the project you've just created is selected on the console, then click 'ADD PEOPLE TO THIS PROJECT'.
Then input your user name and set the role to `Project` > `Owner`.
That's it for now on the Google Cloud Platform Console.

Add other contributors to the project as needed.

##### Step 3: Deploy Using gcloud Command Line Tool

If you haven't installed the [gcloud command line tool](https://cloud.google.com/sdk/gcloud/) do so now.

Next, check your project is active in gcloud using:

`gcloud config get-value project`

Which will print the following on screen:

```
Your active configuration is: [default]

your-project-id
```

To change the project to your desired project, type:

`gcloud config set project your-project-id`

Next, to deploy, type:

`gcloud app deploy`

Then select your desired region (we use `us-west2`)

If you have setup your configuration correctly then it will deploy the Dash app (after a while), which will be available at:

`https://your-project-id.x.x.appspot.com/`

Next, to browse your hosted app, type:

`gcloud app browse`

The youtube-replay app above is hosted [here](https://youtubereplay-project.wl.r.appspot.com).


##### Step 4: Restrict Access to your Application (optional)

By default your application will be accessible to anyone in the world. To restrict the access you can use [Firewall Rules](https://cloud.google.com/blog/products/gcp/introducing-app-engine-firewall-an-easy-way-to-control-access-to-your-app).

## **Built Using <a name = "built_using"></a>**

- [Pyhton](https://www.mongodb.com/) - Database

## **Authors <a name = "authors"></a>**

- [Camilla Lambrocco](https://github.com/cala21)
- [Rishabh Berlia](https://github.com/berliarishabh)
- [Christopher Hodge](https://github.com/)
- [Joshua Jalowiec](https://github.com/)
- [David Scott](https://github.com/)


## **Acknowledgements <a name = "acknowledgement"></a>**
- References
