# Create Manual Non-Catalog Ads with Website and App Optimization

**Doc ID**: 1839882969587906
**Path**: Use Cases/Campaign creation/Create ads with Website and App Optimization/Create Manual Non-Catalog Ads with Website and App Optimization

---

This article walks you through the steps to create Manual Non-Catalog Ads with Website and App Optimization.

# Steps

## 1. Create a campaign
Create a campaign using [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602). Note that the following requirements must be met.

  
    
| 
      Setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Advertising objective | 
      Sales | 
      `virtual_objective_type` | 
      `SALES` | 
     |
    
| 
      `objective_type` | 
      `WEB_CONVERSIONS` | 
     |
    
| 
      Sales destination | 
      Website and app | 
      `sales_destination` | 
      `WEB_AND_APP` | 
     |
    
| 
      Use catalog | 
      Disabled | 
      `catalog_enabled` | 
      `false` or not specified

**Note**: When `objective_type` is `WEB_CONVERSIONS` and `sales_destination` is `WEB_AND_APP`, this field will default to `false`. | 
     |
    
| 
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
      Special ad categories
(Optional) | 
      Disabled or enabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada. | 
      `special_industries` | 
      Not specified or specify a valid value | 
     |
    
| 
      Campaign budget optimization
(Optional) | 
      Disabled or enabled | 
      `budget_optimize_on` | 
      `false` (or not specified) or `true` | 
     |
    
| 
      Set campaign budget
(Optional) | 
      Disabled or enabled with any of the following budget types:
- Daily
- Lifetime | 
      `budget_mode` | 
      Any of the following values:
- `BUDGET_MODE_INFINITE`
- `BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- `BUDGET_MODE_DAY` | 
     |
    
| 
      `budget` | 
      Specify a valid value when `budget_mode` is any of the following values:
- `BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- `BUDGET_MODE_DAY` | 
     |
    
| 
      Realtime API (RTA)
(Optional) | 
      Disabled or enabled | 
      `rta_id` | 
      Not specified or specify a valid value | 
     |
    
| 
      Use RTA to automatically select products
(when RTA is enabled) | 
      Disabled | 
      `rta_product_selection_enabled` | 
      `false` | 
     |
    
| 
      Use RTA BID
(when RTA is enabled)
(Optional) | 
      Disabled or enabled | 
      `rta_bid_enabled` | 
      `false` (or not specified) or `true` | 
     |
  

### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "virtual_objective_type": "SALES",
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "WEB_AND_APP",
    "catalog_enabled": false,
    "campaign_name": "{{campaign_name}}",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": "{{budget}}"
}'
(/code)
```

Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "rta_product_selection_enabled": false,
        "roas_bid": 0,
        "budget_mode": "BUDGET_MODE_TOTAL",
        "rta_bid_enabled": false,
        "campaign_automation_type": "MANUAL",
        "is_smart_performance_campaign": false,
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "objective_type": "WEB_CONVERSIONS",
        "virtual_objective_type": "SALES",
        "sales_destination": "WEB_AND_APP",
        "rta_id": null,
        "is_new_structure": true,
        "operation_status": "ENABLE",
        "is_advanced_dedicated_campaign": false,
        "campaign_id": "{{campaign_id}}",
        "budget": "{{budget}}",
        "disable_skan_campaign": null,
        "deep_bid_type": null,
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "advertiser_id": "{{advertiser_id}}",
        "is_search_campaign": false,
        "catalog_enabled": false,
        "objective": "LANDING_PAGE",
        "modify_time": "{{modify_time}}",
        "campaign_type": "REGULAR_CAMPAIGN"
    }
}
(/code)
```
## 2. Create an ad group
Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). Note that the following requirements must be met.

Here's the formatted HTML table based on your input and requirements:

  
    
| 
      Setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Ad group name | 
      Specify a valid name | 
      `adgroup_name` | 
      Specify a valid value | 
     |
    
| 
      Optimization location
· Web data connection | 
      Specify a valid Pixel | 
      `pixel_id` | 
      Specify a valid value.

To obtain the list of Pixels within your ad account, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978). | 
     |
    
| 
      `promotion_type` | 
      `WEBSITE` | 
     |
    
| 
      Optimization location
· iOS & App | 
      Specify any of the following:
- an Android app
- an iOS app
- an Android app and an iOS app | 
      `app_config` | 
      Specify any of the following:
