# Update an ad group

**Doc ID**: 1739586761631745
**Path**: API Reference/Ad Groups/Update an ad group

---

Use this endpoint to update an ad group. Not all information of an ad group can be modified (For example, **placement**).

> **Important**
This update mode of this endpoint is full replacement, not incremental update. Even if you only want to update one data field, you need to specify all required data fields.

> **Note**

> If you have specified `special_industries` at the campaign level, ensure that ad groups in the campaign meet the targeting requirements outlined in [Targeting requirements for ad groups in a campaign with special ad categories](https://business-api.tiktok.com/portal/docs?id=1739381236849665#item-link-Targeting%20requirements%20for%20ad%20groups%20in%20a%20campaign%20with%20special%20ad%20categories). 

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{26%}|v1.2{34%}|v1.3{38%}|
|---|---|---|
|Endpoint path|/v1.2/adgroup/update/|/v1.3/adgroup/update/|
|Request parameter name|
`age`
`operation_system` 
`connection_type`
 `device_price`
 `android_osv`
 `ios_osv`
`ios_target_device`
`bid`
`conversion_bid` 
`deep_cpabid` 
`daily_retention_ratio` 
`action_v2` 
`user_actions`
`include_custom_actions` 
`exclude_custom_actions` 
`dpa_retargeting_type` 
`dpa_retargeting_actions_days`
`enable_expansion`
`ad_app_profile_page_type`|
`age_groups`
 `operating_systems`
 `network_types`
 `device_price_ranges`
`min_android_version` 
`min_ios_version` 
`ios14_targeting`
`bid_price`
`conversion_bid_price`
`deep_cpa_bid`
`next_day_retention`
`actions`
`video_user_actions`
`included_custom_actions` 
`excluded_custom_actions` 
`shopping_ads_retargeting_type`
` shopping_ads_retargeting_actions_days`
 `expansion_enabled`
 `adgroup_app_profile_page_state`|
|Request parameter data type|`advertiser_id`: number
`adgroup_id`: number|`advertiser_id`: string 
`adgroup_id`: string|
|Request parameter name and data type|`is_comment_disable`: number
 `audience`: number[]
 `excluded_audience`: number[]  
`location`: number[]
`interest_category_v2`: number[]
`interest_keywords`: number[]r
`device_models`: number[]
`carriers_v2`: number[]
 `pangle_block_app_list_id`: 
number[]
 `action_categories`: number[]
 `pangle_audience_package_include`: number[]
 `pangle_audience_package_exclude`: number[]
`catalog_authorized_bc`: number
`automated_targeting`: string|`comment_disabled`: boolean
 `audience_ids`: string[]
 `excluded_audience_ids`: string[]
 `location_ids`: string[]
`interest_category_ids`: string[]
` interest_keyword_ids `: string[]
` device_model_ids `: string[]
`carrier_ids`: string[]
 `blocked_pangle_app_ids`: 
string[]
 `action_category_ids`: string[]
 ` included_pangle_audience_package_ids`: string[]
 ` excluded_pangle_audience_package_ids`: string[]
`catalog_authorized_bc_id`: string
`auto_targeting_enabled`: boolean|
| Request parameters deprecated in v1.3|/ |`carriers`|
|New request parameters |/|`contextual_tag_ids` 
`purchase_intention_keyword_ids` 
`spending_power`
`share_disabled`
 `zipcode_ids`
`isp_ids` 
`shopping_ads_retargeting_custom_audience_relation`
`saved_audience_id`
`smart_audience_enabled`
`smart_interest_behavior_enabled`
`brand_safety_type`
`category_exclusion_ids`
`vertical_sensitivity_id`
`exclude_age_under_eighteen` 
 `deep_funnel_optimization_status` 
`deep_funnel_event_source`  
 `deep_funnel_event_source_id`   
`deep_funnel_optimization_event`
 `search_result_enabled`
 `search_keywords`
 `automated_keywords_enabled`  
 `custom_conversion_id`  
 `is_lhf_compliance`|
|Response parameters|/| We now return the full info of ad entity in v1.3. For details, see the Response section in this page.|
| Response parameters deprecated in v1.3|/ |`need_audit`|
```

## Request

**Endpoint** 

**Method** POST

**Header**

```xtable
|Field{35%}|Data Type{15%}|Description{50%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162). |
|Content-Type {Required}|string|Request message type. Allowed format: `"application/json"`.|
```

**Parameters**

```xtable
|Field{35%}|Data Type{15%}|Description{50%}|
|---|---|---|
|adgroup_id {Required}|string| Ad group ID. |
|advertiser_id {Required}|string| Advertiser ID.|
|adgroup_name |string|Ad group name, maximum character allowed is 512 and it cannot contain emoji.|
|catalog_authorized_bc_id {+Conditional}|string| For catalogs in Business Center, you must specify the ID of the Business Center that a catalog belongs to.

**Note**: Starting June 30th, 2024, when `product_source` is `STORE`, you can no longer use `catalog_authorized_bc_id` to update the ad group because it will be ignored. If you update existing ad group where `product_source` is `STORE`, the existing `catalog_authorized_bc_id`, if present for the ad groups, will no longer be returned.|
| deep_funnel_optimization_status | string | Valid only when `promotion_type` is `LEAD_GENERATION`. 

 The status of deep funnel optimization.  
Deep funnel optimization optimizes both your upper funnel events and deeper funnel events. You can select a secondary event alongside the primary optimization event, which can help improve campaign effectiveness.  

Enum values:   
- `ON`: To enable deep funnel optimization. 
-  `OFF`: To disable deep funnel optimization. Default value: `OFF`. 

 To learn about how to configure deep funnel optimization for Lead Generation ads, see [Lead Generation ad with optimization location as Instant Form](https://business-api.tiktok.com/portal/docs?id=1774482920012801) and [Lead Generation ad with optimization location as Website](https://business-api.tiktok.com/portal/docs?id=1774482976097281). 

**Note**: 
- Deep funnel optimization with CRM events is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. 
- Deep funnel optimization with Pixel or Offline events is generally available.  |
| deep_funnel_event_source {+Conditional} | string | Required when `deep_funnel_optimization_status` is `ON`.  

 The event source type. 

 Enum values:  
- `PIXEL`: Pixel. 
- `OFFLINE`: Offline Event Set.
- `CRM`: CRM Event Set. 
**Note**: When deep funnel optimization is enabled, you cannot update `deep_funnel_event_source`, `deep_funnel_event_source_id`, and `deep_funnel_optimization_event`.  |
| deep_funnel_event_source_id {+Conditional} | string | Required when `deep_funnel_optimization_status` is `ON`.  

Event Source ID.  

- When `deep_funnel_event_source` is `PIXEL`, specify a Pixel ID via this field.   To obtain a list of Pixels, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- When `deep_funnel_event_source` is `OFFLINE`, specify an Offline Event Set ID via this field.  To obtain a list of Offline Event Set IDs, use [/offline/get/](https://business-api.tiktok.com/portal/docs?id=1765596808589313).  
- When `deep_funnel_event_source` is `CRM`, specify a CRM Event Set ID via this field.  To obtain a list of CRM Event Set IDs, use [/crm/list/](https://business-api.tiktok.com/portal/docs?id=1780896521680898).  
 **Note**: When deep funnel optimization is enabled, you cannot update `deep_funnel_event_source`, `deep_funnel_event_source_id`, and `deep_funnel_optimization_event`. |
| deep_funnel_optimization_event {+Conditional} | string | Required when `deep_funnel_optimization_status` is `ON`. 

Deep funnel optimization event. 

- To find out the supported values for Standard Events available for Pixels, Offline Event Sets, and CRM Event Sets, see the **"Event name for ad creation"** column in [Supported Pixel events](https://business-api.tiktok.com/portal/docs?id=1739585696931842).  
- To find the list of optimization events for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978) and check the returned `optimization_event`. 
Example: `SHOPPING`.   |
|comment_disabled |boolean|Whether to allow comments on your ads on TikTok. 
 
**Note**: When deep funnel optimization is enabled, you cannot update `deep_funnel_event_source`, `deep_funnel_event_source_id`, and `deep_funnel_optimization_event`. |
|share_disabled|boolean|Whether to disable sharing of ads in this ad group to third-party platforms. The value `True`is valid when the conditions below are all met:
- `objective_type` at the campaign level is set as one of the following objectives: `APP_PROMOTION`, `WEB_CONVERSIONS`, `REACH`, `TRAFFIC`, `VIDEO_VIEWS`, `ENGAGEMENT`, `LEAD_GENERATION`. 
- Placement: `placement_type`= `PLACEMENT_TYPE_AUTOMATIC` or
- `placement_type`= `PLACEMENT_TYPE_NORMAL`, and `placements` = `PLACEMENT_TIKTOK`
**Note**: This field supports incremental updates.|
|blocked_pangle_app_ids |string[]|Pangle app block list ID. You can get an ID via the `app_package_id` field returned by [Get Pangle block list](https://ads.tiktok.com/marketing_api/docs?id=1740039957181441). It only takes effect when Pangle placement is selected.|
|search_result_enabled|boolean|Whether to include your ads in Search Ads, namely to show your ads to users when they search for your business on TikTok.

You can only use this field when the following conditions are met:
- Advertising objective: The advertising objective (`objective_type`) is one of the following objectives: `APP_PROMOTION`,`WEB_CONVERSIONS` (with `is_search_campaign` as false),`TRAFFIC`, and `LEAD_GENERATION`.When `objective_type` is `LEAD_GENERATION`, `promotion_type` needs to be set to `LEAD_GENERATION`.
- Placements: `placement_type` is set to `PLACEMENT_TYPE_AUTOMATIC`, or `placement_type` is set to `PLACEMENT_TYPE_NORMAL` and `PLACEMENT_TIKTOK` is included in `placements`.
- You want to use this field to update the value of this field from `false` to `true`.
If `is_search_campaign` is `true`, you cannot update the value of this field from `false` to `true`.

To learn more about Search Ads, see [Automatic Search Placement](https://business-api.tiktok.com/portal/docs?id=1771747626094593).|
| automated_keywords_enabled | boolean | Valid only when at the campaign level `is_search_campaign` is `true`.

Whether to enable automated keywords and let the system automatically generate keywords after you add ads. This expands high-quality traffic to improve performance. View high-performing automated keywords in reporting.

Supported values: `true`, `false`.
Default value: `false`.

**Note**: 
- Automated keywords in Search Ads Campaigns are currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.|
| search_keywords | object[] | Valid only in Search Ads Campaigns.

A list of search keywords, that is, words or phrases that are used to match your ads with the terms people are searching for.

Max size: 1,000.

To confirm whether a campaign is a Search Ads Campaign, call [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986) and check the `is_search_campaign` returned for the campaign.

To learn more about Search Ads Campaigns, see [Create Search Ads Campaigns](https://business-api.tiktok.com/portal/docs?id=1815394136739841).

**Note**: For each ad group, you can configure a maximum of 1,000 search keywords.
- Once the search keywords or the targeted locations are updated, the keywords will go into the review process again. |
#|keyword{+Conditional} | string | When `search_keywords` is passed, you need to provide at least one `keyword` and the corresponding `match_type`.

The search keyword.

Length limit: 80 characters.
The name needs to exclude emojis and the following special characters: `!` `#` `$` `%` `&` `(` `)` `*` `-` `/` `:` `;` `` `?` `@` `\` `^` `_` `¥` `……`. Otherwise, an error will occur.

To obtain the review result for search keywords, call [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922) and check the `audit_status` within the `search_keywords` object array.

**Important**: Search keywords must comply with TikTok's [Advertising Terms](https://ads.tiktok.com/help/article/advertising-on-tiktok-first-things-to-note) and Community Guidelines. 
- If all of your keywords are found to be non-compliant, your campaign will not be delivered.
- If part of your search keywords are rejected, you need to remove the violative keyword(s) or replace them with a suitable alternative by using [/adgroup/update/](https://business-api.tiktok.com/portal/docs?id=1739586761631745). Your campaign will continue with the approved keywords. |
#|match_type{+Conditional}| string | When `search_keywords` is passed, you need to provide at least one `keyword` and the corresponding `match_type`.

The match type for the search keyword.

Enum values:
- `PRECISE_WORD`: exact match. Your ads will only show for user search queries that exactly match these keywords.
- `PHRASE_WORD`: phrase match. Your ads will only show for these specific keywords if users search these keywords in the same order.
- `BROAD_WORD`: broad match. Your ads will show for user search queries for any of the words you have included, even if the words are in a different order. |
#|keyword_bid_type | string | The bid type for the keyword and match type combination.

Enum values:
- `FOLLOW_ADGROUP`: To use the ad group level bid (`bid_price`) as the `keyword_bid`.
- `CUSTOM`: To customize the bid via `keyword_bid`.
Default value: `FOLLOW_ADGROUP`.

The enum value `CUSTOM` is valid only when the following conditions are met:
- At the campaign level:`objective_type` is `TRAFFIC`
- `is_search_campaign` is `true`.
- At the ad group level:`bid_type` is `BID_TYPE_CUSTOM`
- `bid_price` is specified. |
#|keyword_bid{+Conditional} | float | 
- Required and valid only when `keyword_bid_type` is `CUSTOM`.
- Ignored when `keyword_bid_type` is `FOLLOW_ADGROUP`.
The bid price for the keyword and match type combination.

Value range: >0. |
|audience_type {+Conditional}|string| 
- Required and valid only when `app_promotion_type` is `APP_RETARGETING` at the campaign level.  
- Not supported when `app_promotion_type` is not set to `APP_RETARGETING` at the campaign level.
App retargeting audience type.

You need to use the same settings as when creating the ad group.

Enum value:`NEW_CUSTOM_AUDIENCE` (retargeting custom audience). 

- If you want to specify an empty retargeting custom audience for your App Retargeting ads, do not pass `audience_ids` and `excluded_audience_ids`. 
- If you want to specify a non-empty retargeting custom audience for your App Retargeting ads, you can specify an Include Audience via `audience_ids`, or an Exclude Audience via `excluded_audience_ids` , or both simultaneously.  If both `audience_ids` and `excluded_audience_ids` are specified, they cannot contain the same IDs.|
|audience_rule |object| Rules that specify your audience. Valid if objective_type is `TRAFFIC` or `APP_PROMOTION`. For details, see [Audience Rules](https://ads.tiktok.com/marketing_api/docs?id=1739566532187138). |
|saved_audience_id |string|This field is supported under the following conditions: 
- The category of Housing, Employment, or Credit (`specical_industries`) is NOT specified in your campaign.
- **AND** the advertising objective (`objective_type`) is NOT Product Sales (`PRODUCT_SALES`) in your campaign. 
- **AND** TikTok placement is selected in your ad group (i.e., `placement_type` is set as `PLACEMENT_TYPE_AUTOMATIC` **or** `placement_type` is set as `PLACEMENT_TYPE_NORMAL` and `PLACEMENT_TIKTOK` is included in `placements`).
- **AND** automatic targeting is NOT used in your ad group(i.e., `auto_targeting_enabled` is NOT set to `true`). 
Saved Audience ID. 
Before using this field, call [/dmp/saved_audience/create/](https://business-api.tiktok.com/portal/docs?id=1780154541898754) to create a Saved Audience and get the Saved Audience ID in response. The advertiser ID associated with your Saved Audience should be the same as the advertiser ID in your ad group. Otherwise, an error will occur. 
If you use `saved_audience_id` to create an ad group, we will return both the Saved Audience ID and the targeting options that are included within your Saved Audience in response.
See [Create a Saved Audience](https://business-api.tiktok.com/portal/docs?id=1780156510696449) to find out the detailed workflow and code examples. 

**Note**:
- When creating a Saved Audience via [/dmp/saved_audience/create/](https://business-api.tiktok.com/portal/docs?id=1780154541898754), you can specify targeting options such as `gender`. However, if you are creating an ad group using a Saved Audience, you must avoid concurrently setting both the `saved_audience_id` and targeting options (like `gender`) already within your Saved Audience. Otherwise, an error will occur. 
- If the device setting of your Saved Audience is in conflict with the device settings of the ad group, an error will occur. Examples include:  When the operating system for your Saved Audience is Android, but while creating an ad group, you set `ios14_targeting` as `IOS14_PLUS`. 
- When you specify `APP_PROMOTION` as the `objective_type` field at the campaign level and use the App ID of an Android App in your ad group, yet your Saved Audience's operating system is iOS.
- If your API request throws an error that is associated with a conflict between your Saved Audience configurations and ad group configurations, the current error message will indicate that the issue pertains to your audience targeting option. To resolve this, we recommend using [/dmp/saved_audience/list/](https://business-api.tiktok.com/portal/docs?id=1780154619404290) to check the details of the corresponding targeting option to identify the source of the problem and then create a new Saved Audience if necessary.
- If the `saved_audience_id` was created with `age_groups` specified, the age restriction rules outlined in [New age restrictions for ads on TikTok](https://business-api.tiktok.com/portal/docs?id=1788755983247362) for different advertising objectives also apply. Make sure that the age targeting setting is allowed before you use the Saved Audience (`saved_audience_id` ) in the ad group.|
|auto_targeting_enabled{-To be deprecated}|boolean|Whether to enable automated targeting. Enum values: `true`, `false`.

**Note**:  Starting June, 2024, you can no longer enable Automatic targeting or Targeting expansion for your ad groups. To ensure a smooth API integration, we recommend you migrate to [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
| shopping_ads_retargeting_type | string |Valid when `shopping_ads_type` is `VIDEO` and `product_source` is `CATALOG`. 

 The retargeting type of shopping ads. 

 Enum values: 
- `LAB1`: Retargeting audiences who viewed products or added products to cart but didn't purchase products. 
- `LAB2`: Retargeting audiences who added products to cart but didn't purchase products. 
- `LAB3`: Retargeting audiences using custom combination. 
- `OFF`: No retargeting.  |
| shopping_ads_retargeting_actions_days{+Conditional} | number | The valid time range for the specified audience action. Audiences who have completed the specified action within the time range will be retargeted by the shopping ads. 
Required when `shopping_ads_retargeting_type` is `LAB1` or `LAB2`. 
Value range: 1, 2, 3, 7, 14, 30, 60, 90, 180. |
| included_custom_actions {+Conditional} | object[] | The custom action that you want to use as "Include" conditions for filtering out the shopping ads audiences to be retargeted. When `shopping_ads_retargeting_type` is `LAB3`, you need to pass in either `included_custom_actions` or `excluded_custom_actions`.|
#| code | string | The custom action used to filter out the audiences to be retargeted. Enum values: 
- `VIEW_PRODUCT`: The audience viewed the product. 
- `ADD_TO_CART`: The audience added the product to the cart. 
- `PURCHASE`: The audience purchased the product. |
#| days | integer | The time range used to filter out the audiences that completed the specified action. Value range: [1,180]. |
| excluded_custom_actions {+Conditional}| object[] | The custom action that you want to use as "Exclude" conditions for filtering out the shopping ads audiences to be retargeted. When `shopping_ads_retargeting_type` is `LAB3`, you need to pass in either `included_custom_actions` or `excluded_custom_actions`.|
#| code | string | The custom action used to filter out the audiences to be retargeted. Enum values: 
- `VIEW_PRODUCT`: The audience viewed the product. 
- `ADD_TO_CART`: The audience added the product to the cart. 
- `PURCHASE`: The audience purchased the product. |
#| days | integer | The time range used to filter out the audiences that didn't complete the specified action. Value range: [1,180]. |
| shopping_ads_retargeting_custom_audience_relation | string | Valid only when the following conditions are all met: 
- `shopping_ads_type` is set to `VIDEO`.
-  `product_source` is set to `CATALOG`.
-  `shopping_ads_retargeting_type` is passed and set to `LAB1`, `LAB2`, or `LAB3`.
- `audience_ids` is passed. 
The logical relation between the Video Shopping Ads (VSA) retargeting audience specified by `shopping_ads_retargeting_type` and the custom audience specified by `audience_ids`. 

Enum values: 
- `OR`: To combine the VSA retargeting audience and the custom audience to create the targeted audience. The targeted audience will consist of individuals who belong to either the VSA retargeting audience or the custom audience. 
- `AND`: To intersect between the VSA retargeting audience and the custom audience to create the targeted audience. The targeted audience will consist of individuals who belong to both the VSA retargeting audience and the custom audience. 
**Note**: If you remove the custom audience after `shopping_ads_retargeting_custom_audience_relation` has been specified, `shopping_ads_retargeting_custom_audience_relation` will be automatically set to a null value. |
|location_ids |string[]|IDs of the locations that you want to target. 
You can set `location_ids` or `zipcode_ids` or both.

Max size: 3,000. If you provide both `location_ids` and `zipcode_ids`, the combined total of location IDs, zip code IDs, and postal code IDs cannot exceed 3,000 per ad group.

To get the available locations and corresponding IDs based on your placement and objective, use the [/tool/targeting/search/](https://ads.tiktok.com/marketing_api/docs?id=1761236883355649) or [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. To get the list of location IDs, see [Location IDs](https://ads.tiktok.com/marketing_api/docs?id=1739311040498689). 

**Note**: 
-  Overlapping targeted locations are not supported. For instance, you cannot target the U.S. and the state of California at the same time.
- If you target locations in the US via `location_ids` or `zipcode_ids` during ad group creation, you can subsequently update those IDs to other US locations but you cannot remove all US locations to target only non-US countries.
- If you create an ad group with `TIKTOK_LITE` in the `tiktok_subplacements` value, you cannot update the ad group to exclude Japan and South Korea from your targeted locations (`location_ids`). 
- If you want to remove all the targeted location IDs from the ad group, set this field to an empty array (`[]`). Note that targeted locations are mandatory for ad groups. Therefore, if you initially only specified location IDs during ad group creation and now want to remove these IDs, you need to set `location_ids` to an empty array (`[]`) and simultaneously specify zip code IDs or postal code IDs via `zipcode_ids`. |
| zipcode_ids|string[]|Zip code IDs or postal code IDs that you want to use to target locations. 
You need to set `location_ids` or `zipcode_ids` or both.

Max size: 3,000. If you provide both `location_ids` and `zipcode_ids`, the combined total of location IDs, zip code IDs, and postal code IDs cannot exceed 3,000 per ad group.

You can get the available zip code IDs or postal code IDs based on your placement, objective and keyword via `geo_id` (when `geo_type` = `ZIP_CODE`) returned from the [/tool/targeting/search/](https://ads.tiktok.com/marketing_api/docs?id=1761236883355649) endpoint. 
**Note**: 
-  Zip code targeting is currently only supported for the US and postal code targeting is currently only supported for Canada, Brazil, Indonesia, Thailand, and Vietnam.
- Targeting postal code areas in Brazil, Indonesia, Thailand, and Vietnam is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- You cannot use zip code targeting in campaigns that have enabled special ad categories (`special_industries`).
-  You cannot use zip code targeting or postal code targeting in campaigns with the `objective_type` as `RF_REACH`.
- You can only use zip code targeting or postal code targeting on TikTok placement. Therefore, the `placements` value needs to include `PLACEMENT_TIKTOK`.
- Overlapping targeted locations are not supported. For instance, you cannot target the US and the state of California at the same time.
- If you target locations in the US via `location_ids` or `zipcode_ids` during ad group creation, you can subsequently update those IDs to other US locations but you cannot remove all US locations to target only non-US countries.
- If you want to remove all the targeted zip code or postal code IDs from the ad group, set this field to an empty array (`[]`). Note that targeted locations are mandatory for ad groups. Therefore, if you initially only specified zip code or postal code IDs during ad group creation and now want to remove these IDs, you need to set `zipcode_ids` to an empty array (`[]`) and simultaneously specify location IDs via `location_ids`.
- Incremental updates to this field are supported.|
|languages |string[]|Codes of the languages that you want to target. For the list of languages codes supported, see [Enumeration - Language Code](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).
You can get language codes via [/tool/language/](https://ads.tiktok.com/marketing_api/docs?id=1737188554152962), and if you don't want to limit the languages you target, assign an empty value to this field or do not pass in this field. |
|gender |string|Gender that you want to target. Enum: `GENDER_FEMALE`,`GENDER_MALE`,`GENDER_UNLIMITED`|
|age_groups |string[]|Age groups you want to target.  

For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138#item-link-Age%20Group). 

-  In certain scenarios, creation of ad groups that target the age group 13-17 (`AGE_13_17`) in the US, Latin America, the European Economic Area, the UK, Switzerland, or Canada will not be allowed. See [New age restrictions for ads on TikTok](https://business-api.tiktok.com/portal/docs?id=1788755983247362) to learn more.
- If you are impacted by the restrictions and leave the `age_groups` field unspecified or set it as `[]` without setting `exclude_age_under_eighteen` to `true`, an error will occur. If the ad group targets the age group 13-17 (`AGE_13_17`) in the US, Latin America, the European Economic Area, the UK, Switzerland, or Canada and you typically leave the `age_groups` field unspecified or set it as `[]`, we recommend that you set `exclude_age_under_eighteen` to `true` simultaneously to avoid any errors.|
| exclude_age_under_eighteen | boolean | Whether to exclude the ages younger than 18. 
Use this field only in scenarios where targeting the age group 13-17 (`AGE_13_17`) in the US, Latin America, the European Economic Area, the UK, Switzerland, or Canada is not supported. In other scenarios, this field is not supported. See the description of `age_groups` for details. 

 Enum values: `true`, `false`. Default value: `false`. |
|spending_power|string|Spending power that you want to target.

Enum values: `ALL`, `HIGH`. 
 If it is set to `HIGH`, you can target high spending users who typically spend more on purchases on TikTok ads than average users.  
 
**Note:** :
- This field does not support the advertising objectives `PRODUCT_SALES` and `RF_REACH` at the campaign level. See [Advertising objectives](https://ads.tiktok.com/marketing_api/docs?id=1737585562434561) for details. 
- This field supports Automatic Placement and Select Placement with TikTok included. Therefore, you need to set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`, or include `PLACEMENT_TIKTOK` in the value of `placements`. Note that if you specify Pangle as a placement, the spending power targeting won't take effect on Pangle. 
- When `auto_targeting_enabled` is `true` at the ad group level, then `spending_power`  will be automatically set to `ALL`. |
|household_income| string[]| Household income that you want to target. Enum values: `TOP5`(Top 5% of ZIP codes), `TOP10`(Top 10% of ZIP codes), `TOP10_25`(Top 10% -25% of ZIP codes), `TOP25_50`(Top 25% - 50% of ZIP codes). 
Currently, this field has the following limitations: 
- Not supported in Reach&Frequency type ads.
- Only works on TikTok Placement in the US.  |
|audience_ids |string[]|An list of audience IDs. You can get audience IDs by using the [/dmp/custom_audience/list/](https://ads.tiktok.com/marketing_api/docs?id=1739940506015746) endpoint.|
| smart_audience_enabled | boolean | Whether to turn on Smart audience. 

Enum values: `true`, `false`. 

To learn more about Smart audience and how to turn on Smart audience, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
|excluded_audience_ids |string[]| A list of audience IDs to be excluded. You can get audience IDs by using the [/dmp/custom_audience/list/](https://ads.tiktok.com/marketing_api/docs?id=1739940506015746) endpoint.|
|interest_category_ids |string[]|IDs of general interest categories that you want to use to target audiences. 

- To search for or list general interest category IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/interest_category/](https://ads.tiktok.com/marketing_api/docs?id=1737174348712961).
- To get recommended interest category IDs based on your industry, use [/tool/targeting_category/recommend/](https://business-api.tiktok.com/portal/docs?id=1736275204260866).|
|interest_keyword_ids|string[]|IDs of additional interest categories that you want to use to target audience.  

  To search for additional interest categories, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/interest_keyword/recommend/](https://ads.tiktok.com/marketing_api/docs?id=1763590884474882). |
|purchase_intention_keyword_ids|string[]| IDs of purchase intention categories that you want to use to target audiences with an interest in purchases related to a content category. 

To search for or list purchase intention category IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218).

**Note**: The endpoint supports the incremental update of `purchase_intention_keyword_ids`.|
|actions| object[] | A list of targeting behavioral category objects.|
#|action_scene | string | The type of user behavior that you want to target.

 Enum values: 
- `VIDEO_RELATED`: Video interactions.
- `CREATOR_RELATED`: Creator interactions.
- `HASHTAG_RELATED`: Hashtag interactions.|
#|action_period |number| Select a time period to include behaviors from. 

Supported values: `0`, `7`, `15`. If `action_scene` is `CREATOR_RELATED` or `HASHTAG_RELATED`, `0` will be used regardless of the value you pass in. `0` means that there is no definite timeframe to select actions from. 

**Note**: Currently, when updating an ad group with video interaction targeting (`action_scene`= `VIDEO_RELATED`) via **TikTok Ads Manager**, you cannot update the time period (`action_period`). However, when updating ad groups via **API**, you can still pass in `0`, `7`, or `15`.|
#|video_user_actions |string[]|The specific user interactions that you want to target for the user behavior type. 
- If `action_scene` is `VIDEO_RELATED`, the allowed values are: `WATCHED_TO_END`,`LIKED`,`COMMENTED`,`SHARED`.
-  If `action_scene` is `CREATOR_RELATED`, the allowed values are: `FOLLOWING`, `VIEW_HOMEPAGE`. 
- If `action_scene` is `HASHTAG_RELATED`, the allowed value is `VIEW_HASHTAG`.
**Note**: Currently, when updating an ad group via **TikTok Ads Manager**, you cannot update the kind of user actions (`video_user_actions`). However, when updating ad groups via **API**, you can still pass in the desired enum value combinations, for example: `["LIKED","COMMENTED"]` if `action_scene`=`VIDEO_RELATED`.|
#|action_category_ids |string[]|IDs of the video interactions categories, creator interactions categories, hashtags, or hashtag bundles that you want to use to target audiences. 

 
- To search for or list video interactions category IDs or creator interactions category IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/action_category/](https://ads.tiktok.com/marketing_api/docs?id=1737166752522241).
- To get hashtag IDs or hashtag bundle IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/hashtag/recommend/](https://ads.tiktok.com/marketing_api/docs?id=1736271339521025).
- To get recommended video interactions category IDs, creator interactions category IDs, hashtag IDs, or hashtag bundle IDs based on your industry, use [/tool/targeting_category/recommend/](https://business-api.tiktok.com/portal/docs?id=1736275204260866). |
| smart_interest_behavior_enabled | boolean | Whether to turn on Smart interests & behaviors. 

Enum values: `true`, `false`. 

To learn more about Smart interests & behaviors and how to turn on Smart interests & behaviors, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
|included_pangle_audience_package_ids |string[]|IDs of the Pangle audiences that you want to include. Valid only for Pangle placement. You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://ads.tiktok.com/marketing_api/docs?id=1740040177229826) endpoint. You need to set `bind_type` to `INCLUDE`.  Do not specify this field and `excluded_pangle_audience_package_ids` at the same time.|
|excluded_pangle_audience_package_ids |string[]|IDs of the Pangle audiences that you want to exclude. Valid only for Pangle placement. You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://ads.tiktok.com/marketing_api/docs?id=1740040177229826) endpoint. You need to set `bind_type` to `EXCLUDE`. Do not specify this field and `included_pangle_audience_package_ids` at the same time.|
|operating_systems {+Conditional}|string[]|Device operating systems that you want to target. 

Only one value is allowed.  

Enum values: `ANDROID`, `IOS`. 

This field is required in two scenarios: 
- `objective_type` is `APP_PROMOTION`
- `objective_type` is `TRAFFIC` and `promotion_type` is `APP_IOS` or `APP_ANDROID`|
|min_android_version |string|Minimum Android version. For enum values, see [Enumeration - Minimum Android Version](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
|ios14_targeting{+Conditional}|string|Required and must be specified as `IOS14_PLUS` when `campaign_type` at the campaign level is `IOS14_CAMPAIGN`.

The iOS devices that you want to target. 

Enum values:
- `UNSET`: Devices with iOS 14.4 or earlier versions.
- `IOS14_MINUS`: Devices with versions earlier than iOS 14.0, which are not affected by the iOS 14 privacy update. 
- `IOS14_PLUS`: Devices with iOS 14.5 or later versions. The iOS 14 privacy update has been enforced in this group of devices. This value is only supported for Dedicated Campaigns. Specify this value if you want to create an iOS 14 campaign. Each iOS 14 campaign can have up to 2 active ad groups. 
- `ALL`: Devices with iOS 14.5 or later versions. The iOS 14 privacy update has been enforced in this group of devices. This value is only supported for iOS App Retargeting ads and iOS retargeting Video Shopping Ads with product source as catalog and optimization location as App.To target devices with iOS 14.5 or later versions in App Retargeting ads, you need to set `ios14_targeting` to `ALL` and set `min_ios_version` to `14.5` or a later version. Otherwise, an error will occur. 
- To target devices with iOS 14.4 or earlier versions in App Retargeting ads, you don't need to pass `ios14_targeting`. 
For the following two scenarios, the value `ALL` will be used regardless of the value you pass in.
- iOS App Retargeting ads:`app_promotion_type` is `APP_RETARGETING`
- and `promotion_type` is `APP_IOS`
- iOS retargeting Video Shopping Ads with product source as catalog and optimization location as App:`shopping_ads_type` is `VIDEO`
- `product_source` is `CATALOG`
- `promotion_type` is `APP_IOS`
- and `shopping_ads_retargeting_type` is not `OFF`For other scenarios, the default value is `UNSET`. 

Once set to `IOS14_PLUS`, this field cannot be updated, and the following requirements must be met. 
-  At the ad group level: `app_id` is set to the ID of an iOS App.
 To get iOS App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). The `platform` of an iOS App should be `IOS`. 
- `operating_systems` is set to `["IOS"]`. 
-  `min_ios_version` is passed and the value should be consistent with the value of `ios14_targeting`. 
-  `optimization_goal` is set to `CLICK`, `INSTALL`, `IN_APP_EVENT` or `VALUE`.
-  The following fields are not specified: `min_android_version`
-  `shopping_ads_retargeting_type`
- `shopping_ads_retargeting_actions_days` 
-  At the ad level: `deeplink_type` is not set to `DEFERRED_DEEPLINK`. |
|min_ios_version {+Conditional} |string|Required when `ios14_targeting` is specified. 

Minimum iOS version. 

For enum values, see [Enumeration - Minimum iOS Version](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
|device_model_ids| string[]| IDs of the device models that you want to target. Use [/tool/device_model/](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369) to get the complete list of device model IDs and their statuses, and only active devices (`is_active` = `True` in the response of  [/tool/device_model/](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369)) can be used to create ads.
**Note**: Device model (`device_model_ids`) and device price (`device_price_ranges`) cannot be set at the same time.|
|network_types|string[]|Device connection types that you want to target. For enum values, see [Enumeration - Connection Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
|carrier_ids| string[]| Carriers that you want to target. A carrier is valid only when the `in_use` field for the carrier is `true`. The carriers must be consistent with the location(s) that you want to target. See [Get Carriers](https://ads.tiktok.com/marketing_api/docs?id=1737168013095938) for detailed information. |
| isp_ids | string[] | IDs of the Internet service providers (ISP) that you want to target. 
Valid only when you specify a valid location ID at the country or region level via `location_ids` at the same time. 
You can use [/tool/targeting/list/](https://ads.tiktok.com/marketing_api/docs?id=1762962378261506) to get the ISP IDs that you can target for a location ID. 
**Note**: When you pass in `isp_ids`, you cannot set the placement as Global App Bundle only (`placements` =`PLACEMENT_GLOBAL_APP_BUNDLE`). |
|device_price_ranges |number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50. 
**Important**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].|
|targeting_expansion{-To be deprecated}| object | Settings about targeting expansion. 

**Note**:  Starting June, 2024, you can no longer enable Automatic targeting or Targeting expansion for your ad groups. To ensure a smooth API integration, we recommend you migrate to [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
#|expansion_enabled|boolean| Whether to enable targeting expansion |
#|expansion_types {+Conditional}|string[]| The target audience types that you want to expand. Required when `expansion_enabled` is `true`. To expand a target audience type is to remove the value for this target audience type and make this target audience type irrelevant. Target audience types that are eligible for expanding must already have a value or selection. Enum values: 
- `AGE`
- `GENDER`
- `INTEREST_AND_BEHAVIOR`: This type includes `ad_tag_v2`, `video_action`, `action_days`, `action_categories`, and `action_scene`. 
- `CUSTOM_AUDIENCE`: This type includes `retargeting_tags` and `retargeting_tags_exclude`. |
|contextual_tag_ids |string[]|Contextual tag IDs. You can use [/tool/contextual_tag/get/](https://ads.tiktok.com/marketing_api/docs?id=1747747118654465) to get available contextual tags.  See [Contextual targeting](https://ads.tiktok.com/marketing_api/docs?id=1745292519923713)  to learn more about how to use contextual targeting.

**Note**: 
- This is an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Only supports `REACH` and `VIDEO_VIEWS` as objectives (`objective_type`) at the campaign level. 
- Not supported when `brand_safety_type` is set to `THIRD_PARTY`.|
|brand_safety_type|string|To learn about the eligibility for updating this field, see [Eligibility for updating pre-bid brand safety filtering settings](https://business-api.tiktok.com/portal/docs?id=1739381752981505#item-link-Eligibility%20for%20updating%20pre-bid%20brand%20safety%20filtering%20settings).

Brand safety type. 

Enum values: 
- `EXPANDED_INVENTORY`: Use TikTok's brand safety solution. Expanded inventory means that your ads will appear next to content where most inappropriate content has been removed, and that does not contain mature themes. In the next API version, `EXPANDED_INVENTORY` will replace `NO_BRAND_SAFETY` and will be the default brand safety option.
- `STANDARD_INVENTORY`: Use TikTok's brand safety solution. Standard inventory means that ads will appear next to content that is appropriate for most brands. 
- `LIMITED_INVENTORY`: Use TikTok's brand safety solution. Limited inventory means that your ads will not appear next to content that contains mature themes. To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. 

**Note**: 
- Updating Brand Safety settings, including `brand_safety_type`, `category_exclusion_ids`, and `vertical_sensitivity_id`, is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
-  Pre-bid first-party Brand Safety solutions for `APP_PROMOTION`, `WEB_CONVERSIONS`, `TRAFFIC`,  `LEAD_GENERATION`,  and `PRODUCT_SALES` objectives in Auction ads are currently allowlist-only features. If you would like to access it, please contact your TikTok representative. 
-  See [Brand safety](https://ads.tiktok.com/marketing_api/docs?id=1739381752981505) to learn about the supported advertising objectives, supported markets, and the general introduction of pre-bid Brand Safety filtering. |
|category_exclusion_ids|string[]|This field can only be updated when any of the following conditions is met: 
- `schedule_start_time` of the ad group has not been reached. 
- `schedule_start_time` of the ad group has been reached, but the `operation_status` is `DISABLE` and the cost is 0. To retrieve the `schedule_start_time` and `operation_status` of an ad group, use [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922).   
Content exclusion category IDs.

You can use [/tool/content_exclusion/get/](https://business-api.tiktok.com/portal/docs?id=1769738074686465) to get a list of content category IDs (`excluded_category_list`) that can be excluded from being displayed next to your ads.

**Note**: 
- Updating Brand Safety settings, including `brand_safety_type`, `category_exclusion_ids`, and `vertical_sensitivity_id`, is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.|
|vertical_sensitivity_id|string|This field can only be updated when any of the following conditions is met: 
- `schedule_start_time` of the ad group has not been reached. 
- `schedule_start_time` of the ad group has been reached, but the `operation_status` is `DISABLE` and the cost is 0. To retrieve the `schedule_start_time` and `operation_status` of an ad group, use [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922).   Vertical sensitivity category ID. 

You can use [/tool/content_exclusion/get/](https://business-api.tiktok.com/portal/docs?id=1769738074686465) to get a list of vertical categories containing sensitive content (`vertical_sensitivity_list`) that can be excluded from appearing next to your ads. 

**Note**: 
- Updating Brand Safety settings, including `brand_safety_type`, `category_exclusion_ids`, and `vertical_sensitivity_id`, is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.|
|budget |float|Advertising budget. It cannot be updated when Campaign Budget Optimization (`budget_optimize_on`) is on. 
For how to configure budget settings, see [Budget](https://ads.tiktok.com/marketing_api/docs?id=1739381246298114). To directly see the daily budget value range for a currency, see [Currency-Daily budget value range](https://ads.tiktok.com/marketing_api/docs?id=1737585839634433).
**Note**: The new budget should be at least 105% of the current spend. You can run [a synchronous report](https://ads.tiktok.com/marketing_api/docs?id=1740302848100353) or [an asynchronous report](https://ads.tiktok.com/marketing_api/docs?id=1740302766489602) to get the spend data via the Basic data metric `spend` .|
|schedule_type |string|The schedule type can be either `SCHEDULE_START_END` or `SCHEDULE_FROM_NOW`. 

- If you choose `SCHEDULE_START_END`, you need to specify a start time and an end time. 
- If you choose `SCHEDULE_FROM_NOW`, you only need to specify a start time and the end time will be automatically set to 10 years later than the start time. |
|schedule_start_time {+Conditional}|datetime|Required when you pass in `schedule_type`.

Schedule start time (UTC+0), in the format of `"YYYY-MM-DD HH:MM:SS"`. 

The start time can be up to 12 hours earlier than the current time, but cannot be later than `"2028-01-01 00:00:00"`.  

**Note**: This field cannot be updated if the `schedule_start_time` for the ad group is earlier than the current time.|
|schedule_end_time {+Conditional}|datetime|Required when schedule_type is `SCHEDULE_START_END`.

Schedule end time (UTC+0), in the format of `"YYYY-MM-DD HH:MM:SS"`.

 The end time cannot be later than `"2038-01-01 00:00:00"`. |
|dayparting |string| Ad delivery arrangement, in the format of a string that consists of 48 x 7 characters. Each character is mapped to a 30-minute timeframe from Monday to Sunday. Each character can be set to either 0 or 1.  1 represents delivery in the 30-minute timeframe, and 0 stands for non-delivery in the 30-minute timeframe. The first character is mapped to 0:01-0:30 of Monday; The second character is mapped to 0:31-1:00 of Monday, and the last character represents 23:31-0:00 Sunday. **Note:**** If not specified, all-0, or all-1 are considered as full-time delivery. |
|frequency|number|Frequency, together with `frequency_schedule`, controls how often people see your ad (only available for `REACH` ads). 
The below conditions should be both met:
- 1 Note**: When `secondary_optimization_event` is specified, you need to pass in `deep_bid_type` at the same time.|
|bid_type |string|Bidding strategy that determines how the system manages your cost per result, spends your budget, and how it delivers ads. 

For enum values, see [Enumeration - Bidding Strategy](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 

This field cannot be updated when Campaign Budget Optimization (CBO) is enabled (`budget_optimize_on` = `TRUE`).
|bid_price |float|Valid only when `bid_type` is `BID_TYPE_CUSTOM` and `billing_event` is `CPC`, `CPM`, or `CPV`.

Bid price. The average cost per result that you want to achieve (for Cost Cap bidding strategy). 

When Campaign Budget Optimization (`budget_optimize_on`) is on, we suggest that you set the same bid value for all ad groups in the campaign. 

`bid_price` needs to be lower than budget set at the campaign level and ad group level. See [Bidding-Bidding limits](https://ads.tiktok.com/marketing_api/docs?id=1745292444424193) to learn more about the bid verification mechanism.|
|conversion_bid_price|float|Valid only when `bid_type` is `BID_TYPE_CUSTOM` and `billing_event` is `OCPM`.

Where you can set a target cost per conversion for oCPM (Optimized Cost per Mille). 

`conversion_bid_price` needs to be lower than budget set at the campaign level and ad group level. See [Bidding-Bidding limits](https://ads.tiktok.com/marketing_api/docs?id=1745292444424193) to learn more about the bid verification mechanism.|
|deep_bid_type{+Conditional} |string|Bidding strategy for in-app events. 
For enum values and their descriptions, see [Enumeration - Deep-level Bidding Strategy](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).
**Note**: When `secondary_optimization_event` is specified, you need to pass in `deep_bid_type` at the same time.|
|roas_bid {+Conditional}|float|Required when `deep_bid_type` is `VO_MIN_ROAS`. 

ROAS goal for Value Optimization.

 Value range: 
- For in-app advertising scenarios (`objective_type` is `APP_PROMOTION`, `optimization_goal` is `VALUE`, and `optimization_event` is `AD_REVENUE_VALUE`): 0.01-10.
- For Product Shopping Ads with product source as TikTok Shop (`shopping_ads_type` is `PRODUCT_SHOPPING_ADS` and `product_source` is `STORE`): 0.01-20.
- For other scenarios: 0.01-1,000.|
|deep_cpa_bid |float|Specify bid price in this field after you've chosen a bidding strategy for in-app events, for example VO_MIN.|
| next_day_retention | float | Day 2 retention ratio. Formula: `next_day_retention` = `conversion_bid_price`/`deep_cpa_bid`. Value range is (0, 1]. Only valid when `placements` is `PLACEMENT_PANGLE` and `secondary_optimization_event` is `NEXT_DAY_OPEN`. 
**Note**: If you want to use this field, please pass in `conversion_bid_price`, `deep_bid_type`, and `next_day_retention` at the same time, and make sure the value of them meets the calculation formula. Otherwise there might be unexpected errors.
  |
|pacing |string| You can choose between `PACING_MODE_SMOOTH` and `PACING_MODE_FAST`. For `PACING_MODE_SMOOTH`, the budget is allocated evenly within the scheduled time. `PACING_MODE_FAST` would consume budget and produce results as soon as possible. When Campaign Budget Optimization (`budget_optimize_on`) is on, your setting will be ignored and it will be set as `PACING_MODE_SMOOTH`. Otherwise, this field is required. |
| is_hfss | boolean |Whether the promoted content is HFSS (High Fat, Salt, Sugar) Product/Brand.

If your ad is promoting or prominently featuring a product/brand classed as high in fat, salt or sugar, set this field to `true`.

In regulated regions, HFSS ads must only be targeted to users aged 18 or over.

You can set this field to `true` when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union. 

Supported values:  `true`,`false`. 

**Note**: You can only update this setting from `false` to `true` but not vice versa.
 |
| is_lhf_compliance | boolean | Whether the promoted content complies with LHF (Less Healthy Foods) regulations.

By setting `is_lhf_compliance` to `true`, you confirm that any food or drink products you advertise on TikTok in the UK comply with the [2024 Less Healthy Foods Regulations](https://www.legislation.gov.uk/uksi/2024/1266/made) and all other applicable laws.

Supported values: `true`,`false`. 

**Note**: Starting January 1st, 2026, when your ad targets locations in the UK and `is_hfss` is `true`, `is_lhf_compliance` is required and must be set to `true`.
 |
```

### Example

```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/adgroup/update/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "adgroup_name": "{{adgroup_name}}"
}'
(/code)
```

## Response

```xtable
|Field{35%}|Data Type{15%}|Description{50%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message |string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|data |object|Returned data. |
#|advertiser_id |string| Advertiser ID.|
#|campaign_id |string| Campaign ID. |
#|campaign_name |string|The name of the campaign that the ad group belongs to.|
#|adgroup_id |string| Ad group ID. |
#|adgroup_name |string| Ad group name.|
#| create_time | string | The time at which the ad group was created, in the format of `"YYYY-MM-DD HH:MM:SS"`. 

Example: `"2023-01-01 00:00:01"`. |
#| modify_time | string | The time at which the ad group was modified, in the format of `"YYYY-MM-DD HH:MM:SS"`.  

 Example: `"2023-01-01 00:00:01"`. |
#|shopping_ads_type|string|Returned when `objective_type` at the campaign level is `PRODUCT_SALES`.

Shopping ads type. 

Enum values: 
- `VIDEO`: Video Shopping Ads.
- `LIVE`: Live Shopping Ads.
- `PRODUCT_SHOPPING_ADS`: Product Shopping Ads.
- `CATALOG_LISTING_ADS`: Catalog Listing Ads.
- `UNSET`: Unset.|
#|identity_id |string|Returned when `shopping_ads_type` is `VIDEO` and `product_source` is `SHOWCASE` or `shopping_ads_type` is `LIVE`.

Identity ID. |
#|identity_type|string|Returned when `shopping_ads_type` is `VIDEO` and `product_source` is `SHOWCASE` or `shopping_ads_type` is `LIVE`.

Identity type. Enum values: `AUTH_CODE` (Authorized Post User), `TT_USER` (TikTok Business Account User), `BC_AUTH_TT`(the TikTok account that a Business Center is authorized to access). Returned when `objective_type` is  `PRODUCT_SALES`. See [Identities](https://ads.tiktok.com/marketing_api/docs?id=1738958351620097) for details. |
#|identity_authorized_bc_id|string|Returned when `identity_type` is `BC_AUTH_TT`.  

 ID of the Business Center that a TikTok Account User in Business Center identity is associated with.  |
#|product_source|string|Returned for Video Shopping Ads and Product Shopping Ads.

Product source where you want to get products for promotion. 

Enum values: `UNSET` ,`CATALOG`(Catalog), `STORE` (TikTok Shop),`SHOWCASE`(TikTok Showcase).|
#|catalog_id|string| Returned in any of the following scenarios:
- `product_source` is `CATALOG` or `STORE`.
- `shopping_ads_type` is `LIVE` and this field is specified in the request.
Catalog ID.

**Note**: Starting June 30th, 2024, `catalog_id` will no longer be returned for newly created Shopping Ads where `product_source` is `STORE` because the specified `catalog_id` will be ignored. Existing Shopping Ads where `product_source` is `STORE` will not be affected unless you update them. If you update the existing ad groups, the existing `catalog_id`, if present for the ad groups, will no longer be returned.|
#|catalog_authorized_bc_id|string| Returned in any of the following scenarios:
- `shopping_ads_type` is `VIDEO` and `product_source` is `CATALOG` or `STORE`.
- `shopping_ads_type` is `LIVE` and this field is specified in the request.
For catalogs in Business Center, this field returns the ID of the Business Center that a catalog belongs to.

**Note**: Starting June 30th, 2024, `catalog_authorized_bc_id` will no longer be returned for newly created Shopping Ads where `product_source` is `STORE` because the specified `catalog_authorized_bc_id` will be ignored. Existing Shopping Ads where `product_source` is `STORE` will not be affected unless you update them. If you update the existing ad groups, the existing `catalog_authorized_bc_id`, if present for the ad groups, will no longer be returned.|
#|store_id |string| Returned in any of the following scenarios:
- `shopping_ads_type` is `VIDEO` and `product_source` is `STORE`.
- `shopping_ads_type` is `PRODUCT_SHOPPING_ADS` and `product_source` is `STORE`.
- `shopping_ads_type` is `LIVE` and this field is specified in the request.
ID of the TikTok Shop. |
#|store_authorized_bc_id |string|Returned when `store_id` is passed. 

ID of the Business Center that is authorized to access the store (`store_id`). |
#|promotion_type |string|Promotion type (Optimization location).
You can decide where you'd like to promote your products using this field. For value definitions, see [Enumeration - Promotion Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
#|promotion_target_type |string| The promotion type for Lead Generation objective. 
Enum values: 
-  `INSTANT_PAGE`：Instant Form. To create a fast-loading in-app TikTok Instant Form to collect more leads.
-  `EXTERNAL_WEBSITE`：Website Form. To use a landing page that has the Website Form or the TikTok Instant Page that redirects to the website with the Website Form to collect more leads. 
- `UNSET`. |
#| messaging_app_type | string | The type of instant messaging app or customized URL to use in the Instant Messaging Ad Group.

Enum values:  
-  `MESSENGER`: Messenger. 
- `WHATSAPP`: WhatsApp.
- `ZALO`: Zalo. 
- `LINE`: Line.
- `IM_URL`: Instant Messaging URL.|
#| messaging_app_account_id | string | The ID of the instant messaging app account.
- When `messaging_app_type` is `MESSENGER`, this field represents the Facebook Page ID.
- When `messaging_app_type` is `LINE`, this field represents the LINE Business ID.
- When `messaging_app_type` is `WHATSAPP`, this field represents the WhatsApp phone number automatically populated based on the specified `phone_region_code`, `phone_region_calling_code`, and `phone_number`.|
#| phone_region_code | string | The region code for the WhatsApp or Zalo phone number. 

 Example: `US`. |
#| phone_region_calling_code | string | The region calling code for the WhatsApp or Zalo phone number. 

Example: `+1`. |
#| phone_number | string | The WhatsApp or Zalo phone number. |
#|promotion_website_type|string|TikTok Instant Page type in the ad group.  
Enum values:
- `UNSET`: To not use TikTok Instant Page. 
- `TIKTOK_NATIVE_PAGE`: To use TikTok Instant Page.  |
#|app_id |string|The App ID of the app to promote.|
#|app_type |string| The type of the promoted app. Enum values: `APP_ANDROID` (Android), `APP_IOS` (iOS).|
#|app_download_url |string|App download link|
#|pixel_id |string|Pixel ID. Only applicable for landing pages. |
#|optimization_event |string|Conversion event for the ad group. See [Conversion events](https://ads.tiktok.com/marketing_api/docs?id=1739361474981889) for more. |
#|custom_conversion_id|string|The ID of the Custom Conversion used in the ad group.|
#| app_config | object[] | Returned when `sales_destination` is `WEB_AND_APP` at the campaign level.

  Details of the app or apps to promote. |
##| app_id | string | The App ID of the app to promote. |
#| deep_funnel_optimization_status | string | The status of deep funnel optimization. 
 With deep funnel optimization, you can select a secondary event alongside the primary optimization event, which can help improve campaign effectiveness.  
 
Enum values:  
- `ON`: enabled.  
-  `OFF`: disabled.  |
#| deep_funnel_event_source| string | Returned when `deep_funnel_optimization_status` is `ON`.   
 
 The event source type. 
 
Enum values: 
- `PIXEL`: Pixel.  
- `OFFLINE`: Offline Event Set. 
- `CRM`: CRM Event Set. |
#| deep_funnel_event_source_id | string | Returned when `deep_funnel_optimization_status` is `ON`. 
 
 Event Source ID.  
 

- When `deep_funnel_event_source` is `PIXEL` , this field represents a Pixel ID.
- When `deep_funnel_event_source` is `OFFLINE`, this field represents an Offline Event Set ID.  
- When `deep_funnel_event_source` is `CRM`, this field represents a CRM Event Set ID. |
#| deep_funnel_optimization_event | string | Returned when `deep_funnel_optimization_status` is `ON`.  
 
Deep funnel optimization event.   
 
Example: `SHOPPING`. |
#|placement_type |string| The placement strategy that decides where your ads will be shown. Enum values: `PLACEMENT_TYPE_AUTOMATIC` (Automatic placement), `PLACEMENT_TYPE_NORMAL` (Select placement).|
#|placements | string[] | The apps where you want to deliver your ads. For enum values, see [Enumeration - Placement](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
**Note**: 
-  If `placement_type` of the ad group is `PLACEMENT_TYPE_AUTOMATIC` (Automatic placement), the placements supported for your advertising objective will be returned for this field. For instance, if the actual supported placement is TikTok only, the returned value for this field will be `PLACEMENT_TIKTOK`.  However, if `PLACEMENT_GLOBAL_APP_BUNDLE` is supported for your objective, but you are not allowlisted for the Global App Bundle placement feature, `PLACEMENT_GLOBAL_APP_BUNDLE` will not be included in the returned value for this field.
-  If `placement_type` of the ad group is `PLACEMENT_TYPE_NORMAL` (Select placement), the placements you specified through `placements` in the request will usually be returned for this field.  The only exception is that if `PLACEMENT_GLOBAL_APP_BUNDLE` is specified through `placements` in the request, but you are not allowlisted for the Global App Bundle placement feature, `PLACEMENT_GLOBAL_APP_BUNDLE` will be filtered out from the returned value for this field. For instance, if you specify placements as `["PLACEMENT_TIKTOK", "PLACEMENT_GLOBAL_APP_BUNDLE"]` in the request, but you are not allowlisted for Global App Bundle, the returned value for this field will be `["PLACEMENT_TIKTOK"]`.  |
#| tiktok_subplacements | string[] | The subplacements within TikTok for your ads, allowing you to choose where your ads will appear. 

Enum value: 
- `IN_FEED`: In-feed. Ads will be placed in the For You feed and might also be placed in Profile Page and Following feeds.
- `SEARCH_FEED`: Search feed.
- `TIKTOK_LITE`: TikTok Lite, a streamlined version of TikTok that features a smaller app size and faster video loading speed. The TikTok Lite subplacement is currently available for Japan or South Korea as targeting locations.
- `LEMON8`: Lemon8, a community app for lifestyle content, focusing on real-life experiences, tips, guides, and product reviews. By including Lemon8 as a subplacement, your ads will appear in its For You feed, Search feed, and Immersive Video feed. [Learn more about Lemon8](https://ads.tiktok.com/help/article/about-lemon8-in-tiktok-ads-manager).
**Note**: If `tiktok_subplacements` is not specified when you create the ad group, the value of this field will be an empty list (`[]`). |
#| search_result_enabled | boolean | Whether to include your ads in Search Ads, namely to show your ads to users when they search for your business on TikTok. |
#|automated_keywords_enabled| boolean |Whether to enable automated keywords and let the system automatically generate keywords after you add ads. This expands high-quality traffic to improve performance. View high-performing automated keywords in reporting.

Supported values: `true`, `false`. |
#|search_keywords|object[] |Returned only for Search Ads Campaigns.

 A list of search keywords, that is, words or phrases that are used to match your ads with the terms people are searching for.  |
##|keyword | string | The search keyword. |
##|match_type | string | The match type for the search keyword.

Enum values:
- `PRECISE_WORD`: exact match. Your ads will only show for user search queries that exactly match these keywords.
- `PHRASE_WORD`: phrase match. Your ads will only show for these specific keywords if users search these keywords in the same order.
- `BROAD_WORD`: broad match. Your ads will show for user search queries for any of the words you have included, even if the words are in a different order. |
##|keyword_bid_type | string | The bid type for the keyword and match type combination.

Enum values:
- `FOLLOW_ADGROUP`: To use the ad group level bid (`bid_price`) as the `keyword_bid`.
- `CUSTOM`: To customize the bid via `keyword_bid`. |
##|keyword_bid | float | The bid price for the keyword and match type combination. |
##|audit_status | string | The review status of the search keyword.

Enum values:
- `AUDITING`: The keyword is under review.
- `PASS`: The keyword has passed review and can be delivered.
- `REJECTED`: The keyword failed to pass the review and cannot be delivered.|
##|reject_info | object[] | Returned only when `audit_status` is `REJECTED`.

Details about the rejection.|
###|forbidden_location| string |The targeted region that failed the review. 

For enum values, see [Appendix - Location codes](https://business-api.tiktok.com/portal/docs?id=1737585867307010).|
###|reject_reasons| object[] |List of rejection reasons.|
####|reason| string |The rejection reason. |
#|comment_disabled |boolean| Whether to allow comments on your ads on TikTok.  |
#|video_download_disabled |boolean| Whether users can download your video ads on TikTok. |
#|share_disabled|boolean|Whether sharing to third-party platforms is disabled for ads in this ad group. |
#|blocked_pangle_app_ids |string[]|Pangle app block list ID.|
#|audience_type |string| App retargeting audience type. For enum values, see [Enumeration - App Retargeting Audience Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
#|audience_rule |object| Rules that specify your audience.  |
#|saved_audience_id |string|Returned when you have specified `saved_audience_id` in the request. 
Saved Audience ID.|
#|auto_targeting_enabled{-To be deprecated}|boolean|Whether to enable automated targeting. Enum values: `True`, `False`.|
#| shopping_ads_retargeting_type | string | Returned when `shopping_ads_type` is `VIDEO` and `product_source` is `CATALOG`. 

The retargeting type of shopping ads. Enum values: 
- `LAB1`: Retargeting audiences who viewed products or added products to cart but didn't purchase products. 
- `LAB2`: Retargeting audiences who added products to cart but didn't purchase products. 
- `LAB3`: Retargeting audiences using custom combination. 
- `OFF`: No retargeting.  |
#| shopping_ads_retargeting_actions_days | number | The valid time range for the specified audience action. Audiences who have completed the specified action within the time range will be retargeted by the shopping ads. 

Value range: 1, 2, 3, 7, 14, 30, 60, 90, 180. |
#| included_custom_actions | object[] | The custom action that you want to use as "Include" conditions for filtering out the shopping ads audiences to be retargeted. |
##| code | string | The custom action used to filter out the audiences to be retargeted. Enum values: 
- `VIEW_PRODUCT`: The audience viewed the product. 
- `ADD_TO_CART`: The audience added the product to the cart. 
- `PURCHASE`: The audience purchased the product. |
##| days | integer | The time range used to filter out the audiences that completed the specified action. Value range: [1,180]. |
#| excluded_custom_actions | object[] | The custom action that you want to use as "Exclude" conditions for filtering out the shopping ads audiences to be retargeted. |
##| code | string | The custom action used to filter out the audiences to be retargeted. Enum values: 
- `VIEW_PRODUCT`: The audience viewed the product. 
- `ADD_TO_CART`: The audience added the product to the cart. 
- `PURCHASE`: The audience purchased the product. |
##| days | integer | The time range used to filter out the audiences that didn't complete the specified action. Value range: [1,180]. |
#| shopping_ads_retargeting_custom_audience_relation | string | The logical relation between the Video Shopping Ads (VSA) retargeting audience specified by `shopping_ads_retargeting_type` and the custom audience specified by `audience_ids`.

Enum values: 
- `OR`: To combine the VSA retargeting audience and the custom audience to create the targeted audience. The targeted audience will consist of individuals who belong to either the VSA retargeting audience or the custom audience. 
- `AND`: To intersect between the VSA retargeting audience and the custom audience to create the targeted audience. The targeted audience will consist of individuals who belong to both the VSA retargeting audience and the custom audience. |
#|location_ids |string[]|IDs of the targeted locations. Use [Get locations](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) to get available locations. |
#| zipcode_ids|string[]|Zip code IDs or postal code IDs of the targeted locations. |
#|languages |string[]|Codes of the languages that you want to target. For the list of languages codes supported, see [Enumeration - Language Code](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|gender |string|Gender that you want to target. Enum values: `GENDER_FEMALE`,`GENDER_MALE`,`GENDER_UNLIMITED`|
#|age_groups |string[]|Age groups you want to target. For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|spending_power|string|Spending power that you want to target. Enum values: `ALL`, `HIGH`.   If it is set to `HIGH`, you can target high spending users who typically spend more on purchases on TikTok ads than average users. |
#|household_income| string[]| Household income that you want to target. Enum values: `TOP5`(Top 5% of ZIP codes), `TOP10`(Top 10% of ZIP codes), `TOP10_25`(Top 10% -25% of ZIP codes), `TOP25_50`(Top 25% - 50% of ZIP codes). |
#|audience_ids|string[]|A list of audience IDs. |
#| smart_audience_enabled | boolean | Whether Smart audience is turned on. 

Enum values: `true`, `false`. |
#|excluded_audience_ids |string[]|A list of excluded audience ID.|
#|interest_category_ids |string[]|IDs of general interest keywords that you want to use to target audiences.|
#|interest_keyword_ids|string[]|IDs of additional interest keywords that you want to use to target audiences. |
#|purchase_intention_keyword_ids|string[]|IDs of purchase intention categories that you want to use to target audiences with an interest in purchases related to a content category. |
#|actions| object[] | A list of targeting behavioral category objects.|
##|action_scene | string | The type of user behavior that you want to target.

 Enum values: 
- `VIDEO_RELATED`: Video interactions.
- `CREATOR_RELATED`: Creator interactions.
- `HASHTAG_RELATED`: Hashtag interactions.|
##|action_period |number| The time period to include behaviors from.  |
##|video_user_actions|string[]| The specific user interactions that you want to target for the user behavior type.

- If `action_scene` is `VIDEO_RELATED`, the allowed values are: `WATCHED_TO_END`,`LIKED`,`COMMENTED`,`SHARED`.
-  If `action_scene` is `CREATOR_RELATED`, the allowed values are: `FOLLOWING`, `VIEW_HOMEPAGE`. 
- If `action_scene` is `HASHTAG_RELATED`, the allowed value is `VIEW_HASHTAG`. |
##|action_category_ids |string[]|IDs of the video interactions categories, creator interactions categories, hashtags, or hashtag bundles that you want to use to target audiences.|
#| smart_interest_behavior_enabled | boolean | Whether Smart interests & behaviors is turned on. 

 Enum values: `true`, `false`. |
#|included_pangle_audience_package_ids |string[]| IDs of the Pangle audiences that you want to include. Valid only for Pangle placement. You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://ads.tiktok.com/marketing_api/docs?id=1740040177229826) endpoint. You need to set `bind_type` to `INCLUDE`.  Do not specify this field and `excluded_pangle_audience_package_ids` at the same time.|
#|excluded_pangle_audience_package_ids |string[]| IDs of the Pangle audiences that you want to exclude. Valid only for Pangle placement. You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://ads.tiktok.com/marketing_api/docs?id=1740040177229826) endpoint. You need to set `bind_type` to `EXCLUDE`. Do not specify this field and `included_pangle_audience_package_ids` at the same time.|
#|operating_systems |string[]|Device operating systems that you want to target. Only one value is allowed.  Enum: `ANDROID`, `IOS`|
#|min_android_version|string|Minimum Android version. For enum values, see [Enumeration - Minimum Android Version](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|ios14_targeting |string|The iOS devices that you want to target. Enum values:
- `UNSET`: Devices with iOS 14.4 or earlier versions.
- `IOS14_MINUS`: Devices with iOS 14.0 or earlier version that are not affected by the iOS 14 privacy update.
- `IOS14_PLUS`: Devices with iOS 14.5 or later versions. The iOS 14 privacy update has been enforced in this group of devices. This value is only supported for Dedicated Campaigns. 
- `ALL`: Devices with iOS 14.5 or later versions. The iOS 14 privacy update has been enforced in this group of devices. This value is only supported for iOS App Retargeting ads and iOS retargeting Video Shopping Ads with product source as catalog and optimization location as App. |
#|min_ios_version|string|Audience minimum ios version. For enum values, see [Enumeration - Minimum iOS Version](https://ads.tiktok.com/marketing_api/docs?id=1738308662898689).|
#|ios14_quota_type|string|Whether the campaign will be counted against the iOS 14 dedicated campaign quota. Enum: `OCCUPIED`, `UNOCCUPIED`. For non-R&F campaigns, when `ios14_targeting` is `IOS14_PLUS`, this field is automatically set to `OCCUPIED`.|
#|device_model_ids| string[]| List of device model IDs. For more details about device models, see [Device Models](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369).|
#|network_types |string[]|Network types that you want to target. For enum values, see [Enumeration - Connection Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|carrier_ids |string[]| Carriers  that you want to target. A carrier is valid only when the `in_use` field for the carrier is `true`. For detailed information, see [get carriers](https://ads.tiktok.com/marketing_api/docs?id=1737168013095938). |
#| isp_ids | string[] |IDs of the targeted Internet service providers. |
#|device_price_ranges|number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50. 
**Important**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].|
#|targeting_expansion{-To be deprecated}| object | Settings about targeting expansion|
##|expansion_enabled|boolean| Whether to enable targeting expansion |
##|expansion_types |string[]| The target audience types that you want to expand|
#|contextual_tag_ids |string[]|Contextual tag IDs.|
#|brand_safety_type|string|Enum values: 
- `NO_BRAND_SAFETY`:  To not use any brand safety solution.  Full inventory, which means your ads may appear next to some content featuring mature themes. 
- `EXPANDED_INVENTORY`: Use TikTok's brand safety solution. Expanded inventory means that your ads will appear next to content where most inappropriate content has been removed, and that does not contain mature themes. In the next API version, `EXPANDED_INVENTORY` will replace `NO_BRAND_SAFETY` and will be the default brand safety option.
- `STANDARD_INVENTORY`: Use TikTok's brand safety solution. Standard inventory means that ads will appear next to content that is appropriate for most brands. 
- `LIMITED_INVENTORY`: Use TikTok's brand safety solution. Limited inventory means that your ads will not appear next to content that contains mature themes.
- `THIRD_PARTY`: Use a third-party brand safety solution.  To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. |
#|brand_safety_partner|string| Brand safety partner. Available only when `brand_safety_type` is `THIRD_PARTY`. Enum values: `IAS`, `OPEN_SLATE`(The partner is named **DoubleVerify** on TikTok Ads Manager because the partner has been acquired by DoubleVerify).
 To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. You need to pass in the brand safety type and brand safety partner.
**Note**: 
-  Pre-bid third-party brand safety solutions are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. |
#|inventory_filter_enabled|boolean|Inventory filtering (filtering security videos, hides unsafe videos), valid only for the `PLACEMENT_TIKTOK` placement. Optional values are: true to filter, false not to filter. |
#|category_exclusion_ids|string[]|Content exclusion category IDs.|
#|vertical_sensitivity_id|string|Vertical sensitivity category ID.  |
#|budget_mode |string|Budget mode. If Campaign Budget Optimization is enabled, `BUDGET_MODE_INFINITE` will be returned. For more information about budget modes, see [Budget](https://ads.tiktok.com/marketing_api/docs?id=1739381246298114). |
#|budget |float|Ad budget. Returns 0.0 when Campaign Budget Optimization (`budget_optimize_on`) is on. |
#|scheduled_budget|float|Scheduled ad budget for next day. A value not equal to 0 means the scheduled budget is set and the value represents the budget; a value equals to 0 means the scheduled budget is not set.|
#|schedule_type |string|The schedule type can be either `SCHEDULE_START_END` or `SCHEDULE_FROM_NOW`. If you choose `SCHEDULE_START_END`, you need to specify a start time and an end time. If you choose `SCHEDULE_FROM_NOW`, you only need to specify a start time.|
#|schedule_start_time |datetime|Ad delivery start time (UTC+0). Format should be `YYYY-MM-DD HH:MM:SS`|
#|schedule_end_time |datetime|Ad delivery end time (UTC+0). Format should be `YYYY-MM-DD HH:MM:SS`|
#|delivery_mode |string| The strategy for sequencing and scheduling your ad delivery in a Reach & Frequency ad group. 

Enum values:
- `STANDARD`: Standard delivery. Your ads will be distributed evenly and are expected to achieve similar traffic size. 
- `SCHEDULE`: Scheduled delivery.  Set specific time periods to deliver each ad in. 
- `SEQUENCE`: Sequenced delivery. Set a specific sequence to deliver your ads in. 
- `OPTIMIZE`: Optimized delivery that delivers ads to achieve the best performance.|
#|dayparting |string| Ad delivery arrangement, in the format of a string that consists of 48 x 7 characters. Each character is mapped to a 30-minute timeframe from Monday to Sunday. Each character can be set to either 0 or 1.  1 represents delivery in the 30-minute timeframe, and 0 stands for non-delivery in the 30-minute timeframe. The first character is mapped to 0:01-0:30 of Monday; The second character is mapped to 0:31-1:00 of Monday, and the last character represents 23:31-0:00 Sunday.**Note**
Not specified, all-0, or all-1 are considered as full-time delivery. 
|
#|optimization_goal|string|The measurable results that you'd like to drive your ads with. For enum values, see [Enumeration - Optimization Goal](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|secondary_optimization_event|string|The secondary goal when optimization goal (`optimization_goal`) is Install (`INSTALL`) or Value (`VALUE`). For enum values, see [Conversion events - Secondary-goal events](https://ads.tiktok.com/marketing_api/docs?id=1739361474981889).|
#| message_event_set_id | string | The ID of the message event set to use in the Instant Messaging Ad Group. |
#|frequency |number| Frequency, together with `frequency_schedule`, controls how often people see your ad (only available for REACH ads). For example, frequency = 2 frequency_schedule = 3 means "show ads no more than twice every 3 day". |
#|frequency_schedule |number| Frequency schedule, together with `frequency`, controls how often people see your ad (only available for REACH ads). See frequency fields for more.|
#|bid_type |string|Bidding strategy that determines how the system manages your cost per result, spends your budget, and how it delivers ads. **See [Enumeration - Bidding Strategy](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|bid_price |float|Bid price. The average cost per result that you want to achieve (for Cost Cap bidding strategy). |
#|conversion_bid_price |float|Where you can set a target cost per conversion for oCPM(Optimized Cost per Mille).|
#|deep_bid_type |string|Bidding strategy for in-app events. For enum values and their descriptions, see [Enumeration - Deep-level Bidding Strategy](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|roas_bid|float|ROAS goal for Value Optimization.|
#| vbo_window | string | The time window of the specified bidding strategy for [VBO IAA](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app advertising) or [VBO IAP](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app purchase).   

 Enum values: 
- `SEVEN_DAYS`: The first seven days (day 7).  
- `ZERO_DAY`: The current day (day 0). |
#|bid_display_mode|string|How you calculate and measure Cost per View.  |
#|deep_cpa_bid |float|Specify bid price in this field after you've chosen a bidding strategy for in-app events, for example VO_MIN.|
#|cpv_video_duration |string| Optimized video playback duration  Optional values include: `SIX_SECONDS` (video playback 6 seconds) and ` TWO_SECONDS` (video playback 2 seconds) |
#|next_day_retention | float | Day 2 retention ratio. Formula: `next_day_retention` = `conversion_bid_price`/`deep_cpa_bid`. Value range is (0,1]. Only valid when `placements` is `PLACEMENT_PANGLE` and `secondary_optimization_event` is `NEXT_DAY_OPEN`. |
#| click_attribution_window | string | Click-through window for the ad group. This attribution window is the time between when a person clicks your ad and then takes an action. 

Enum values: 
- `OFF`: Off. 
-  `ONE_DAY`: 1-day click.
- `SEVEN_DAYS`: 7-day click. 
- `FOURTEEN_DAYS`: 14-day click.
-  `TWENTY_EIGHT_DAYS`: 28-day click. |
#| engaged_view_attribution_window | string | Engaged view-through window for the ad group. This attribution window is the time after someone watches at least 6 seconds of your video ad that a conversion is counted.

Enum values: 
- `ONE_DAY`: 1-day engaged view.
- `SEVEN_DAYS`: 7-day engaged view.|
#| view_attribution_window | string | View-through window for the ad group. This attribution window is the time between when a person views your ad and then takes an action. 

Enum values: 
- `OFF`: Off.
- `ONE_DAY`: 1-day view.
- `SEVEN_DAYS`: 7-day view.|
#| attribution_event_count | string | Event count (Statistic type) for the ad group. 
The way that people's actions are counted after only viewing or clicking an ad. 

Enum values: 
- `UNSET`: Unset. 
-  `EVERY`: Every. To count multiple events from someone as separate conversions. 
-  `ONCE`: Once. To count multiple events from someone as 1 conversion.|
#|billing_event |string| Billing event. 
To learn about the enum values, see [Enumerations - Billing Event](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Billing%20Event).|
#|pacing |string| You can choose between `PACING_MODE_SMOOTH` and `PACING_MODE_FAST`. For `PACING_MODE_SMOOTH`, the budget is allocated evenly within the scheduled time. `PACING_MODE_FAST` would consume budget and produce results as soon as possible. |
#|operation_status |string|Operation status.

Enum values:
- `ENABLE` : The ad group is enabled (in 'ON' status).
- `DISABLE`: The ad group is disabled (in 'OFF' status). 
- `FROZEN`: The ad group is terminated and cannot be enabled. |
#|secondary_status |string|Ad group status  See [Enumeration - Ad group status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138) for optional values.|
#|statistic_type |string| Conversion bid statistic type, bid for `EVERYTIME` (Each Purchase)/ `NONE` (Unique Purchase)|
#|is_hfss |boolean|Whether the promoted content is HFSS (High Fat, Salt, Sugar) Product/Brand.

Supported values: `true`,`false`. |
#| is_lhf_compliance | boolean | Whether the promoted content complies with LHF (Less Healthy Foods) regulations.

When `is_lhf_compliance` is `true`, you confirm that any food or drink products you advertise on TikTok in the UK comply with the [2024 Less Healthy Foods Regulations](https://www.legislation.gov.uk/uksi/2024/1266/made) and all other applicable laws.

Supported values: `true`,`false`. |
#|creative_material_mode |string|The strategy that your creatives will be delivered. 
Enum values: `CUSTOM`(custom), `DYNAMIC`(Automated Creative Optimization) (Deprecated), and `SMART_CREATIVE`(Smart Creative). |
#|adgroup_app_profile_page_state|string| Indicates whether the ad group is using app profile page. Enum values: `INVALID`, `UNSET`, `ON`, `OFF`.|
#|feed_type |string| Feed type option. Enum values: `STANDARD_FEED`, `TOP_FEED`.  |
#| rf_purchased_type  | string | Billing method of Reach & Frequency ad groups. For more details, see [Enumeration - Reach & Frequency Buy Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
Note**: The value of this field will always be null.|
#| purchased_impression | number | Impressions to be purchased. 
**Note**: The value of this field will always be null.|
#| purchased_reach  | number | Purchased user reach. 
**Note**: The value of this field will always be null.|
#| rf_estimated_cpr | number |  The estimated cost per mile reach. 
**Note**: The value of this field will always be null.|
#| rf_estimated_frequency | number | The estimated show frequency. 
**Note**: The value of this field will always be null.|
#|is_new_structure|boolean|Whether the campaign is a new structure |
#|skip_learning_phase |boolean|Whether to skip the learning stage. |
#|conversion_window {-Deprecated} |string| The time frame when you would like a conversion to happen after a user clicks on or views your ad. Your ad delivery will be optimized using the conversion data during the time frame you select. This setting will not impact your attribution data. For enum values, ee [Enumeration - Conversion Window](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|page_info |object|Paging information |
##|page |number|current page number |
##|page_size |number|Paging Size |
##|total_number |number|Total, the total number of eligible ad groups |
##|total_page |number|total pages |
|request_id |string|The log id of a request, which uniquely identifies the request.|
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
        "purchased_reach": null,
        "budget_mode": "BUDGET_MODE_TOTAL",
        "conversion_bid_price": 0,
        "adgroup_app_profile_page_state": null,
        "search_result_enabled": false,
        "create_time": "{{create_time}}",
        "rf_purchased_type": null,
        "comment_disabled": false,
        "category_id": "0",
        "statistic_type": null,
        "brand_safety_type": "NO_BRAND_SAFETY",
        "promotion_type": "WEBSITE",
        "modify_time": "{{modify_time}}",
        "pixel_id": null,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "is_hfss": false,
        "excluded_audience_ids": [],
        "actions": [],
        "gender": "GENDER_UNLIMITED",
        "adgroup_name": "{{adgroup_name}}",
        "adgroup_id": "{{adgroup_id}}",
        "app_download_url": null,
        "optimization_goal": "CLICK",
        "frequency": null,
        "deep_cpa_bid": 0,
        "inventory_filter_enabled": false,
        "audience_ids": [],
        "auto_targeting_enabled": false,
        "deep_bid_type": null,
        "brand_safety_partner": null,
        "campaign_name": "{{campaign_name}}",
        "operating_systems": [
            "ANDROID"
        ],
        "network_types": [],
        "is_new_structure": true,
        "scheduled_budget": 0,
        "schedule_end_time": "{{schedule_end_time}}",
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "video_download_disabled": false,
        "app_type": null,
        "category_exclusion_ids": [],
        "age_groups": null,
        "location_ids": [
            "{{location_id}}"
        ],
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "optimization_event": null,
        "interest_keyword_ids": [],
        "campaign_id": "{{campaign_id}}",
        "bid_price": 0,
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "ios14_quota_type": "UNOCCUPIED",
        "delivery_mode": null,
        "secondary_optimization_event": null,
        "app_id": null,
        "creative_material_mode": "CUSTOM",
        "share_disabled": false,
        "purchased_impression": null,
        "rf_estimated_frequency": null,
        "operation_status": "ENABLE",
        "next_day_retention": null,
        "schedule_type": "SCHEDULE_START_END",
        "frequency_schedule": null,
        "schedule_infos": null,
        "keywords": null,
        "bid_type": "BID_TYPE_NO_BID",
        "bid_display_mode": "CPMV",
        "skip_learning_phase": false,
        "billing_event": "CPC",
        "interest_category_ids": [],
        "rf_estimated_cpr": null,
        "isp_ids": [],
        "pacing": "PACING_MODE_SMOOTH",
        "feed_type": null,
        "schedule_start_time": "{{schedule_start_time}}",
        "languages": [],
        "conversion_window": null,
        "budget": {{budget}},
        "advertiser_id": "{{advertiser_id}}",
        "device_price_ranges": null,
        "need_audit": false
    }
}
(/code);
```
