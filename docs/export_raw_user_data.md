# Export Raw User Data
Updated on 06 Feb 2025
7 Minutes to read

This API prepares the raw user data, exports it into Insider's AWS S3 Bucket, and returns a link to your webhook endpoint as a response. This link enables you to access the raw user data and transfer it to your end.

The API prepares the raw user data for all users for all requested attributes and for a list of events and their event parameters. You can filter to narrow down the user set (e.g., the raw user data can return the users who made a purchase on the last day).

The API can prepare the raw data for attributes and events together. You can choose the events you will receive and the attributes that will be added to each event entry.

Suggested Reading: Understanding Events and Attributes
You should provide a webhook endpoint in the request to be notified when the export link is ready. After sending a request, your webhook endpoint receives an export link as follows to have access to the raw user data.

https://insider-data-export.useinsider.com/{partner name}/p/{file name}

You can export raw user data to analyze user information using a business intelligence tool and sync the data that you want via daily jobs.

Using the Export API, Insider sends the file as a link via Webhook to your endpoint. Export files are sent from specific Insider IP addresses. To enhance security, whitelist Insider IP addresses on your system to restrict access to your endpoint. Remember that whitelisting our IP addresses is about restricting access to your endpoint, which ensures only approved sources can access your endpoint.
To add our IP addresses to your approved list for whitelisting, reach out to the Insider team.
It might take several hours to receive the file after you get the 200 response. If there is an issue with the file size while exporting, you will be notified. In this case, try exporting the data in a smaller range. If you still do not receive the export link, we highly suggest checking if your endpoint is publicly accessible and functioning properly.
The Raw Export logs events based on their actual timestamp, regardless of when they are recorded in the User Content Database (UCD). In contrast, the S3 Export captures events within specific intervals, like the past hour, according to their UCD entry time. For example, the event counts displayed on the Metadata Analytics page represent all transmissions sent to UCD. Sending the same event 100 times results in only one entry in the database but shows a transmission count of 100 on the page, while Raw Export will show only 1.
If an event was timestamped three days ago but sent today, it will appear in S3 Export based on the current transmission timeframe, like the last hour.

## Endpoint and Headers
POST https://unification.useinsider.com/api/raw/v1/export

### Headers
| Header | Sample Value | Description |
| --- | --- | --- |
| X-PARTNER-NAME | mybrand | This is your partner name. Navigate to Inone > Inone Settings > Account Preferences to copy your partner name. The partner name should be lowercase. |
| X-REQUEST-TOKEN | 1a2b3c4e5d6f | This key is required to authorize your request. Refer to API Authentication Tokens to generate your token. |
| Content-Type | application/json | This header specifies the media type of the resource. |

## Body Parameters
Before starting the implementation, make sure to share the following information with the Insider team:

- A webhook endpoint that will be notified when the export link is ready
- A preferred format: CSV, Parquet, or JSON
- A list of attributes, events, and event parameters that you want to export
- A dynamic segment that you want to export

You can consult the Insider team on which parameters to add to the request.
The date range of the segments in requests to the Raw Export API must align with the date range of the requested events. For example, if you're requesting data for the last 5 days of a segment, the event date range should also cover that same period. If the event date range is set to only 2 days, data for users who entered the segment in the last 3 days will not appear in the export.
Each request must have attributes or events object to return the respective user profiles. If you are using an events object, its keys are required, as stated in the table below.

| Parameter | Description | Data Type | Required |
| --- | --- | --- | --- |
| segment | Segment ID of the user filter. To find your Dynamic Segment ID, navigate to Audience > Segments > Saved Segments > Dynamic Segments. Click on the Segment whose ID you want to get. You can see it both on the top right corner of the Summary and Users page. | Object | Yes |
| attributes | Array of attributes | Array (of string) | Yes (if the body does not have the events object) |
| events | Array of events | Object | Yes (if the body does not have the attributes object) |
| start_date | Beginning of the date range for the wanted events | Number | Yes (if the body has the events object) |
| end_date | End of the date range for the wanted events | Number | Yes (if the body has the events object) |
| wanted | Object of the wanted events | Array | Yes (if the body has the events object) |
| event_name | Name of the event | String | Yes (if the body has the events object) |
| params | Event parameters of the event | Array (of string) | Yes (if the body has the events object) |
| filters | Event parameter filters (only one filter is allowed per event_name) | Array (of object) | No |
| key | Event parameter name to be filtered by | String | Yes (if the body has the filters object) |
| operator | Name of the operator to be applied on the values. The valid operators are eq (equals to), ne (not equals to), lt (less than), gt (greater than), lteq (less than or equal to), gteq (greater than or equal to). | String | Yes (if the body has the filters object) |
| values | Event parameter values | Array (of string or number) | Yes (if the body has the filters object) Only one of values and values_url should be provided. |
| values_url | File URL containing event parameter values (file should have one column without any headers) | String | Yes (if the body has the filters object) Only one of values and values_url should be provided. |
| format | The export format | String | Yes |
| hook | Your webhook endpoint | String | Yes |