- App ID of an Android app
- App ID of iOS app
- App ID of an Android app and that of an iOS app
To obtain the list of App IDs within your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786) and check the returned `app_id`. | 
     |
    
| 
      Optimization location
· Optimization event | 
      Specify a valid event | 
      `optimization_event` | 
      Specify a valid value.

To learn about the supported event types, see [List of values for `optimization_event` for Manual Non-Catalog Ads](#item-link-List of values for optimization_event for Manual Non-Catalog Ads).

You need to ensure the specified optimization event is active for both the Pixel and the app or apps.
- To obtain the optimization events that have been configured for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- To obtain the active optimization events for an app, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977). | 
     |
    
| 
      Placement | 
      Any of the following options:
- **Automatic Placement**
- **Select Placement** with any of the following placements:TikTok
- Pangle
- Global App Bundle | 
      `placement_type`
`placements` | 
      Any of the following settings:
- Set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`.
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and include any of the following placements in the value of `placements`:`PLACEMENT_TIKTOK`
- `PLACEMENT_PANGLE`
- `PLACEMENT_GLOBAL_APP_BUNDLE` | 
     |
    
| 
      User comment
(Optional) | 
      Disabled or enabled | 
      `comment_disabled` | 
      `true` or `false` | 
     |
    
| 
      Allow video download
(Optional) | 
      Disabled or enabled | 
      `video_download_disabled` | 
      `true` or `false` | 
     |
    
| 
      Allow video sharing
(Optional) | 
      Disabled or enabled | 
      `video_download_disabled` | 
      `true` or `false` | 
     |
    
| 
      Pangle block list
(Optional) | 
      Enabled or disabled | 
      `blocked_pangle_app_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Saved audience
(Optional) | 
      Enabled or disabled | 
      `saved_audience_id` | 
      Specify a valid value or not specified | 
     |
    
| 
      Audience targeting
· Demographics
    · Location | 
      Enabled | 
      `location_ids` or `zipcode_ids` or both | 
      Specify valid values | 
     |
    
| 
      Audience targeting
· Demographics
    · Age (Optional) | 
      Enabled or disabled | 
      `age_groups` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Demographics
    · Gender (Optional) | 
      Enabled or disabled | 
      `gender` | 
      Specify a valid value or not specified | 
     |
    
| 
      Audience targeting
· Demographics
    · Languages (Optional) | 
      Enabled or disabled | 
      `languages` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Custom audience
    · Include audience (Optional) | 
      Enabled or disabled | 
      `audience_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Custom audience
    · Exclude audience (Optional) | 
      Enabled or disabled | 
      `exclude_audience_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Custom audience
    · Pangle audience packages
(Optional) | 
      Enabled or disabled | 
      `included_pangle_audience_package_ids`
`excluded_pangle_audience_package_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Interests & behaviors
    · Interests (Optional) | 
      Enabled or disabled | 
      `interest_category_ids`
`interest_keyword_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Interests & behaviors
    · Purchase intention (Optional) | 
      Enabled or disabled | 
      `purchase_intention_keyword_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Interests & behaviors
    · Video interactions
    · Creator interactions
    · Hashtag interactions
(Optional) | 
      Enabled or disabled | 
      `actions` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Spending power (Optional) | 
      Enabled or disabled | 
      `spending_power` | 
      Specify a valid value or not specified | 
     |
    
| 
      Audience targeting
· Household income (Optional) | 
      Enabled or disabled | 
      `household_income` | 
      Specify a valid value or not specified | 
     |
    
| 
      Audience targeting
· Device
    · Operating system (Optional) | 
      Enabled or disabled | 
      `operating_systems` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Device
    · OS versions (Optional) | 
      Enabled or disabled | 
      `min_android_version` or `min_ios_version` | 
      Specify a valid value or not specified | 
     |
    
| 
      Audience targeting
· Device
    · Device model (Optional) | 
      Enabled or disabled | 
      `device_model_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Device
    · Connection type (Optional) | 
      Enabled or disabled | 
      `network_types` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Device
    · Carriers (Optional) | 
      Enabled or disabled | 
      `carrier_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Device
    · Internet service provider (Optional) | 
      Enabled or disabled | 
      `isp_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Device
    · Device price (Optional) | 
      Enabled or disabled | 
      `device_price_ranges` | 
      Specify valid values or not specified | 
     |
    
| 
      Brand safety and suitability
