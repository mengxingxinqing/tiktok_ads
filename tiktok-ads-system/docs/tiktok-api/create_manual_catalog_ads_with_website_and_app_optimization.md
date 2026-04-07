# Create Manual Catalog Ads with Website and App Optimization

**Doc ID**: 1839882947475458
**Path**: Use Cases/Campaign creation/Create ads with Website and App Optimization/Create Manual Catalog Ads with Website and App Optimization

---

This article walks you through the steps to create Manual Catalog Ads with Website and App Optimization.

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
      `PRODUCT_SALES` | 
     |
    
| 
      Sales destination | 
      Website and app | 
      `sales_destination` | 
      `WEB_AND_APP` | 
     |
    
| 
      Use catalog | 
      **Enabled with an E-commerce catalog** | 
      `catalog_enabled` | 
      `true` or not specified

**Note**: When `objective_type` is `PRODUCT_SALES` and `sales_destination` is `WEB_AND_APP`, this field will default to `true`. | 
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
      Use RTA to automatically select products
(when RTA is enabled)
(Optional) | 
      Disabled or enabled | 
      `rta_product_selection_enabled` | 
      `false` (or not specified) or `true` | 
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
 curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "virtual_objective_type": "SALES",
    "objective_type": "PRODUCT_SALES",
    "sales_destination": "WEB_AND_APP",
    "catalog_enabled": true,
    "campaign_name": "{{campaign_name}}",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}}
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
        "campaign_app_profile_page_state": "UNSET",
        "is_smart_performance_campaign": false,
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "objective_type": "PRODUCT_SALES",
        "virtual_objective_type": "SALES",
        "sales_destination": "WEB_AND_APP",
        "rta_id": null,
        "is_new_structure": true,
        "operation_status": "ENABLE",
        "is_advanced_dedicated_campaign": false,
        "campaign_id": "{{campaign_id}}",
        "budget": {{budget}},
        "disable_skan_campaign": null,
        "deep_bid_type": null,
        "campaign_name": "{{campaign_name}}",
        "campaign_product_source": "CATALOG",
        "create_time": "{{create_time}}",
        "advertiser_id": "{{advertiser_id}}",
        "is_search_campaign": false,
        "catalog_enabled": true,
        "objective": "LANDING_PAGE",
        "modify_time": "{{modify_time}}",
        "campaign_type": "REGULAR_CAMPAIGN"
    }
}
(/code)
```
## 2. Create an ad group
Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). Note that the following requirements must be met.

  
    
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
      Product source details
· Catalog | 
      Specify an **E-commerce catalog with at least one approved product** | 
      `product_source` | 
      `CATALOG` | 
     |
    
| 
      `catalog_id`
`catalog_authorized_bc_id` | 
      Pass valid values.

The catalog (`catalog_id`) needs to have at least one approved product. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 1.

- To obtain E-commerce catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610). For E-commerce catalogs, the `catalog_type` should be `ECOM`.
- To create an E-commerce catalog, use [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961). | 
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

To learn about the supported event types, see [List of values for `optimization_event` for Manual Catalog Ads](#item-link-List of values for optimization_event for Manual Catalog Ads).

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
      Pangle block list
(Optional) | 
      Enabled or disabled | 
      `blocked_pangle_app_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Audience | 
      Any of the following options:
- Find prospective customers: Find prospective customers, including those who have not interacted with your products.
- Retarget audience: Promote products to people who have already interacted with them.If you select Retarget audience, ensure that an event source has been connected to the catalog. This will enable you to precisely target users who have interacted with your products. | 
      `shopping_ads_retargeting_type`
`shopping_ads_retargeting_actions_days`
`included_custom_actions`
`excluded_custom_actions`
`shopping_ads_retargeting_custom_audience_relation` | 
      Pass valid values
