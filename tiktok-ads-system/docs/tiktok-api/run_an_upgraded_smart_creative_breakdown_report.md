# Run an Upgraded Smart+ Creative Breakdown Report

**Doc ID**: 1843317510389761
**Path**: API Reference/Upgraded Smart+/Reporting/Run an Upgraded Smart+ Creative Breakdown Report

---

Use this endpoint to retrieve an Upgraded Smart+ Creative Breakdown Report, a breakdown of the reporting data on creatives within Upgraded Smart+ Ads.

Upgraded Smart+ Creative Breakdown Reports support breakdown by time range (hour, day, week, or month).

## Request
**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/material_report/breakdown/

**Method** GET

**Header**
```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
```

**Parameters**
```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|--- |--- |--- |
| advertiser_id {Required} | string | Advertiser ID. |
| dimensions {Required} | string[] | Dimension grouping conditions.

For example, `["main_material_id","stat_time_day"]` indicates that both `main_material_id` and `stat_time_day` are grouped.

To learn about available dimensions and supported dimension groupings, see [Supported dimensions](https://business-api.tiktok.com/portal/docs?id=1843337879988226). |
| metrics | string[] | Metrics to query.

Default value: `["spend", "impressions"]`.

Note that the amount of currency metrics is based on the currency of the ad account (`advertiser_id`).

To learn about the supported metrics at the ad level, see [Supported ad-level metrics for Upgraded Smart+ Creative Reports](https://business-api.tiktok.com/portal/docs?id=1843337909199938). |
| filtering | object | Filtering conditions. |
#| campaign_ids | string[] | A list of campaign IDs.

Max size: 200.

To obtain campaign IDs, use [/smart_plus/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1843312818332930).

- Filter combination rule: You cannot combine the filter `campaign_ids` with the filter `adgroup_ids` or `smart_plus_ad_ids`.
- Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id`  |
#| adgroup_ids | string[] | A list of campaign IDs.

Max size: 200.

To obtain ad group IDs, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).

-  Filter combination rule: You cannot combine the filter `campaign_ids` with the filter `adgroup_ids` or `smart_plus_ad_ids`.
- Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id`|
#| smart_plus_ad_ids | string[] | A list of ad IDs.

Max size: 200.

To obtain ad IDs, use [/smart_plus/ad/get/](https://business-api.tiktok.com/portal/docs?id=1843317378982914).

- Filter combination rule: You cannot combine the filter `smart_plus_ad_ids` with the filter `campaign_ids` or `adgroup_ids`.
-  Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `smart_plus_ad_id` |
#| main_material_types | string[] | A list of main creative types.

Enum values:
- `VIDEO_NON_SPARK_ADS`: Video (non-Spark Ads).
- `VIDEO_SPARK_ADS`: Video (Spark Ads).
- `CAROUSEL_NON_SPARK_ADS`: Carousel (non-Spark Ads).
- `CAROUSEL_SPARK_ADS`: Carousel (Spark Ads).
- `SINGLE_IMAGE_NON_SPARK_ADS`: Single image (non-Spark Ads).
- `CATALOG_VIDEO`: Catalog video.
- `CATALOG_VIDEO_TEMPLATE`: Catalog video template.
- `CATALOG_CAROUSEL`: Catalog carousel.
- `CATALOG_MULTI_SHOW`: Catalog Multi Show.

- Filter combination rule: The filter `main_material_types` can be used alone.
- Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id` |
#| main_material_id | string[] | A list of of main creative IDs.

- Filter combination rule: When you use this filter, you can specify up to 400 IDs in total for the filters `main_material_id`, `ad_text_entity_id`, `call_to_action_entity_id`, and `interactive_add_on_entity_id`.
- Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id`  |
#| ad_text_entity_id | string[] | A list of ad text entity IDs.

The ID is a system-generated unique identifier for an ad text.

- Filter combination rule: When you use this filter, you can specify up to 400 IDs in total for the filters `main_material_id`, `ad_text_entity_id`, `call_to_action_entity_id`, and `interactive_add_on_entity_id`.
- Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id` |
#| call_to_action_entity_id | string[] | A list of call-to-action entity IDs.

The ID is a system-generated unique identifier for a call-to-action.

- Filter combination rule: When you use this filter, you can specify up to 400 IDs in total for the filters `main_material_id`, `ad_text_entity_id`, `call_to_action_entity_id`, and `interactive_add_on_entity_id`.
-  Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id`  |
#| interactive_add_on_entity_id | string[] | A list of interactive add-on entity IDs.

The ID is a system-generated unique identifier for an interactive add-on.

- Filter combination rule: When you use this filter, you can specify up to 400 IDs in total for the filters `main_material_id`, `ad_text_entity_id`, `call_to_action_entity_id`, and `interactive_add_on_entity_id`.
- Filter and dimension combination rule: You can combine the filter with any of the following dimensions:`advertiser_id`
- `campaign_id`
- `adgroup_id`
- `smart_plus_ad_id`  |
| start_date {Required} | string | Query start date (closed interval) in the format of `YYYY-MM-DD`.

The date is based on the ad account time zone. |
| end_date {Required} | string | Query end date (closed interval) in the format of `YYYY-MM-DD`.

The date is based on the ad account time zone.

**Note**:
- The time difference between `start_date` and `end_date` must be equal to or less than 365 days.
- If `dimensions` contains `stat_time_hour`, the time difference between `start_date` and `end_date` must be equal to or less than 7 days
 |
| sort_field | string | Sorting field.

Default sorting field: `spend`.

All supported metrics (excluding attribute metrics) support sorting. |
| sort_type | string | Sorting order.

Enum values: `ASC` (ascending), `DESC`(descending).
Default value: `DESC`. |
| page | number | Current page number.

Value range: ≥1.
Default value: 1. |
| page_size | number | Page size.

Value range: 1-100.
Default value: 10. |
```

