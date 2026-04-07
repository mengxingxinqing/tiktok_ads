# Create an audience by file

**Doc ID**: 1739940570793985
**Path**: API Reference/Audience/Customer File/Create an audience by file

---

Use this endpoint to create an audience by file. You must first upload the data file and obtain a globally unique `file_path`. The obtained  `file_path`  is used to create a corresponding audience.

Refer to [Guidelines for identifier normalization](https://business-api.tiktok.com/portal/docs?id=1850030360880129) to learn about how to normalize your identifiers.

## Notes
See the table below to learn about the restrictions on size limit, audience valid time, audience status, and targeting settings.
 
``` xtable
| Type {30%}| Details{70%} |
|---|---|
| Size limit | You can create up to a max of 400 audiences for an advertiser account. Existing audiences need to be deleted prior to new audience creation if the advertiser account reaches this limit. This limit is at advertiser level. |
| Audience valid time | Newly created audiences require at most 48 hours  to be analyzed and processed before they become active. |
| Audience status | Use the [Get audience details](https://ads.tiktok.com/marketing_api/docs?id=1739940507792385) endpoint to check the current status of an audience. Only 'available' (`is_valid` = `true`) audiences can be operated on.
Upon expiration, the audience will become 'Unavailable' (`is_valid` = `false`), and get detached from any active campaign.|
| Targeting setting | If a campaign has no targeting settings other than audience targeting, it will be paused. |
| Related endpoint | An incorrect `file_path` passed during audience creation can be modified through the [Update an audience](https://ads.tiktok.com/marketing_api/docs?id=1739940572667906) endpoint.|
```

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/dmp/custom_audience/create/|/v1.3/dmp/custom_audience/create/|
|Request parameter data type|`advertiser_id`: number
|`advertiser_id`: string
|
|New request parameters| / |`retention_in_days`|
|Response parameter data type|`custom_audience_id`: number
|`custom_audience_id`: string
|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/create/

**Method** POST

**Header**

``` xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type. 
Allowed format: `"application/json"`.|
```

**Parameters**

```xtable
|Field|Data Type|Description|
|---|---|---|
|advertiser_id {Required}|string| Advertiser ID.|
|custom_audience_name {Required}|string|Audience name. Maximum of 128 characters.|
|audience_sub_type|string| Audience sub type, indicating the type of ads that the audience can be used. Enum values: `NORMAL` Normal audience. It can be used in non-R&F ads. `REACH_FREQUENCY`: Audience for Reach & Frequency. It can only be used in R&F ads. Default: `NORMAL`.|
|file_paths {Required}|string[]|List of file paths.
The recommended size is ****Note**:
- If this field is passed, the expiration date will be the specified number of retention days from the date when the audience was created. Any operations to the audience CANNOT reset the expiration date.
- If this field is not passed, the expiration date will be 365 days from the last time the audience was applied to an active ad group or modified. Applying the audience to an active ad group or modifying the audience will reset the expiration date. To learn about the actions that will reset the expiration date, refer to the Help Center article [Audience Expiration Policy](https://ads.tiktok.com/help/article/audience-expiration-policy?redirected=2). |
```

### Example

``` xcodeblock
(code curl http)
curl --location --request POST 'https://ads.tiktok.com/open_api/v1.3/dmp/custom_audience/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "advertiser_id": "{{advertiser_id}}",
    "custom_audience_name": "test_new",
    "file_paths": ["{{file_paths}}"],
    "calculate_type": "{{calculate_type}}"
}'
(/code)
```
## Response

``` xtable
|Field|Data Type|Description|
|---|---|---|
|code |number|Return code, see [Appendix-Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|Return message, see [Appendix-Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|data |object|Returned Data. |
#|custom_audience_id |string|Custom audience ID.|
|request_id |string|The log id of a request, which uniquely identifies the request.|
```

### Example

``` xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "message": "OK",
    "code": 0,
    "data": {
        "custom_audience_id": "123"
    }
}
(/code);
```
