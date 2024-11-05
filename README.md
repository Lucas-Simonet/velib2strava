# Velib 2 Strava 

## set up 

After cloning the repo set up your environment by running `poetry install`

To use this connector, you will need to set up a developer account on strava. You can follow this documentation to do so : [Strava dev doc](https://developers.strava.com/docs/getting-started/#account)

Once you have access to your `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET` put them in your `.env` file

Go to your velib account and track the network call for `https://www.velib-metropole.fr/api/private/getCourseList?limit=10&offset=0`. copy the response under `velib2strava/resource/run_list.json`

On your first run you will be prompted to connect to a url and copy paste a code from the redict url. This is to issue a token allowing your strava app to read and write from/to your strava personal account.

TODO : 
- automate run retrieval
- fix activity duration vs ellapsed time problem
    - Runs with low track points in the GPX have the problem, and not the ones with high track points. Strava must think I'm slacking off if I don't have track points.
- fix uneven speed during activity 
- enhance alternative route choice

