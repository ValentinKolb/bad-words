# Bad-Words-API

![banner](/assets/banner.png)

This API is designed to identify so-called "bad words" and minimize the number of false positives.

This API supports the following languages:

- English
- German

## Endpoints

Currently, there is only one endpoint:

### POST `/check`

This endpoint receives a json object and returns a json object containing a boolean indicating whether the string
contains bad words.

#### Request

```json
{
  "text": "This is a text with bad words"
}
```

#### Response

```json
{
  "containsBadWords": true
}
```

## Inner workings

This API uses the [bad-words-next](https://www.npmjs.com/package/bad-words-next) package and
the [@2toad/profanity](https://www.npmjs.com/package/@2toad/profanity) package to identify bad words.

The API also provides a custom list of words that are considered bad words.

## Deployment

This API is deployed using Docker. To deploy the API, run the following command:

```bash
docker run -p 3000:3000 -d valentinkolb/bad-words-api

curl -X POST http://localhost:3000/check -H "Content-Type: application/json" -d '{"text": "This is a text with bad words"}'
```