# Create an asynchronous report task

**Doc ID**: 1740302766489602
**Path**: API Reference/Reporting/Create an asynchronous report task

---

Use this endpoint to create an asynchronous report task. 

See [Run an asynchronous report](https://ads.tiktok.com/marketing_api/docs?id=1738864800380930) to learn about how to run an asynchronous report. 

You can use different endpoints to create a standard (synchronous) report and an asynchrounous report. To find out the supported dimensions, metrics, and use cases for different report types, see [Report types](https://ads.tiktok.com/marketing_api/docs?id=1738864835805186). Also, you need to use `POST` method for asynchronous reports and `GET` method for standard (synchronous) reports.

## Notes
See the table below to learn about the notes about rate limit, supported report types, query time range, filtering, compatibility between metrics and dimensions, CHUNK mode, pagination, validity period, data, and more.

``` xtable
| Type{30%} | Details{70%} |
|---|---|
| Rate limit | Due to computing resource limits, the rate limit for each app is 1 QPS. Please do not create a large number of asynchronous report tasks in a short period of time.
Furthermore, the user associated with your access token (`Access-Token`) has a separate limit of 500 asynchronous report creations per ad account every hour. |
| Supported report types | Playable ads reports are not supported in asynchronous reports. |
| Query time range | There are no limits on starting times and ending times for asynchronous reports. |
| Filtering | 
- Asynchronous reports only support filtering by `campaign_ids`, `adgroup_ids`, `ad_ids` or `country_code`. You can filter the data by 20000 IDs at most. 
- If you want to use `country_code` as your grouping filter, then please specify `country_code` in the `dimensions` field of the request. Note that `country_code` works with basic report (sync and async), audience report (sync and async), and playable ad report (sync only). |
| Compatibility between metrics and dimensions | 
- Querying UV metrics with audience dimensions is not supported in asynchronous reports. Please query UV metrics without audience dimensions or audience dimensions without UV metrics in asynchronous reports instead. Audience dimensions include `"gender"`, `"age"`, `"country_code"`, `"ac"`, `"language"`, `"platform"`, `"interest_category"`, `"placement"`, `"contextual_tag"`. 
- UV metrics include `"average_video_play_per_user"`, `"frequency"`, `"cost_per_1000_reached"`, `"real_time_result"`, `"real_time_result_rate"`, `"real_time_cost_per_result"`, `"result"`, `"result_rate"`, `"cost_per_result"`, `"reach"`, `"live_play_count"`. 
- The dimension and metric combinations that are supported may vary between synchronous and asynchronous reports. Therefore, a valid dimension and metric combination in synchronous reports may not be supported in asynchronous reports.|
| CHUNK mode | CHUNK mode only supports synchronous basic reports. |
| Pagination | Paging is not supported. |
| Validity period | An asynchronous report task is valid for 30 days, after which you cannot query for its status or download its output. |
| Data | Data for asynchronous reports is refreshed once every several hours. The data for the current day may be inaccurate. |
| Known issue | Currently, asynchronous reports return the dimension `country_code` (e.g. `US`) as `country_name`(e.g. `United States`). This is a known issue and will be fixed in future release. |
```

## Comparing v1.2 and v1.3 

 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 
 ```xtable
|Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
| Endpoint path | /v1.2/reports/integrated/get/ (POST method) | /v1.3/report/task/create/ (POST method) |
| Request parameter name | `filters` | `filtering` |
| Request parameter data type | `advertiser_id`: number | `advertiser_id`: string |
| Request parameter deprecated in v1.3 | / | `lifetime` (replaced by the new request parameter `query_lifetime`) |
| New request parameters | / | `output_format`
 `file_name`
`query_lifetime` 
`advertiser_ids`
`enable_report_title_translation` |
| Dimensions  | / | See the corresponding articles under [Report types](https://ads.tiktok.com/marketing_api/docs?id=1738864835805186) to find out the dimension changes in each report type.   |
|Metrics  | / | See the corresponding articles under [Report types](https://ads.tiktok.com/marketing_api/docs?id=1738864835805186) to find out the metric changes in each report type.   |
```

## Request

**Endpoint**
https://business-api.tiktok.com/open_api/v1.3/report/task/create/

**Method** POST

**Header**

```xtable
|Field|Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

```xtable
| Field{35%} | Data Type{15%} | Description{50%} |
|---|---|---|
| advertiser_id {+Conditional} | string | Either `advertiser_id` or `advertiser_ids` has to be set. If you pass in both `advertiser_id` and `advertiser_ids`, `advertiser_id` will be ignored. 

Advertiser ID.|
| advertiser_ids
{+Conditional} | string[] | Either `advertiser_id` or `advertiser_ids` has to be set. If you pass in both `advertiser_id` and `advertiser_ids`, `advertiser_id` will be ignored.

A list of advertiser IDs. 
Max size: 5.

**Note**:
-  This field is only valid when `report_type` is `BASIC` or `AUDIENCE`.
-   The advertisers specified in `advertiser_ids` should all belong to the same TikTok for Business user. Otherwise, an error will occur. Use [/oauth2/advertiser/get/](https://business-api.tiktok.com/portal/docs?id=1738455508553729) to retrieve a list of advertiser IDs that belong to the same TikTok for Business user.
-  If you specify `start_date` and `end_date` at the same time, the data will be pulled according to the timezone of each ad account.
-  When you pass multiple advertiser IDs, you can specify up to two ID dimensions (`advertiser_id` + another ID dimension) in dimensions. However, many metrics do not support the `advertiser_id` dimension. Also, it's recommended that you include `currency` in `metrics`, because the ad accounts may have different currencies.|
| service_type | string | Ad service type. 

 Enum values:
- `AUCTION`: auction ads, or both auction ads and reservation ads.
- `RESERVATION` (deprecated) : reservation ads.  Default value: `AUCTION`.

**Note**: To retrieve the reporting data of TopView ads, use the [basic reports](https://business-api.tiktok.com/portal/docs?id=1738864915188737) or [audience reports](https://business-api.tiktok.com/portal/docs?id=1738864928947201) and specify the value `RESERVATION_TOP_VIEW` for the `buying_type` [filter](https://business-api.tiktok.com/portal/docs?id=1751443975608321). |
| report_type {Required} | string | Report type. 

 Enum values: `BASIC` (basic report), `AUDIENCE` (audience report), `PLAYABLE_MATERIAL` (playable ads report), `CATALOG` (DSA report).  

When `service_type` is `AUCTION`, `BASIC`, `AUDIENCE`, `PLAYABLE_MATERIAL`, and `CATALOG` reports are all supported.

**Note**: You can retrieve the creative level data for Upgraded Smart+ Ads when `report_type` is `BASIC`, `AUDIENCE`, or `CATALOG`.
 |
| data_level {+Conditional}| string | The data level that you'd like to query in reports. Required when `report_type` is `BASIC`,`AUDIENCE` or `CATALOG`. 

 Enum values:
- `AUCTION_AD`: auction ads or both auction ads and reservation ads, ad level.
- `AUCTION_ADGROUP`: auction ads or both auction ads and reservation ads, ad group level. 
- `AUCTION_CAMPAIGN`: auction ads or both auction ads and reservation ads, campaign level.
- `AUCTION_ADVERTISER`: auction ads or both auction ads and reservation ads, advertiser level. 
- `RESERVATION_AD`(deprecated): reservation ads, ad level. 
- `RESERVATION_ADGROUP`(deprecated): reservation ads, ad group level. 
- `RESERVATION_CAMPAIGN`(deprecated): reservation ads, campaign level. 
- `RESERVATION_ADVERTISER`(deprecated): reservation ads, advertiser level.  |
| dimensions {Required} | string[] |  Grouping conditions. For example: `["campaign_id", "stat_time_day"]` indicates that both `campaign_id` and `stat_time_day` (days) are grouped. 

Different report types support different dimensions. 
- Supported dimensions in [basic reports](https://business-api.tiktok.com/portal/docs?id=1751443956638721)
- Supported dimensions in [audience reports](https://business-api.tiktok.com/portal/docs?id=1751454103714818)
- Supported dimensions in [playable ad reports](https://business-api.tiktok.com/portal/docs?id=1751617879104514)
- Supported dimensions in [DSA reports](https://business-api.tiktok.com/portal/docs?id=1751617879104514)
-  Supported dimensions in [Business Center reports](https://business-api.tiktok.com/portal/docs?id=1775747465089026)
**Note** : 
- Different report types support different dimensions. For supported dimensions for each report type, see the corresponding articles under [Report types](https://ads.tiktok.com/marketing_api/docs?id=1738864835805186). 
- If your query `dimensions` contain more than xx_id and there is no ads reporting within the query time range, an empty list will be returned.
- The dimension and metric combinations that are supported may vary between synchronous and asynchronous reports. Therefore, a valid dimension and metric combination in synchronous reports may not be supported in asynchronous reports.
- The dimension `ad_id_v2` is available. Note that:You need to ensure the `report_type` is `BASIC`, `AUDIENCE`, or `CATALOG`.
- You cannot use it together with the dimension `ad_id` or the filter `ad_ids`.
- The types of data you can get include:the ad level data for Manual Ads.
- the ad level data for Smart+ Campaigns.
- the ad level data for Upgraded Smart+ Ads.|
| metrics | string[] | Metrics to query. 

Different report types support different metrics.  For supported metrics for each report type, see the corresponding articles under [Report types](https://ads.tiktok.com/marketing_api/docs?id=1738864835805186). 

Default value: `["spend", "impressions"]`. |
| start_date {+Conditional} | string | This field is required when `query_lifetime` is `false` or not specified.

Query start date (closed interval) in the format of `YYYY-MM-DD`. The date is based on the ad account time zone. 

**Note**: Asynchronous reports have no time range limitations.|
| end_date {+Conditional} | string | This field is required when `query_lifetime` is `false` or not specified.

Query end date (closed interval) in the format of `YYYY-MM-DD`. The date is based on the ad account time zone.

**Note**: Asynchronous reports have no time range limitations.|
|query_lifetime | boolean  |Whether to request the lifetime metrics. 

 Default value: `false`. 

If `query_lifetime` = `true`, the `start_date` and `end_date` parameters will be ignored. The lifetime metric name is the same as the normal one. 
**Note**: 
- Breakdown by time or audience is not supported when querying for lifetime metrics.
- Breakdown by location code (`country_code`) is not supported when querying for lifetime metrics.
- DSA reports do not support lifetime metrics. Besides, Audience reports do not support lifetime metrics at the time, and will support lifetime metrics in the first half of 2023.|
| order_field | string | Sorting field. 

All supported metrics (excluding attribute metrics) support sorting. Not sorting by default.|
| order_type | string | Sorting order. 

Enum values: `ASC`, `DESC`.
Default value: `DESC`.|
| enable_report_title_translation | boolean | Whether to enable the translation of the title row of the asynchronous report (including dimension names and metric names).
For instance, if this field is set to `false`, a report title can be `ad_id` (untranslated title) rather than `AD ID` (translated title).
Default value: `true`.

**Note**: 
- This field is only valid when `report_type` is `BASIC` or `AUDIENCE`.
- Starting November 15th, 2024, the translation of certain metrics in the title row of async reports will be updated to provide a better user experience. This change will not affect the metric field names themselves. To minimize potential disruptions, we strongly recommend setting `enable_report_title_translation` to `false` in your code. This will eliminate dependencies on metric translations, which are subject to periodic updates. While these translations are provided to help map metrics to their corresponding names in TikTok Ads Manager, relying on them in your code may lead to breaking changes in the future. By disabling title row  translation, you can ensure more stable and predictable behavior in your integration.  |
| output_format | string | Format of output. 

Enum values: `CSV_STRING`, `CSV_DOWNLOAD`, `XLSX_DOWNLOAD`.
 Default value: `CSV_STRING`.|
|file_name | string | Customized download file name, which is optional to pass when `output_format` is `CSV_DOWNLOAD` or  `XLSX_DOWNLOAD`. The maximum length is 255 characters. The file name needs to exclude the following special characters: ['/', '\t', '\b', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']']. |
| filtering | object[] | Filtering conditions. Supported filtering conditions vary based on `service_type` and `data_level`. For filters supported in different report types, refer to the articles under [Report types](https://ads.tiktok.com/marketing_api/docs?id=1738864835805186). 
**Note**: 
- When you pass in `filtering`, please make sure you specify the fields `field_name`, `filter_type`, and `filter_value` at the same time as an object in a list.
- If you want to use `country_code` as your grouping filter, then please specify `country_code` in the `dimensions` field of the request. Note that `country_code` works with basic report (sync and async), audience report (sync and async), and playable ad report (sync only).
- In asynchronous mode for the report types of basic reports, audience reports, and DSA reports, the only supported filter fields are `campaign_ids`, `adgroup_ids`, and `ad_ids`. |
# | field_name| string | Filter field name.

The filter `ad_ids_v2` is available. Note that:
- You cannot use it together with the dimension `ad_id` or the filter `ad_ids`.
- The types of ID you can filter include:The ID of a Manual Ad.
- The ID of an ad within a Smart+ Campaign.
- The ID of an Upgraded Smart+ Ad.
- You need to set `data_level` to `AUCTION_AD`and include `ad_id_v2` in `dimensions`.
- You can specify up to 100 values when using this filter.|
# | filter_type | string | Filter type. 

Enum values: 
- `IN`: Contains. When the filter type is this item, the filtered value needs to be a valid JSON array character string.
- `MATCH`: Fuzzy matching, equivalent to `like` operations in MySQL.
- `GREATER_EQUAL`: Greater than or equal to.
- `GREATER_THAN`: Greater than.
- `LOWER_EQUAL`: Less than or equal to.
- `LOWER_THAN`: Less than.
- `BETWEEN`: Between. When the filter type is this item, the filtered value needs to be a valid JSON array of 2-element string.
When `field_name` is `ad_id_v2`, set `filter_type` to `IN`. |
# | filter_value | string | The value to filter. 
  When `filter_type` is `IN`, `filter_value` needs to be a valid JSON array character string. |
```

### Example 
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/report/task/create/' \
--header 'Access-Token: {{access-token}}' \
--data-raw '{
    "advertiser_id": "{{advertiser_id}}",
    "data_level":"AUCTION_AD",
    "report_type":"BASIC",
    "dimensions": ["ad_id"],
    "metrics": ["clicks"],
    "start_date": "{{start_date}}",
    "end_date": "{{end_date}}",
    "output_format": "CSV_DOWNLOAD",
    "file_name": "{{file_name}}",
    "filtering": [
        {
        "field_name":"ad_ids",
        "filter_type":"IN",
        "filter_value": "[\"{{ad_id}}\",\"{{ad_id}}\"]"
        }
    ]
}'
(/code)
```

## Response

```xtable
|Field|Type|Description|
|---|---|---|
|code |number|The response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message |string|The response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|data |object|The returned data.  |
#|task_id |string| The ID of the asynchronous report task. |
|request_id |string|The unique ID of the request.  |
```

### Example

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "message": "OK",
    "code": 0,
    "data": {
        "task_id": "{{task_id}}"
    },
    "request_id": "{{request_id}}"
}
(/code);
```