- To find prospective customers, set `shopping_ads_retargeting_type` to `OFF`.
- To retarget audience, set `shopping_ads_retargeting_type` to `LAB1`, `LAB2`, or `LAB3`, and pass other related parameters. You also need to ensure an event source has been bound to the catalog (`catalog_id`). Otherwise, an error will occur.To check if an event source has been bound to your catalog, use [/catalog/eventsource_bind/get/](https://business-api.tiktok.com/portal/docs?id=1740492531343362).
- To bind an event source to your catalog, use [/catalog/eventsource/bind/](https://business-api.tiktok.com/portal/docs?id=1740492491200513). | 
     |
    
| 
      Audience targeting
· Audience
    · Include (Optional)
(for Find prospective customers mode) | 
      Enabled or disabled | 
      `audience_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Audience
    · Exclude (Optional)
(for Find prospective customers mode) | 
      Enabled or disabled | 
      `exclude_audience_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience targeting
· Demographics
    · Location | 
      The location should match or be the subset of the targeting location of your catalog. | 
      `location_ids` or `zipcode_ids` or both | 
      Specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.

To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
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
      Content exclusions
· Inventory filter (Optional) | 
      Enabled or disabled | 
      `brand_safety_type` | 
      Specify a valid value or not specified | 
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
      To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - Product Sales](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-Product%20Sales). | 
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
  

### List of values for `optimization_event` for Manual Catalog Ads

The following tables list the events supported for Manual Catalog Ads with Website and App Optimization.

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
#### Find prospective customers
Request
```xcodeblock
(code curl http)
url --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "product_source": "CATALOG",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "pixel_id": "{{pixel_id}}",
    "promotion_type": "WEBSITE",
    "app_config": [
        {
            "app_id": "{{app_id}}"
        },
        {
            "app_id": "{{app_id}}"
        }
    ],
    "optimization_event": "ADD_BILLING",
    "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
    "shopping_ads_retargeting_type":"OFF",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "CONVERT",
    "location_ids": [
        "6252001"
    ],
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": {{conversion_bid_price}},
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
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "pacing": "PACING_MODE_FAST",
        "ios14_quota_type": "UNOCCUPIED",
        "deep_funnel_event_source_id": null,
        "campaign_name": "{{campaign_name}}",
        "languages": [],
        "budget": {{budget}},
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
        "shopping_ads_retargeting_type": "OFF",
        "audience_ids": [],
        "adgroup_id": "{{adgroup_id}}",
        "app_config": [
            {
                "app_id": "{{app_id}}"
            },
            {
                "app_id": "{{app_id}}"
            }
        ],
        "conversion_window": null,
        "gender": "GENDER_UNLIMITED",
        "deep_funnel_optimization_event": null,
        "purchased_impression": null,
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_PANGLE"
        ],
        "category_exclusion_ids": [],
        "schedule_end_time": "{{schedule_end_time}}",
        "deep_cpa_bid": 0,
        "is_hfss": false,
        "location_ids": [
            "6252001"
        ],
        "promotion_type": "WEBSITE",
        "search_result_enabled": false,
        "device_price_ranges": null,
        "operation_status": "ENABLE",
        "inventory_filter_enabled": false,
        "operating_systems": [],
        "view_attribution_window": "ONE_DAY",
        "create_time": "{{create_time}}",
        "optimization_event": "ADD_BILLING",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "auto_targeting_enabled": false,
        "catalog_id": "{{catalog_id}}",
        "smart_interest_behavior_enabled": null,
        "bid_display_mode": "CPMV",
        "delivery_mode": null,
        "product_source": "CATALOG",
        "attribution_event_count": "EVERY",
        "conversion_bid_price": 11,
        "smart_audience_enabled": null,
        "pixel_id": "{{pixel_id}}",
        "creative_material_mode": "CATALOG_SALES",
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
        "shopping_ads_type": "VIDEO",
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
#### Retarget audience
Request
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "product_source": "CATALOG",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "pixel_id": "{{pixel_id}}",
    "promotion_type": "WEBSITE",
    "app_config": [
        {
            "app_id": "{{app_id}}"
        },
        {
            "app_id": "{{app_id}}"
        }
    ],
    "optimization_event": "ADD_BILLING",
    "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
    "shopping_ads_retargeting_type": "LAB1",
    "shopping_ads_retargeting_actions_days": 30,
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "CONVERT",
    "location_ids": [
        "1861060"
    ],
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": {{conversion_bid_price}},
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
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "pacing": "PACING_MODE_FAST",
        "ios14_quota_type": "UNOCCUPIED",
        "deep_funnel_event_source_id": null,
        "campaign_name": "{{campaign_name}}",
        "languages": [],
        "budget": {{budget}},
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
        "shopping_ads_retargeting_type": "LAB1",
        "audience_ids": [],
        "adgroup_id": "{{adgroup_id}}",
        "app_config": [
            {
                "app_id": "{{app_id}}"
            },
            {
                "app_id": "{{app_id}}"
            }
        ],
        "conversion_window": null,
        "gender": "GENDER_UNLIMITED",
        "deep_funnel_optimization_event": null,
        "purchased_impression": null,
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_PANGLE"
        ],
        "category_exclusion_ids": [],
        "schedule_end_time": "{{schedule_end_time}}",
        "deep_cpa_bid": 0,
        "is_hfss": false,
        "location_ids": [
            "1861060"
        ],
        "promotion_type": "WEBSITE",
        "search_result_enabled": false,
        "device_price_ranges": null,
        "operation_status": "ENABLE",
        "inventory_filter_enabled": false,
        "operating_systems": [],
        "view_attribution_window": "ONE_DAY",
        "create_time": "{{create_time}}",
        "optimization_event": "ADD_BILLING",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "auto_targeting_enabled": false,
        "catalog_id": "{{catalog_id}}",
        "smart_interest_behavior_enabled": null,
        "bid_display_mode": "CPMV",
        "delivery_mode": null,
        "product_source": "CATALOG",
        "attribution_event_count": "EVERY",
        "conversion_bid_price": 11,
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
        "video_download_disabled": true,
        "schedule_start_time": "{{schedule_start_time}}",
        "feed_type": null,
        "scheduled_budget": 0,
        "schedule_infos": null,
        "frequency": null,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "is_smart_performance_campaign": false,
        "shopping_ads_type": "VIDEO",
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

### Ad format as Single Video

  
    
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
      Specify a valid value.

To get the list of identities under your ad account, use [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057). | 
     |
    
| 
      `identity_authorized_bc_id` | 
      Specify a valid value when `identity_type` is `BC_AUTH_TT` | 
     |
    
| 
      Products | 
      Any of the following options:
- All products
- Product set
- Specific products with a maximum of 20 products | 
      `catalog_id`
`product_specific_type`
`item_group_ids`
`product_set_id`
`sku_ids` | 
      
- Set `catalog_id` to ID of the same catalog specified at the ad group level.
-  Set `product_specific_type` to `ALL`, `PRODUCT_SET` or `CUSTOMIZED_PRODUCTS`.If `product_specific_type` is set to `ALL`, you don't need to pass `sku_ids`, `item_group_ids`, and `product_set_id`.
- If `product_specific_type` is set to `PRODUCT_SET`, you need to pass either `item_group_ids` or `product_set_id`. `sku_ids` is not needed.
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to pass a maximum of 20 products through `sku_ids`. `item_group_ids` and `product_set_id` are not needed.
**Note**: To determine whether an E-commerce catalog product can be used in ads, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). If the returned `ad_creation_eligible` for the product is `AVAILABLE`, you can use the product in ads. | 
     |
    
| 
      Ad format | 
      **Single video**: Use a video creative to promote your products. | 
      `ad_format` | 
      `SINGLE_VIDEO` | 
     |
	
| 
      `vertical_video_strategy` | 
      `SINGLE_VIDEO` | 
     |
    
| 
      Ad creative | 
      
-  For Custom User identity or Spark Ads PUSH with TikTok User identity, specify a video and a cover image.
- For TikTok Account User in Business Center identity, Authorized User identity, or Spark Ads PULL with TikTok User identity, specify a TikTok post. | 
      `video_id`
`image_ids`
`ad_text`
`tiktok_item_id`
`dark_post_status` | 
      
- If `identity_type` is `CUSTOMIZED_USER`, specify the video (`video_id`), video cover (`image_ids`), and ad text (`ad_text`). Do not pass `tiktok_item_id`.
- If `identity_type` is `TT_USER`, you can create the ad through Spark Ads PULL or Spark Ads PUSH:Spark Ads PUSH: Specify the video (`video_id`), video cover (`image_ids`), and ad text (`ad_text`). Do not pass `tiktok_item_id`. You can set `dark_post_status` to `ON` to ensure the video only shows as ad and does not organically appear on the TikTok Account.
- Spark Ads PULL: Specify the TikTok post through `tiktok_item_id`. Do not pass `video_id`, `image_ids`, `ad_text`, and `dark_post_status`.To learn more about Spark Ads, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298).
- If `identity_type` is `AUTH_CODE` or `BC_AUTH_TT`, specify the TikTok post through `tiktok_item_id`. Do not pass `video_id`, `image_ids`, and `ad_text`. | 
     |
    
| 
      `shopping_ads_video_package_id` | 
      Not specified | 
     |
	
| 
      `music_id` | 
      Not specified | 
     |
    
| 
      Interactive add-on
(Optional) | 
      Disabled or enabled with any of the following types:
- Product Card
- Product Tiles (supported with allowlist)
- Countdown Sticker
- Gift Code Sticker
- Display Card | 
      `card_id` | 
      Not specified or specify the ID of one of the following creative portfolio types:
- Product Card
- Product Tiles
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
      `shopping_ads_deeplink_type` | 
      `CUSTOM` | 
     |
	
| 
      `deeplink_type` | 
      `NORMAL` | 
     |
	
| 
      `deeplink` | 
      Specify a custom deeplink.
The deeplink format can be any of the following:
- Custom URL scheme, in the format of `scheme://resource`. For instance, a Custom URL scheme of WhatsApp should follow the format `whatsapp://resource`.
- Apple’s universal link or Android App Link starting with `http://` or `https://`. | 
     |
    
| 
      Deeplink parameters
(Optional) | 
      Enabled or disabled | 
      `deeplink_utm_params` | 
      Specify valid values or not specified

You can manually add deeplink URL parameters to the custom deeplink by directly setting `deeplink` to a deeplink that already includes URL parameters.
- However, if you use a custom deeplink in your ad and specify `deeplink_utm_params` at the same time, the URL parameters will not be automatically appended to the custom deeplink (`deeplink`) upon ad delivery. In such cases, you need to ensure that `deeplink_utm_params` exactly matches the used deeplink URL parameters. Otherwise, an error will occur. | 
     |
    
| 
      Fallback URL | 
      Enabled with a custom link (the promoted web page) | 
      `shopping_ads_fallback_type` | 
      `CUSTOM` | 
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
      Enabled | 
      `call_to_action` | 
      Specify a valid value.

To get the enum values, see [Enumerations - Call-to-action](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Call-to-action). | 
     |
    
| 
      Tracking
· TikTok events tracking
    · Offline events
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
  

#### Example
##### Spark Ads Pull
Request
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "TT_USER",
            "identity_id": "{{identity_id}}",
            "catalog_id": "{{catalog_id}}",
            "product_specific_type": "ALL",
            "ad_format": "SINGLE_VIDEO",
            "vertical_video_strategy": "SINGLE_VIDEO",
            "tiktok_item_id": "{{tiktok_item_id}}",
            "card_id": "{{card_id}}",
            "shopping_ads_deeplink_type": "CUSTOM",
            "deeplink_type": "NORMAL",
            "deeplink": "{{deeplink}}",
            "shopping_ads_fallback_type": "CUSTOM",
            "landing_page_url": "{{landing_page_url}}",
            "call_to_action": "LEARN_MORE"
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
            "{{ad_ids}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "deeplink": "{{deeplink}}",
                "profile_image_url": "",
                "card_id": "{{card_id}}",
                "campaign_name": "{{campaign_name}}",
                "video_id": null,
                "viewability_vast_url": null,
                "shopping_ads_video_package_id": "",
                "ad_texts": null,
                "is_aco": false,
                "modify_time": "{{modify_time}}",
                "ad_name": "{{ad_name}}",
                "adgroup_name": "{{adgroup_name}}",
                "promotional_music_disabled": true,
                "image_ids": [],
                "ad_id": "{{ad_id}}",
                "dynamic_format": "UNSET",
                "music_id": null,
                "landing_page_urls": null,
                "identity_id": "{{identity_id}}",
                "landing_page_url": "{{landing_page_url}}",
                "product_specific_type": "ALL",
                "identity_type": "TT_USER",
                "playable_url": "",
                "call_to_action": "LEARN_MORE",
                "avatar_icon_web_uri": "",
                "operation_status": "ENABLE",
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "create_time": "{{create_time}}",
                "optimization_event": "ADD_BILLING",
                "dynamic_destination": "UNSET",
                "display_name": "{{display_name}}",
                "vast_moat_enabled": false,
                "ad_text": "{{ad_text}}",
                "deeplink_type": "NORMAL",
                "catalog_id": "{{catalog_id}}",
                "tiktok_item_id": "{{tiktok_item_id}}",
                "viewability_postbid_partner": "UNSET",
                "creative_type": null,
                "shopping_ads_deeplink_type": "CUSTOM",
                "creative_authorized": false,
                "carousel_image_labels": null,
                "app_name": "{{app_name}}",
                "campaign_automation_type": "MANUAL",
                "impression_tracking_url": null,
                "ad_format": "SINGLE_VIDEO",
                "click_tracking_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_ids}}"
                ],
                "is_new_structure": true,
                "campaign_id": "{{campaign_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "vertical_video_strategy": "SINGLE_VIDEO",
                "brand_safety_vast_url": null,
                "adgroup_id": "{{adgroup_id}}",
                "call_to_action_id": null,
                "page_id": null,
                "advertiser_id": "{{advertiser_id}}",
                "shopping_ads_fallback_type": "CUSTOM"
            }
        ]
    }
}
(/code)
```
##### Spark Ads Push
Request
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{AccessToken}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "TT_USER",
            "identity_id": "{{identity_id}}",
            "catalog_id": "{{catalog_id}}",
            "product_specific_type": "ALL",
            "ad_format": "SINGLE_VIDEO",
            "vertical_video_strategy": "SINGLE_VIDEO",
            "video_id": "{{video_id}}",
            "image_ids": [
                "{{image_ids}}"
            ],
            "ad_text": "{{ad_text}}",
            "card_id": "{{card_id}}",
            "shopping_ads_deeplink_type": "CUSTOM",
            "deeplink_type": "NORMAL",
            "deeplink": "{{deeplink}}",
            "shopping_ads_fallback_type": "CUSTOM",
            "landing_page_url": "{{landing_page_url}}",
            "call_to_action": "LEARN_MORE"
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
            "{{ad_ids}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "deeplink": "{{deeplink}}",
                "profile_image_url": "",
                "card_id": "{{card_id}}",
                "campaign_name": "{{campaign_name}}",
                "video_id": "{{video_id}}",
                "viewability_vast_url": null,
                "shopping_ads_video_package_id": "",
                "ad_texts": null,
                "is_aco": false,
                "modify_time": "{{modify_time}}",
                "ad_name": "{{ad_name}}",
                "adgroup_name": "{{adgroup_name}}",
                "dark_post_status": "OFF",
                "image_ids": [
                    "{{image_ids}}"
                ],
                "ad_id": "{{ad_id}}",
                "dynamic_format": "UNSET",
                "music_id": null,
                "landing_page_urls": null,
                "identity_id": "{{identity_id}}",
                "landing_page_url": "{{landing_page_url}}",
                "product_specific_type": "ALL",
                "identity_type": "TT_USER",
                "playable_url": "",
                "call_to_action": "LEARN_MORE",
                "avatar_icon_web_uri": "",
                "operation_status": "ENABLE",
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "create_time": "{{create_time}}",
                "optimization_event": "ADD_BILLING",
                "dynamic_destination": "UNSET",
                "display_name": "{{display_name}}",
                "vast_moat_enabled": false,
                "ad_text": "{{ad_text}}",
                "deeplink_type": "NORMAL",
                "catalog_id": "{{catalog_id}}",
                "viewability_postbid_partner": "UNSET",
                "creative_type": null,
                "shopping_ads_deeplink_type": "CUSTOM",
                "creative_authorized": false,
                "branded_content_disabled": false,
                "carousel_image_labels": null,
                "app_name": "{{app_name}}",
                "campaign_automation_type": "MANUAL",
                "impression_tracking_url": null,
                "ad_format": "SINGLE_VIDEO",
                "click_tracking_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_ids}}"
                ],
                "is_new_structure": true,
                "campaign_id": "{{campaign_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "vertical_video_strategy": "SINGLE_VIDEO",
                "brand_safety_vast_url": null,
                "adgroup_id": "{{adgroup_id}}",
                "call_to_action_id": null,
                "page_id": null,
                "advertiser_id": "{{advertiser_id}}",
                "shopping_ads_fallback_type": "CUSTOM"
            }
        ]
    }
}
(/code)
```

