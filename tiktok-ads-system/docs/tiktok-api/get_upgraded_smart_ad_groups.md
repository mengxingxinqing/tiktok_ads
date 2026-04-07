# Get Upgraded Smart+ Ad Groups

**Doc ID**: 1843314879617026
**Path**: API Reference/Upgraded Smart+/Ad groups/Get Upgraded Smart+ Ad Groups

---

Use this endpoint to retrieve Upgraded Smart+ Ad Groups within an ad account.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/get/

**Method** GET

**Header**

```xtable
|Field{35%}|Type{15%}|Description{50%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
```

**Parameters**

```xtable
|Field{35%}|Type{15%}|Description{50%}|
|--- |--- |--- |
| advertiser_id {Required} | string | Advertiser ID. |
| fields | string[] | Fields that you want to get.

When this field is not specified, all fields are returned by default.

For allowed fields, see the fields under `list` in the [Response](#item-link-Response) section.|
| filtering | object | Filtering conditions.

Example: `filtering={"objective_type":"APP_PROMOTION"}`|
#|campaign_ids | string[] | Filter by campaign IDs.

Max size: 100.

To obtain campaign IDs, use [/smart_plus/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1843312818332930). |
#|adgroup_ids | string[] | Filter by ad group IDs.

Max size: 100. |
#|adgroup_name | string | Ad group name. |
#|primary_status | string | Primary status. 

For enum values, see [Enumeration-Primary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Primary%20Status).
The default value is `STATUS_NOT_DELETE`, which returns ad groups in all statuses excluding `STATUS_DELETE`. 

If you want to get ad groups in all statuses including `STATUS_DELETE`, use `STATUS_ALL` instead. |
#|secondary_status | string | Ad group secondary status. 

For enum values, see [Enumeration - Ad Group Status - Secondary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Ad%20group%20status%20-%20secondary%20status). |
#|objective_type | string | Advertising objective.

Currently, we support `APP_PROMOTION`, `WEB_CONVERSIONS`, and `LEAD_GENERATION`.

For detailed explanation of enum values, see [Enumeration-Advertising Objective](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Advertising%20Objective). |
#| sales_destination | string | Sales destination, the destination where you want to drive your sales.

Enum values:
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.|
#|promotion_type|string|Promotion type (Optimization location). You can decide where you'd like to promote your products using this field.

Currently, we support `APP_ANDROID`, `APP_IOS`, `WEBSITE`, and `LEAD_GENERATION`.
- When `objective_type` is `APP_PROMOTION`, set this field to `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `WEB_CONVERSIONS`, set this field to `WEBSITE`.
- When `objective_type` is `LEAD_GENERATION`, set this field to `LEAD_GENERATION`.|
#|optimization_goal | string | The measurable results you'd like to drive with your campaigns.

Currently, we support `CLICK`, `INSTALL`, `IN_APP_EVENT`, `VALUE`, `CONVERT`, `TRAFFIC_LANDING_PAGE_VIEW`, and `LEAD_GENERATION`.

To find the detailed description for each optimization goal, see [Enumeration - Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal). |
| page | number | Current page number.

Default value: 1. 
Value range: ≥ 1. |
| page_size | number | Page size.

Default value: 10. 
Value range: 1-1,000. |
```

### Example

```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/get/?advertiser_id={{advertiser_id}}&page=1&page_size=1000' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

## Response

```xtable
|Field{35%}|Type{15%}|Description{50%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://business-api.tiktok.com/portal/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#|list |object[]|A list of Upgraded Smart+ ad groups within an ad account.|
##|advertiser_id |string|Advertiser ID.|
##|campaign_id |string|Campaign ID.|
##|campaign_name |string|The name of the campaign that the ad group belongs to.|
##|adgroup_id |string|Ad group ID.|
##|adgroup_name |string|Ad group name.|
##|catalog_id |string|Returned when `catalog_enabled` is  `true` at the campaign level.

The ID of the catalog used in the ad group.|
##|catalog_authorized_bc_id |string|Returned when `catalog_enabled` is  `true` at the campaign level.

The ID of the Business Center that the catalog (`catalog_id`) belongs to.|
##|promotion_type |string|Promotion type (Optimization location). You can decide where you'd like to promote your products using this field.

Currently, we support `APP_ANDROID`, `APP_IOS`, `WEBSITE`, and `LEAD_GENERATION`.
- When `objective_type` is `APP_PROMOTION`, this field will be `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `WEB_CONVERSIONS`, this field will be `WEBSITE`.
- When `objective_type` is `LEAD_GENERATION`, this field will be `LEAD_GENERATION`.|
##|app_id |string|The App ID of the app to promote.

