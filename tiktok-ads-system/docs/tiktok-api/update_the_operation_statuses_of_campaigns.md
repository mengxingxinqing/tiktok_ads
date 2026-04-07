# Update the operation statuses of campaigns

**Doc ID**: 1739320994354178
**Path**: API Reference/Campaign/Update the operation statuses of campaigns

---

Use this endpoint to enable, disable or delete a campaign. 
> **Note**

> The operation status of a deleted campaign cannot be modified. You can use [/campaign/get/](https://ads.tiktok.com/marketing_api/docs?id=1739315828649986) to get the operation status of a campaign via `operation_status`.

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/campaign/update/status/|/v1.3/campaign/status/update/|
|Request parameter name|`opt_status`|`operation_status`|
|Request parameter data type |`advertiser_id`: number
`campaign_ids`: number[]|`advertiser_id`: string
`campaign_ids`: string[]|
| New request parameters | / |`postback_window_mode`|
|Response parameter data type|`campaign_ids`: number[]|`campaign_ids`: string[]|
| New response parameters|/ | `campaign_list` (including all parameters inside the object array) |
```

## Request

**Endpoint** 

**Method** POST

**Header**

```xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type
Allowed format: `"application/json"`.  |
```

**Parameters**

```xtable
|Field|Data Type|Descripton|
|---|---|---|
|advertiser_id {Required}|string| Advertiser ID |
|campaign_ids {Required}|string[]| A list of campaign IDs, with an allowed quantity range `1-20`.|
|operation_status {Required}|string| The operation being made. 
Enum values: `DELETE` (delete),` DISABLE` (pause), `ENABLE` (enable). 
**Note**: The status of deleted campaigns cannot be modified.|
| postback_window_mode | string | Valid only when the following conditions are all met: 
-  The campaigns (`campaign_ids`) are Dedicated Campaigns (`campaign_type` is `IOS14_CAMPAIGN`). 
-  You specify `operation_status` as `DISABLE` at the same time in the request.
- `postback_window_mode` has not been configured for the campaign.
-  You have enabled SKAN 4.0 for your App. 
The mode that defines which SKAN (SKAdNetwork) 4.0 postback you want to secure. Options with longer windows require more time to receive and, as a result, more time to release the campaign back to the available number. 

Enum values: 
- `POSTBACK_WINDOW_MODE1`: This option secures the first postback, which corresponds to the 0-2 day attribution window. The data can take up to 4 days to return, and the campaign will wait for 4 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE2`: This mode secures the first two postbacks, which corresponds to the 3-7 day attribution window. The data can take up to 13 days to return, and the campaign will wait for 13 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE3`: This mode secures all three postbacks, which correspond to the 8-35 day attribution window. The data can take up to 41 days to return, and the campaign will wait for 41 days to release the campaign quota.
To learn more about SKAN 4.0 attribution window configuration and campaign quota, see [Dedicated Campaigns](https://business-api.tiktok.com/portal/docs?id=1740029173531649).

**Note**: 
-  If you have set up Mobile Measurement Partner (MMP) Tracking with **Adjust**, **Airbridge**, **Appsflyer**,  **Branch**, **Kochava**, or **Singular** for your App and your MMP SDK version is updated to a SKAN 4.0 supported SDK, you can transition your App to SKAN 4.0 on Events Manager. To learn about how to set up MMP tracking for your App, see [How to Set Up App Attribution in TikTok Ads Manager](https://ads.tiktok.com/help/article/set-up-app-attribution-tiktok-ads-manager?lang=en). To learn more about how to transition your App to SKAN 4.0, see [About SKAN 4.0 and TikTok](https://ads.tiktok.com/help/article/about-skan-4-0-and-tiktok?lang=en) and [How to transition to SKAN 4.0](https://ads.tiktok.com/help/article/how-to-transition-to-skan-4-0).
-  Once set, this field cannot be updated. 
-  If `operation_status` is set to `ENABLE` or not passed, and you pass in this field at the same time, an error will occur. 
-  If you pass in this field when you have not enabled SKAN 4.0 for your App (`app_id`), an error will occur. 
-  If this field is not passed when `campaign_type` is set to `IOS14_CAMPAIGN`, `operation_status` is set to `DISABLE`, and you have enabled SKAN 4.0 for your App, this field will default to `POSTBACK_WINDOW_MODE1`.
-  The postback window mode configuration can be partially successful. If you provide `campaign_ids` for non-Dedicated Campaigns, or Dedicated Campaigns for which `postback_window_mode` has been configured, those campaigns will be ignored and their `postback_window_mode` will not be modified. Only the Dedicated Campaigns that meet the conditions mentioned above will have their `postback_window_mode` configured.
-  If you have enabled SKAN 4.0 for your App, ensure that you target devices running iOS 16.1 and later so that you can receive SKAN 4.0 postbacks. To only target iOS 16.1+ devices, set `min_ios_version` to `16.1` at the ad group level. |
```

### Example

```xcodeblock
(code curl http)
curl -H "Access-Token:xxx" -H "Content-Type:application/json" -X POST \
-d '{
    "advertiser_id": "ADVERTISER_ID",
    "campaign_ids": [
        "CAMPAIGN_IDS"
    ],
    "opt_status": "OPT_STATUS"
}' \
https://business-api.tiktok.com/open_api/v1.3/campaign/status/update/
(/code)
```

## Response

```xtable
|Field|Data Type|Description|
|---|---|---|
|code |number|The response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
|message |string|The response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|data |object| Return data |
#|campaign_ids | string[]| A list of modified campaign ids |
#|status |string|The operation that was executed, optional values include: `DELETE`,`DISABLE`,`ENABLE`  |
#| campaign_list | object[] | Information about the list of specified campaigns. |
##| campaign_id | string | Campaign ID. |
##| status | string | The current status of the campaign (`campaign_id`). 
 
Enum values: `DELETE` (deleted), `DISABLE` (paused), `ENABLE` (enabled). |
##| postback_window_mode| string | The mode that determines which SKAN 4.0 postback you want to secure. 
Enum values: 
-  `POSTBACK_WINDOW_MODE1`: This option secures the first postback, which corresponds to the 0-2 day attribution window. The data can take up to 4 days to return, and the campaign will wait for 4 days to release the campaign quota. 
- `POSTBACK_WINDOW_MODE2`: This mode secures the first two postbacks, which correspond to the 3-7 day attribution window. The data can take up to 13 days to return, and the campaign will wait for 13 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE3`: This mode secures all three postbacks, which correspond to the 8-35 day attribution window. The data can take up to 41 days to return, and the campaign will wait for 41 days to release the campaign quota. |
|request_id |string|The log id of a request, which uniquely identifies the request.|
```

### Example

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
  "message": "OK",
  "code": 0,
  "data": {
    "status": "ENABLE",
    "campaign_ids": [
      11,
      22
    ]
  },
  "request_id": "2019091810032301011023224213551"
}
(/code);
```