· Inventory filter (Optional) | 
      Enabled or disabled | 
      `brand_safety_type` | 
      Specify a valid value or not specified | 
     |
    
| 
      Brand safety and suitability
· Category exclusions (Optional) | 
      Enabled or disabled | 
      `category_exclusion_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Budget and schedule
· Budget mode & budget | 
      Specify a valid budget | 
      `budget_mode`
`budget` | 
      Specify valid values | 
     |
    
| 
      Budget and schedule
· Schedule | 
      Any of the following types:
- Set start time and run ad group continuously
- Set start and end time | 
      `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
      Any of the following configurations:
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`. | 
     |
    
| 
      Budget and schedule
· Dayparting | 
      Any of the following types:
- All day (default)
- Select specific time | 
      `dayparting` | 
      Any of the following configurations:
- Specify an all-1 value, or do not specify this field
- Specify a value that contains 0 to indicate non-delivery | 
     |
    
| 
      Bidding and optimization
· Optimization goal | 
      Conversion | 
      `optimization_goal` | 
      `CONVERT` | 
     |
    
| 
      Bidding and optimization
· Bid Strategy | 
      Any of the following types:
- Maximum Delivery
- Cost Cap (or Target CPA) | 
      `bid_type`
`conversion_bid_price` | 
      Set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`.