To get a list of App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).|
##| gaming_ad_compliance_agreement|string|Returned only in any of the following scenarios:
- Scenario 1: When the following conditions are both met at the campaign level:`objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_RETARGETING`.
- Scenario 2: When the following conditions are all met at the campaign level:`objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_INSTALL`.
- `campaign_type` is `REGULAR_CAMPAIGN`.
Whether to agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok.

The policy is as follows: Yo confirms and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.

Enum values:
- `ON`: To agree to the policy.
- `OFF`: To leave the policy not accepted.|
##|promotion_website_type |string|TikTok Instant Page type.

Currently, we only support `TIKTOK_NATIVE_PAGE`(To use TikTok Instant Page).|
##|promotion_type|string|Promotion type (Optimization location). You can decide where you'd like to promote your products using this field.

Currently, we support `APP_ANDROID`, `APP_IOS`, `WEBSITE`, `MINI_GAME`, and `LEAD_GENERATION`.
- When `objective_type` is `APP_PROMOTION`  and `app_promotion_type` is `APP_INSTAL`, this field will be `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `MINIS`, this field will be `MINI_APP` or `MINI_GAME`.
- When `objective_type` is `WEB_CONVERSIONS`:If `sales_destination` is `WEBSITE`, this field will be `WEBSITE`.
- If `sales_destination` is `APP`, this field will be `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `LEAD_GENERATION`, this field will be any of the following values:`LEAD_GENERATION`
- `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
- `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
- `LEAD_GEN_CLICK_TO_CALL`|
##|optimization_goal |string|The measurable results that you'd like to drive your ads with.

For enum values, see [Enumeration - Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal).|
##|pixel_id |string|Pixel ID.|
##| app_config | object[] | Returned when `sales_destination` is `WEB_AND_APP`.

Details of the app or apps to promote. |
###| app_id | string | The App ID of the app to promote. |
##| minis_id|string|Returned when `promotion_type` is `MINI_APP` or `MINI_GAME`.

The ID of the TikTok Minis.|
##|optimization_event |string|Conversion event for the ad group.

