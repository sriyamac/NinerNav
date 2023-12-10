# NinerNav

<p>Group: 12</p>
<p>Joshua Higgins, Parth Patel, Paul Warner, Sriya Machunuri, Manny Merino</p>

## Product Vision:
<p>NinerNav is FOR new and prospective UNCC students WHO want to learn more about the layout of and
services on campus. NinerNav is an entertainment and educational service THAT brings the campus to
life by gamifying the process of discovery. NinerNav empowers users to learn about and explore the
diverse sites and locations on campus that they might not have visited yet. UNLIKE GeoGuesser, OUR
PRODUCT is specifically designed around the UNCC campus, making it the perfect tool for new UNC
Charlotte students who are eager to explore and get acclimated to the campus. NinerNav provides an
engaging, immersive, and educational experience that turns acclimation into an adventure.</p>

## Requirements:
1. Install the packages in `requirements.txt` (preferably in a virtual environment).
2. Make a folder called `secrets` and place a file called `secrets.json` in it.
3. In `secrets.json`, you should place you database connection string and session signing key.

```json
{
    "dbconnection": "Database connection string here",
    "sessionkey": "Session signing key here, can be any string"
}
```

4. Optionally, run `docs/databaseReset.sql` in your database of choice to generate sample data.
5. Run the application with `flask run` or `python app.py`.