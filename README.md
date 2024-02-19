# dates-in-sg
A simple CRUD API to track and review dates to go on around the little red dot.

# Document Schema
```
{
    _id: ObjectId
    location: str
    activity: str
    number_of_reviews: int
    review_rating: float
    reviews: [{
        title: str
        user_id: str
        date_added: datetime.datetime(tz=datetime.timezone.utc)
        description: str
        rating: float}]
}
```
Reviews are represented as embedded documents in the database as the use case is such that there are no worries about bloated documents or massive unbounded arrays.

Additionally, this conforms to the mantra of "data that is accesssed together should be stored together".

If the needs arises in the future, reviews can be placed into their own collection with an additional field that links them to their specific date.

# Routes
## /get-all
Gets all exisitng date entries.

## /get-one
Given an id, returns the corresponding date entry.

## /add
Given the id as a query parameter and a JSON HTTP request body formatted according to the Document Schema (w/o a _id), adds a date entry to the collection and returns the value of `_id`.

## /update
Given the id as a query parameter and a JSON HTTP request body formatted according to the Document Schema (w/o a _id), updates the date entry and returns confirmation of the update.

## /remove
Given an id, removes the corresponding date entry in the collection.

# Deploying
## Render
1. On Render, select "new +" and create a new instance of a web service.
2. Select "Build and deploy from a Git repository".
3. Under "Public Git repository" enter the URL of this Git repository.
4. Add a unique name for the service, select the appropriate tier for the web app service. The other fields should be automtically filled.
5. Copy the connection string from your own MongoDB cluster and add it to the environmental variable under the name "MONGODB_URI".
6. Deploy the model. On the webservice page, select "Connect" and note down the IP addresses.
5. On MongoDB Atlas, add the IP addresses in the "Network Access Tabs".

After these steps, you should be able to send requests to the API.

# Notes
- MongoDB connection string must be added as an environmental variable before deployment.

e.g.
```
MONGODB_URI="mongodb+srv://<username>:<password>@cluster0.a1bc2de.mongodb.net/?retryWrites=true&w=majority"
```

- To run locally, enter
`
poetry run flask run
`
in the CLI in the root directory of the project.