See [Conversion events](https://business-api.tiktok.com/portal/docs?id=1739361474981889) for more.|
##|custom_conversion_id |string|The ID of the Custom Conversion used in the ad group.|
##|deep_funnel_optimization_status |string|With deep funnel optimization, you can select a secondary event alongside the primary optimization event, which can help improve campaign effectiveness.  

Enum values:  
- `ON`: enabled.
- `OFF`: disabled.|
##|deep_funnel_event_source |string|Returned when `deep_funnel_optimization_status` is `ON`.

The event source type.

Enum values:
- `PIXEL`: Pixel.
- `OFFLINE`: Offline Event Set.
- `CRM`: CRM Event Set.|
##|deep_funnel_event_source_id |string|Returned when `deep_funnel_optimization_status` is `ON`.

Event Source ID.
- When `deep_funnel_event_source` is `PIXEL` , this field represents a Pixel ID.
- When `deep_funnel_event_source` is `OFFLINE`, this field represents an Offline Event Set ID.
- When `deep_funnel_event_source` is `CRM`, this field represents a CRM Event Set ID.|
##|deep_funnel_optimization_event |string|Returned when `deep_funnel_optimization_status` is `ON`.

Deep funnel optimization event.

Example: `SHOPPING`.|
##| identity_id|string|Returned only when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` and your ad account is allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.

Identity ID.|
##| identity_type |string|Returned only when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` and your ad account is allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.

Identity type.

Enum values: 
- `TT_USER` : TikTok Business Account User.
- `BC_AUTH_TT`: The TikTok account that a Business Center is authorized to access.
See [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097) for details.|
##| identity_authorized_bc_id|string|Returned when `identity_type` is `BC_AUTH_TT`.

ID of the Business Center that a TikTok Account User in Business Center identity is associated with.|
##| messaging_app_type|string|The type of instant messaging app or customized URL to use in the Instant Messaging Ad Group.

Enum values:
- `MESSENGER`: Messenger. 
- `WHATSAPP`: WhatsApp. 
- `ZALO`: Zalo. 
- `LINE`: Line. 
- `IM_URL`: Instant Messaging URL.
To learn more about how to create Upgraded Smart+ TikTok Instant Messaging Ads, see [Create an Upgraded Smart+ Lead Generation Campaign with optimization location as instant messaging apps](https://business-api.tiktok.com/portal/docs?id=1847302988449921).|
##| zalo_id_type |string|The type of Zalo contact format.

Enum values:
- `ZALO_OFFICIAL_ACCOUNT`: Zalo Official Account ID. 
- `ZALO_PHONE_ACCOUNT`: Zalo phone number. |
##| messaging_app_account_id |string|The ID of the instant messaging app account.
- When `messaging_app_type` is `MESSENGER`, this field represents the Facebook Page ID.
- When `messaging_app_type` is `LINE`, this field represents the LINE Business ID.
- When `zalo_id_type` is `ZALO_OFFICIAL_ACCOUNT`, this field represents the Zalo Official Account ID.
- When `messaging_app_type` is `WHATSAPP` or when `zalo_id_type` is `ZALO_PHONE_ACCOUNT`, this field represents the WhatsApp or Zalo phone number automatically populated based on the specified `phone_info`.|
##| message_event_set_id|string|The ID of the message event set to be used in the Instant Messaging Ad Group.

If the instant messaging app account, either the Messenger account or Zalo Official Account specified via `messaging_app_account_id` or the WhatsApp or Zalo phone account matched from the specified `phone_info`, in your ad group settings matches an existing event set, this field will be **automatically populated** with the unique message event set associated with the instant messaging app account you choose.|
##| phone_info|object|Details of WhatsApp or Zalo phone number.|
###| phone_region_code |string|The region code for WhatsApp or Zalo phone number.

Example: `US`.|
###| phone_region_calling_code|string|The region calling code for the WhatsApp or Zalo phone number.

Example: `+1`.|
###| phone_number|string|The WhatsApp or Zalo phone number.|
##|bid_type |string|Bidding strategy.

For enum values and their descriptions, see [Enumeration - Bidding Strategy](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Bidding%20Strategy).|
##|bid_price |float|The target cost per click. The system will aim to get the most results while keeping the average cost per result around or lower than the specified amount.|
##|conversion_bid_price |float|The target cost per conversion or cost per landing page view. The system will aim to get the most results while keeping the average cost per result around or lower than the specified amount.|
##|deep_bid_type |string|Bidding strategy for in-app events.

For enum values and their descriptions, see [Enumeration - Deep Event Bidding Strategy](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Deep%20Event%20Bidding%20Strategy).|
##|roas_bid |float|Target ROAS for Value-Based Optimization.|
##| incentive_offer_type|string|The type of incentive offer applicable to the Upgraded Smart+ Ad Group.
If your ad group meets the eligibility criteria and exceeds certain CPA or Minimum ROAS/Target ROAS thresholds, you will be incentivized with ad credits to use within the same ad account.
To learn more about the incentive offer eligibility criteria and the calculation of incentive amount, see [Smart+ Platform Incentive Offer (Cost Cap/Minimum ROAS/Target ROAS)](https://ads.tiktok.com/help/article/incentive-offer). 

Enum values:
- `INELIGIBLE`: The ad group is ineligible for any incentive offer.
- `COST_CAP_AND_MIN_ROAS`: The ad group uses the Cost Cap or Minimum ROAS/Target ROAS bidding strategy and is eligible for the incentive offer. |
##|vbo_window |string|The time window of the specified bidding strategy for [VBO IAA](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app advertising) or [VBO IAP](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app purchase).

Enum values:
- `SEVEN_DAYS`: The first seven days (day 7).
- `ZERO_DAY`: The current day (day 0).|
##|click_attribution_window|string|Click-through window. This attribution window is the time between when a person clicks your ad and then takes an action.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day click.
- `SEVEN_DAYS`: 7-day click.
- `FOURTEEN_DAYS`: 14-day click.
- `TWENTY_EIGHT_DAYS`: 28-day click.
- `THIRTY_DAYS`: 30-day click.
- `THIRTY_TWO_DAYS`: 32-day click.
- `ONE_HUNDRED_EIGHTY_DAYS`: 180-day click.|
##| engaged_view_attribution_window | string | Engaged view-through window. This attribution window is the time after someone watches at least 6 seconds of your video ad that a conversion is counted.

Enum values:
- `OFF`: off.
- `ONE_DAY`: 1-day engaged view.
- `SEVEN_DAYS`: 7-day engaged view.
- `FOURTEEN_DAYS`: 14-day engaged view.
- `TWENTY_EIGHT_DAYS`: 28-day engaged view.|
##|view_attribution_window |string|View-through window. This attribution window is the time between when a person views your ad and then takes an action.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day view.
- `SEVEN_DAYS`: 7-day view.|
##|attribution_event_count |string|Event count (Statistic type).
The way that people's actions are counted after only viewing or clicking an ad.

Enum values:
- `UNSET`: Unset.
- `EVERY`: Every. To count multiple events from someone as separate conversions.
- `ONCE`: Once. To count multiple events from someone as 1 conversion.|
##|billing_event |string|Billing event.

For enum values, see [Enumerations - Billing event](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Billing%20Event).|
##|pacing |string|Delivery type. Your choice of ad delivery type determines the speed at which your daily budget is used.

Enum values:
- `PACING_MODE_SMOOTH`: Standard. Your budget will be used as evenly as possible depending on market demand and peaktime rates. This delivery type is suitable for advertisers who prefer steady spending.|
##|budget_mode |string|Ad group budget mode. 

Enum values:
- `BUDGET_MODE_TOTAL`: Lifetime budget.
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.|
##| budget_auto_adjust_strategy |string|Returned only when the following conditions are both met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level: `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
The ad group budget strategy for custom ad group budget.

Enum values: 
- `AUTO_BUDGET_INCREASE`: To enable Goal-based udget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. 
- When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, the specified `budget` will be the initial daily budget. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based budget increase.|
##|budget|float|Fixed ad group budget or initial ad group budget.
- When `budget_auto_adjust_strategy`  is `UNSET`, this field represents your fixed ad group budget.
- When `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`, this field represents your initial ad group budget. To retrieve the current campaign budget, check the returned `current_budget`.|
##| current_budget|float|Returned only when `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`.

Current ad group budget for an ad group with Goal-based budget increase enabled.|
##|min_budget |float|Ad group minimum budget. 
The system will aim to spend at least this amount, but it is not guaranteed.|
##|schedule_type |string|Schedule type.

Enum values:
- `SCHEDULE_FROM_NOW`: To run the ad group continuously after the scheduled start time.
- `SCHEDULE_START_END`: To run the ad group between the scheduled start time and end time.|
##|schedule_start_time |string|Ad group delivery start time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).|
##|schedule_end_time |string|Ad group delivery end time, in the format of`YYYY-MM-DD HH:MM:SS` (UTC+0).|
##| movie_premiere_date|string|The theatrical release date, in the format of `YYYY-MM-DD` (UTC+0).

Providing the movie release date allows the system to incorporate this timing into performance enhancements.|
##|dayparting |string|Ad delivery arrangement, in the format of a string that consists of 48 x 7 characters. 
Each character is mapped to a 30-minute timeframe from Monday to Sunday. Each character can be set to either 0 or 1. 1 represents delivery in the 30-minute timeframe, and 0 stands for non-delivery in the 30-minute timeframe. The first character is mapped to 0:01-0:30 of Monday; The second character is mapped to 0:31-1:00 of Monday, and the last character represents 23:31-0:00 Sunday.

**Note**: All-0 and all-1 values are considered full-time delivery.
|
##|targeting_optimization_mode |string|Audience targeting optimization mode.

Enum values:
- `MANUAL`: Custom targeting. You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
- `AUTOMATIC`: Automatic targeting. You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.|
##|suggestion_audience_enabled |boolean|Whether to enable audience suggestions.
Audience suggestions guide automatic targeting by choosing additional audience settings. These serve as suggestions only, and delivery to those audiences is not guaranteed.

Supported values: `true`, `false`.|
##|targeting_spec |object|Targeting settings.|
###| app_targeting_type |string|Returned only when the following conditions are all met:
- At the campaign level:
- `objective_type` is `WEB_CONVERSIONS`
- `sales_destination` is `APP`.
- `optimization_goal` is `CLICK`, `IN_APP_EVENT`, or `VALUE`.
App targeting type.

Enum values:
- `PROSPECT`: Prospecting. Find prospective customers, including those who have not interacted with your products.
- `RETARGETING`: Retargeting. Show ads to people who have already interacted with your business on and off TikTok.|
###|location_ids |string[]|IDs of the locations that you want to target.|
###|zipcode_ids |string[]|Zip code IDs or postal code IDs of the targeted locations.|
###|spc_audience_age |string|The age group that the ad group targets.

Enum values:
- `ALL`: all age groups.
- `OVER_EIGHTEEN`: 18+.
- `OVER_TWENTY_FIVE`: 25+.|
###|languages |string[]|Codes of the languages that you want to target. 
For the list of language codes supported, see [Enumerations - Language Code](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Language%20Code).|
###|operating_systems |string[]|Device operating systems that you want to target. 

Enum values: `ANDROID`, `IOS`|
###|excluded_audience_ids |string[]|List of audience IDs to be excluded.|
###|age_groups |string[]|Age groups you want to target. 

For enum values, see [Enumeration - Age Group](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Age%20Group).|
###|gender |string|Gender that you want to target.

Enum values: `GENDER_FEMALE`, `GENDER_MALE`, `GENDER_UNLIMITED`.|
###|audience_ids |string[]|A list of audience IDs.|
###|shopping_ads_retargeting_type|string|The retargeting type.

Enum values:
- `LAB1`: Retargeting audiences who viewed products or added products to cart but didn't purchase products.
- `LAB2`: Retargeting audiences who added products to cart but didn't purchase products.
- `LAB3`: Retargeting audiences using custom combination.
- `OFF`: No retargeting.|
###|shopping_ads_retargeting_actions_days|number|Returned when `shopping_ads_retargeting_type` is `LAB1` or `LAB2`.

The valid time range for the specified audience action. Audiences who have completed the specified action within the time range will be retargeted.|
###|included_custom_actions|object[]|Details of the catalog audience to include.
Catalog audience is based on people's interactions with specific products and often drives better performance than custom audience.|
####|code|string|The custom action used to filter the audiences to be retargeted.

Enum values:
- `VIEW_PRODUCT`: The audience viewed the product.
- `ADD_TO_CART`: The audience added the product to the cart.
- `PURCHASE`: The audience purchased the product.|
####|days|integer|The time range used to filter the audiences that completed the specified action.|
###|excluded_custom_actions|object[]|Details of the catalog audience to exclude.
Improve ad performance by excluding products that people have already interacted with, ensuring they only see relevant ads from your brand.|
####|code|string|The custom action used to filter out the audiences.

Enum values:
- `VIEW_PRODUCT`: The audience viewed the product.
- `ADD_TO_CART`: The audience added the product to the cart.
- `PURCHASE`: The audience purchased the product.|
####|days|integer|The time range used to filter out the audiences that completed the specified action.|
###|shopping_ads_retargeting_custom_audience_relation|string|The logical relation between the retargeting audience specified by `shopping_ads_retargeting_type` and the custom audience specified by `audience_ids`.

Enum values:
- `OR`: To combine the retargeting audience and the custom audience to create the targeted audience. The ad group will target anyone in catalog or custom audiences.
- `AND`: To intersect between the retargeting audience and the custom audience to create the targeted audience. The ad group will target individuals who belong to both the retargeting audience and the custom audience.|
###|included_pangle_audience_package_ids |string[]|IDs of the Pangle audiences that you want to include. |
###|excluded_pangle_audience_package_ids |string[]|IDs of the Pangle audiences that you want to exclude. |
###|interest_category_ids |string[]|IDs of general interest keywords that you want to use to target audiences.|
###|interest_keyword_ids |string[]|IDs of additional interest categories that you want to use to target audience.

To search for additional interest categories, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/interest_keyword/recommend/](https://business-api.tiktok.com/portal/docs?id=1763590884474882).|
###|purchase_intention_keyword_ids |string[]|IDs of purchase intention categories that you want to use to target audiences with an interest in purchases related to a content category.|
###|actions |object[]|A list of targeting behavioral category objects.|
####|action_scene |string|The type of user behavior that you want to target.

Enum values:
- `VIDEO_RELATED`: Video interactions.
- `CREATOR_RELATED`: Creator interactions.
- `HASHTAG_RELATED`: Hashtag interactions.|
####|action_period |number|The time period to include behaviors from.|
####|video_user_actions |string[]|The specific user interactions that you want to target for the user behavior type.
- If `action_scene` is `VIDEO_RELATED`, the allowed values are: `WATCHED_TO_END`,`LIKED`,`COMMENTED`,`SHARED`.
- If `action_scene` is `CREATOR_RELATED`, the allowed values are: `FOLLOWING`, `VIEW_HOMEPAGE`.
- If `action_scene` is `HASHTAG_RELATED`, the allowed value is `VIEW_HASHTAG`.|
####|action_category_ids |string[]|IDs of the video interactions categories, creator interactions categories, hashtags, or hashtag bundles that you want to use to target audiences.|
###|smart_interest_behavior_enabled |boolean|Whether Smart interests & behaviors is turned on.

Supported values: `true`, `false`.

To learn more about Smart interests & behaviors and how to turn on Smart interests & behaviors, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586).|
###|smart_audience_enabled |boolean|Whether to turn on Smart audience.

Supported values: `true`, `false`.

To learn more about Smart audience and how to turn on Smart audience, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586).|
###|spending_power |string|Spending power that you want to target. 

Enum values: `ALL`, `HIGH`. 

If it is set to `HIGH`, you can target high spending users who typically spend more on purchases on TikTok ads than average users.|
###|household_income |string[]|Household income that you want to target. 

Enum values: `TOP5`(Top 5% of ZIP codes), `TOP10`(Top 10% of ZIP codes), `TOP10_25`(Top 10% -25% of ZIP codes), `TOP25_50`(Top 25% - 50% of ZIP codes).|
###|min_android_version |string|Minimum Android version. 

For enum values, see [Enumeration - Minimum Android Version](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Minimum%20Android%20Version).|
###|min_ios_version |string|Audience minimum ios version. 

For enum values, see [Enumeration - Minimum iOS Version](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Minimum%20iOS%20Version).|
###|device_model_ids |string[]|List of device model IDs. |
###|network_types |string[]|Network types that you want to target. 

For enum values, see [Enumeration - Connection Type](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Connection%20Type).|
###|carrier_ids |string[]|Carriers that you want to target. |
###|isp_ids |string[]|IDs of the targeted Internet service providers.|
###|device_price_ranges |number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50.

**Important**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].
|
###|saved_audience_id |string|Returned when you have specified `saved_audience_id` when creating an ad group.