- If `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time. | 
     |
    
| 
      Bidding and optimization
· Attribution settings | 
      Select from the supported attribution setting options for the specific scenario. | 
      `click_attribution_window`
`view_attribution_window`
`engaged_view_attribution_window`
`attribution_event_count` | 
      To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - Website conversions](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-Website%20conversions). | 
     |
    
| 
      Bidding and optimization
· Billing event | 
      oCPM | 
      `billing_event` | 
      `OCPM` | 
     |
    
| 
      Bidding and optimization
· Delivery type | 
      
- If Bid Strategy is set to Cost Cap, you can set Delivery Type to Standard or Accelerated.
- If Bid Strategy is set to Maximum Delivery, you can only set Delivery Type to Standard. | 
      `pacing` | 
      
- If `bid_type` is `BID_TYPE_CUSTOM`, you can set `pacing` to `PACING_MODE_SMOOTH` or `PACING_MODE_FAST`.
- If `bid_type` is `BID_TYPE_NO_BID`, you can only set `pacing` to `PACING_MODE_SMOOTH`. | 
     |
  

### List of values for `optimization_event` for Manual Non-Catalog Ads
The following tables list the events supported for Manual Non-Catalog Ads with Website and App Optimization.

``` xtable
| Event name{20%} | `optimization_event` value{25%} | Corresponding Pixel event
(`optimization_event`){20%} | Corresponding app event
(`optimization_event` or `secondary_optimization_event`){35%} |
|---|---|---|---|
| Add payment info | `ADD_BILLING` | `ADD_BILLING` | `ADD_PAYMENT_INFO` |
| Add to Cart | `ON_WEB_CART` | `ON_WEB_CART` | `IN_APP_CART` |
| Add to wishlist | `ON_WEB_ADD_TO_WISHLIST` | `ON_WEB_ADD_TO_WISHLIST` | `ADD_TO_WISHLIST` |
| Initiate Checkout/Checkout | `INITIATE_ORDER` | `INITIATE_ORDER` | `IN_APP_ORDER` |
| Purchase | `SHOPPING` | `SHOPPING` | `ACTIVE_PAY` |
| Search | `ON_WEB_SEARCH` | `ON_WEB_SEARCH` | `SEARCH` |
| Subscribe | `ON_WEB_SUBSCRIBE` | `ON_WEB_SUBSCRIBE` | `SUBSCRIBE` |
| View Content | `ON_WEB_DETAIL` | `ON_WEB_DETAIL` | `IN_APP_DETAIL_UV` |
```
### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/adgroup/create/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "pixel_id": "{{pixel_id}}",
    "promotion_type": "WEBSITE",
    "app_config": [
        {
            "app_id": "{{app_id_1}}"
        },
        {
            "app_id": "{{app_id_2}}"
        }
    ],
    "optimization_event": "ADD_BILLING",
    "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": "{{budget}}",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "CONVERT",
    "location_ids": [
        "357994"
    ],
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": "{{conversion_bid_price}}",
    "billing_event": "OCPM"
}'
(/code)
```

Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "age_groups": null,
        "vbo_window": null,
        "keywords": null,
        "statistic_type": null,
        "skip_learning_phase": true,
        "interest_keyword_ids": [],
        "excluded_audience_ids": [],
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "pacing": "PACING_MODE_FAST",
        "ios14_quota_type": "UNOCCUPIED",
        "deep_funnel_event_source_id": null,
        "campaign_name": "{{campaign_name}}",
        "languages": [],
        "budget": "{{budget}}",
        "adgroup_name": "{{adgroup_name}}",
        "adgroup_app_profile_page_state": null,
        "next_day_retention": null,
        "isp_ids": [],
        "network_types": [],
        "actions": [],
        "modify_time": "{{modify_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "billing_event": "OCPM",
        "budget_mode": "BUDGET_MODE_TOTAL",
        "rf_estimated_cpr": null,
        "deep_funnel_optimization_status": null,
        "purchased_reach": null,
        "rf_estimated_frequency": null,
        "click_attribution_window": "SEVEN_DAYS",
        "audience_ids": [],
        "adgroup_id": "{{adgroup_id}}",
        "app_config": [
            {
                "app_id": "{{app_id_1}}"
            },
            {
                "app_id": "{{app_id_2}}"
            }
        ],
        "conversion_window": null,
        "gender": "GENDER_UNLIMITED",
        "deep_funnel_optimization_event": null,
        "purchased_impression": null,
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "category_exclusion_ids": [],
        "schedule_end_time": "{{schedule_end_time}}",
        "deep_cpa_bid": 0,
        "is_hfss": false,
        "location_ids": [
            "357994"
        ],
        "promotion_type": "WEBSITE",
        "search_result_enabled": true,
        "device_price_ranges": null,
        "operation_status": "ENABLE",
        "inventory_filter_enabled": false,
        "operating_systems": [],
        "view_attribution_window": "ONE_DAY",
        "create_time": "{{create_time}}",
        "optimization_event": "ADD_BILLING",
        "auto_targeting_enabled": false,
        "promotion_website_type": "UNSET",
        "smart_interest_behavior_enabled": null,
        "bid_display_mode": "CPMV",
        "delivery_mode": null,
        "product_source": "UNSET",
        "attribution_event_count": "EVERY",
        "conversion_bid_price": "{{conversion_bid_price}}",
        "smart_audience_enabled": null,
        "pixel_id": "{{pixel_id}}",
        "creative_material_mode": "CUSTOM",
        "app_download_url": null,
        "category_id": "0",
        "brand_safety_type": "NO_BRAND_SAFETY",
        "app_id": null,
        "brand_safety_partner": null,
        "share_disabled": false,
        "campaign_automation_type": "MANUAL",
        "interest_category_ids": [],
        "app_type": null,
        "video_download_disabled": false,
        "schedule_start_time": "{{schedule_start_time}}",
        "feed_type": null,
        "scheduled_budget": 0,
        "schedule_infos": null,
        "frequency": null,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "is_smart_performance_campaign": false,
        "is_new_structure": true,
        "campaign_id": "{{campaign_id}}",
        "bid_price": 0,
        "secondary_optimization_event": null,
        "deep_bid_type": null,
        "rf_purchased_type": null,
        "frequency_schedule": null,
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "optimization_goal": "CONVERT",
        "comment_disabled": false,
        "bid_type": "BID_TYPE_CUSTOM",
        "advertiser_id": "{{advertiser_id}}",
        "deep_funnel_event_source": null,
        "automated_keywords_enabled": null,
        "engaged_view_attribution_window": "ONE_DAY"
    }
}
(/code)
```
## 3. Create an ad
Create an ad using [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). Note that the following requirements must be met.

  
    
| 
      Setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Ad name
(Optional) | 
      By default, the system will auto-generate the ad name.
You can customize the ad name by specifying a valid ad name. | 
      `ad_name` | 
      
- To have the system auto-generate the ad name, set this field to `""` (empty string).
-  To customize the ad name, specify a non-empty string value. | 
     |
    
| 
      Identity | 
      Any of the following options:
- Custom User (custom identity)
- Authorized User
- TikTok User
- TikTok Account User in Business Center | 
      `identity_type` | 
      Any of the following values:
- `CUSTOMIZED_USER`
- `AUTH_CODE`
- `TT_USER`
- `BC_AUTH_TT` | 
     |
    
| 
      `identity_id` | 
      Specify a valid value
To get the list of identities under your ad account, use [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057). | 
     |
    
| 
      `identity_authorized_bc_id` | 
      Specify a valid value when `identity_type` is `BC_AUTH_TT` | 
     |
    
| 
      Ad format | 
      Single video: Use a video creative to promote your products. | 
      `ad_format` | 
      `SINGLE_VIDEO` | 
     |
    
| 
      Ad creative | 
      
- For Custom User identity or Spark Ads PUSH with TikTok User identity, specify a video and a cover image.
- For TikTok Account User in Business Center identity, Authorized User identity, or Spark Ads PULL with TikTok User identity, specify a TikTok post. | 
      `video_id`
`image_ids`
`ad_text`
`tiktok_item_id`
`dark_post_status` | 
      
- If `identity_type` is `CUSTOMIZED_USER`, specify the video (`video_id`), video cover (`image_ids`), and ad text (`ad_text`). Do not pass `tiktok_item_id`.
- If `identity_type` is `TT_USER`, you can create the ad through Spark Ads PULL or Spark Ads PUSH:Spark Ads PUSH: Specify the video (`video_id`), video cover (`image_ids`), and ad text (`ad_text`) . Do not pass `tiktok_item_id`. You can set `dark_post_status` to `ON` to ensure the video only shows as ad and does not organically appear on the TikTok Account.
- Spark Ads PULL: Specify the TikTok post through `tiktok_item_id`. Do not pass `video_id`, `image_ids`, `ad_text`, and `dark_post_status`.To learn more about Spark Ads, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298).
- If `identity_type` is `AUTH_CODE` or `BC_AUTH_TT`, specify the TikTok post through `tiktok_item_id`. Do not pass `video_id`, `image_ids`, and `ad_text`. | 
     |
    
| 
      Interactive add-on
(Optional) | 
      Disabled or enabled with any of the following types:
- Countdown Sticker
- Gift Code Sticker
- Display Card | 
      `card_id` | 
      Not specified or specify the ID of one of the following creative portfolio types:
- Countdown Sticker
- Gift Code Sticker
- Display Card
To create a creative portfolio, use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to get the ID of a Display Card, Product Card, or Product Tiles portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058).
- To learn about how to get the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177).
**Note**: Using a Product Tiles portfolio to create ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. | 
     |
    
| 
      Destination | 
      Website | 
      N/A | 
      N/A | 
     |
    
| 
      Deeplink | 
      Enabled with a custom deeplink | 
      `deeplink_type` | 
      `NORMAL` | 
     |
    
| 
      `deeplink` | 
      Specify a deeplink.
The deeplink format can be any of the following:
- Custom URL scheme, in the format of `scheme://resource`. For instance, a Custom URL scheme of WhatsApp should follow the format `whatsapp://resource`.
- Apple's universal link or Android App Link starting with `http://` or `https://`. | 
     |
    
