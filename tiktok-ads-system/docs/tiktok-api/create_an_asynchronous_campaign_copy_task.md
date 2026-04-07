# Create an asynchronous campaign copy task

**Doc ID**: 1788434394151938
**Path**: API Reference/Campaign/Create an asynchronous campaign copy task

---

Use this endpoint to create an asynchronous campaign copy task. 

You can only copy one campaign at a time. To learn about the detailed steps, see [Copy a campaign](https://business-api.tiktok.com/portal/docs?id=1788434533212162). After you create the task, use [/campaign/copy/task/check/](https://business-api.tiktok.com/portal/docs?id=1788434463507458) to check the results.

>**Note**

>  
- Asynchronous Campaign Copy API is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- The rate limits for this endpoint are 1 query per second (QPS) and 30 queries per minute (QPM) per developer app. [Global rate limits](https://business-api.tiktok.com/portal/docs?id=1740029171730433#item-link-Global%20rate%20limits) are not applicable to this endpoint. 

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/campaign/copy/task/create/

**Method** POST

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type.
Allowed format: `application/json`.  |
```

**Parameters**

``` xtable
|Field{35%}|Data Type{10%}|Description{55%}|
|--- |--- |--- |
| advertiser_id {Required} | string | Advertiser ID. |
| campaign_id {Required} | string | The ID of the campaign that you want to copy.  

**Note**: 
- You cannot copy existing GMV Max Campaigns with customized TikTok posts. To check whether the campaign contains customized TikTok posts, use [/campaign/gmv_max/info/](https://business-api.tiktok.com/portal/docs?id=1822000968821762) and check whether the returned `custom_anchor_video_list` is `[]`.
- You cannot copy iOS Dedicated Campaigns with Apps that have not activated the SAN module on your MMP. To ensure that TikTok SAN integration is enabled for your App, see [How to transition to SAN for existing apps](https://ads.tiktok.com/help/article/transition-to-san-for-existing-apps) and [How to integrate to SAN for new apps](https://ads.tiktok.com/help/article/integrate-to-san-for-new-apps).   
- Starting September 30, 2024, you will no longer be able to copy campaigns that contain [Playable Ads](https://business-api.tiktok.com/portal/docs?id=1737730803189826) delivered to TikTok placement.
- Only campaigns with the supported advertising objectives (`REACH`, `TRAFFIC`, `VIDEO_VIEWS`, `ENGAGEMENT`, `APP_PROMOTION`, `LEAD_GENERATION`, `WEB_CONVERSIONS`) can be copied.  Ad groups belonging to an `ENGAGEMENT` campaign and with a `promotion_type` of `LIVE_SHOPPING` cannot be copied.
-  Ad groups belonging to an `ENGAGEMENT` campaign and with an `optimization_goal` of `PAGE_VISIT` cannot be copied.
-  Smart+ Campaigns are not supported.
-  The campaign to be copied must have at least one undeleted ad group with at least one undeleted ad.
-  The campaign to be copied should not exceed a limit of 20 undeleted ad groups, with a maximum of 50 undeleted ads per ad group.
-  You cannot copy Automated Creative Optimization (ACO) ad groups in the campaign, but you can copy Smart Creative ad groups.
-  If you copy a campaign that contains ad groups bound to a split test, only the ad groups will be copied. Split test groups associated with those ad groups will not be created. |
| request_id {Required} | string | Request ID that supports idempotency to prevent you from sending the same request twice. 
If you retry requests with the same request ID multiple times within the 10-second cache time, then only one request will succeed. If a duplicate request with the expired request ID is received after the cache time, the server will treat it as a new request and process it accordingly. 

It is different from the `request_id` returned in the response parameters, which is used to uniquely identify an HTTP request. 

The value should be a string representation of a 64-bit integer. 

Example: `"123456789"`. |
| operation_status | string | The status of the new campaign when created. 

 Enum values: 
-  `ENABLE`: The campaign is enabled when created. 
- `DISABLE`: The campaign is disabled when created. 
Default value: `DISABLE`. 

If you want to update the status of the campaign after creation, use [/campaign/status/update/](https://business-api.tiktok.com/portal/docs?id=1739320994354178). |
|virtual_objective_type|string|The new objective type.

Enum value: `SALES`.

Use this field to create a campaign with the Sales objective, the combined objective for Website Conversions and Product Sales objectives. Learn more about [the Sales objective](https://business-api.tiktok.com/portal/docs?id=1834189283112962).|
|sales_destination{+Conditional}|string|Required and valid only when `virtual_objective_type` is specified.

Sales destination, the destination where you want to drive your sales.

Enum values: 
- `TIKTOK_SHOP`: TikTok Shop. Drive sales on your TikTok Shop.
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).|
| campaign_name | string | The name for the new campaign. 

Length limit: 512 characters. Emojis are not supported. 
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character. 

If not specified, this field will default to `"COPIED_{{name_of_the_original_campaign}}"`. For instance, if the original campaign is named `"FIRST_CAMPAIGN"` and this field is not specified, the name of the new campaign will be `"COPIED_FIRST_CAMPAIGN"`. |
| is_advanced_dedicated_campaign | boolean | Whether to enable the Advanced Dedicated Campaign setting for the new campaign. Advanced Dedicated Campaigns leverage advanced delivery models that benefit from real-time signals. 

To learn about how to create such campaigns, see [Create Advanced Dedicated Campaigns](https://business-api.tiktok.com/portal/docs?id=1797011827608577). 

Enum values: `true`, `false`. 
If this field is not passed, the new campaign will inherit the same Advanced Dedicated Campaign setting as the original campaign.

**Note**: Once set, this field cannot be updated. |
| budget | number | The budget for the new campaign. 

If not specified, this field will default to the budget of the original campaign. 

To learn about the minimum budget and how to set budget modes, see [Budget](https://business-api.tiktok.com/portal/docs?id=1739381246298114). To obtain the daily budget value range for a currency, see [Currency-Daily budget value range](https://business-api.tiktok.com/portal/docs?id=1737585839634433). |
| rta_id | string | Realtime API (RTA) ID, the RTA strategy identifier. 

To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative. 
To learn about the prerequisites for and the steps of enabling RTA for your ads, see [Realtime API](https://business-api.tiktok.com/portal/docs?id=1805437148769281). 

**Note**: Enabling RTA for your ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. You will need to complete the onboarding process to be able to receive and respond to RTA requests sent to your system first. |
|po_number|string|PO (purchase order) number.
PO numbers are useful for invoice tracking and reconciliation.

[Learn more about PO numbers on monthly invoices](https://ads.tiktok.com/help/article/update-po-number-on-monthly-invoices).|
| schedule_type | string | 
-  Specify this field only when you want to set the same schedule for all ad groups in the new campaign. 
-  If you want to set schedules separately for each ad group in the new campaign, you can pass the `schedule_type` within the object array `adgroup_list` instead.   
 Schedule type for all new ad groups. 
 
 Enum values: 
- `SCHEDULE_START_END`: Set start time and end time to run ad groups. You need to pass both `schedule_start_time` and `schedule_end_time` at the same time.
- `SCHEDULE_FROM_NOW`: Set start time to run ad groups continuously. You need to pass `schedule_start_time` and the end time will be automatically set to 10 years later than the start time.  |
| schedule_start_time {+Conditional} | string | Required when `schedule_type` is passed. 
 
Schedule start time (UTC+0) for all new ad groups, in the format of `"YYYY-MM-DD HH:MM:SS"`. 

The start time can be up to 12 hours earlier than the current time, but cannot be later than `"2028-01-01 00:00:00"`. |
| schedule_end_time {+Conditional} | string |
-  Required when `schedule_type` is `SCHEDULE_START_END`. 
-  Not supported when `schedule_type` is `SCHEDULE_FROM_NOW`.  
 Schedule end time (UTC+0) for all new ad groups, in the format of `"YYYY-MM-DD HH:MM:SS"`.

 The end time cannot be later than `"2038-01-01 00:00:00"`. |
| deep_copy_mode | string | The copying mode, which determines how ad groups and ads are created in the new campaign. 

Enum values: 
- `DEFAULT`: Default copy mode. This mode copies all undeleted ad groups and ads from the original campaign to the new campaign. The field `adgroup_list` will be ignored.
-  `CUSTOM`: Custom copy mode. This mode only copies the specified undeleted ad groups and ads from the original campaign to the new campaign.  In this mode, you need to provide the field `adgroup_list` simultaneously. The maximum number of ads that can be copied is 50 ads per ad group, with a maximum of 20 ad groups. 
Default value: `DEFAULT`. |
| adgroup_list {+Conditional} | object[] | 
-  When `deep_copy_mode` is set to `DEFAULT` or not passed, this field is ignored. 
-  When `deep_copy_mode` is set to `CUSTOM`, this field is required. 
The customized settings for ad groups in the new campaign. 

Max size: 20. |
#| adgroup_id {+Conditional} | string | Required when `adgroup_list` is passed. 

The ID of the ad group that you want to copy. The ad group should belong to the original campaign (`campaign_id`). 

-  If the ad group is a non-ACO non-Smart Creative ad group, you need to specify `ad_list` within the `adgroup_id` object array. 
-  If the ad group is a Smart Creative ad group, you don't need to specify `ad_list` within the `adgroup_id` object array, but you have the option to pass `smart_creative_info` to customize the ad creatives used to generate Smart Creative ads in the new ad group. 
**Note**: 
- Starting July 19th, 2025, you will no longer be able to create or copy ad groups using the TikTok Lite subplacement (`TIKTOK_LITE`). To ensure a smooth and uninterrupted ad creation experience, we recommend that you avoid creating new ad groups with this subplacement or copying campaigns that contain such ad groups.
- Starting November 30th, 2024, you will no longer be able to create or copy ad groups with the optimization goal "Install with in-app event" on TikTok placement or Automatic Placement. This change affects ad groups with the following configuration: At the campaign level: `objective_type` is `APP_PROMOTION`
- At the ad group level:`optimization_goal` is `INSTALL` and a valid `secondary_optimization_event` value is specified 
- `placement_type` is `PLACEMENT_TYPE_NORMAL` with `placements` as `["PLACEMENT_TIKTOK"]`, or `placement_type` is `PLACEMENT_TYPE_AUTOMATIC`  
- Existing "Install with in-app event" ad groups on TikTok placement will not be affected. Additionally, Pangle placement and Global App Bundle placement (where `placement_type` is `PLACEMENT_TYPE_NORMAL` and `placements` includes only `PLACEMENT_PANGLE` or `PLACEMENT_GLOBAL_APP_BUNDLE` or both) will not be impacted. Please be aware of this change and make appropriate adjustments to your integration if necessary.
- You cannot copy ad groups with Apps that have not activated the SAN module on your MMP. To ensure that TikTok SAN integration is enabled for your App, see [How to transition to SAN for existing apps](https://ads.tiktok.com/help/article/transition-to-san-for-existing-apps) and [How to integrate to SAN for new apps](https://ads.tiktok.com/help/article/integrate-to-san-for-new-apps).|
#| operation_status| string | The status of the new ad group when created. 

 Enum values: 
-  `ENABLE`: The ad group is enabled when created.
- `DISABLE`: The ad group is disabled when created. 
Default value: `ENABLE`. 

If you want to update the status of the ad group after creation, use [/adgroup/status/update/](https://business-api.tiktok.com/portal/docs?id=1739591716326402). |
#| adgroup_name| string | The name for the new ad group. 

 Length limit: 512 characters. Emojis are not supported. 
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character. 

 If not specified, this field will default to the name of the original ad group. |
#| automated_keywords_enabled | boolean | Valid only when at the campaign level `is_search_campaign` is `true`.

Whether to enable automated keywords and let the system automatically generate keywords after you add ads. This expands high-quality traffic to improve performance. View high-performing automated keywords in reporting.

Supported values: `true`, `false`.
Default value: `false`.

**Note**: 
- Automated keywords in Search Ads Campaigns are currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.|
#| location_ids| string[] | IDs of the locations that the new ad group targets. 

Max size: 3,000. If you provide both `location_ids` and `zipcode_ids`, the combined total of location IDs, zip code IDs, and postal code IDs cannot exceed 3,000 per ad group.

To get the available locations and corresponding IDs based on your placement and objective, use [/tool/region/](https://business-api.tiktok.com/portal/docs?id=1737189539571713) or [/tool/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1761236883355649). 
To get the list of location IDs, see [Location IDs](https://business-api.tiktok.com/portal/docs?id=1739311040498689). 
 
**Note**:  Overlapping targeted locations are not supported. For instance, you cannot target the U.S. and the state of California at the same time.
- If you target locations in the US via `location_ids` or `zipcode_ids` during ad group creation, you can subsequently update those IDs to other US locations but you cannot remove all US locations to target only non-US countries.
- If you copy an existing ad group with `TIKTOK_LITE` specified in the `tiktok_subplacements` value, you cannot exclude Japan and South Korea from the targeted locations (`location_ids`) of the new ad group.|
#| zipcode_ids| string[] | Zip code IDs or postal code IDs that the new ad group targets. 

Max size: 3,000. If you provide both `location_ids` and `zipcode_ids`, the combined total of location IDs, zip code IDs, and postal code IDs cannot exceed 3,000 per ad group.

You can get the available zip code IDs or postal code IDs based on your placement, objective and keyword via `geo_id` (when `geo_type` = `ZIP_CODE`) returned from the [/tool/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1761236883355649) endpoint. 

**Note**: 
-  Zip code targeting is currently only supported for the US and postal code targeting is currently only supported for Canada, Brazil, Indonesia, Thailand, and Vietnam.
- Targeting postal code areas in Brazil, Indonesia, Thailand, and Vietnam is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- You cannot use zip code targeting in campaigns that have enabled special ad categories (`special_industries`).
-  You cannot use zip code targeting or postal code targeting in campaigns with the `objective_type` as `RF_REACH`.
- You can only use zip code targeting or postal code targeting on TikTok placement. Therefore, the `placements` value needs to include `PLACEMENT_TIKTOK`.
-  Overlapping targeted locations are not supported. For instance, you cannot target the US and the state of California at the same time.
- If you target locations in the US via `location_ids` or `zipcode_ids` during ad group creation, you can subsequently update those IDs to other US locations but you cannot remove all US locations to target only non-US countries. 
-  To get information about the zip code IDs or postal code IDs, you can only use [/tool/targeting/info/](https://business-api.tiktok.com/portal/docs?id=1761237001980929).|
#| audience_ids | string[] | The list of audience IDs that the new ad group targets. 

To get audience IDs, use [/dmp/custom_audience/list/](https://business-api.tiktok.com/portal/docs?id=1739940506015746). |
#| excluded_audience_ids | string[] | The list of audience IDs to be excluded for the new ad group. 

 To get audience IDs, use [/dmp/custom_audience/list/](https://business-api.tiktok.com/portal/docs?id=1739940506015746). |
#| age_groups | string[] | Age groups that the new ad group targets. 

For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138#item-link-Age%20Group). 

In certain scenarios, creation of ad groups that target the age group 13-17 (`AGE_13_17`) in the US, Latin America, the European Economic Area, the UK, Switzerland, or Canada will not be allowed. See [New age restrictions for ads on TikTok](https://business-api.tiktok.com/portal/docs?id=1788755983247362) to learn more. 
If you use targeting options that are not supported for the age group 13-17 in the US, Latin America, the European Economic Area, the UK, Switzerland, or Canada and leave the `age_groups` field unspecified or set it as `[]`, the field will default to `["AGE_18_24", "AGE_25_34", "AGE_35_44", "AGE_45_54", "AGE_55_100"]`. 

**Note**: If the ad group targets the age group 13-17 (`AGE_13_17`) in the US, Latin America, the European Economic Area, the UK, Switzerland, or Canada and you typically leave the `age_groups` field unspecified or set it as `[]`, we recommend that you explicitly specify the exact age groups that you want to target, such as `AGE_18_24`, in the field. |
#| budget | number | The budget for the new ad group. 

To learn about the minimum budget and how to set budget modes, see [Budget](https://business-api.tiktok.com/portal/docs?id=1739381246298114). To obtain the daily budget value range for a currency, see [Currency-Daily budget value range](https://business-api.tiktok.com/portal/docs?id=1737585839634433). |
#| schedule_type {+Conditional} | string | Required when you want to customize the schedule settings of the new ad group. 

Schedule type for the new ad group. 
 
 Enum values: 
- `SCHEDULE_START_END`: Set start time and end time to run ad groups. You need to pass both `schedule_start_time` and `schedule_end_time` at the same time.
- `SCHEDULE_FROM_NOW`: Set start time to run ad groups continuously. You need to pass `schedule_start_time` and the end time will be automatically set to 10 years later than the start time.  |
#| schedule_start_time {+Conditional} | string | Required when `schedule_type` within the `adgroup_list` object array is passed. 
 
Schedule start time (UTC+0) for the new ad group, in the format of `"YYYY-MM-DD HH:MM:SS"`. 

The start time can be up to 12 hours earlier than the current time, but cannot be later than `"2028-01-01 00:00:00"`. |
#| schedule_end_time {+Conditional} | string |
-  Required when `schedule_type` within the `adgroup_list` object array is `SCHEDULE_START_END`. 
-  Not supported when `schedule_type` within the `adgroup_list` object array is `SCHEDULE_FROM_NOW`.  
 Schedule end time (UTC+0) for the new ad group, in the format of `"YYYY-MM-DD HH:MM:SS"`.

 The end time cannot be later than `"2038-01-01 00:00:00"`. |
#| ad_list {+Conditional} | object[] | 
-  When `deep_copy_mode` is set to `DEFAULT` or not passed, this field is ignored.
-  When `deep_copy_mode` is set to `CUSTOM` and the original ad group (`adgroup_id`) is a non-ACO non-Smart Creative ad group, this field is required.  If you don't want to customize the settings of the ads to be generated in the new ad group, only pass `ad_id` in this object array. 
-  If you want to customize the settings of the ads to be generated in the new ad group, pass `ad_id` and other parameters simultaneously in this object array.   
 The settings for ads in the new non-ACO non-Smart Creative ad group. 

Max size: 50. |
##| ad_id {+Conditional} | string | Required} when `ad_list` is passed. 

The ID of the ad that you want to copy. The ad should belong to the original ad group (`adgroup_id`). |
##| operation_status | string | The status of the new ad when created. 

Enum values: 
-  `ENABLE`: The ad is enabled when created.
- `DISABLE`: The ad is disabled when created.
Default value: `ENABLE`. 

If you want to update the status of the ad after creation, use [/ad/status/update/](https://business-api.tiktok.com/portal/docs?id=1739953422970882). |
##| ad_name | string | The name for the new ad. 

Length limit: 512 characters. Emojis are not supported. 
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character. 

If not specified, this field will default to `"COPIED_{{{ {name_of_the_original_ad}}_{ {ID_of_the_original_ad}}"`. For instance, if the original ad is named `"FIRST_AD"` with the ad ID 1234567891234567, and this field is not specified, the name of the new ad will be `"COPIED_FIRST_AD_1234567891234567"`. |
##| identity_type | string | Identity type. 

Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`. 
For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097).  |
##| identity_id | string | Identity ID. 

If you are not using Spark Ads, `identity_id` and `identity_type` (`CUSTOMIZED_USER`) can be used for better management of ads information.  |
##| identity_authorized_bc_id {+Conditional} | string | Required when `identity_type` is `BC_AUTH_TT`. 

ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
##| ad_format {+Conditional} | string | The ad format. 

Enum values: 
- `SINGLE_VIDEO`: single video.
- `SINGLE_IMAGE`: single image.
-  `CAROUSEL_ADS`: Standard Carousel.

-  If you want to copy the original ad into a TikTok Standard Carousel ad, this field is required and must be set to `CAROUSEL_ADS`. 
-  If you want to copy a TikTok Standard Carousel ad into a single video ad or a single image ad, this field is required as well.  |
##| video_id | string | Video ID. 

 To obtain video IDs, use [/file/video/ad/search/](https://business-api.tiktok.com/portal/docs?id=1740050472224769).

 If you want to create Spark Ads, you can use `video_id` or `tiktok_item_id`. To learn more about Spark Ads, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298). |
##| image_ids | string[] | A list of image IDs (images used in an ad or as a video cover). 

To obtain the image IDs, use [/file/image/ad/search/](https://business-api.tiktok.com/portal/docs?id=1740052016789506) or [/file/image/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1739067433456642). |
##| music_id | string | The ID of the piece of music that you want to use in the TikTok Carousel Ad. 

 To learn about how to get music that can be used in TikTok Carousel Ads, see [Create Carousel Ads](https://business-api.tiktok.com/portal/docs?id=1766217791987713). |
##| tiktok_item_id | string | The ID of the TikTok post to be used as a Spark Ad. 

To learn more about Spark Ads, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298). 

Pass in the `item_id` you get from the response of [/tt_video/info/](https://business-api.tiktok.com/portal/docs?id=1738376324021250) or [/identity/video/get/](https://business-api.tiktok.com/portal/docs?id=1740218475032577). 

**Note**: By using Spark Ads, you confirm that you have the rights to use the music in the videos for commercial purposes. |
##| ad_text | string | An ad text. It is shown to your audience as part of your ad creative, to deliver the message you intend to communicate to them. 

 If you don't know how to create effective ad texts, you can try the [Smart Text](https://business-api.tiktok.com/portal/docs?id=1739084248002626) feature, which generates ad text recommendations based on the industry and language. 

 Length limit: 100 characters. Emojis are not supported. 
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character. |
##| aigc_disclosure_type | string | Whether to turn on the AIGC (Artificial Intelligence Generated Content) self-disclosure toggle to indicate the ad contains AI-generated content. After the toggle is turned on, your ad will carry an "Advertiser labeled as Al-generated" label when viewed in full. 

 Enum values: 
- `SELF_DISCLOSURE`: To turn on the toggle to declare that the ad contains AI-generated content. 
- `NOT_DECLARED`: To not declare that the ad contains AI-generated content.Default value: `NOT_DECLARED`.

To learn about the supported advertising objectives and ad formats for the toggle and the detailed steps for using the toggle, see [AIGC self-disclosure toggle](https://business-api.tiktok.com/portal/docs?id=1799186631031809).|
##| creative_auto_enhancement_strategy_list | string[] | The list of automatic enhancement strategies to apply to your ads.
The enhancements you specified will be automatically applied in real-time as your campaign is delivered.

Enum values:
- `VIDEO_QUALITY`: Video quality. Improve overall visual quality with increased resolution and clarity.
- `MUSIC_REFRESH`: Music refresh. Stay on-trend by swapping in music currently popular on TikTok.
- `IMAGE_QUALITY`: Image quality. Improve overall visual quality with increased resolution and clarity.
- `IMAGE_RESIZE`: Resize. Resize your image to take advantage of full-screen capabilities.
The default value for this field is determined by your allowlist status for the "automatic enhancements enabled by default" feature:
- If you are allowlisted for certain strategies to be enabled by default, this field will default to a list of those strategies.For example, if you are allowlisted for all these strategies to be enabled by default, this field will default to `["MUSIC_REFRESH","VIDEO_QUALITY","IMAGE_QUALITY","IMAGE_RESIZE"]`. 
- If you are not allowlisted for any strategies to be enabled by default, this field will default to an empty list (`[]`).
To learn about the scenarios where you can enable this setting, see [Availability of Automatic Enhancements for Manual Ads](https://business-api.tiktok.com/portal/docs?id=1855450880142402#item-link-For%20Manual%20Ads).

**Note**: Automatic enhancements are available to all advertisers. However, having them turned on by default is currently a separate allowlist-only feature for each enhancement. If you would like to access it, please contact your TikTok representative. 
|
##| tracking_pixel_id | string | The pixel ID that you'd like to track. You can use this field to track offsite events. 

It supports the following campaign objectives for Auction ads: `REACH`, `VIDEO_VIEWS`, `TRAFFIC`, `WEB_CONVERSIONS`, `LEAD_GENERATION`, `APP_PROMOTION`, and `ENGAGEMENT`.  
-  For Auction objectives: If `pixel_id` is specified at the ad group level and you want to use pixel to track offsite events, then the pixel ID you pass in the `tracking_pixel_id` field must be the same ID that you specified in the `pixel_id` field for the ad group. Otherwise, you can pass in any pixel ID that you'd like to track in the `tracking_pixel_id` field. |
##| tracking_app_id | string | The ID of the application that you want to track. You can use this field to track offsite app events. 

It supports the following campaign objectives for Auction ads: `REACH`, `VIDEO_VIEWS`, `TRAFFIC`, `WEB_CONVERSIONS`, `LEAD_GENERATION`, `APP_PROMOTION`, and `ENGAGEMENT`.

 If `app_id` is specified at the ad group level and you want to track offsite app events, then the application ID you pass via this field must be the same ID that you specified at the ad group level. Otherwise, you can pass in any application ID that you'd like to track via this field. You can get application ID (`app_id`) via [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). |
#| smart_creative_info | object | 
-  When `deep_copy_mode` is set to `DEFAULT` or not passed, this field is ignored.
-  When `deep_copy_mode` is set to `CUSTOM` and the original ad group (`adgroup_id`) is a Smart Creative ad group, this field is optional.  If you want the ads in the new ad group to be generated based on the same ad creatives in the original ad group, do not pass this field. 
-  If you want to customize the ad creatives used to generate Smart Creative ads in the new ad group, pass this field.  
 The ad creatives used to generate Smart Creative ads in the new Smart Creative ad group. 

**Note**: Smart Creative only supports `APP_PROMOTION`, `WEB_CONVERSIONS`, `TRAFFIC`, or `LEAD_GENERATION` as advertising objective (`objective_type`) at the campaign level. |
##| media_info_list{+Conditional} | object[] | Required when `smart_creative_info` is passed. 

List of media information. 

Max size: 30. |
###| media_info {+Conditional} | object | Required when `media_info_list` is passed. 

Material information. |
####| image_info| object[] | Image information. 
-  When you want to upload image materials (`video_info` is NOT included in the request), this field will be used as image materials. 
-  When you want to upload video materials (`video_info` is included in the request), this field will be used as the video cover. Only one picture can be submitted to each `image_info` object array.|
#####| web_uri{+Conditional} | string | Required when `image_info` is passed. 

 Image ID. 

You can find the image ID in the response after you upload an image via the [/file/image/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1739067433456642) endpoint. |
#####| file_name | string | Image name. 

 Length limit: 100 characters. 

 If image materials are used, this field is used to form the ad's name. To learn about the ad name generation rules, see [Ad name generation rules](https://business-api.tiktok.com/portal/docs?id=1739473063234626#item-link-Ad%20name%20generation%20rules). |
####| video_info| object | Video information. |
#####| video_id{+Conditional} | string | Required when `video_info` is passed. 

Video ID. 

You can get the video ID after you upload a video using the [/file/video/ad/upload/](https://ads.tiktok.com/marketing_api/docs?id=1737587322856449) endpoint. |
#####| file_name | string | Video name. 

Length limit: 100 characters. 

If video materials are used, this field is used to form the ad's name. To learn about the ad name generation rules, see [Ad name generation rules](https://business-api.tiktok.com/portal/docs?id=1739473063234626#item-link-Ad%20name%20generation%20rules). |
####| aigc_disclosure_type | string | Whether to turn on the AIGC (Artificial Intelligence Generated Content) self-disclosure toggle to indicate the ad contains AI-generated content. After the toggle is turned on, your ad will carry an "Advertiser labeled as Al-generated" label when viewed in full. 

 Enum values: 
- `SELF_DISCLOSURE`: To turn on the toggle to declare that the ad contains AI-generated content. 
- `NOT_DECLARED`: To not declare that the ad contains AI-generated content.Default value: `NOT_DECLARED`.

To learn about the supported advertising objectives and ad formats for the toggle and the detailed steps for using the toggle, see [AIGC self-disclosure toggle](https://business-api.tiktok.com/portal/docs?id=1799186631031809). |
####| tiktok_item_id | string | The ID of the TikTok post to be used as a Spark Ad. 

Pass in the `tiktok_item_id` you get from the response of the [/tt_video/info/](https://ads.tiktok.com/marketing_api/docs?id=1738376324021250) or [/identity/video/get/](https://ads.tiktok.com/marketing_api/docs?id=1740218475032577) endpoint. 

**Note**: 
-  By using Spark Ads, you confirm that you have the rights to use the music in the videos for commercial purposes. 
-  Once you pass in `tiktok_item_id`, you don't have to pass in the objects `image_info`, `video_info`, and `title_list`.  |
####| identity_id {+Conditional} | string | Required when `tiktok_item_id` is passed. 

 Identity ID. |
####| identity_type {+Conditional} | string | Required when `tiktok_item_id` is passed. 

Identity type. 

 Enum values: `AUTH_CODE`, `TT_USER`. 

For details about identities, see [Identities](https://ads.tiktok.com/marketing_api/docs?id=1738958351620097). |
##| title_list | object[] | List of ad titles (also called ad texts). Ad titles are shown to your audience as part of your ad creative, to deliver the message you intend to communicate to them. 

Max size: 5. |
###| title {+Conditional} | string | Required when `title_list` is passed. 

Ad title (ad text). If you don't know how to create effective ad texts, you can try the [Smart Text](https://ads.tiktok.com/marketing_api/docs?id=1739084248002626) feature, which generates ad text recommendations based on the industry and language. 

 An ad text must be 12-40 characters long and cannot contain emojis.
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character. |
##| call_to_action_list | object[] | Call-to-action list. 

Max size: 3. 

**Note**: For TikTok ads, either this field or `call_to_action_id` must be specified. If both are specified, this field will be ignored. |
###| call_to_action {+Conditional} | string | Required when `call_to_action_list` is passed. 

Call-to-action text. 

 For enum values, see [Enumeration - Call-to-action](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
##| deeplink_list | object[] | List of deeplinks. 

Max size: 1. |
###| deeplink | string | The specific location where you want your audience to go if they have your app installed. |
###| deeplink_type | string | The deeplink type. 

Enum values: 
-  `NORMAL`: non-deferred deeplink.
- `DEFERRED_DEEPLINK`: deferred deeplink. 
Default value: `NORMAL`. 

To learn about the supported scenarios for non-deferred deeplinks and deferred deeplinks, see the "[Deeplink - Availability – Deeplink](https://business-api.tiktok.com/portal/docs?id=1779541971843073#item-link-Availability)" section. 

**Note**: Deferred deeplinks are not supported in Dedicated Campaigns. Therefore, if the `campaign_type` of the campaign that the ad belongs to is `IOS14_CAMPAIGN`, you cannot set this field to `DEFERRED_DEEPLINK`. |
##| display_name_list |object[] | List of display names. 

You can include only one `app_name` or `landing_page_name` in each `display_name_list`. |
###| app_name | string | App name that is displayed in the ad. 

 If not specified, the name in the App Store will be used. 

Length limit: 40 characters. |
###| landing_page_name | string | The display name of the landing page. 

Length limit: 40 characters. |
##| page_list | object[]| List of page IDs. 

Max size: 3. |
###| page_id {+Conditional} | string | Required when `page_list` is passed. 

Page ID. 

- To obtain pages within your ad account, use [/page/get/](https://business-api.tiktok.com/portal/docs?id=1820826387779586).
- To create instant pages, use [Instant Page Editor SDK](https://business-api.tiktok.com/portal/docs?id=1740307202170881).|
##| card_list | object[] | List of creative portfolio IDs. 

 Max size: 1. |
###| card_id | string | Pass the ID of one of the following creative portfolio types: 
-  Countdown Sticker.
-  Gift Code Sticker.
-  Display Card.
-  Download Card.
To create a creative portfolio, use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426). 
-  To learn about how to get the ID of a Display Card, or Download Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058).
-  To learn about how to get the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177).  |
##| landing_page_urls {+Conditional} | object[] | Required when `fallback_type` is set to `WEBSITE`. 

List of landing page URLs. 

Max size: 1. |
###| landing_page_url {+Conditional} | string | Required when `landing_page_urls` is passed. 

Landing page URL. |
##| common_material | object | Common material. |
###| identity_id | string | Identity ID. |
###| identity_type| string | Identity type. 

Enum values: `CUSTOMIZED_USER`. 

For details about identities, see [Identities](https://ads.tiktok.com/marketing_api/docs?id=1738958351620097). |
###| ad_name | string | Ad name. 

Length limit: 512 characters. Emojis are not supported. 
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character. 

Set as `""` (empty string) for it to be automatically generated. The format of auto-generated ad name is creative name + creation time (e.g. adcreative20210111190739). 

To learn about how the ad name is generated, see the section "[Ad name generation rules](https://business-api.tiktok.com/portal/docs?id=1739473063234626#item-link-Ad%20name%20generation%20rules)". 
 
**Note**: If you don't specify an ad name here, you will not be able to change the name via [/ad/aco/update/](https://business-api.tiktok.com/portal/docs?id=1739473077112833). |
###| call_to_action_id | string | The ID of the CTA portfolio that you want to use in your ads. 

A CTA portfolio is a group of auto-optimized CTAs. For details about auto-optimized CTAs, see [CTA recommendations > Dynamic CTAs](https://ads.tiktok.com/marketing_api/docs?id=1740307296329730). 

**Note**: If both this field and `call_to_action_list` are specified, `call_to_action_list` will be ignored. |
###| creative_authorized | string | Whether you grant displaying some of your ads in our TikTok for Business Creative Center. Only valid for non-US advertisers, and the default value is `false`. 

**Note**: `creative_authorized` can only be used for video ads. |
###| playable_url | string | Playable material URL. 

 The URL is only valid for Pangle placement. 

 To get the URL, use [/playable/get/](https://ads.tiktok.com/marketing_api/docs?id=1737732758495234). 

Note that all ads in the same ad group share the same playable material. |
###| fallback_type | string | Fallback Type. 

 If the audience do not have the app installed, you can have them fall back to install the app, or to view a specific web page. 

 Enum values: `APP_INSTALL`, `WEBSITE`. If the website is chosen, you need to specify the URL via `landing_page_urls` field.
 
**Note**: Not applicable for Deferred Deeplinks. |
###| tracking_info | object | Tracking information. |
####|impression_tracking_urls|string[]|Default Impression Tracking URL. URL generated by your data partner to track impression events in your ads. Generally, you can find and copy the URL from their platform. 

-  If the partner ID for the App (`app_id` specified at the ad group level) that you want to track is `44` (TikTok Business SDK) or `49` (TikTok App API), you don't need to pass in this field. If you do, this field will be ignored. You can obtain the partner ID of an App through `partner_id` returned from [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786) or [/app/info/](https://ads.tiktok.com/marketing_api/docs?id=1740859272887297).
-  If self-attribution has been enabled for the App (`app_id` specified at the ad group level ) that you want to track and the partner ID for the App is not `44` (TikTok Business SDK) or `49` (TikTok App API), you don't need to pass in this field because this field will default to the Default Impression Tracking URL you have configured for the App, and updates to the URL are not supported. You can check whether self-attribution has been enabled for the App through `self_attribution_enabled` returned from [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786) or [/app/info/](https://ads.tiktok.com/marketing_api/docs?id=1740859272887297).
You can pass in only one URL.|
####| click_tracking_urls|string[]|Click Tracking URL. URL generated by your data partner to track click events in your ads. Generally, you can find and copy the URL from their platform. 

-  If the partner ID for the App (`app_id` specified at the ad group level) that you want to track is `44` (TikTok Business SDK) or `49` (TikTok App API), you don't need to pass in this field. If you do, this field will be ignored. You can obtain the partner ID of an App through `partner_id` returned from [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786) or [/app/info/](https://ads.tiktok.com/marketing_api/docs?id=1740859272887297).
-  If self-attribution has been enabled for the App (`app_id` specified at the ad group level ) that you want to track and the partner ID for the App is not `44` (TikTok Business SDK) or `49` (TikTok App API), you don't need to pass in this field because this field will default to the Click Tracking URL you have configured for the App, and updates to the URL are not supported. You can check whether self-attribution has been enabled for the App through `self_attribution_enabled` returned from [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786) or [/app/info/](https://ads.tiktok.com/marketing_api/docs?id=1740859272887297).
You can pass in only one URL.

Currently Pangle does not support DCM, Sizmek or Flashtalking. |
####|tracking_pixel_id|string| The Pixel ID that you'd like to track. You can use this field to track offsite events. 

 This field supports the following campaign objectives for Auction ads: `TRAFFIC`, `WEB_CONVERSIONS`, `LEAD_GENERATION`, and `APP_PROMOTION`.
- For Auction objectives: 
If `pixel_id` is specified at the ad group level **and** you want to use Pixel to track offsite events, then the pixel ID you pass in the `tracking_pixel_id` field must be the same ID that you specified in the `pixel_id` field for the ad group. Otherwise, you can pass in any Pixel ID that you'd like to track in the `tracking_pixel_id` field. |
####|tracking_app_id | string| The ID of the App that you want to track. You can use this field to track offsite app events. 

 the following campaign objectives for Auction ads: `TRAFFIC`, `WEB_CONVERSIONS`, `LEAD_GENERATION`, and `APP_PROMOTION`.

If `app_id` is specified at the ad group level and you want to track offsite app events, then the App ID you pass via this field must be the same ID that you specified at the ad group level. Otherwise, you can pass in any App ID that you'd like to track via this field.

You can get App IDs (`app_id`) via [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786). |
####| tracking_offline_event_set_ids |string[]| A list of Offline Event set IDs that you want to track. You can use this field to track and measure offline activity from people that see or interact with your ads. 

Max size: 50. 

See [here](https://ads.tiktok.com/marketing_api/docs?id=1758051319816193) to learn more about how to create and manage Offline Event sets. 

**Note**:  Offline Events Tracking is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. 
-  If you are allowlisted for Offline Events Tracking, then existing auto-tracking Offline Event sets have to be tracked under a newly created ad:  You can omit this parameter, then this field will automatically default to the IDs of all the **existing** auto-tracking Offline Event sets under the advertiser account, or 
-  You can manually pass in this parameter. You need to specify via this field at least all the **existing** auto-tracking Offline Event set IDs, and non-auto-tracking ones are optional. To get the IDs of current auto-tracking Offline Event sets, call [/offline/get/](https://ads.tiktok.com/marketing_api/docs?id=1765596808589313) to get all Offline Event set IDs and then select all the auto-tracking ones according to the returned `auto_tracking` parameter. 
-  This field supports the following campaign objectives: `TRAFFIC`, `LEAD_GENERATION`, `APP_PROMOTION`, and  `WEB_CONVERSIONS`. |
```
  
### Example
Depending on your preferences for the copy mode and whether you want to define a shared schedule for new ad groups, you can copy a campaign using any of the following code examples:

#### Default copy mode with no shared schedule for new ad groups
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/copy/task/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "deep_copy_mode": "DEFAULT"
}'
(/code)
```

#### Default copy mode with shared schedule for new ad groups
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/copy/task/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "deep_copy_mode": "DEFAULT",
    "schedule_type":"SCHEDULE_START_END",
    "schedule_start_time":"{{schedule_start_time}}",
    "schedule_end_time":"{{schedule_end_time}}"
}'
(/code)
```

#### Custom copy mode with no shared schedule for new ad groups
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/copy/task/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "deep_copy_mode": "CUSTOM",
    "adgroup_list": [
        {
            "adgroup_id": "{{adgroup_id}}",
            "schedule_type":"SCHEDULE_START_END",
            "schedule_start_time":"{{schedule_start_time}}",
            "schedule_end_time":"{{schedule_end_time}}",
            "ad_list":[{"ad_id":"{{ad_id}}"}]
        },
        {
            "adgroup_id": "{{adgroup_id}}",
            "schedule_type":"SCHEDULE_START_END",
            "schedule_start_time":"{{schedule_start_time}}",
            "schedule_end_time":"{{schedule_end_time}}",
            "ad_list":[{"ad_id":"{{ad_id}}"}]
        }
    ]
}'
(/code)
```

#### Custom copy mode with shared schedule for new ad groups
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/copy/task/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "deep_copy_mode": "CUSTOM",
    "schedule_type":"SCHEDULE_START_END",
    "schedule_start_time":"{{schedule_start_time}}",
    "schedule_end_time":"{{schedule_end_time}}",
    "adgroup_list": [
        {
            "adgroup_id": "{{adgroup_id}}",
            "ad_list":[{"ad_id":"{{ad_id}}"}]
        },
        {
            "adgroup_id": "{{adgroup_id}}",
            "ad_list":[{"ad_id":"{{ad_id}}"}]
        }
    ]
}'
(/code)
```
## Response

``` xtable
|Field{30%}|Type{15%}|Description{55%}|
|-|-|-|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#| task_id | string | ID of the asynchronous campaign copy task.

To check the results of the task, use [/campaign/copy/task/check/](https://business-api.tiktok.com/portal/docs?id=1788434463507458). 

 If errors occur (`adgroup_error_list` is not empty), task ID will not be generated, and the value of this field will be an empty string (`""`). |
#| adgroup_error_list | object[] | The errors encountered during the process of copying specific ad groups.

 If no errors occur, the value of this field will be an empty list (`[]`). |
##| adgroup_id | string | The ID of the ad group that fails to be copied. |
##| error_message | string | The error encountered during the process of copying the ad group (`adgroup_id`). |
```

### Example
#### Successful call with task ID generated
  ```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "task_id": "{{task_id}}",
        "adgroup_error_list": []
    }
}
(/code)
```
#### Successful call with no task ID generated
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "adgroup_error_list": [
            {
                "adgroup_id": "{{adgroup_id}}",
                "error_message": "Start time cannot be earlier than the current time. Please edit the start time and try again."
            },
            {
                "adgroup_id": "{{adgroup_id}}",
                "error_message": "Start time cannot be earlier than the current time. Please edit the start time and try again."
            }
        ],
        "task_id": ""
    }
}
(/code)
```