### Example
```xcodeblock
(code curl http)
curl --location--request GET 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/material_report/breakdown/?advertiser_id={{advertiser_id}}&dimensions=["main_material_id","ad_text_entity_id"]&metrics=["spend","clicks"]&filtering={"adgroup_ids": ["{{adgroup_id}}"]}&&start_date={{start_date}}&end_date={{end_date}}&page=1&page_size=100' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

## Response
```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|message|string|Response message. For details, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|request_id|string|The log ID of a request, which uniquely identifies the request.|
|data|object|Returned data.|
#| list|object[]|Data list.|
##| dimensions|object|Dimension data.|
###| main_material_id|string|Returned when the parameter `dimensions` contains `main_material_id` in the request.

Material ID.

- When `main_material_type` is `VIDEO_NON_SPARK_ADS`, `CATALOG_VIDEO`, or `SINGLE_IMAGE_NON_SPARK_ADS`, this field represents the ID of a main creative.
- When `main_material_type` is `VIDEO_SPARK_ADS` or `CAROUSEL_SPARK_ADS`, this field represents the ID of TikTok post.
- When `main_material_type` is `CATALOG_VIDEO_TEMPLATE`, `CATALOG_CAROUSEL`, or `CATALOG_MULTI_SHOW`, this field represents the ID of a catalog.
- When `main_material_type` is `CAROUSEL_NON_SPARK_ADS`, this field represents the ID of a carousel.|
###| main_material_type|string|Main creative type.

Enum values:
- `VIDEO_NON_SPARK_ADS`: Video (non-Spark Ads).
- `VIDEO_SPARK_ADS`: Video (Spark Ads).
- `CAROUSEL_NON_SPARK_ADS`: Carousel (non-Spark Ads).
- `CAROUSEL_SPARK_ADS`: Carousel (Spark Ads).
- `SINGLE_IMAGE_NON_SPARK_ADS`: Single image (non-Spark Ads).
- `CATALOG_VIDEO`: Catalog video.
- `CATALOG_VIDEO_TEMPLATE`: Catalog video template.
- `CATALOG_CAROUSEL`: Catalog carousel.
- `CATALOG_MULTI_SHOW`: Catalog Multi Show.|
###| ad_text_entity_id|string|Ad text entity ID.

The ID is a system-generated unique identifier for an ad text.|
###| ad_text_entity_type|string|Ad text entity type.

Enum value:
- `text`: ad text.|
###| call_to_action_entity_id|string|Call-to-action entity ID.

The ID is a system-generated unique identifier for a call-to-action.|
###| call_to_action_entity_type|string|Call-to-action entity type.

Enum values:
- `manual_call_to_action`: standard call to action.
- `dynamic_call_to_action`: dynamic call to action.|
###| interactive_add_on_entity_id|string|Interactive add-on entity ID.

The ID is a system-generated unique identifier for an interactive add-on.|
###| interactive_add_on_entity_type|string|Interactive add-on entity type.

Enum value:
- `add_on`: interactive add-on.|
##| metrics|object|Metric data.|
###| {metric_name}|string|Returned metrics, which are determined by the `metrics` field specified in the request.|
###| multi_name|string|A combination of setting names based on the setting dimensions (`ad_text_entity_ids`, `call_to_action_entity_ids`, and `interactive_add_on_entity_ids`) specified in the request.

For instance, if you specify the dimensions `ad_text_entity_ids` and `call_to_action_entity_ids` in the request, the `multi_name` will be `{ad_text_name}_{call_to_action_name}`.

Example: `Video1_Adtext1_CTA1`.|
###| main_material_name|string|Main creative name.|
###| ad_text|string|Ad text.|
###| call_to_action|string|Call-to-action.|
###| interactive_add_on_name|string|Interactive add-on name.|
###| interactive_add_on_id|string|Interactive add-on ID.

This ID is generated when you create the interactive add-on in the Creative Library and is different from `interactive_add_on_entity_id`.|
#| page_info|object|Pagination information.|
##| page|number|Current page number.|
##| page_size|number|Page size.|
##| total_number|number|Total number of results.|
##| total_page|number|Total pages of results.|
```

### Example
```xcodeblock
(code Success-Response http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "list": [
            {
                "dimensions": {
                    "ad_text_entity_id": "{{ad_text_entity_id}}",
                    "ad_text_entity_type": "text",
                    "main_material_id": "{{main_material_id}}",
                    "main_material_type": "CAROUSEL_SPARK_ADS"
                },
                "metrics": {
                    "ad_text": "{{ad_text}}",
                    "clicks": "{{clicks}}",
                    "main_material_name": "{{main_material_name}}",
                    "multi_name": "{{multi_name}}",
                    "spend": "{{spend}}"
                }
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 100,
            "total_number": 1,
            "total_page": 1
        }
    }
}
(/code)
```
