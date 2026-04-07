# Check the occupancy of identities or products in Shopping Ads

**Doc ID**: 1822001136924674
**Path**: API Reference/GMV Max/Check the occupancy of identities or products in Shopping Ads

---

Use this endpoint to check whether an identity or a product has been occupied by enabled Shopping Ads ([Video Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1750361719059457), [Product Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1785886237030401) or [Live Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1754162402455554)).

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/gmv_max/occupied_custom_shop_ads/list/

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token.
 For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|--- |--- |--- |
| advertiser_id {Required} | string | Advertiser ID. |
| store_id {Required} | string | The ID of the TikTok Shop.

 To obtain a TikTok Shop that is available for GMV Max Campaigns, use [/gmv_max/store/list/](https://business-api.tiktok.com/portal/docs?id=1822001044479041) and confirm that the returned `is_gmv_max_available` is `true`. |
| occupied_asset_type {Required} | string | The type of asset that you want to check for occupancy in enabled Video Shopping Ads, Product Shopping Ads, or Live Shopping Ads.

Enum values: 
- `IDENTITY_TT_USER`: TikTok User (`TT_USER`) identity.
- `IDENTITY_BC_AUTH_TT`: TikTok Account User in Business Center (`BC_AUTH_TT`) identity.
- `IDENTITY_TTS_TT`: TikTok Account User for TikTok Shop (`TTS_TT`) identity.
- `SPU`: SPU.|
| asset_ids {Required} | string[] | The asset IDs. 

Max size: 1. 

- When `occupied_asset_type` is `IDENTITY_TT_USER`, specify one `TT_USER` identity ID via this field.
- When `occupied_asset_type` is `IDENTITY_BC_AUTH_TT`, specify one `BC_AUTH_TT` identity ID via this field.
- When `occupied_asset_type` is `IDENTITY_TTS_TT`, specify one `TTS_TT` identity ID via this field. 
- When `occupied_asset_type` is `SPU`, specify the SPU ID of a product within the TikTok Shop via this field. 

- To obtain a list of identities, use [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882).
- To obtain the list of SPU IDs for products within a TikTok Shop, use [/store/product/get/](https://business-api.tiktok.com/portal/docs?id=1793482248880130). Set `ad_creation_eligible` to `GMV_MAX` and check the returned `item_group_id`.|
```

### Example
```xcodeblock
(code curl http)
curl --location  --request GET 'https://business-api.tiktok.com/open_api/v1.3/gmv_max/occupied_custom_shop_ads/list/?advertiser_id={{advertiser_id}}&store_id={{store_id}}&occupied_asset_type=IDENTITY_BC_AUTH_TT&asset_ids=["{{asset_id}}"]' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

## Response

``` xtable
|Field{30%}|Type{15%}|Description{55%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#| occupied_custom_shop_ads| object[] | The list of enabled Shopping Ads that are currently using the assets. |
##| advertiser_id | string | Advertiser ID. |
##| campaign_id | string | Campaign ID. |
##| adgroup_id | string | Ad group ID. |
##| ad_id | string | Ad ID. |
##| create_time | string | The time when the ad group or ad was created, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0). 

- When `campaign_id` and `adgroup_id` are returned, this field represents the time when the ad group was created.
-  When `adgroup_id` and `ad_id` are returned, this field represents the time when the ad was created.|
```

### Example
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "occupied_custom_shop_ads": []
    }
}
(/code)
```
