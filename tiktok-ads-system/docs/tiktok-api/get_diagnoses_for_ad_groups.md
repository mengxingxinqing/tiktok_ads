# Get diagnoses for ad groups

**Doc ID**: 1738674986981378
**Path**: API Reference/Ad Diagnosis/Get diagnoses for ad groups

---

Use this endpoint to get diagnoses, including possible issues and suggestions for corrections or improvements, for your active ad groups. 

Ad groups with no suggestions will not be returned.

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{30%}|v1.2{30%}|v1.3{40%}|
|---|---|---|
|Endpoint path|/v1.2/tools/diagnosis/get/|/v1.3/tool/diagnosis/get/|
|Request parameter data type |`advertiser_id`: number
`adgroup_ids`: number[]|`advertiser_id`: string
`adgroup_ids`: string[]|
|Request parameter name|`filters`|`filtering`|
 | Request parameters deprecated in v1.3 | / | 
- `fields`
- `diagnosis_status` 
- `page` 
-  `page_size` |
| New request parameters | / | `issue_category` |
|Response parameter name|`list`|`results`|
|Response parameter data type|`adgroup_id`: number
`pixel_id`: number
`adgroup_id`(in `related_ad_groups`): number|`adgroup_id`(in `results`): string
`pixel_id`: string
`adgroup_id`(in `related_ad_groups`): string|
| Response parameters deprecated in v1.3 | / | 
- `diagnosis_status`
-  `learning_status` 
-  `targeting` (including all parameters within the object array) 
-  `website_url` (in `creative`) 
- `loading_time` (in `creative`) 
-  `related_ad_groups` (including all parameters within the object array, in `event_track`) 
- `page_info`  |
| New response parameters | / |
-  In `creative`: `suggestion_time`
- `ad_id`
-  In `bid_and_budget`:`suggestion_time` 
-  `ad_id`
- `bid_edr_info` (including all parameters within the object array)
- `budget_edr_info` (including all parameters within the object array) 
-  In `event_track`: `suggestion_time` |
| Enum values deprecated in v1.3 | / | 
- `LANDING_PAGE` deprecated in the `issue_suggestion` response parameter within `creative`
- `TRAFFIC_EXPLORE` deprecated in the `issue_suggestion` response parameter within `bid_and_budget` |
| New enum values in v1.3 | / | `BID_EDR` and `BUDGET_EDR` added to the `issue_suggestion` response parameter within `bid_and_budget` |
```
## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/tool/diagnosis/get/

**Method** GET

**Header**

```xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162). |
```

**Parameters**

```xtable
|Field|Data Type|Description|
|---|---|---|
|advertiser_id {required}|string| Advertiser ID. |
|filtering|object| Filtering conditions. |
#|adgroup_ids|string[]|IDs of the ad groups that you want to get diagnosis for. 
Max size: 20.|
#| issue_category | string[] | The issue category or categories. 

Allowed values：
-  `CREATIVE`: creative-related issues.
- `BID_AND_BUDGET`: issues related to bids and budgets. 
-  `EVENT_TRACK`: issues related to event tracking. 

-  If multiple values are specified for this field, diagnoses belonging to any of the specified issue categories will be returned. 
-  If this field is not specified, diagnoses belonging to all issue categories will be returned. |
```

### Example
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/tool/diagnosis/get/?advertiser_id={{advertiser_id}}&filtering={"adgroup_ids":["{{adgroup_ids}}"], "issue_category": ["CREATIVE", "BID_AND_BUDGET", "EVENT_TRACK"]}' \
--header 'Access-Token: {{Access-Token}}' \
(/code)
```

## Response