| 
      Deeplink parameters
(Optional) | 
      Enabled or disabled | 
      `deeplink_utm_params` | 
      Specify valid values or not specified

You can manually add deeplink URL parameters to the deeplink by directly setting `deeplink` to a deeplink that already includes URL parameters.
- However, if you use a custom deeplink in your ad and specify `deeplink_utm_params` at the same time, the URL parameters will not be automatically appended to the custom deeplink (`deeplink`) upon ad delivery. In such cases, you need to ensure that `deeplink_utm_params` exactly matches the used deeplink URL parameters. Otherwise, an error will occur. | 
     |
    
| 
      Fallback URL | 
      Enabled with a custom link | 
      `fallback_type` | 
      `UNSET` | 
     |
    
| 
      `landing_page_url` | 
      Specify a custom link.
This URL directs users who have not installed the App to a designated page (for instance, the homepage of your official website) when a deeplink is configured for an ad. | 
     |
    
| 
      URL parameters
(Optional) | 
      Enabled or disabled | 
      `utm_params` | 
      Specify valid values or not specified

You can manually add URL parameters to the custom link by directly setting `landing_page_url` to a URL that already includes URL parameters.
- However, if you use a custom link in your ad and specify `utm_params` at the same time, the URL parameters will not be automatically appended to the custom link (`landing_page_url`) upon ad delivery. In such cases, you need to ensure that you specify a `landing_page_url` with the URL parameters already appended, and that `utm_params` exactly matches the used URL parameters. Otherwise, an error will occur. | 
     |
    