### Ad format as Catalog Video

  
    
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
      Custom User (custom identity) | 
      `identity_type` | 
      `CUSTOMIZED_USER` | 
     |
    
| 
      `identity_id` | 
      Specify a valid value.
To get the list of identities under your ad account, use [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057). | 
     |
    
| 
      `identity_authorized_bc_id` | 
      Not specified | 
     |
    
| 
      Products | 
      Any of the following options:
- All products
- Product set
- Specific products with a maximum of 20 products | 
      `catalog_id`
`product_specific_type`
`item_group_ids`
`product_set_id`
`sku_ids` | 
      
- Set `catalog_id` to ID of the same catalog specified at the ad group level.
-  Set `product_specific_type` to `ALL`, `PRODUCT_SET` or `CUSTOMIZED_PRODUCTS`.If `product_specific_type` is set to `ALL`, you don't need to pass `sku_ids`, `item_group_ids`, and `product_set_id`.
- If `product_specific_type` is set to `PRODUCT_SET`, you need to pass either `item_group_ids` or `product_set_id`. `sku_ids` is not needed.
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to pass a maximum of 20 products through `sku_ids`. `item_group_ids` and `product_set_id` are not needed.
**Note**: To determine whether an E-commerce catalog product can be used in ads, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). If the returned `ad_creation_eligible` for the product is `AVAILABLE`, you can use the product in ads. | 
     |
    
