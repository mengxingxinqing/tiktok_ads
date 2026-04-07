# Get filters for catalog product insights

**Doc ID**: 1805640864553985
**Path**: API Reference/Catalog Insights/Get filters for catalog product insights

---

Use this endpoint to obtain the available filters for generating targeted insights on a limited number of products within an E-commerce catalog.

The returned filter values can be used with [/catalog/insight/product/get/](https://business-api.tiktok.com/portal/docs?id=1805640886872066) to obtain insights about trending products in your catalog.

>**Note**
 
> 
- Catalog Product Insights become available 24 hours after you have uploaded a minimum of 20 products to your E-commerce catalog.
-  The insights are refreshed daily at around 4:00 AM UTC time.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/catalog/insight/filter/get/

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

```xtable
| Field{30%} | Data Type {15%}| Description {55%}|
|---|---|---|
| bc_id {Required} | string | Business Center ID.

To obtain the list of Business Centers that you have access to, use [/bc/get/](https://business-api.tiktok.com/portal/docs?id=1737115687501826). |
| catalog_id {Required} | string | Catalog ID. 
The catalog needs to be an E-commerce catalog that contains at least 20 products. 

To obtain the list of E-commerce catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and retrieve `catalog_id` values with `catalog_type` as `ECOM`. 
To verify that the catalog contains at least 20 products, use [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345) and check whether the sum of the values of the returned `approved`, `rejected`, and `processing` fields is equal to or greater than 20. |
| filter_type {Required} | string | The type of filter options.

Enum values: 
-  `CATEGORY_ID`: Product category ID. 
-  `BRAND`: Product brand name. 
- `AVAILABILITY`: Product availability status.|
| page | integer | Current page number. 

 Default value: 1. Value range: ≥ 1. |
| page_size | integer | Page size. 

Default value: 10. Value range: 1-200.
 
**Note**: The `page` and `page_size` parameters are provided to allow you to retrieve paginated results in smaller batches, if needed. However, note that this endpoint does not include pagination information in the response. 
 If you don't want to retrieve paginated results, set `page_size` to 50 to obtain the complete set of results in a single response. |
```

### Example
```xcodeblock
(code curl http)
curl --location  --request GET 'https://business-api.tiktok.com/open_api/v1.3/catalog/insight/filter/get/?bc_id={{bc_id}}&catalog_id={{catalog_id}}&filter_type=AVAILABILITY&page=1&page_size=200' \
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
#| brands | string[] | Returned only when `filter_type` is set to `BRAND` in the request.

 The brand names by which you can filter products within the catalog. |
#| availabilities | string[] | Returned only when `filter_type` is set to `AVAILABILITY` in the request. 

 The availability statuses by which you can filter products within the catalog. |
#| categories | object[] | Returned only when `filter_type` is set to `CATEGORY_ID` in the request.

Information about the categories by which you can filter products within the catalog. |
##| category_id| string | The TikTok product category ID assigned to the product, consisting of three levels separated by the number sign (#), in the format of `"level_id_1#level_id_2#level_id_3"`. 

Example: `601152#842248#601302`. |
##| level_info | object | Details of the levels that the category belongs to. |
###| level_id_1 | string | The ID of the level-1 TikTok product category. |
###| level_name_1 | string | The name of the level-1 TikTok product category. |
###| level_id_2 | string | The ID of the level-2 TikTok product category. |
###| level_name_2 | string | The name of the level-2 TikTok product category. |
###| level_id_3 | string | The ID of the level-3 TikTok product category. |
###| level_name_3 | string | The name of the level-3 TikTok product category. |
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
        "availabilities": [
            "OUT_OF_STOCK",
            "IN_STOCK"
        ]
    }
}
(/code)
```