| 
      Call to action | 
      Any of the following options:
- Dynamic
- Standard | 
      `call_to_action_id`
 `call_to_action` | 
      
- To use dynamic call to action, specify `call_to_action_id`.To learn about how to create such call to actions, see [Dynamic CTAs](https://business-api.tiktok.com/portal/docs?id=1740307296329730#item-link-Dynamic%20CTAs).
- To use standard call to action, specify `call_to_action`.For enum values, see [Enumeration - Call-to-Action](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Call-to-action). | 
     |
    
| 
      Disclaimer 
(for TikTok placement)
(Optional) | 
      Enabled or disabled | 
      `disclaimer_type`
`disclaimer_text`
`disclaimer_clickable_texts` | 
      Specify valid values or not specified | 
     |
    
| 
      Tracking
· TikTok events tracking
    - Offline events
(Optional) | 
      Enabled or disabled | 
      `tracking_offline_event_set_ids` | 
      Specify a valid value or not specified | 
     |
    
| 
      Tracking
· Third-party tracking settings
    · Impression tracking URL
(Optional) | 
      Enabled or disabled | 
      `impression_tracking_url` | 
      Specify a valid value or not specified | 
     |
    
| 
      Tracking
· Third-party tracking settings
    · Click tracking URL
(Optional) | 
      Enabled or disabled | 
      `click_tracking_url` | 
      Specify a valid value or not specified | 
     |
    
| 
      Tracking
· Third-party tracking settings
    · Measure brand safety with third-party partner
(Optional) | 
      Enabled or disabled | 
      `brand_safety_postbid_partner`
`brand_safety_vast_url` | 
      Specify valid values or not specified | 
     |
    
| 
      Tracking
· Third-party tracking settings
    · Track viewability with third-party partner
(Optional) | 
      Enabled or disabled | 
      `viewability_postbid_partner`
`viewability_vast_url` | 
      Specify valid values or not specified | 
     |
  

### Example
#### Spark Ads pull
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "TT_USER",
            "identity_id": "{{identity_id}}",
            "ad_format": "SINGLE_VIDEO",
            "tiktok_item_id": "{{tiktok_item_id}}",
            "card_id": "{{card_id}}",
            "deeplink_type": "NORMAL",
            "deeplink": "{{deeplink}}",
            "fallback_type": "UNSET",
            "landing_page_url": "{{landing_page_url}}",
            "call_to_action_id": "{{call_to_action_id}}"
        }
    ]
}'
(/code)
```

Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_ids": [
            "{{ad_id}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "landing_page_url": "{{landing_page_url}}",
                "create_time": "{{create_time}}",
                "adgroup_name": "{{adgroup_name}}",
                "vertical_video_strategy": "UNSET",
                "campaign_automation_type": "MANUAL",
                "deeplink": "{{deeplink}}",
                "landing_page_urls": null,
                "viewability_vast_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}"
                ],
                "brand_safety_vast_url": null,
                "impression_tracking_url": null,
                "identity_type": "TT_USER",
                "music_id": null,
                "adgroup_id": "{{adgroup_id}}",
                "operation_status": "ENABLE",
                "click_tracking_url": null,
                "display_name": "{{display_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "ad_texts": null,
                "tiktok_item_id": "{{tiktok_item_id}}",
                "creative_authorized": false,
                "call_to_action_id": "{{call_to_action_id}}",
                "creative_type": null,
                "campaign_id": "{{campaign_id}}",
                "optimization_event": "ADD_BILLING",
                "viewability_postbid_partner": "UNSET",
                "shopping_ads_fallback_type": "DEFAULT",
                "ad_name": "{{ad_name}}",
                "deeplink_type": "NORMAL",
                "ad_id": "{{ad_id}}",
                "profile_image_url": "",
                "promotional_music_disabled": true,
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "campaign_name": "{{campaign_name}}",
                "fallback_type": "UNSET",
                "video_id": null,
                "ad_text": "{{ad_text}}",
                "is_new_structure": true,
                "image_ids": [],
                "app_name": "{{app_name}}",
                "is_aco": false,
                "card_id": "{{card_id}}",
                "modify_time": "{{modify_time}}",
                "playable_url": "",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "avatar_icon_web_uri": "",
                "identity_id": "{{identity_id}}",
                "dynamic_destination": "UNSET",
                "page_id": null,
                "carousel_image_labels": null,
                "ad_format": "SINGLE_VIDEO",
                "vast_moat_enabled": false
            }
        ]
    }
}
(/code)
```