```xtable
|Field {40%}|Data Type{10%}|Description{50%}|
|---|---|---|
|code |number|Response code. For the complete list of error codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id|string| Unique ID of the request.|
|data|object| Returned data.|
#|results|object[]|List of ad groups with the corresponding diagnoses.|
##|adgroup_id|string| Ad group ID.|
##|adgroup_name|string|Ad group name.|
##|diagnosis|object| Diagnosis for the ad group .|
###|diagnosis_time|string|The date and time (UTC + 0 time) when the diagnosis was requested, in the format of "YYYY-MM-DD HH:MM:SS".
Example: "2024-01-01 00:00:01".|
###|suggestions|object[]|Suggestions for the ad group.|
####|creative|object[]| Suggestions for creatives  in the ad group.
If no issues are detected for the creatives in the ad group, the value of this field will be an empty list (`[]`).|
#####|suggestion_time|string|The date and time (UTC + 0 time) when the issue was detected and the suggestion was generated, in the format of "YYYY-MM-DD HH:MM:SS".
Example: "2024-01-01 00:00:01".|
#####|vid|string|Video ID.
Example: v07033g50000c1irpg9l3c4i8hcdp7hg.|
#####|name|string|Ad name.|
#####|ad_id|string|Ad ID.
Example: 1700286510378002.|
#####|issue_suggestion|string|The suggestion for the issue.
Enum values: 
- `NOBGM`: The video lacks background music. You need to add background music to the video. You can use [/creative/quick_optimization/create/](https://business-api.tiktok.com/portal/docs?id=1739355078757377) to create a Quick Optimization task for the video.
- `VIDEO_LENGTH`: The video duration is too short. Edit your video to increase its duration. You can use [/creative/quick_optimization/create/](https://business-api.tiktok.com/portal/docs?id=1739355078757377) to create a Quick Optimization task for the video.
- `VIDEO_RESOLUTION`: The video resolution is too low. Replace the video with a higher resolution version.|
#####|suggestion_id|string|Suggestion ID.|
####|bid_and_budget|object[]|Suggestions for the ad group regarding bidding and budget.
If no issues are detected for the bidding and budget of the ad group, the value of this field will be an empty list (`[]`).|
#####|suggestion_time|string|The date and time (UTC + 0 time) when the issue was detected and the suggestion was generated, in the format of "YYYY-MM-DD HH:MM:SS".
Example: "2024-01-01 00:00:01".|
#####|suggestion_id|string|Suggestion ID.|
#####|issue_suggestion|string| The suggestion for the issue.
 Enum values: 
- `SUGGEST_BID`: A new suggested bid will be provided
- `SUGGEST_BUDGET`: A suggested budget will be provided.
- `NOBID_SWITCH`: Switch to the Maximum Delivery bidding strategy.
-  `BUDGET_EDR`: The Budget EDR (EDR) recommendations will be provided. To learn about EDR, see [Estimated Delivery Results](https://business-api.tiktok.com/portal/docs?id=1746463274713089).
-  `BID_EDR`: The Bid EDR recommendations will be provided. |
#####|bid|number|Returned if `issue_suggestion` is `SUGGEST_BID`.
Current bid value. |
#####|budget|number|Returned if `issue_suggestion` is `SUGGEST_BID`, `SUGGEST_BUDGET`, or `NOBID_SWITCH`.
Current budget. |
#####|suggest_bid|number|Returned if `issue_suggestion` is `SUGGEST_BID`.
Suggested bid value. |
#####|suggest_budget|number|  Returned if `issue_suggestion` is `SUGGEST_BUDGET` or `NOBID_SWITCH`.
Suggested budget value.|
#####|cost_floor|number|Returned if `issue_suggestion` is `SUGGEST_BID`. 
Estimated minimum cost.|
#####| bid_edr_info| object[] | If `issue_suggestion` is not `BID_EDR`, the value of this field will be an empty list (`[]`).
Bid EDR recommendations for the ad group. 
9 sets of data for recommended bid raise ratios from -10% to 30% with a step of 5% and corresponding estimated results. |
######| recommended_bid | number | Recommended bid. 
Adopt one suitable bid using [/adgroup/update/](https://ads.tiktok.com/marketing_api/docs?id=1739586761631745) and pass the adopted bid price to `conversion_bid_price` within the same day (advertiser account time zone). |
######| bid_increase_ratio | number | Estimated bid increase ratio. |
######| estimated_cost | number | Estimated cost. |
######| cost_uplift | number | Estimated cost uplift. |
######| cost_uplift_ratio | number | Estimated cost uplift ratio. |
#####| budget_edr_info | object[] | If `issue_suggestion` is not `BUDGET_EDR`, the value of this field will be an empty list (`[]`). 
Budget EDR recommendations for the ad group. 
15 sets of data for recommended budget raise ratios from -20% to 50% with a step of 5%, and corresponding estimated results. |
######| recommended_budget | number | Recommended budget. 
Adopt one suitable budget using [/adgroup/budget/update/](https://business-api.tiktok.com/portal/docs?id=1739591133130817) within the same day (advertiser account time zone). |
######| budget_increase_ratio | number | Estimated budget increase ratio. |
######| estimated_conversion | number | Estimated conversion. |
######| conversion_uplift | number | Estimated conversion uplift. |
######| conversion_uplift_ratio | number | Estimated conversion uplift ratio. |
######| cpa | number | Estimated CPA. |
######| cpa_uplift | number | Estimated CPA uplift. |
######| cpa_uplift_ratio | number | Estimated CPA uplift ratio. |
######| impression | number | Estimated impression. |
####|event_track|object[]|Suggestions for the ad group regarding event tracking.
If no issues are detected for the event tracking of the ad group, the value of this field will be an empty list (`[]`).|
#####|suggestion_time|string|The date and time (UTC + 0 time) when the issue was detected and the suggestion was generated, in the format of "YYYY-MM-DD HH:MM:SS".
Example: "2024-01-01 00:00:01".|
#####|suggestion_id|string|Suggestion ID.|
#####|issue_suggestion|string| The suggestion for the issue.
Enum values: 
- `PIXEL`: This pixel had no activity in the last 7 days. Test your pixel settings.|
#####|pixel_id|string|Pixel ID.|
#####|pixel_code|string|Pixel code.|
```

### Example
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "results": [
            {
                "adgroup_id": "{{adgroup_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "diagnosis": {
                    "diagnosis_time": "{{diagnosis_time}}",
                    "suggestions": [
                        {
                            "bid_and_budget": [],
                            "creative": [],
                            "event_track": [
                                {
                                    "issue_suggestion": "PIXEL",
                                    "pixel_code": "{{pixel_code}}",
                                    "pixel_id": "{{pixel_id}}",
                                    "suggestion_id": "{{suggestion_id}}",
                                    "suggestion_time": "{{suggestion_time}}"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
}
(/code)
```