| 
      Ad format | 
      **Catalog video**: Generate a dynamic video based on information from the product catalog. | 
      `ad_format` | 
      `SINGLE_VIDEO` | 
     |
    
| 
      `vertical_video_strategy` | 
      Any of the following values:
- `CATALOG_UPLOADED_VIDEOS`: catalog video using uploaded videos. To learn more about how to manage uploaded catalog videos, see [Upload catalog videos to associate with catalog products](https://business-api.tiktok.com/portal/docs?id=1803654904260674).
- `CATALOG_VIDEOS`: catalog video using video templates. | 
     |
    
| 
      Ad creative | 
      A catalog video. You need to ensure that at least one uploaded video or video template has been bound to your catalog or a video URL has been configured for each catalog product.
- If you select Your Videos (uploaded videos), the system will automatically select uploaded videos featuring your products.
- If you select a video template, the video template will be used to automatically generate the catalog video for each catalog product.
- If you don't select the video template, the system will automatically select one of your video templates for each catalog product to generate the corresponding catalog video. When a product has a video URL, that video will be used instead. | 
      `shopping_ads_video_package_id` | 
      Specified or not specified.
- If this field is not specified and `vertical_video_strategy` is set to `CATALOG_UPLOADED_VIDEOS`, the system will automatically select uploaded videos featuring your products.
- If this field is specified and `vertical_video_strategy` is set to `CATALOG_VIDEOS`, the specified video template will be used to automatically generate the catalog video for each catalog product.
- If this field is not specified and `vertical_video_strategy` is set to `CATALOG_VIDEOS`, the system will automatically select one of your video templates for each catalog product to generate the corresponding catalog video. When a product has a video URL, that video will be used instead.
To obtain the IDs of video templates (video packages) bound to your catalog, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073).
To learn about how to create video packages on TikTok Ads Manager, see [Create Video Packages](https://ads.tiktok.com/help/article/how-to-create-video-packages-in-a-catalog). | 
     |
    
| 
      `video_id`
`image_ids`
`tiktok_item_id`
`music_id` | 
      Not specified | 
     |
    
| 
      Ad text | 
      Specified | 
      `ad_text` | 
      Specify a valid value. | 
     |
    
| 
      Interactive add-on
(Optional) | 
      Disabled or enabled with any of the following types:
- Product Card
- Product Tiles (supported with allowlist)
- Countdown Sticker
- Gift Code Sticker
- Display Card | 
      `card_id` | 
      Not specified or specify the ID of one of the following creative portfolio types:
- Product Card
- Product Tiles
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
      `shopping_ads_deeplink_type` | 
      `CUSTOM` | 
     |
    
| 
      `deeplink_type` | 
      `NORMAL` | 
     |
    
| 
      `deeplink` | 
      Specify a custom deeplink.
The deeplink format can be any of the following:
- Custom URL scheme, in the format of `scheme://resource`. For instance, a Custom URL scheme of WhatsApp should follow the format `whatsapp://resource`.
- Apple’s universal link or Android App Link starting with `http://` or `https://`. | 
     |
    
| 
      Deeplink parameters
(Optional) | 
      Enabled or disabled | 
      `deeplink_utm_params` | 
      Specify valid values or not specified

You can manually add deeplink URL parameters to the custom deeplink by directly setting `deeplink` to a deeplink that already includes URL parameters.
- However, if you use a custom deeplink in your ad and specify `deeplink_utm_params` at the same time, the URL parameters will not be automatically appended to the custom deeplink (`deeplink`) upon ad delivery. In such cases, you need to ensure that `deeplink_utm_params` exactly matches the used deeplink URL parameters. Otherwise, an error will occur. | 
     |
    
| 
      Fallback URL | 
      Enabled with a custom link (the promoted web page) | 
      `shopping_ads_fallback_type` | 
      `CUSTOM` | 
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
      Enabled | 
      `call_to_action` | 
      Specify a valid value.

To get the enum values, see [Enumerations - Call-to-action](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Call-to-action). | 
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
  

#### Example
##### Using video templates
Request
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{AccessToken}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "CUSTOMIZED_USER",
            "identity_id": "{{identity_id}}",
            "catalog_id": "{{catalog_id}}",
            "product_specific_type": "ALL",
            "ad_format": "SINGLE_VIDEO",
            "vertical_video_strategy": "CATALOG_VIDEOS",
            "ad_text": "{{ad_text}}",
            "card_id": "{{card_id}}",
            "shopping_ads_deeplink_type": "CUSTOM",
            "deeplink_type": "NORMAL",
            "deeplink": "{{deeplink}}",
            "shopping_ads_fallback_type": "CUSTOM",
            "landing_page_url": "{{landing_page_url}}",
            "call_to_action": "LEARN_MORE"
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
            "{{ad_ids}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "deeplink": "{{deeplink}}",
                "profile_image_url": "",
                "card_id": "{{card_id}}",
                "campaign_name": "{{campaign_name}}",
                "video_id": null,
                "viewability_vast_url": null,
                "shopping_ads_video_package_id": "",
                "ad_texts": null,
                "is_aco": false,
                "modify_time": "{{modify_time}}",
                "ad_name": "{{ad_name}}",
                "adgroup_name": "{{adgroup_name}}",
                "image_ids": [],
                "ad_id": "{{ad_id}}",
                "dynamic_format": "UNSET",
                "music_id": null,
                "landing_page_urls": null,
                "identity_id": "{{identity_id}}",
                "landing_page_url": "{{landing_page_url}}",
                "product_specific_type": "ALL",
                "identity_type": "CUSTOMIZED_USER",
                "playable_url": "",
                "call_to_action": "LEARN_MORE",
                "avatar_icon_web_uri": "",
                "operation_status": "ENABLE",
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "create_time": "{{create_time}}",
                "optimization_event": "ADD_BILLING",
                "dynamic_destination": "UNSET",
                "display_name": "{{display_name}}",
                "vast_moat_enabled": false,
                "ad_text": "{{ad_text}}",
                "deeplink_type": "NORMAL",
                "catalog_id": "{{catalog_id}}",
                "viewability_postbid_partner": "UNSET",
                "creative_type": null,
                "shopping_ads_deeplink_type": "CUSTOM",
                "creative_authorized": false,
                "carousel_image_labels": null,
                "app_name": "",
                "campaign_automation_type": "MANUAL",
                "impression_tracking_url": null,
                "ad_format": "SINGLE_VIDEO",
                "click_tracking_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_ids}}"
                ],
                "is_new_structure": true,
                "campaign_id": "{{campaign_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "vertical_video_strategy": "CATALOG_VIDEOS",
                "brand_safety_vast_url": null,
                "adgroup_id": "{{adgroup_id}}",
                "call_to_action_id": null,
                "page_id": null,
                "advertiser_id": "{{advertiser_id}}",
                "shopping_ads_fallback_type": "CUSTOM"
            }
        ]
    }
}
(/code)
```
##### Using uploaded catalog videos
Request
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{AccessToken}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "CUSTOMIZED_USER",
            "identity_id": "{{identity_id}}",
            "catalog_id": "{{catalog_id}}",
            "product_specific_type": "ALL",
            "ad_format": "SINGLE_VIDEO",
            "vertical_video_strategy": "CATALOG_UPLOADED_VIDEOS",
            "ad_text": "{{ad_text}}",
            "card_id": "{{card_id}}",
            "shopping_ads_deeplink_type": "CUSTOM",
            "deeplink_type": "NORMAL",
            "deeplink": "{{deeplink}}",
            "shopping_ads_fallback_type": "CUSTOM",
            "landing_page_url": "{{landing_page_url}}",
            "call_to_action": "LEARN_MORE"
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
            "{{ad_ids}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "deeplink": "{{deeplink}}",
                "profile_image_url": "",
                "card_id": "{{card_id}}",
                "campaign_name": "{{campaign_name}}",
                "video_id": null,
                "viewability_vast_url": null,
                "shopping_ads_video_package_id": "",
                "ad_texts": null,
                "is_aco": false,
                "modify_time": "{{modify_time}}",
                "ad_name": "{{ad_name}}",
                "adgroup_name": "{{adgroup_name}}",
                "image_ids": [],
                "ad_id": "{{ad_id}}",
                "dynamic_format": "UNSET",
                "music_id": null,
                "landing_page_urls": null,
                "identity_id": "{{identity_id}}",
                "landing_page_url": "{{landing_page_url}}",
                "product_specific_type": "ALL",
                "identity_type": "CUSTOMIZED_USER",
                "playable_url": "",
                "call_to_action": "LEARN_MORE",
                "avatar_icon_web_uri": "",
                "operation_status": "ENABLE",
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "create_time": "{{create_time}}",
                "optimization_event": "ADD_BILLING",
                "dynamic_destination": "UNSET",
                "display_name": "{{display_name}}",
                "vast_moat_enabled": false,
                "ad_text": "{{ad_text}}",
                "deeplink_type": "NORMAL",
                "catalog_id": "{{catalog_id}}",
                "viewability_postbid_partner": "UNSET",
                "creative_type": null,
                "shopping_ads_deeplink_type": "CUSTOM",
                "creative_authorized": false,
                "carousel_image_labels": null,
                "app_name": "",
                "campaign_automation_type": "MANUAL",
                "impression_tracking_url": null,
                "ad_format": "SINGLE_VIDEO",
                "click_tracking_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_ids}}"
                ],
                "is_new_structure": true,
                "campaign_id": "{{campaign_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "vertical_video_strategy": "CATALOG_UPLOADED_VIDEOS",
                "brand_safety_vast_url": null,
                "adgroup_id": "{{adgroup_id}}",
                "call_to_action_id": null,
                "page_id": null,
                "advertiser_id": "{{advertiser_id}}",
                "shopping_ads_fallback_type": "CUSTOM"
            }
        ]
    }
}
(/code)
```
### Ad format as Catalog Carousel

  
    
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
      Custom User (custom identity) | 
      `identity_type` | 
      `CUSTOMIZED_USER` | 
     |
    