#### Spark Ads push
Request
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_ids": [
            "{{ad_id}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "landing_page_url": "{{landing_page_url}}",
                "create_time": "{{create_time}}",
                "adgroup_name": "{{adgroup_name}}",
                "vertical_video_strategy": "UNSET",
                "campaign_automation_type": "MANUAL",
                "deeplink": "{{deeplink}}",
                "landing_page_urls": null,
                "viewability_vast_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}"
                ],
                "brand_safety_vast_url": null,
                "impression_tracking_url": null,
                "identity_type": "TT_USER",
                "music_id": null,
                "adgroup_id": "{{adgroup_id}}",
                "operation_status": "ENABLE",
                "click_tracking_url": null,
                "display_name": "{{display_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "ad_texts": null,
                "tiktok_item_id": "{{tiktok_item_id}}",
                "creative_authorized": false,
                "call_to_action_id": "{{call_to_action_id}}",
                "creative_type": null,
                "campaign_id": "{{campaign_id}}",
                "optimization_event": "ADD_BILLING",
                "viewability_postbid_partner": "UNSET",
                "shopping_ads_fallback_type": "DEFAULT",
                "ad_name": "{{ad_name}}",
                "deeplink_type": "NORMAL",
                "ad_id": "{{ad_id}}",
                "profile_image_url": "",
                "promotional_music_disabled": true,
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "campaign_name": "{{campaign_name}}",
                "fallback_type": "UNSET",
                "video_id": null,
                "ad_text": "{{ad_text}}",
                "is_new_structure": true,
                "image_ids": [],
                "app_name": "{{app_name}}",
                "is_aco": false,
                "card_id": "{{card_id}}",
                "modify_time": "{{modify_time}}",
                "playable_url": "",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "avatar_icon_web_uri": "",
                "identity_id": "{{identity_id}}",
                "dynamic_destination": "UNSET",
                "page_id": null,
                "carousel_image_labels": null,
                "ad_format": "SINGLE_VIDEO",
                "vast_moat_enabled": false
            }
        ]
    }
}
(/code)
```

Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_ids": [
            "{{ad_id}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "landing_page_url": "{{landing_page_url}}",
                "create_time": "{{create_time}}",
                "adgroup_name": "{{adgroup_name}}",
                "vertical_video_strategy": "UNSET",
                "campaign_automation_type": "MANUAL",
                "deeplink": "{{deeplink}}",
                "landing_page_urls": null,
                "viewability_vast_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}"
                ],
                "brand_safety_vast_url": null,
                "impression_tracking_url": null,
                "identity_type": "TT_USER",
                "music_id": null,
                "adgroup_id": "{{adgroup_id}}",
                "operation_status": "ENABLE",
                "click_tracking_url": null,
                "display_name": "{{display_name}}",
                "branded_content_disabled": false,
                "advertiser_id": "{{advertiser_id}}",
                "ad_texts": null,
                "creative_authorized": false,
                "call_to_action_id": "{{call_to_action_id}}",
                "creative_type": null,
                "campaign_id": "{{campaign_id}}",
                "optimization_event": "ADD_BILLING",
                "viewability_postbid_partner": "UNSET",
                "shopping_ads_fallback_type": "DEFAULT",
                "ad_name": "{{ad_name}}",
                "deeplink_type": "NORMAL",
                "ad_id": "{{ad_id}}",
                "profile_image_url": "",
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "campaign_name": "{{campaign_name}}",
                "fallback_type": "UNSET",
                "video_id": "{{video_id}}",
                "ad_text": "{{ad_text}}",
                "is_new_structure": true,
                "image_ids": [
                    "{{image_id}}"
                ],
                "app_name": "{{app_name}}",
                "is_aco": false,
                "card_id": "{{card_id}}",
                "modify_time": "{{modify_time}}",
                "playable_url": "",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "dark_post_status": "OFF",
                "avatar_icon_web_uri": "",
                "identity_id": "{{identity_id}}",
                "dynamic_destination": "UNSET",
                "page_id": null,
                "carousel_image_labels": null,
                "ad_format": "SINGLE_VIDEO",
                "vast_moat_enabled": false
            }
        ]
    }
}
(/code)
```
