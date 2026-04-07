# Get recommended CTAs

**Doc ID**: 1739362202742785
**Path**: API Reference/Creative Tools/Get recommended CTAs

---

Use this endpoint to get recommended call-to-actions (CTAs) that you can use to create or update your ads. 

See [CTA recommendations](https://ads.tiktok.com/marketing_api/docs?id=1740307296329730) to find out the introduction of the two types of recommended CTAs (Standard Recommended CTAs and Dynamic CTAs).

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/creative/recommend_asset/get/|/v1.3/creative/cta/recommend/|
|Request parameter name|`external_type`|`content_type`|
|Request parameter data type |`advertiser_id`: number |`advertiser_id`: string|
|New request parameters | /|`new_version`
 `objective_type`
 `promotion_type`
 `language`
 `app_id`
 `placements`
 `region_codes`
 `optimization_goal`
 `ad_texts`
 `landing_page_url` |
|Response parameter name and data type|`asset_id`: number[] |`asset_ids`: string[]|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/creative/cta/recommend/

**Method** GET

**Header**

``` xtable
|Field|Type|Description|
|---|---|---|
|Access-Token {required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
|Field|Type|Description|
|--- |--- |--- |
|advertiser_id {required}|string|Advertiser ID.|
| new_version | boolean | Whether to use the new version of the endpoint that supports retrieval of Dynamic CTAs based on your ad settings.

Supported values: `true`, `false`. 
Default value: `false`. |
|asset_type {+Conditional} |string|
- Required when `new_version` is `false` or not passed.
-  Ignored when `new_version` is `true`. 
The asset type. 

 Enum values：
-  `CTA_NORMAL`: Standard Recommended CTAs.
- `CTA_AUTO_OPTIMIZED`: Dynamic CTAs.|
|content_type {+Conditional} |string|
- Required when `new_version` is `false` or not passed.
-  Ignored when `new_version` is `true`. 
The ads content type. 

Enum values:
- `APP_DOWNLOAD`
- `LANDING_PAGE`
- `OTHER`
- `MESSAGE` : a Lead Generation ad with promotion type as TikTok direct message.
- `SOCIAL_MEDIA_APP_MESSAGE` : a Lead Generation ad with promotion type as social media app. 
- `PHONE_CALL`:  a Lead Generation ad with promotion type as phone call. |
| objective_type {+Conditional} | string |
- Required when `new_version` is `true`.
- Not supported when `new_version` is `false` or not passed.
Advertising objective. 

For enum values and descriptions, see [Objectives](https://ads.tiktok.com/marketing_api/docs?id=1737585562434561). |
| promotion_type{+Conditional}  | string | 
- Required when `new_version` is `true`.
- Not supported when `new_version` is `false` or not passed.
 Promotion type (Optimization location). 

For enum values, see [Enumeration - Promotion Type](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Promotion%20Type). |
| language | string | Valid only when `new_version` is `true`. 

The code of language for the recommended CTAs. 

To obtain the list of available language codes, use [/tool/language/](https://ads.tiktok.com/marketing_api/docs?id=1737188554152962). 

 Default value: `en`. 

 For example, if you set this field to `fr`, the returned `asset_content` will be in French. |
| app_id | string | Valid only when `new_version` is `true`.

The application ID of the promoted app. 

 To obtain the list of apps within your ad account, use [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786).  

**Note**: Due to limited historical data for generating customized results, you might receive the same recommended CTAs even if you provide a different value for this field. |
| placements | string[] | Valid only when `new_version` is `true`. 

The apps where you want to deliver your ads.

Enum values: 
- `PLACEMENT_TIKTOK`: TikTok.
- `PLACEMENT_PANGLE`: Pangle. 
- `PLACEMENT_GLOBAL_APP_BUNDLE`: Global App Bundle. 
**Note**: Due to limited historical data for generating customized results, you might receive the same recommended CTAs even if you provide a different value for this field. |
| region_codes | string[] | Valid only when `new_version` is `true`. 

Codes of the regions that you want to target. 

For enum values, see [Location code](https://business-api.tiktok.com/portal/docs?id=1737585867307010). 

Example: `US`. 

**Note**: Due to limited historical data for generating customized results, you might receive the same recommended CTAs even if you provide a different value for this field. |
| optimization_goal | string | Valid only when `new_version` is `true`.

 The measurable results you'd like to drive with your ads. 

For a complete list of enum values, see [Enumeration - Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal). 

**Note**: Due to limited historical data for generating customized results, you might receive the same recommended CTAs even if you provide a different value for this field. |
| ad_texts | string[] | Valid only when `new_version` is `true`.

 A list of ad texts. 
 Each ad text is shown to your audience as part of your ad creative, to deliver the message you intend to communicate to them. 
- Ad text must be 1-100 characters long and cannot contain emoji.
- Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character.
 Recommended size: 1. 

If you don't know how to create effective ad texts, you can try the [Smart Text](https://ads.tiktok.com/marketing_api/docs?id=1739084248002626) feature, which generates ad text recommendations based on the industry and language. 

**Note**: Due to limited historical data for generating customized results, you might receive the same recommended CTAs even if you provide a different value for this field. |
| landing_page_url | string | Valid only when `new_version` is `true`. 

The landing page that users will be redirected to. 

**Note**: Due to limited historical data for generating customized results, you might receive the same recommended CTAs even if you provide a different value for this field. |
```

### Example
#### Retrieve recommended CTAs based on your ad settings
```xcodeblock
(code curl http)
curl --location  --request GET 'https://business-api.tiktok.com/open_api/v1.3/creative/cta/recommend/?advertiser_id={{advertiser_id}}&new_version=true&objective_type=WEB_CONVERSIONS&promotion_type=WEBSITE&language=en' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

#### Retrieve recommended CTAs not based on your ad settings
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/creative/cta/recommend/?advertiser_id={{advertiser_id}}&asset_type=CTA_AUTO_OPTIMIZED&content_type=APP_DOWNLOAD' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

## Response

``` xtable
|Field|Type|Description|
|-|-|-|
|message|string|The return message. For details, see [Appendix-Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|code |number|The return code. For details, see [Appendix-Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|data |object|The returned data.|
#|recommend_assets|object[]| The recommended assets. |
##|asset_ids|string[]|The asset IDs of recommended CTAs|
##|asset_content|string|The CTA text. For example, `"Learn More"`.|
|request_id |string|The request log ID|
```

### Example

``` xcodeblock
(code curl http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "recommend_assets": [
            {
                "asset_ids": [
                    "201902",
                    "201404"
                ],
                "asset_content": "Download now"
            },
            {
                "asset_ids": [
                    "202114",
                    "201743"
                ],
                "asset_content": "Install now"
            },
            {
                "asset_ids": [
                    "201850",
                    "201352"
                ],
                "asset_content": "Install app"
            },
            {
                "asset_ids": [
                    "202141",
                    "201716"
                ],
                "asset_content": "Enroll today"
            },
            {
                "asset_ids": [
                    "201899",
                    "201401"
                ],
                "asset_content": "Check it now"
            },
            {
                "asset_ids": [
                    "201808",
                    "201598"
                ],
                "asset_content": "Check in app"
            },
            {
                "asset_ids": [
                    "201836",
                    "201628"
                ],
                "asset_content": "Try this new app"
            },
            {
                "asset_ids": [
                    "202116",
                    "201740"
                ],
                "asset_content": "Install app now"
            },
            {
                "asset_ids": [
                    "201934",
                    "202158"
                ],
                "asset_content": "Download"
            },
            {
                "asset_ids": [
                    "202124",
                    "201733"
                ],
                "asset_content": "Install it now"
            }
        ]
    }
}
(/code)
```