| 
      `identity_id` | 
      Specify a valid value
To get the list of identities under your ad account, use [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057). | 
     |
    
| 
      `identity_authorized_bc_id` | 
      Not specified | 
     |
    
| 
      Ad format | 
      **Catalog Carousel**: Create an ad with 2–20 products displayed in a slideshow format. This format will showcase product images of up to 20 products from your catalog at a time. | 
      `ad_format` | 
      `CATALOG_CAROUSEL` | 
     |
    
| 
      `vertical_video_strategy` | 
      Not specified | 
     |
    
| 
      Products | 
      Any of the following options:
- All products
- Product set
- Specific products with a maximum of 20 products | 
      `catalog_id`
`product_specific_type`
`item_group_ids`
`product_set_id`
`sku_ids` | 
      
- Set `catalog_id` to ID of the same catalog specified at the ad group level.
- Carousel image selection scope: The product images for products in a catalog (`catalog_id`) will be dynamically chosen as images in the delivering Carousel Ads. You can specify the scope of product images to choose from using the `product_specific_type` parameter:To have the Carousel images dynamically chosen from all products in the catalog, set `product_specific_type` to `ALL`, and do not pass any of `item_group_ids`, `product_set_id`, or `sku_ids`. The catalog (`catalog_id`) needs to include at least two products.
- To have the Carousel images dynamically chosen from products in a product set, set `product_specific_type` to `PRODUCT_SET`, and pass either `item_group_ids` or `product_set_id`. The specified `item_group_ids` or `product_set_id` needs to include at least two products.
- To have the images dynamically chosen from a customized product range consisting of up to 20 products, set `product_specific_type` to `CUSTOMIZED_PRODUCTS`, and pass `sku_ids`. The specified `sku_ids` needs to include at least two products.
**Note**: To determine whether an E-commerce catalog product can be used in ads, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). If the returned `ad_creation_eligible` for the product is `AVAILABLE`, you can use the product in ads.
- Carousel image type:Use the main images of the products: By default, the main image URLs of the dynamically selected catalog products will be used as Carousel images. | 
     |
    