Ensure the hook parameter value in your request starts with http:// or https://. Otherwise, you receive an invalid hook error.

## Sample Example
### Sample Request
The sample below displays a request to get the raw user data with all attributes.

```bash
curl --location --request POST 'https://unification.useinsider.com/api/raw/v1/export' \
--header 'X-PARTNER-NAME: mybrand' \
--header 'X-REQUEST-TOKEN: 1a2b3c4d5e6f' \
--header 'Content-Type: application/json' \
--header 'Cookie: __cfduid=d1a0bc0c8335c7fecbd3485839787329b1615112066' \
--data-raw '{
   "segment": {
        "segment_id": 123456789
    },
   "attributes":[
      "*"
   ],
   "events":{
      "start_date":1606311893,
      "end_date":1611582293,
      "wanted":[
         {
            "event_name":"email_click",
            "params":[
               "email_campaign_id",
               "timestamp"
            ],
            "filters": [
               {
                  "key": "email_campaign_id",
                  "operator": "eq",
                  "values": [369, 877]
               }
            ]
         },
         {
            "event_name":"item_added_to_cart",
            "params":[
               "product_id",
               "name",
               "timestamp"
            ]
         },
         {
            "event_name":"journey_entered",
            "params":[
               "journey_id",
               "timestamp"
            ]
         }
      ]
   },
   "format":"parquet",
   "hook":"https://xyz.test.com"
}'
```

The sample below displays a request to get the raw user data with selected attributes.

```bash
curl --location --request POST 'https://unification.useinsider.com/api/raw/v1/export' \
--header 'X-PARTNER-NAME: mybrand' \
--header 'X-REQUEST-TOKEN: 1a2b3c4d5e6f' \
--header 'Content-Type: application/json' \
--header 'Cookie: __cfduid=d1a0bc0c8335c7fecbd3485839787329b1615112066' \
--data-raw '{
   "segment": {
        "segment_id": 123456789
    },
  "attributes": [
    "last_visited_product",
    "email",
    "name"
  ],
   "events":{
      "start_date":1606311893,
      "end_date":1611582293,
      "wanted":[
         {
            "event_name":"email_click",
            "params":[
               "email_campaign_id",
               "timestamp"
            ],
            "filters": [
               {
                  "key": "email_campaign_id",
                  "operator": "eq",
                  "values": [369, 877]
               }
            ]
         },
         {
            "event_name":"item_added_to_cart",
            "params":[
               "product_id",
               "name",
               "timestamp"
            ]
         },
         {
            "event_name":"journey_entered",
            "params":[
               "journey_id",
               "timestamp"
            ]
         }
      ]
   },
   "format":"parquet",
   "hook":"https://xyz.test.com"
}'
```

### Sample Responses
#### 200 OK
When the data is ready to download, you will receive the export link on your webhook URL as displayed below.

```json
{"url":"https://insider-data-export.useinsider.com/{partner name}/p/{file name}"}
```

If a user has performed the requested event(s) N times, that user will be displayed in N rows in the exported file. However, since attributes always display the latest information of the user, the attributes on N rows will be the same.
Remember that it might take several hours to receive the file after you get the 200 response. You will be notified if there is an issue with the file size while exporting. In this case, try exporting the data in a smaller range. If you still do not receive the export link, we highly suggest checking if your endpoint is publicly accessible and functioning properly.

#### 429 Too Many Requests
If you exceed the rate limits, you receive an error shown below:

```json
{
    "error": "rejected: too many requests"
}
```

#### 400 Empty Partner
#### 400 Empty Token
#### 403 Authentication Failed

## Limitations
- All functions must be executed with a simple HTTPS POST request.
- Only a response stating whether the request is successful or failed can be received via this API. No data can be inserted.
- The request token should be provided on the request header. If the token is incorrect, the operation will not be executed.
- The exported data can be in CSV, Parquet (version 1.0), or JSON formats.
- The export link expires in 24 hours after it is ready.
- The rate limit for raw export is 1 request per day. Failed requests don't count. Based on the UTC time zone, the API can be called only once in 24 hours. The limitation timeline resets at UTC 00:00.
- The value of X-PARTNER-NAME header should be lowercase.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/40998781/ed362b3a-2d16-4352-85dd-1382e986306b/paste.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/40998781/ed362b3a-2d16-4352-85dd-1382e986306b/paste.txt

---
Resposta do Perplexity: pplx.ai/share