# Update the schedule status of a feed

**Doc ID**: 1750349624999937
**Path**: API Reference/Catalog Feeds/Update the schedule status of a feed

---

Use this endpoint to update the schedule status of a feed.
 
## Request
 
**Endpoint** 

**Method** POST

**Header**
 
```xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {required}|string|Request message type.
Allowed format: `"application/json"`.  |
```
 
**Parameters**
 
```xtable
|Field|Data Type|Description|
|---|---|---|
|bc_id {required}|string| Business Center ID. |
|catalog_id {required}|string| Catalog ID.|
|feed_id {required}|string| ID of the feed that you want to update the schedule status for.|
|status {required}|string| Use this field to update the feed schedule status. Enum values: `ON`, `OFF`.
**Note**: 
-  You can only pass in via this field a status different from the current one. For instance, you cannot set status as `ON` for a feed whose schedule status is already `ON`. 
-  If you want to update status from `OFF` to `ON`, you need to ensure the three parameters `uri`, `interval_type` , and `timezone` have been set for the feed. Otherwise, the update will fail.
-  If you want to specify the three parameters `uri`, `interval_type` , and `timezone` for an existing feed, use [/catalog/feed/update/](https://ads.tiktok.com/marketing_api/docs?id=1740665197662210).|
```
 
## Response
 
```xtable
|Field|Data Type|Description|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id|string| The log ID of a request, which uniquely identifies the request.|
|data|object| Returned data.|
```