Saved Audience ID.|
###|blocked_pangle_app_ids |string[]|Pangle app block ID list.|
###|brand_safety_type |string|Inventory filter tier for the Smart+ Campaign.

Enum values:
- `EXPANDED_INVENTORY`: Expanded inventory. Your ads will not appear next to explicitly inappropriate content, but they may appear next to content that features mature themes.
- `STANDARD_INVENTORY`: Standard inventory. Your ads will appear next to content that is appropriate for most brands.
- `LIMITED_INVENTORY`: Limited inventory. Your ads will not appear next to content that contains mature themes.
- `NO_BRAND_SAFETY`: Full inventory without using any brand safety solution, which means your ads may appear next to some content featuring mature themes.

**Note**: The setting is automatically applied based on your [Brand Safety Hub](https://business-api.tiktok.com/portal/docs?id=1739381752981505#item-link-Brand%20Safety%20Hub) configurations. To retrieve the details of such settings for your ad account, use [/tiktok_inventory_filters/get/](https://business-api.tiktok.com/portal/docs?id=1830112550443073).
|
###|category_exclusion_ids |string[]|Content exclusion category IDs.|
##| is_hfss|boolean|Whether the promoted content is HFSS (High Fat, Salt, Sugar) Product/Brand.

Supported values: `true`, `false`.|
##| is_lhf_compliance |boolean|Whether the promoted content complies with LHF (Less Healthy Foods) regulations.

When `is_lhf_compliance` is `true`, you confirm that any food or drink products you advertise on TikTok in the UK comply with the [2024 Less Healthy Foods Regulations](https://www.legislation.gov.uk/uksi/2024/1266/made) and all other applicable laws.

Supported values: `true`, `false`.|
##|placement_type |string[]|The placement strategy that decides where your ads will be shown.

Enum values: 
- `PLACEMENT_TYPE_AUTOMATIC`: Automatic placement.
- `PLACEMENT_TYPE_NORMAL` : Select placement.|
##|placements |string[]|The apps where you want to deliver your ads.

Enum values: 
- `PLACEMENT_TIKTOK`: TikTok.
- `PLACEMENT_PANGLE`: Pangle.
- `PLACEMENT_GLOBAL_APP_BUNDLE`: Global App Bundle.|
##|search_result_enabled |boolean|Whether to include your ads in Search Ads, namely to show your ads to users when they search for your business on TikTok.

Supported values: `true`, `false`.|
##|comment_disabled |boolean|Whether to allow comments on your ads on TikTok.

Supported values: `true`, `false`.|
##|share_disabled |boolean|Whether to disable sharing of the campaign to third-party platforms.

Supported values: `true`, `false`.|
##|video_download_disabled |boolean|Whether users can download your video ads on TikTok.

Supported values: `true`, `false`.|
##|skip_learning_phase |boolean|Whether to skip the learning stage.

Supported value: `true`.|
##|create_time |string|The time when the ad group was created, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).

Example: `2025-01-01 00:00:01`.|
##|modify_time |string|The time when the ad group was last modified, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).

Example: `2025-01-01 00:00:01`.|
#|page_info |object|Pagination information.|
##|page |number|Current page number.|
##|page_size |number|Page size.|
##|total_number |number|Total number of results.|
##|total_page |number|Total pages of results.|
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
                "adgroup_id": "{{adgroup_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "bid_type": "BID_TYPE_NO_BID",
                "billing_event": "CPC",
                "budget": 0,
                "budget_mode": "BUDGET_MODE_INFINITE",
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
                "catalog_id": "{{catalog_id}}",
                "comment_disabled": false,
                "conversion_bid_price": 0,
                "create_time": "{{create_time}}",
                "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "optimization_goal": "CLICK",
                "pacing": "PACING_MODE_SMOOTH",
                "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
                "placements": [
                    "PLACEMENT_TIKTOK"
                ],
                "product_source": "CATALOG",
                "promotion_type": "WEBSITE",
                "promotion_website_type": "UNSET",
                "schedule_end_time": "{{schedule_end_time}}",
                "schedule_start_time": "{{schedule_start_time}}",
                "schedule_type": "SCHEDULE_START_END",
                "search_result_enabled": true,
                "secondary_status": "ADGROUP_STATUS_TIME_DONE",
                "share_disabled": false,
                "targeting_optimization_mode": "AUTOMATIC",
                "targeting_spec": {
                    "age_groups": [
                        "AGE_18_24",
                        "AGE_25_34",
                        "AGE_35_44",
                        "AGE_45_54",
                        "AGE_55_100"
                    ],
                    "brand_safety_type": "EXPANDED_INVENTORY",
                    "gender": "GENDER_UNLIMITED",
                    "location_ids": [
                        "3686110"
                    ],
                    "spc_audience_age": "OVER_EIGHTEEN",
                    "spending_power": "ALL"
                },
                "video_download_disabled": false
            },
            {
                "adgroup_id": "{{adgroup_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "attribution_event_count": "EVERY",
                "bid_type": "BID_TYPE_NO_BID",
                "billing_event": "OCPM",
                "budget": 0,
                "budget_mode": "BUDGET_MODE_INFINITE",
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
                "catalog_id": "{{catalog_id}}",
                "click_attribution_window": "SEVEN_DAYS",
                "comment_disabled": false,
                "conversion_bid_price": 0,
                "create_time": "{{create_time}}",
                "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "optimization_event": "ADD_BILLING",
                "optimization_goal": "CONVERT",
                "pacing": "PACING_MODE_SMOOTH",
                "pixel_id": "{{pixel_id}}",
                "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
                "placements": [
                    "PLACEMENT_TIKTOK"
                ],
                "product_source": "CATALOG",
                "promotion_type": "WEBSITE",
                "promotion_website_type": "UNSET",
                "schedule_end_time": "{{schedule_end_time}}",
                "schedule_start_time": "{{schedule_start_time}}",
                "schedule_type": "SCHEDULE_START_END",
                "search_result_enabled": true,
                "secondary_status": "ADGROUP_STATUS_TIME_DONE",
                "share_disabled": false,
                "skip_learning_phase": true,
                "targeting_optimization_mode": "AUTOMATIC",
                "targeting_spec": {
                    "age_groups": [
                        "AGE_18_24",
                        "AGE_25_34",
                        "AGE_35_44",
                        "AGE_45_54",
                        "AGE_55_100"
                    ],
                    "brand_safety_type": "EXPANDED_INVENTORY",
                    "gender": "GENDER_UNLIMITED",
                    "location_ids": [
                        "6252001"
                    ],
                    "spc_audience_age": "OVER_EIGHTEEN",
                    "spending_power": "ALL"
                },
                "video_download_disabled": false,
                "view_attribution_window": "ONE_DAY"
            },
            {
                "adgroup_id": "{{adgroup_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "app_id": "{{app_id}}",
                "attribution_event_count": "EVERY",
                "bid_type": "BID_TYPE_NO_BID",
                "billing_event": "OCPM",
                "budget": 0,
                "budget_mode": "BUDGET_MODE_INFINITE",
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "click_attribution_window": "SEVEN_DAYS",
                "comment_disabled": false,
                "conversion_bid_price": 0,
                "create_time": "{{create_time}}",
                "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
                "deep_bid_type": "AEO",
                "engaged_view_attribution_window": "SEVEN_DAYS",
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "optimization_event": "ACTIVE_PAY",
                "optimization_goal": "IN_APP_EVENT",
                "pacing": "PACING_MODE_SMOOTH",
                "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
                "placements": [
                    "PLACEMENT_TIKTOK",
                    "PLACEMENT_GLOBAL_APP_BUNDLE",
                    "PLACEMENT_PANGLE"
                ],
                "promotion_type": "APP_ANDROID",
                "schedule_end_time": "{{schedule_end_time}}",
                "schedule_start_time": "{{schedule_start_time}}",
                "schedule_type": "SCHEDULE_START_END",
                "search_result_enabled": true,
                "secondary_status": "ADGROUP_STATUS_TIME_DONE",
                "share_disabled": false,
                "skip_learning_phase": true,
                "targeting_optimization_mode": "AUTOMATIC",
                "targeting_spec": {
                    "age_groups": [
                        "AGE_18_24",
                        "AGE_25_34",
                        "AGE_35_44",
                        "AGE_45_54",
                        "AGE_55_100"
                    ],
                    "brand_safety_type": "EXPANDED_INVENTORY",
                    "gender": "GENDER_UNLIMITED",
                    "location_ids": [
                        "1562822"
                    ],
                    "operating_systems": [
                        "ANDROID"
                    ],
                    "spc_audience_age": "OVER_EIGHTEEN",
                    "spending_power": "ALL"
                },
                "video_download_disabled": false,
                "view_attribution_window": "ONE_DAY"
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 1000,
            "total_number": 3,
            "total_page": 1
        }
    }
}
(/code)
```
