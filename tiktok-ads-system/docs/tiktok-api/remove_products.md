# Remove products

**Doc ID**: 1740562489236481
**Path**: API Reference/Catalog Products/Remove products

---

Use this endpoint to delete products in bulk.

In the response, you will get a task processing ID `feed_log_id`. With this ID you can view the processing status and final results of the task via the [/catalog/product/log/](https://ads.tiktok.com/marketing_api/docs?id=1740570027173889) endpoint.

>  **Note**

>  
- The SKU is unique under the same Catalog, and the re-upload operation for a SKU can only be carried out under the feed that belongs to this SKU.
- For each catalog, you can make up to 1,000 requests per hour. If this does not meet your needs, please contact your TikTok representative.
- For each catalog, you can only send one request at a time. The limit applies to both uploading and deleting. If you send two requests at the same time, the latter will fail. You are recommended to send one request first, and send the next after the previous request is completed.

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path| /v1.2/catalog/product/delete/| /v1.3/catalog/product/delete/|
|Request parameter data type |`bc_id`: number
`catalog_id`: number
`sku_ids`: number[]|`bc_id`: string
`catalog_id`: string 
`sku_ids`: string[]|
|Request parameter name and data type|`feeds_id`: number|`feed_id`: string|
|New request parameters|/|`hotel_ids`
`flight_ids`
`destination_ids`
`vehicle_ids`
`series_ids`|
|Response parameter data type|`feed_log_id`: number|`feed_log_id`: string|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/catalog/product/delete/

**Method** POST

**Header**

``` xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request content type. 
Accepted Value: `"application/json"` . |
```

**Parameters**

``` xtable
| Field {30%}| Type{15%} | Description{55%} |
|--- |--- |--- |
| bc_id {Required} | string | Business Center ID. 

To obtain the list of Business Centers that you can access, use [/bc/get/](https://business-api.tiktok.com/portal/docs?id=1737115687501826).|
| catalog_id {Required} | string | Catalog ID. 

To obtain the list of catalogs that you can access, use [/bc/asset/get/](https://business-api.tiktok.com/portal/docs?id=1739432717798401) and set `asset_type` to `CATALOG`.|
| sku_ids {+Conditional} | string[] |Required for products in an E-commerce catalog.
 
 SKU IDs of E-commerce products that you want to delete. 
 
   Max size: 1,000.  
 Length limit: 100 characters for each SKU ID and cannot contain emojis.

To obtain SKU IDs for products in an E-commerce catalog, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The SKU IDs will be available from the response parameter `sku_id`.
 
 **Note**: Duplicate SKU IDs are not supported. |
| hotel_ids {+Conditional} | string[] | Required for products in a hotel catalog. 
 
Hotel IDs of products that you want to delete.
 
Max size: 1,000. 
Length limit: 100 characters for each hotel ID.

To obtain hotel IDs for products in a hotel catalog, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The hotel IDs will be available from the response parameter `hotel_id`.

**Note**: Duplicate hotel IDs are not supported. |
| flight_ids {+Conditional} | string[] | Required for products in a flight catalog.
 
 Flight IDs of products that you want to delete.  
 
 Max size: 1,000.  
 Length limit: 150 characters for each flight ID.  

To obtain flight IDs for products in a flight catalog, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The flight IDs will be available from the response parameter `flight_id`. 
 
**Note**: Duplicate flight IDs are not supported. |
| destination_ids {+Conditional} | string[] | Required for products in a destination catalog. 
 
Destination IDs of products that you want to delete.  
 
 Max size: 1,000. 
 Length limit: 100 characters for each destination ID.  

To obtain destination IDs for products in a destination catalog, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The destination IDs will be available from the response parameter `destination_id`.
 
**Note**: Duplicate destination IDs are not supported. |
|vehicle_ids {+Conditional} | string[] | Required for products in an Auto-Inventory or Auto-Model catalog.
 
IDs of vehicles that you want to delete.  
 
Max size: 1,000.  
 Length limit: 100 characters for each vehicle ID and cannot contain emojis.

To obtain vehicle IDs for products in an Auto-Inventory or Auto-Model catalog, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The vehicle IDs will be available from the response parameter `vehicle_id`.
 
**Note**: Duplicate vehicle IDs are not supported. |
|series_ids{+Conditional} | string[] | Required for products in a mini series catalog.
 
IDs of the short drama series that you want to delete. 
 
Max size: 1,000.  
 Length limit: 100 characters for each short drama series ID.

To obtain short drama series IDs for products in a mini series catalog, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The short drama series IDs will be available from the response parameter `series_id`.
 
**Note**: Duplicate short drama series IDs are not supported.|
|feed_id|string|Feed ID.  

If the value of this field is empty, the default catalog will be processed.|
```

### Example

```xcodeblock
(code curl http)

    curl -X POST -H "Access-Token:YOUR_ACCESS_TOKEN" \
    -H "Content-Type:application/json" \
    -d '{\"bc_id\": BC_ID,\"catalog_id\": CATALOG_ID,\"feed_id\": FEEDS_ID,\"sku_ids\": [\"SKU_IDS\"]}' \
    https://ads.tiktok.com/open_api/v1.3/catalog/product/delete/

(/code)
```

## Response

``` xtable
| Field | Type | Description |
|--- |--- |--- |
| code | number  |Return code, see [Appendix - return code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message |string|Return message, see [Appendix-Return message](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
| request_id | string | The log id of a request, which uniquely identifies the request. |
| data |object| Returned data. |
# | feed_log_id | string | Product handling log ID. |
```

### Example

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
"message": "OK",
"code": 0,
"data": {
    "feed_log_id": "73474"
},
"request_id": "2020091405212201023125321410665"
}
(/code);
```
