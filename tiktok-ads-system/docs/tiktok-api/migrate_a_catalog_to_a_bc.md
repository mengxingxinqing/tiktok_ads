# Migrate a catalog to a BC

**Doc ID**: 1740490222539778
**Path**: API Reference/Catalog Management/Migrate a catalog to a BC

---

Use this endpoint to migrate a catalog under your ad account to your Business Center.

>  **Note**

> To be able to migrate catalogs to a Business Center, you must meet two requirements:
- You are the owner of the ad account that the catalogs belong to.
- You are an Admin of an existing Business Center. If you do not have a Business Center, create one in TikTok Ads Manager. For details, see [How to Create a Business Center](https://ads.tiktok.com/help/article?aid=12789). If either of the requirements are not met, you'll get an error.

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path| /v1.2/catalog/capitalize/| /v1.3/catalog/capitalize/|
|Request parameter data type |`bc_id`: number
`advertiser_id`: number
`catalog_id`: number|`bc_id`: string
`advertiser_id`: string
`catalog_id`: string |
```
## Request

**Endpoint** 
https://business-api.tiktok.com/open_api/v1.3/catalog/capitalize/

**Method** POST

**Header**
``` xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request content type. 
 Allowed Value: `"application/json"`.  |
```

**Parameters**

``` xtable
|Field|Data Type|Description|
|---|---|---|
|bc_id {Required}|string| ID of the Business Center that you want to migrate the catalog to.|
|advertiser_id {Required}|string| ID of the ad account that the catalog belongs to.|
|catalog_id {Required}|string| ID of the catalog that you want to migrate.|
```
### Example
```xcodeblock
(code curl http)
curl --location --request POST https://business-api.tiktok.com/open_api/v1.3/catalog/capitalize/
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "advertiser_id": "{{advertiser_id}}",
    "bc_id": "{{bc_id}}",
    "catalog_id": "{{catalog_id}}"
}'
(/code)
```

## Response

``` xtable
| Field | Type | Description |
|--- |--- |--- |
| code | number  |Return code. For the complete list of response codes and descriptions, see [Appendix - Return codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|Return message. For details, see [Appendix-Return codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
| request_id | string | The log id of a request, which uniquely identifies the request. |
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
