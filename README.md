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

YouTube Replay is an interactive data visualization tool that allows you to gain insights from your YouTube watch history. Simply upload your "watch_history.json" file and start exploring!

Features:
* Top Watched Videos
* Videos vs Ads Watched
* Word Cloud based on History
* Genres Watched Over Time
* Popularity of Watched Videos
* Watched Video - Time of Day Trend
* Recommendations based on your viewing history and preferences! (not Youtube's algorithm)
* OAuth 2.0 integration

YouTube Replay is being built as a useful tool for researchers and data enthusiasts. The goal of the app is to provide a comprehensive view of your viewing history, including insights and trends.

You can use this data to analyze your viewing habits on YouTube and gain valuable insights into your interests and behaviors.

Whether you're taking a walk down the YouTube memory-lane or analyze your viewing history for research purposes, we hope that YouTube Replay is the perfect tool for you.


## **Getting Started <a name = "getting_started"></a>**
This section covers the steps to have a hosting server, backend, and frontend up and running locally. See [deployment](#deployment) for notes on how to deploy the project on the cloud.

### **Setting Up The environment**
Run the following to start the virtual env and install all the required packages
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```

### **Downloading personal youtube history**
Navigate to [Google Takeout](https://takeout.google.com/settings/takeout):

1. Go to Google Takeout at https://takeout.google.com/settings/takeout.
2. Log in to your Google account which you need to analyze the YOuTube data for.
3. Scroll down the page until you find "YouTube and YouTube Music" and select it.
4. On the right side of the screen, you should see "All YouTube data included". Click on it.
5. Deselect all and select only "history".
5. Make sure to Select JSON format as the file type for the data.
6. Customize any other options you want to (e.g., file size, delivery method).
7. Click on "Create export".
8. Wait for the export to be created. Depending on the size of your history, this may take several hours (usually few minutes).
9. Once the export is ready, you will receive an email notification with a link to download your data.

*Or save (as .json) the example file provided from https://storage.googleapis.com/youtubereplay-project.appspot.com/watch-history.json

### Here are step-by-step instructions on how to get a YouTube API key:

1. Go to the Google Developers Console (https://console.developers.google.com/) and sign in with your Google account.
2. Create a new project by clicking on the "Select a project" dropdown menu at the top of the page and then clicking on the "New project" button.
3. Name your project and click on the "Create" button. You will be taken to the dashboard for your new project.
4. Click on the "APIs & Services" menu item in the left sidebar.
5. Click on the "Enable APIs and Services" button at the top of the page.
6. Search for "YouTube Data API" and click on the result.
7. Click on the "Enable" button.
8. Go to the "Credentials" tab in the left sidebar.
9. Click on the "Create credentials" dropdown button and select "API key".
10. Copy your API key and keep it in a safe place.
11. Replace this API key in the utils.py file :
        self.yth = YoutubeHelper("Place API_KEY here")


### **Starting the local server**
After having started the virtual environment run 
```
python run.py
```
The web application should now be available at the address **http://127.0.0.1:8080/** or **http:/localhost:8080/**


## **Usage <a name="usage"></a>**

See the "How to Use?" section from the website at : **http://localhost:8080/help-page** or https://youtubereplay-project.wl.r.appspot.com/help-page

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

- [Python](https://www.python.org) - Language
- [Dash](https://dash.plotly.com) - framework for building data apps in Python
- [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) - Using OAuth 2.0 to Access Google APIs


## **Authors <a name = "authors"></a>**

- [Camilla Lambrocco](https://github.com/cala21)
- [Rishabh Berlia](https://github.com/berliarishabh)
- [Christopher Hodge](https://github.com/)
- [Joshua Jalowiec](https://github.com/)
- [David Scott](https://github.com/)


## **Acknowledgements <a name = "acknowledgement"></a>**
- References
