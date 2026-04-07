# Bind an event source to a catalog

**Doc ID**: 1740492491200513
**Path**: API Reference/Catalog Event Sources/Bind an event source to a catalog

---

Use this endpoint to bind an app event or a website event to a catalog in a Business Center.

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/catalog/eventsource_bind/create/|/v1.3/catalog/eventsource/bind/|
|Request parameter data type |`bc_id`: number
`advertiser_id`: number
`catalog_id`: number|`bc_id`: string 
`advertiser_id`: string
`catalog_id`: string|
```

## Request

**Endpoint** 

**Method** POST

**Header**

```xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type.
Allowed format: `"application/json"`.  |
```

**Parameters**

```xtable
|Field|Data Type|Description|
|---|---|---|
|advertiser_id {Required}|string| Advertiser ID. |
|bc_id {Required}|string| Business Center ID.|
|catalog_id {Required}|string| Catalog ID.|
|app_id| string| Mobile application ID. You can find the mobile app ID by navigating to **Assets** > **Events** > **App Events** in TikTok Ads Manager. You need to specify at least the mobile app ID (`app_id`) or website Pixel code (`pixel_code`). You can specify both if you want to bind both events to the same catalog.|
|pixel_code|string| Website Pixel code. You can find the pixel code by navigating to **Assets** > **Events** > **Website Events** in TikTok Ads Manager. You need to specify at least the mobile app ID (`app_id`) or website Pixel code (`pixel_code`). You can specify both if you want to bind both events to the same catalog.|
```
### Example
```xcodeblock
(code curl http)
curl --location --request POST https://business-api.tiktok.com/open_api/v1.3/catalog/eventsource/bind/
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "advertiser_id": "{{advertiser_id}}",
    "bc_id": "{{bc_id}}",
    "catalog_id": "{{catalog_id}}",
    "app_id": "{{app_id}}"
}'
(/code)
```

## Response

```xtable
|Field|Data Type|Description|
|---|---|---|
|code |number|The response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|The response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
```
### Example
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {}
}
(/code)
```
