# Create an R&F ad group

**Doc ID**: 1738235338194945
**Path**: API Reference/Reach & Frequency/Create an R&F ad group

---

Use this endpoint to create a Reach & Frequency ad group.   

See [Create a Reach & Frequency campaign](https://ads.tiktok.com/marketing_api/docs?id=1744571205201922) for detailed instructions. 

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/adgroup/rf/create/|/v1.3/adgroup/rf/create/|
|Request parameter name|`external_type`
`external_action`
 `age` 
`operation_system` 
 `connection_type`
 `device_price` 
 `rf_buy_type` 
  `buy_impression`
 `buy_reach` 
 `optimize_goal` 
 `brand_safety` 
`display_mode` | `promotion_type`
`optimization_event`
 `age_groups` 
`operating_systems` 
`network_types`
 `device_price_ranges` 
`rf_purchased_type` 
`purchased_impression` 
`purchased_reach`
 `optimization_goal`  
 `brand_safety_type`
`delivery_mode` |
|Request parameter data type|`request_id`: number
`advertiser_id`: number
`campaign_id`: number
`app_id`: number | `request_id`: string
`advertiser_id`: string
`campaign_id`: string
`app_id`: string|
|Request parameter name and data type|`is_share_disable`: number
`is_comment_disable`: number
`audience`: number[]
`excluded_audience`: number[]
`location`: number[]
`device_models`: number[]
`carriers_v2`: number[]
`interest_category_v2`: number[]
`video_download`: string| `share_disabled`: boolean
 `comment_disabled`: boolean
`audience_ids`: string[]
`excluded_audience_ids`: string[]
 `location_ids`: string[]
 `device_model_ids`: string[]
`carrier_ids`: string[]
`interest_category_ids`: string[]
`video_download_disabled`:boolean|
| Request parameters deprecated in v1.3| /|`estimate_key`|
|New request parameter |/|`contextual_tag_ids`|
|Response parameter data type|`adgroup_id`: number| `adgroup_id`: string|
|Response parameter| /|We now return the full info of ad entity in v1.3. For details, see the Response section in this page.|
|New response parameter |/|`contextual_tag_ids`|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/adgroup/rf/create/

**Method** POST

**Header**

``` xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type**Allowed format: `"application/json"`  |
```

**Parameters**

``` xtable
| Field | Data Type | Description |
| --- | --- | --- |
| request_id {Required} | string | Request ID with which you can create ad groups with duplicate names. It also supports idempotency to prevent you from sending the same request twice. 
It is different from the `request_id` returned in the response parameters, which is used to uniquely identify an HTTP request. 

The value should be a string representation of a 64-bit integer number. 

Example: `"123456789"` |
| advertiser_id {Required} | string | Advertiser ID. |
| campaign_id {Required} | string | The campaign the ad group belongs to. |
|share_disabled|boolean|Whether sharing to third-party platforms is disabled for ads in this ad group. Default value: `False`.|
| adgroup_name {Required} | string | Name of the ad group. It must not exceed 100 characters or contain any emojis. |
|promotion_type {Required}|string| Promotion type and you can decide where you'd like to promote your products using this field. Enum values: `APP_ANDROID`, `APP_IOS`, `WEBSITE`, `WEBSITE_OR_DISPLAY`.
 If `objective_type` is `RF_REACH`, set this field to `WEBSITE_OR_DISPLAY`.|
|optimization_event |string|Conversion event for the ad group. It is required when the promoted object is an App with tracking urls. For the supported app events, see [Conversion events](https://ads.tiktok.com/marketing_api/docs?id=1739361474981889). You can use the [/app/external_action/](https://ads.tiktok.com/marketing_api/docs?id=1740859338750977) endpoint to find out the supported events for your app. |
| app_id | string | ID of the promoted mobile application.  |
| comment_disabled | boolean | Whether to prohibit users from commenting on your ads on TikTok. Default value: `False`. |
|audience_ids | string[]|IDs of the audiences that you want to target. For an audience to be targeted or excluded in R&F ads, you must set `audience_sub_type` to `REACH_FREQUENCY` when creating or updating the audience. 
Note**: 
You cannot use Lookalike Audience in R&F ads. Otherwise, an error will occur. |
|excluded_audience_ids|string[]|IDs of the audiences that you want to exclude. For an audience to be targeted or excluded in R&F ads, you must set `audience_sub_type` to `REACH_FREQUENCY` when creating or updating the audience. 
**Note**: 
You cannot use Lookalike Audience in R&F ads. Otherwise, an error will occur. |
| age_groups| string[] | Age groups you want to target.  

If your targeting locations include Israel or Brazil, `AGE_13_17` cannot be used.  

For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 

 In certain scenarios, creation of ad groups that target the age group 13-17 (`AGE_13_17`) in the US will not be allowed. See [New age restrictions for ads on TikTok](https://business-api.tiktok.com/portal/docs?id=1788755983247362) to learn more.
If you use targeting options that are not supported for the age group 13-17 in the US and leave the `age_groups` field unspecified or set it as `[]`, an error will occur. You need to explicitly specify the exact age groups that you want to target, such as `AGE_18_24`, in the field to avoid any errors.|
| gender | string | Audience gender. For more details, see [Enumeration - Audience Gender](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
| languages | string[] | Codes of the languages that you want to target. For the list of languages codes supported, see [Enumeration - Language Code](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).  |
| location_ids {Required} | string[] | IDs of the targeted locations. The location can be at the country or region level, the Province, DMA (Designated Market Area) or Metropolitan level, or the city level.
Location targeting supports a single country or region only.  If you want to target multiple locations, they must from the same country or region. 
You can find the supported countries and regions in [About Reach & Frequency](https://ads.tiktok.com/marketing_api/docs?id=1744571201117186). |
| is_hfss | boolean | Whether the promoted content is HFSS foods (foods that are high in fat, salt, or sugar). Please note that the European market prohibits the promotion of HFSS foods to underage users.  |
| operating_systems | string[] |Device operating systems that you want to target. 
 Enum values: `ANDROID`, `IOS`, `PC`.|
| network_types |string[]| Device connection types that you want to target. Default value: `unlimited`. For enum values, see [Enumeration - Connection Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
|device_model_ids| string[]| IDs of the device models that you want to target. Currently only brand-level model IDs are supported. When this field is specified, `device_price_ranges` must not be specified. For enum values of device model IDs on different levels, please see [Device Models](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369). 
**Note**: Only active devices (`is_active` = `True` in the response of [/tool/device_model/](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369)) can be used to create ads.|
| device_price_ranges|number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50. 
**Important**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].|
| carrier_ids |string[]| Carriers that you want to target. A carrier is valid only when the `in_use` field for the carrier is `true`. The carriers must be consistent with the location(s) that you want to target. Use [Get Carriers](https://ads.tiktok.com/marketing_api/docs?id=1737168013095938) to get carrier IDs. |
| interest_category_ids |string[]|List of interest categories that you want to target. Use [/tool/interest_category/](https://ads.tiktok.com/marketing_api/docs?id=1737174348712961) endpoint to get the complete list of interest categories.|
| rf_purchased_type{Required}  | string | Buying type. Allowed values: 
- `FIXED_SHOW`: Purchase to achieve a fixed amount of impressions.
- `FIXED_REACH`: Purchase to reach a fixed number of users.
- `FIXED_BUDGET`: Purchase with a fixed budget.|
| budget {Required} | float | Budget. Please fill in this number based on the data returned via the ad inventory estimate API. See [Create a Reach & Frequency campaign - Step 4](https://ads.tiktok.com/marketing_api/docs?id=1744571205201922) for how to specify the field. |
| purchased_impression {Required} | number | Impressions to be purchased, **in the unit of 1,000**. Please fill in this number based on the data returned via the ad inventory estimate API. See [Create a Reach & Frequency campaign - Step 4](https://ads.tiktok.com/marketing_api/docs?id=1744571205201922) for how to specify the field. |
| purchased_reach {Required} | number | Purchased user reach, **in the unit of 1,000**. Please fill in this number based on the data returned via the ad inventory estimate API. See [Create a Reach & Frequency campaign - Step 4](https://ads.tiktok.com/marketing_api/docs?id=1744571205201922) for how to specify the field. |
| schedule_start_time {Required} | string | Schedule start time (UTC+0), in the format of  `YYYY-MM-DD HH:MM:SS`. 

 The time interval between `schedule_start_time` and `schedule_end_time` must not exceed 90 days.

 The value of this field must be at `YYYY-MM-DD HH:00:00`  for the time zone where the ad will be delivered. 
For instance, if an advertiser in the UTC-5 time zone wants to create an R&F ad group that starts delivery on November 1st, 2023, this field must be set to `"2023-11-01 05:00:00"`.|
| schedule_end_time {Required} | string | Schedule end time (UTC+0), in the format of `YYYY-MM-DD HH:MM:SS`. 

The time interval between `schedule_start_time` and `schedule_end_time` must not exceed 90 days.

 The value of this field must be at `YYYY-MM-DD HH:59:59`  for the time zone where the ad will be delivered. 
For instance, if an advertiser in the UTC-5 time zone wants to create an R&F ad group that ends delivery on November 10th, 2023, this field must be set to `"2023-11-10 04:59:59"`.|
| frequency {Required} | number | `frequency`, together with `frequency_schedule`, controls how often people see your ad (only available for `REACH` ads). 
For example, `frequency` = 2 & `frequency_schedule` = 3 means "show ads no more than twice every 3 days".
The following conditions should be met:
- 1 ≤ `frequency` ≤ `frequency_schedule`.
- 1 ≤ `frequency_schedule` ≤ min (`schedule_end_time` - `schedule_start_time`, 30).
- The frequency cap determined by `frequency` and `frequency_schedule` does not exceed four times a day. |
| frequency_schedule {Required} | number | `frequency_schedule`, together with `frequency`, controls how often people see your ad (only available for `REACH` ads). See `frequency` field for more. |
|optimization_goal {Required} | string |The measurable results you'd like to drive with your ads. It must be aligned with the value for `objective_type` on the campaign level. Enum values: `REACH`, `VIDEO_VIEW`, `CLICK`, `POST_ENGAGEMENT`, `INSTALL`.|
|cpv_video_duration {+Conditional} | string | Required when `optimization_goal` is `VIDEO_VIEW`.

 The target video view duration.

 Enum value: `SIX_SECONDS`. |
|brand_safety_type|string|Brand safety type for Reach and Frequency ads. Default value: `NO_BRAND_SAFETY`. Enum values: 
- `NO_BRAND_SAFETY`:  To not use any brand safety solution.  Full inventory, which means your ads may appear next to some content featuring mature themes. 
- `EXPANDED_INVENTORY`: Use TikTok's brand safety solution. Expanded inventory means that your ads will appear next to content where most inappropriate content has been removed, and that does not contain mature themes. In the next API version, `EXPANDED_INVENTORY` will replace `NO_BRAND_SAFETY` and will be the default brand safety option.
- `STANDARD_INVENTORY`: Use TikTok's brand safety solution. Standard inventory means that ads will appear next to content that is appropriate for most brands. 
- `LIMITED_INVENTORY`: Use TikTok's brand safety solution. Limited inventory means that your ads will not appear next to content that contains mature themes.
- `THIRD_PARTY`: Use a third-party brand safety solution. You also need to pass in a value to the `brand_safety_partner` field. To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. 
**Note**: 
-  Pre-bid third-party brand safety solutions are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. 
-  See [Brand safety](https://ads.tiktok.com/marketing_api/docs?id=1739381752981505) to learn about the supported advertising objectives, supported markets, and the general introduction of pre-bid Brand Safety filtering. |
|brand_safety_partner{+Conditional}|string|Brand safety partner for Reach and Frequency ads. Required when `brand_safety_type` is `THIRD_PARTY`. Enum values: `IAS`, `OPEN_SLATE`(The partner is named **DoubleVerify** on TikTok Ads Manager because the partner has been acquired by DoubleVerify).
**Note**: 
-  Pre-bid third-party brand safety solutions are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. 
-  Once set, this field cannot be modified. |
|category_exclusion_ids|string[]|Valid when `brand_safety_type` is set to  `STANDARD_INVENTORY` or `LIMITED_INVENTORY`.

Content exclusion category IDs. 

You can use [/tool/content_exclusion/get/](https://business-api.tiktok.com/portal/docs?id=1769738074686465) to get a list of content category IDs (`excluded_category_list`) that can be excluded from being displayed next to your ads.  |
|video_download_disabled|boolean| Whether users can download your video ads on TikTok(cannot be updated once created).  Default value: `false`.|
|feed_type |string| Feed type option. Enum values: `STANDARD_FEED`, `TOP_FEED`. `STANDARD_FEED` refers to large inventory with normal CPM price while `TOP_FEED`refers to limited inventory with higher CPM price. |
|delivery_mode |string|  The strategy for sequencing and scheduling your ad delivery. 

Enum values:
- `STANDARD`: Standard delivery. Your ads will be distributed evenly and are expected to achieve similar traffic size. 
- `SCHEDULE`: Scheduled delivery.  Set specific time periods to deliver each ad in. If you use this value, you need to pass the object array `schedules` at the same time. 
- `SEQUENCE`: Sequenced delivery. Set a specific sequence to deliver your ads in. If you use this value, you need to pass the field `expected_orders` at the same time. 
- `OPTIMIZE` (Deprecated): Optimized delivery that delivers ads to achieve the best performance.
Default value: `STANDARD`.|
|schedule_infos |object[]| Ad delivery information.  

When `delivery_mode` is set to `SEQUENCE`, the number of objects in this array represents the number of ads that you will specify the sequence for. |
#|schedules {+Conditional} |object[]| Required when `delivery_mode` is set to `SCHEDULE`. 

The details of the scheduled delivery that you want to set for the ad.

Ensure that the schedule is continuous and covers the whole delivery period that is specified through `schedule_start_time` and `schedule_end_time`.|
##|start_time |string| Ad delivery start time, in the format of `"YYYY-MM-DD HH:MM:SS"`. |
##|end_time |string| Ad delivery end time, in the format of `"YYYY-MM-DD HH:MM:SS"`. |
#|expected_orders {+Conditional} |number[]| Required when `delivery_mode` is set to `SEQUENCE`.  

The delivery order for an ad within the ad group. 

To set a fixed sequence for each ad within the ad group, pass only one number (for instance, `[1]`) to this field. A value of `[1]` indicates that the ad will be delivered first. |
|contextual_tag_ids |string[]|
Not supported when `brand_safety_type` is set to `THIRD_PARTY`.
Not supported when `feed_type` is set to `TOP_FEED`.

Contextual tag IDs. You can use [/tool/contextual_tag/get/](https://ads.tiktok.com/marketing_api/docs?id=1747747118654465) to get available contextual tags. 
**Note**:  
- If you set `rf_campaign_type` to `PULSE` in [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602), you must include the contextual tags from either the `MAX_PULSE` or `CUSTOM` content lineup types under `PREMIUM` type when creating an ad group. `GENERAL` type contextual tags are optional. See [TikTok Pulse](https://business-api.tiktok.com/portal/docs?id=1744571201117186#item-link-TikTok%20Pulse) to learn more about how to use TikTok Pulse.  

 Currently, you can run Max Pulse targeting `AE` (United Arab Emirates), `AU` (Australia), `BR` (Brazil), `CA` (Canada), `DE` (Germany), `ES` (Spain), `FR` (France), `GB` (United Kingdom), `IT` (Italy), `MX` (Mexico), `SA` (Saudi Arabia), `TR` (Turkey), and `US` (United States), and Category Lineups targeting `US`(the United States), `CA`(Canada), `BR`(Brazil), `AU`(Australia), `GB`(the United Kingdom), `FR`(France), `IT`(Italy), `ES`(Spain), `DE`(Germany). Both features are allowlist only. If you want to use them in the above markets, please contact your TikTok representative. 
- This is an allowlist-only feature. If you would like to access it, please contact your TikTok representative.|
```

### Example

``` xcodeblock
(code curl http)
curl -H "Access-Token:xxx" -H "Content-Type:application/json" -X POST \
-d '{
    "languages": [
        "LANGUAGES"
    ], 
    "buy_impression": "BUY_IMPRESSION", 
    "is_comment_disable": "IS_COMMENT_DISABLE", 
    "estimate_key": "ESTIMATE_KEY", 
    "gender": "GENDER", 
    "age": [
        "AGE"
    ], 
    "frequency_schedule": "FREQUENCY_SCHEDULE", 
    "budget": "BUDGET", 
    "campaign_id": "CAMPAIGN_ID", 
    "advertiser_id": "ADVERTISER_ID", 
    "frequency": "FREQUENCY", 
    "location": [
        "LOCATION"
    ], 
    "schedule_end_time": "SCHEDULE_END_TIME", 
    "request_id": "REQUEST_ID", 
    "operation_system": [
        "OPERATION_SYSTEM"
    ], 
    "buy_reach": "BUY_REACH", 
    "rf_buy_type": "RF_BUY_TYPE", 
    "adgroup_name": "ADGROUP_NAME", 
    "schedule_start_time": "SCHEDULE_START_TIME"
}' \
https://business-api.tiktok.com/open_api/v1.3/adgroup/rf/create/
(/code)
```

## Response

```xtable
|Field|Data Type|Description|
|---|---|---|
|code |number|The response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|The response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id|string| The log id of a request, which uniquely identifies the request.|
|data |object|Returned data. |
#| advertiser_id  | string | Advertiser ID. |
#| campaign_id | string | The campaign the ad group belongs to. |
#| adgroup_id | string | Ad group ID. |
#|share_disabled|boolean|Whether sharing to third-party platforms is disabled for ads in this ad group. Default value: `False`.|
#| adgroup_name  | string | Name of the ad group. It must not exceed 100 characters or contain any emojis. |
#|promotion_type |string| Promotion type and you can decide where you'd like to promote your products using this field. Enum values: `APP_ANDROID`, `APP_IOS`, `WEBSITE`, `WEBSITE_OR_DISPLAY`. |
#|optimization_event |string|Conversion event for the ad group. It is required when the promoted object is an App with tracking urls. For the supported app events, see [Conversion events](https://ads.tiktok.com/marketing_api/docs?id=1739361474981889). You can use the [/app/external_action/](https://ads.tiktok.com/marketing_api/docs?id=1740859338750977) endpoint to find out the supported events for your app. |
#| app_id | string | ID of the promoted mobile application.  |
#| comment_disabled | boolean | Whether to prohibit users from commenting on your ads on TikTok. Default value: `False`. |
#|audience_ids | string[]|IDs of the audiences that you want to target. For an audience to be targeted or excluded in R&F ads, you must set `audience_sub_type` to `REACH_FREQUENCY` when creating or updating the audience. |
#|excluded_audience_ids|string[]|IDs of the audiences that you want to exclude. For an audience to be targeted or excluded in R&F ads, you must set `audience_sub_type` to `REACH_FREQUENCY` when creating or updating the audience.|
#| age_groups| string[] | Age groups you want to target. If your targeting locations include Israel or Brazil, `AGE_13_17` cannot be used. For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
#| gender | string | Audience gender. For more details, see [Enumeration - Audience Gender](https://ads.tiktok.com/marketing_api/docs?id=100641). Enum values: `GENDER_FEMALE`, `GENDER_MALE`, and `GENDER_UNLIMITED`. |
#| languages | string[] | Codes of the languages that you want to target. For the list of languages codes supported, see [Enumeration - Language Code](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).  |
#| location_ids  | string[] | IDs of the targeted locations. If you want to target multiple locations, they must from the same country or region. You can find the supported countries and regions in [Reach & Frequency](https://ads.tiktok.com/marketing_api/docs?id=1739470723315713). For the list of location IDs, see [Location IDs](https://ads.tiktok.com/marketing_api/docs?id=1701890989574146).|
#| is_hfss | boolean | Whether the promoted content is HFSS foods (foods that are high in fat, salt, or sugar). Please note that the European market prohibits the promotion of HFSS foods to underage users.  |
#| operating_systems| string[] |Device operating systems that you want to target.  Enum values: `ANDROID`, `IOS`, `PC`.|
#| network_types |string[]| Device connection types that you want to target. Default value: `unlimited`. For enum values, see [Enumeration - Connection Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|device_model_ids| string[]| IDs of the device models that you want to target. Currently only brand-level model IDs are supported. For enum values of device model IDs on different levels, please see [Device Models](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369).|
#| device_price_ranges|number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50. 
**Important**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].|
#| carrier_ids |string[]| Carriers that you want to target. A carrier is valid only when the `in_use` field for the carrier is `true`. The carriers must be consistent with the location(s) that you want to target. For enum values (`carrier_id`), see [Get Carriers](https://ads.tiktok.com/marketing_api/docs?id=1737168013095938). |
#| interest_category_ids |string[]|List of interest categories that you want to target. Use [/tool/interest_category/](https://ads.tiktok.com/marketing_api/docs?id=1737174348712961) endpoint to get the complete list of interest categories.|
#| rf_purchased_type  | string | Buying type. Enum values: 
- `FIXED_SHOW`: Purchase to achieve a fixed amount of impressions.
- `FIXED_REACH`: Purchase to reach a fixed number of users.
- `FIXED_BUDGET`: Purchase with a fixed budget.|
#| budget  | float | Budget. Please fill in this number based on the data returned via the ad inventory estimate API. |
#| purchased_impression | number | Impressions to be purchased, **in the unit of 1,000**. |
#| purchased_reach  | number | Purchased user reach, **in the unit of 1,000**. |
#| schedule_start_time | string | Schedule start time (UTC+0), in the format of  `YYYY-MM-DD HH:MM:SS`.|
#| schedule_end_time | string | Schedule end time (UTC+0), in the format of `YYYY-MM-DD HH:MM:SS`.|
#|frequency |number| `frequency`, together with `frequency_schedule`, controls how often people see your ad (only available for `REACH` ads). 
For example, `frequency` = 2 & `frequency_schedule` = 3 means "show ads no more than twice every 3 days". |
#|frequency_schedule |number| `frequency_schedule`, together with `frequency`, controls how often people see your ad (only available for `REACH` ads). See `frequency` field for more. |
#|optimization_goal  | string |The measurable results you'd like to drive with your ads. It must be aligned with the value for `objective_type` on the campaign level. Enum values: `REACH`, `VIDEO_VIEW`, `CLICK`, `POST_ENGAGEMENT`, `INSTALL`.|
#|cpv_video_duration  | string | The target video view duration. 

Enum value:  `SIX_SECONDS`. |
#|brand_safety_type|string|Brand safety type for Reach and Frequency ads. Enum values: 
- `NO_BRAND_SAFETY`:  To not use any brand safety solution.  Full inventory, which means your ads may appear next to some content featuring mature themes. 
- `EXPANDED_INVENTORY`: Use TikTok's brand safety solution. Expanded inventory means that your ads will appear next to content where most inappropriate content has been removed, and that does not contain mature themes. In the next API version, `EXPANDED_INVENTORY` will replace `NO_BRAND_SAFETY` and will be the default brand safety option.
- `STANDARD_INVENTORY`: Use TikTok's brand safety solution. Standard inventory means that ads will appear next to content that is appropriate for most brands. 
- `LIMITED_INVENTORY`: Use TikTok's brand safety solution. Limited inventory means that your ads will not appear next to content that contains mature themes.
- `THIRD_PARTY`: Use a third-party brand safety solution.  To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. |
#|brand_safety_partner|string|Brand safety partner for Reach and Frequency ads. Available only when `brand_safety_type` is `THIRD_PARTY`. Enum values: `IAS`, `OPEN_SLATE`(The partner is named **DoubleVerify** on TikTok Ads Manager because the partner has been acquired by DoubleVerify).|
#|category_exclusion_ids|string[]|Content exclusion category IDs.|
#|video_download_disabled|boolean| Whether users can download your video ads on TikTok(cannot be updated once created).  Default value: `false`.|
#|feed_type |string| Feed type option. Enum values: `STANDARD_FEED`, `TOP_FEED`. `STANDARD_FEED` refers to large inventory with normal CPM price while `TOP_FEED`refers to limited inventory with higher CPM price. |
#|delivery_mode |string| The strategy for sequencing and scheduling your ad delivery. 

Enum values:
- `STANDARD`: Standard delivery. Your ads will be distributed evenly and are expected to achieve similar traffic size. 
- `SCHEDULE`: Scheduled delivery.  Set specific time periods to deliver each ad in.  
- `SEQUENCE`: Sequenced delivery. Set a specific sequence to deliver your ads in. 
- `OPTIMIZE` (Deprecated): Optimized delivery that delivers ads to achieve the best performance.|
#|schedule_infos |object[]| Ad delivery information. |
##|schedules |object[]| The details of the scheduled delivery for the ad. |
###|start_time |string| Ad delivery start time. |
###|end_time |string| Ad delivery end time. |
##|expected_orders |number[]| The delivery order for an ad within the ad group.
 
For example, a value of `[1]` indicates that the ad will be delivered first.|
##|is_draft|boolean|Whether the ad delivery information is in draft mode.
 
If the value of this field is `true`, then the ad delivery information defined in the request has not been associated with any specific ads. 
 
To associate the ad delivery information with ads, pass the value of the returned `schedule_id` to the request parameter `schedule_id` in [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). After you associate the ad delivery information with an ad, the value of this field will automatically be set to `false`, and the value of `schedule_id` will be the ID of the ad that you have associated the ad delivery information with.|
##|schedule_id|string|Schedule ID.
 
 If the value of `is_draft` is `true`, then the ad delivery information defined in the request has not been associated with any specific ads. 
 
To associate the ad delivery information with ads, pass the value of this field to the request parameter `schedule_id` in [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). After you associate the ad delivery information with an ad, the value of `is_draft` will automatically be set to `false`, and the value of this field will be the ID of the ad that you have associated the ad delivery information with.|
#|notice|string|System notice.|
#|contextual_tag_ids |string[]|Contextual tag IDs. |
```

### Example

``` xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 40002,
    "message": "This campaign has been deleted.",
    "request_id": "{{request_id}}",
    "data": {}
}
(/code);
```