| 
      Ad creative
· image | 
      At least two images supported in the Carousel Ad | 
     |
	
| 
      `image_ids` | 
      Not specified | 
     |
    
| 
      Ad creative 
· video | 
      Disabled | 
      `video_id`
`tiktok_item_id`
`shopping_ads_video_package_id` | 
      Not specified | 
     |
    
| 
      Ad creative 
· music | 
      A piece of music supported in the Carousel Ad | 
      `music_id` | 
      Pass one music ID that is valid for use in Catalog Carousel Ads.
To obtain a valid music ID, you can use any of the following methods:
- Filter the pieces of music for Catalog Carousel Ads under an ad account by specifying `music_scene` as `CATALOG_CAROUSEL` in [/file/music/get/](https://ads.tiktok.com/marketing_api/docs?id=1740053909509122).
- Upload a piece of customized music for Catalog Carousel Ads to an ad account by using any of the following methods:Specify `music_scene` as `CATALOG_CAROUSEL` and pass `music_file` and `music_signature` in [/file/music/upload/](https://ads.tiktok.com/marketing_api/docs?id=1740052650395650).
- Specify `music_scene` as `CATALOG_CAROUSEL`, `upload_type` as `UPLOAD_BY_FILE_ID`, and pass `file_id` to [/file/music/upload/](https://ads.tiktok.com/marketing_api/docs?id=1740052650395650). | 
     |
    
| 
      Ad text | 
      Specified | 
      `ad_text` | 
      Specify a valid value | 
     |
    
| 
      Interactive add-on | 
      Disabled | 
      `card_id` | 
      Not specified | 
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
      `shopping_ads_deeplink_type` | 
      `CUSTOM` | 
     |
    
| 
      `deeplink_type` | 
      `NORMAL` | 
     |
    
| 
      `deeplink` | 
      Specify a custom deeplink.
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

You can manually add deeplink URL parameters to the custom deeplink by directly setting `deeplink` to a deeplink that already includes URL parameters.
- However, if you use a custom deeplink in your ad and specify `deeplink_utm_params` at the same time, the URL parameters will not be automatically appended to the custom deeplink (`deeplink`) upon ad delivery. In such cases, you need to ensure that `deeplink_utm_params` exactly matches the used deeplink URL parameters. Otherwise, an error will occur. | 
     |
    
| 
      Fallback URL | 
      Enabled with a custom link (the promoted web page) | 
      `shopping_ads_fallback_type` | 
      `CUSTOM` | 
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
      Enabled | 
      `call_to_action` | 
      Specify a valid value.

To get the enum values, see [Enumerations - Call-to-action](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Call-to-action). | 
     |
    
| 
      Tracking
- TikTok events tracking
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
  

#### Example
Request
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{AccessToken}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "CUSTOMIZED_USER",
            "identity_id": "{{identity_id}}",
            "catalog_id": "{{catalog_id}}",
            "product_specific_type": "ALL",
            "ad_format": "CATALOG_CAROUSEL",
            "music_id": "{{music_id}}",
            "ad_text": "{{ad_text}}",
            "shopping_ads_deeplink_type": "CUSTOM",
            "deeplink_type": "NORMAL",
            "deeplink": "{{deeplink}}",
            "shopping_ads_fallback_type": "CUSTOM",
            "landing_page_url": "{{landing_page_url}}",
            "call_to_action": "LEARN_MORE"
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
            "{{ad_ids}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "deeplink": "{{deeplink}}",
                "profile_image_url": "",
                "card_id": null,
                "campaign_name": "{{campaign_name}}",
                "video_id": null,
                "viewability_vast_url": null,
                "shopping_ads_video_package_id": "",
                "ad_texts": null,
                "is_aco": false,
                "modify_time": "{{modify_time}}",
                "ad_name": "{{ad_name}}",
                "adgroup_name": "{{adgroup_name}}",
                "image_ids": [],
                "ad_id": "{{ad_id}}",
                "dynamic_format": "UNSET",
                "music_id": "{{music_id}}",
                "landing_page_urls": null,
                "identity_id": "{{identity_id}}",
                "landing_page_url": "{{landing_page_url}}",
                "product_specific_type": "ALL",
                "identity_type": "CUSTOMIZED_USER",
                "playable_url": "",
                "call_to_action": "LEARN_MORE",
                "avatar_icon_web_uri": "",
                "operation_status": "ENABLE",
                "ad_ref_pixel_id": "{{ad_ref_pixel_id}}",
                "create_time": "{{create_time}}",
                "optimization_event": "ADD_BILLING",
                "dynamic_destination": "UNSET",
                "display_name": "{{display_name}}",
                "vast_moat_enabled": false,
                "ad_text": "test",
                "deeplink_type": "NORMAL",
                "catalog_id": "{{catalog_id}}",
                "viewability_postbid_partner": "UNSET",
                "creative_type": null,
                "shopping_ads_deeplink_type": "CUSTOM",
                "creative_authorized": false,
                "carousel_image_labels": null,
                "app_name": "",
                "campaign_automation_type": "MANUAL",
                "impression_tracking_url": null,
                "ad_format": "CATALOG_CAROUSEL",
                "click_tracking_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_ids}}"
                ],
                "is_new_structure": true,
                "campaign_id": "{{campaign_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}",
                "vertical_video_strategy": null,
                "brand_safety_vast_url": null,
                "adgroup_id": "{{adgroup_id}}",
                "call_to_action_id": null,
                "page_id": null,
                "advertiser_id": "{{advertiser_id}}",
                "shopping_ads_fallback_type": "CUSTOM"
            }
        ]
    }
}
(/code)
```
