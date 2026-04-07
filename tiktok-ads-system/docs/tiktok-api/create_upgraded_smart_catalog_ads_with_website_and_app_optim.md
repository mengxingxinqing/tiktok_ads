# Create Upgraded Smart+ Catalog Ads with Website and App Optimization

**Doc ID**: 1855007137120578
**Path**: Use Cases/Campaign creation/Create an Upgraded Smart+ Campaign/Create Upgraded Smart+ Ads with Website and App Optimization/Create Upgraded Smart+ Catalog Ads with Website and App Optimization

---

Upgraded Smart+ Catalog Ads with Website and App Optimization are Upgraded Smart+ Sales Campaigns that use catalog products to drive sales on both your website and your app. For such campaigns, you need to set `objective_type` to `WEB_CONVERSIONS`, `sales_destination` to `WEB_AND_APP`, and `catalog_enabled `to `true` at the campaign level. 

# Prerequisite
Creating Upgraded Smart+ Catalog Ads with Website and App Optimization requires setting up a catalog in your Business Center first.

To set up the catalog:

1. Create a catalog using [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961).

The catalog type can be any of the following:
- E-commerce
- hotel
- flight
- destination
- entertainment

2. Upload products to the catalog using [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) (JSON schema), [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) (CSV feed template), or [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377)(online data feed schedule).
3. Check the product handling results.
	- For CSV feed and JSON schema, use [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889).
		- Pass in the `feed_log_id` obtained from Step 2. If the field `error_affected_products` in the response is not null, examine the issue details and return to Step 2 to reupload the product.
	- For online feed, use [/catalog/feed/log/](https://business-api.tiktok.com/portal/docs?id=1740665225631810).
		- Pass in the `feed_id` obtained from Step 2. If the field `error_count` in the response is not 0, examine your online feed and return to Step 2 to reupload the product.
4. (Optional) Create a product set using [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257).

If you want to have products selected from a product set, creating a product set is necessary. Otherwise, you can skip this step.
5. (Optional) Invite members to Business Center and grant the admin permission using [/bc/member/invite/](https://business-api.tiktok.com/portal/docs?id=1739939455765505).

You can also choose `advertiser_role` that you want to assign to the members invited.
6. (Optional) Share a catalog with members and grant catalog management access using [/bc/asset/assign/](https://business-api.tiktok.com/portal/docs?id=1739438211077121).

Make sure to specify `CATALOG` in the `asset_type` field and `ADMIN` in the `catalog_role` field.

For all catalog APIs, see [here](https://business-api.tiktok.com/portal/docs?id=1739578477445121).

# Steps
## Create a campaign
Create a campaign using [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706).

    
        
| 
            Setting | 
            Requirement | 
            Parameter | 
            How to configure the parameter | 
         |
    
    
        
| 
            Advertising objective | 
            Sales | 
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
            iOS 14 dedicated campaign | 
            Disabled | 
            `campaign_type` | 
            `REGULAR_CAMPAIGN` or not specified | 
         |
        
| 
            `app_id` | 
            Not specified | 
         |
        
| 
            `campaign_app_profile_page_state` | 
            Not specified | 
         |
        
| 
            Use catalog | 
            **Enabled** | 
            `catalog_enabled ` | 
            `true` | 
         |
        
| 
            Catalog type | 
            Any of the following types:
- E-commerce
- Travel and entertainment | 
            `catalog_type` | 
            Any of the following values:
- `ECOMMERCE`
- `TRAVEL_ENTERTAINMENT` | 
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

**Note**: This setting is only supported for advertisers who are registered in the US or Canada.
 | 
            `special_industries` | 
            Not specified or specify a valid value | 
         |
    
| 
        Campaign budget strategy | 
        Any of the following types:
- **Campaign budget**: Your budget will be automatically allocated and optimized across ad groups. All ad groups must share the same budget and optimization settings.
- **Ad group budget**: Precisely control spend for each ad group, using different budget and optimization settings for each. | 
        `budget_optimize_on` | 
        
- To set a campaign budget, set this field to `true` or leave it unspecified.
- To set an ad group budget, set this field to `false`. | 
     |
	
| 
        Campaign budget mode | 
        
- When Campaign budget strategy is Campaign budget, specify any of the following modes:Daily
- Lifetime
- When Campaign budget strategy is Ad group budget, specify any of the following modes to determine the budget limit for all ad groups:No limit
- Daily
- Lifetime | 
        `budget_mode` | 
        
- When `budget_optimize_on` is `true` or not specified, use any of the following values:`BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- When `budget_optimize_on` is `false`, use any of the following values:`BUDGET_MODE_INFINITE`
- `BUDGET_MODE_DAY`
- `BUDGET_MODE_TOTAL` | 
     |
	
| 
        Campaign budget | 
        
- When Campaign budget strategy is Campaign budget:Specify a valid budget.
- When Campaign budget strategy is Ad group budget:If the budget limit is No limit:Disabled
- If the budget limit is Daily or Lifetime limit:Specify a valid budget | 
        `budget` | 
        
- When `budget_optimize_on` is `true` or not specified:Specify a valid value.
- When `budget_optimize_on` is `false`:If `budget_mode` is `BUDGET_MODE_INFINITE`:Not specified
- If `budget_mode` is `BUDGET_MODE_DAY` or `BUDGET_MODE_TOTAL`:Specify a valid value | 
     |
        
| 
            PO number (Optional) | 
            Enabled or disabled | 
            `po_number` | 
            Specify valid values or not specified | 
         |
    

### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \\
--header 'Access-Token: {{Access-Token}}' \\
--header 'Content-Type: application/json' \\
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "WEB_AND_APP",
    "catalog_enabled": true,
    "catalog_type": "ECOMMERCE",
    "campaign_name": "{{campaign_name}}",
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
        "advertiser_id": "{{advertiser_id}}",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "budget_optimize_on": true,
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "campaign_type": "REGULAR_CAMPAIGN",
        "catalog_enabled": true,
        "catalog_type": "ECOMMERCE",
        "create_time": "{{create_time}}",
        "is_promotional_campaign": false,
        "modify_time": "{{modify_time}}",
        "objective_type": "WEB_CONVERSIONS",
        "operation_status": "ENABLE",
        "sales_destination": "WEB_AND_APP",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "smart_plus_adgroup_mode": "MULTIPLE"
    }
}

(/code)
```

## Create an ad group
Create an ad group using [/smart_plus/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1843314887930946). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1843314887930946).

    
        
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
            Specify **a catalog with at least two approved products**

The catalog type can be any of the following:
- E-commerce
- hotel
- flight
- destination
- entertainment | 
            `catalog_id`
`catalog_authorized_bc_id` | 
            Specify valid values.

The catalog (`catalog_id`) needs to have at least one approved product. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 2. 
The `catalog_type` of the catalog (`catalog_id`)  can be any of the following:
- `ECOM`
- `HOTEL`
- `FLIGHT`
- `DESTINATION`
- `ENTERTAINMENT`

- To obtain catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610).
- To learn about how to create a catalog, see [Prerequisite](#item-link-Prerequisite). | 
         |
        
| 
            Optimization and bidding
· Optimization location | 
            Website

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
            `promotion_type` | 
            `WEBSITE`

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign.
 | 
         |
        
| 
            Optimization and bidding
· Android & iOS | 
            Specify any of the following:
- an Android app
- an iOS app
- an Android app and an iOS app | 
            `app_config` | 
            Specify any of the following:
- App ID of an Android app
- App ID of an iOS app
- App IDs of an Android app and an iOS app
To obtain the list of App IDs within your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786) and check the returned `app_id`. | 
         |
        
| 
            Optimization and bidding
· Goal | 
            Any of the following types:
- Conversion
- Value
**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
            `optimization_goal` | 
            Any of the following values:
- `CONVERT`
- `VALUE`

**Note**:  When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign. | 
         |
        
| 
            Optimization and bidding
· Data connection | 
            Specify a valid Pixel | 
            `pixel_id` | 
            Specify a valid value.

To obtain the list of Pixels within your ad account, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978). | 
         |
        
| 
            Optimization and bidding
· Optimization event | 
            Specify a valid optimization event
- When optimization goal is Value, specify the optimization event as Complete Payment.**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
            `optimization_event` | 
            Specify a valid value.

**Note**:  When `optimization_goal` is set to `VALUE`, set this field to `SHOPPING`.

To learn about the supported event types, see [List of values for `optimization_event` for Upgraded Smart+ Ads with Website and App Optimization](#item-link-List of values for optimization_event for Upgraded Smart+ Ads with Website and App Optimization).
You need to ensure the specified optimization event is active for both the Pixel and the app or apps.

- To obtain the optimization events that have been configured for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- To obtain the active optimization events for an app, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977). 
**Note**:  When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_event`for ad groups within the same campaign. | 
         |
         
| 
            Optimization and bidding
· Bid Strategy, (Optional) Target CPA, 
and (Optional) Target ROAS | 
            
- If Goal is Conversion, the strategy can only be Maximum Delivery or Cost Cap.For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Value, the strategy can be Highest value or Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.**Note**: 
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
            `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
            
- If `optimization_goal` is `CONVERT`:Set `bid_type` to `BID_TYPE_CUSTOM` (Cost Cap) or `BID_TYPE_NO_BID`  (Maximum Delivery). Do not specify `deep_bid_type` and `roas_bid`.If `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `VALUE`:Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
**Note**:  
- The `bid_type` must be the same across ad groups within the same campaign.
-  When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`conversion_bid_price`
- `bid_price`
- `deep_bid_type`
- `roas_bid`
- You can only set `bid_type` to `BID_TYPE_CUSTOM` or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
         |
    
        
| 
            Optimization and bidding
· Attribution window
  · Click-through window | 
            Any of the following types:
- 1-day click
- 7-day click
- 14-day click
- 28-day click | 
            `click_attribution_window` | 
            Any of the following values:
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
         |
        
| 
            Optimization and bidding
· Attribution window
  · Engaged view-through window | 
            Any of the following types:
- 1-day engaged view
- 7-day engaged view
- 14-day engaged view
- 28-day engaged view | 
            `view_attribution_window` | 
            Any of the following values:
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
         |
        
| 
            Optimization and bidding
· Attribution window
  · View-through window | 
            Any of the following types:
- Off
- 1-day view
- 7-day view | 
            `engaged_view_attribution_window` | 
            Any of the following values:
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
         |
        
| 
            Optimization and bidding
· Event count | 
            Any of the following types:
- Every
- Once | 
            `attribution_event_count` | 
            Any of the following values:
- `ONCE`
- `EVERY` | 
         |
        
| 
            Optimization and bidding
· Billing event | 
            
- If Goal is Click, the billing event should be CPC.
- If Goal is Install, In-app event, or Value, the billing event should be oCPM.**Note**: 
- When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign.
 | 
            `billing_event` | 
            
- If `optimization_goal` is `CLICK`, set this field to `CPC`.
- If `optimization_goal` is `INSTALL`, `IN_APP_EVENT`,  or `VALUE`, set this field to `OCPM`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `billing_event`for ad groups within the same campaign.
 | 
         |
        
| 
            Optimization and bidding
· Delivery Type | 
            Standard (default) | 
            N/A | 
            By default, the Delivery Type for the Upgraded Smart+ Campaign is Standard. | 
         |
        
| 
            Budget and schedule
· Budget | 
            
- When you select a campaign budget mode:The ad group budget is disabled. The campaign-level budget will be used as the ad group budget.
- When you select an ad group budget strategy:If the ad group budget limit is No limit or Lifetime limit, you can use any of the following ad group budget modes:Lifetime
- Daily
- If the ad group budget limit is Daily limit, you can use the following ad group budget mode:Daily

**Note**: The ad group budget mode, if specified, must be the same across ad groups within the same campaign.
 | 
            `budget_mode`
`budget` | 
            
- When `budget_optimize_on` is `true` at the campaign level, `budget_mode` and `budget` are not supported.
- When `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_INFINITE` or `BUDGET_MODE_TOTAL` at the campaign level:Set `budget_mode` to `BUDGET_MODE_TOTAL` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`
- When `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_DAY` at the campaign level:Set `budget_mode` to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`

**Note**: The `budget_mode`, if specified, must be the same across ad groups within the same campaign.
 | 
         |
        
| 
            Budget and schedule
· Add spend target per ad group
  · Daily minimum | 
            
- When you use a daily campaign budget, you can enable or disable this setting.
- When you use a lifetime campaign budget or an ad group budget, this setting is not supported. | 
            `min_budget` | 
            
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` at the campaign level, you can either specify a valid value through this field or leave it unspecified.
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_TOTAL` or when `budget_optimize_on` is `false` at the campaign level, this field is not supported. | 
         |
        
| 
            Budget and schedule
· Schedule | 
            Any of the following types:
- Set start time and run ad group continuously
- Set start and end time
**Note**: You can only choose "Set start time and run ad group continuously" in any of the following scenarios: 
- At the campaign level, a daily campaign budget is set.
- At the ad group level, a daily ad group budget is set.
 | 
            `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
            
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`.
**Note**: You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
         |
        
| 
            Budget and schedule
· Dayparting (Optional) | 
            Any of the following types:
- All day (default)
- Select specific time | 
            `dayparting` | 
            Any of the following configurations:
- Specify an all-1 value, or do not specify this field
- Specify a value that contains 0 to indicate non-delivery | 
         |
        
| 
            Audience targeting optimization mode | 
            Any of the following modes:
- **Automatic targeting**You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
- **Custom targeting**You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads with Website and App Optimization](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads with Website and App Optimization). | 
            `targeting_optimization_mode` | 
            Any of the following values:
- `AUTOMATIC`
- `MANUAL`To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads with Website and App Optimization](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads with Website and App Optimization). | 
         |
        
| 
            Placements and brand safety
· Placement | 
            Any of the following types:
- **Automatic Placement**
- **Select specific placements**:TikTok
- Global App Bundle
- Pangle | 
            `placement_type`
`placements` | 
            
- To use Automatic Placement, do not specify `placement_type` and `placements`.The system will automatically configure placements for your Upgraded Smart+ Ad Groups based on your other settings and select high-quality traffic from various placements to deliver better results. If provided, the parameters `placement_type` and `placements` will be ignored.
- To retrieve the exact placement setting of an Upgraded Smart+ Ad Group, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- To use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and specify one or more of the following placements in `placements`:`PLACEMENT_TIKTOK`
- `PLACEMENT_PANGLE`
- `PLACEMENT_GLOBAL_APP_BUNDLE` | 
         |
        
| 
            Placements and brand safety
· Brand safety and suitability | 
            These settings only apply to **TikTok in-feed** and **search** ads. Any previous account-level settings in the brand safety hub will apply to your campaign. | 
            N/A | 
            N/A
To retrieve the ad account-level brand safety and suitability settings in the brand safety hub, use [/tiktok_inventory_filters/get/](https://business-api.tiktok.com/portal/docs?id=1830112550443073).
To configure or update the ad account-level brand safety and suitability settings in the brand safety hub, use [/tiktok_inventory_filters/update/](https://business-api.tiktok.com/portal/docs?id=1830112569774274). | 
         |
        
| 
            Placements and brand safety
· User comment | 
            Enabled or disabled | 
            `comment_disabled` | 
            Specify valid values or not specified | 
         |
        
| 
            Placements and brand safety
· Allow video download | 
            Enabled or disabled | 
            `share_disabled` | 
            Specify valid values or not specified | 
         |
        
| 
            Placements and brand safety
· Allow video sharing | 
            Enabled or disabled | 
            `video_download_disabled` | 
            Specify valid values or not specified | 
         |
        
| 
            Placements and brand safety
· Pangle block list | 
            Disabled | 
            N/A | 
            N/A | 
         |
    

### List of values for `optimization_event` for Upgraded Smart+ Ads with Website and App Optimization
The following tables list the events supported for Upgraded Smart+ Ads with Website and App Optimization.

    
        
| 
            Event name | 
            `optimization_event` value | 
            Corresponding Pixel event
(`optimization_event`) | 
            Corresponding app event
(`optimization_event` or `secondary_optimization_event`) | 
         |
    
    
        
| 
            Add payment info | 
            `ADD_BILLING` | 
            `ADD_BILLING` | 
            `ADD_PAYMENT_INFO` | 
         |
        
| 
            Add to Cart | 
            `ON_WEB_CART` | 
            `ON_WEB_CART` | 
            `IN_APP_CART` | 
         |
        
| 
            Add to wishlist | 
            `ON_WEB_ADD_TO_WISHLIST` | 
            `ON_WEB_ADD_TO_WISHLIST` | 
            `ADD_TO_WISHLIST` | 
         |
        
| 
            Initiate Checkout
/Checkout | 
            `INITIATE_ORDER` | 
            `INITIATE_ORDER` | 
            `IN_APP_ORDER` | 
         |
        
| 
            Purchase | 
            `SHOPPING` | 
            `SHOPPING` | 
            `ACTIVE_PAY` | 
         |
        
| 
            Search | 
            `ON_WEB_SEARCH` | 
            `ON_WEB_SEARCH` | 
            `SEARCH` | 
         |
        
| 
            Subscribe | 
            `ON_WEB_SUBSCRIBE` | 
            `ON_WEB_SUBSCRIBE` | 
            `SUBSCRIBE` | 
         |
        
| 
            View Content | 
            `ON_WEB_DETAIL` | 
            `ON_WEB_DETAIL` | 
            `IN_APP_DETAIL_UV` | 
         |
    

### Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads with Website and App Optimization

    
        
| 
            Targeting optimization mode | 
            Available targeting setting | 
            Requirement | 
            Parameter | 
            How to configure the parameter | 
         |
    
    
        
| 
            Automatic targeting
(`targeting_optimization_mode`
 as `AUTOMATIC` or not specified) | 
            Audience controls
· Location | 
            Specify valid locations.
If a catalog is specified, the location should match or be the subset of the targeting location of your catalog. | 
            `location_ids` or `zipcode_ids` or both | 
            Specify valid values.

If a catalog is specified, specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
         |
        
| 
            Audience controls
· Minimum age | 
            Any of the following options:
                
                    
- 18
                    
- 25
                 | 
            `spc_audience_age` | 
            Any of the following values:
                
                    
- `OVER_EIGHTEEN` or unspecified
                    
- `OVER_TWENTY_FIVE`
                 | 
         |
        
| 
            Audience controls
· Languages
 (Optional) | 
            Enabled or disabled | 
            `languages` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience controls
· Exclude audience
(Optional) | 
            Enabled or disabled | 
            `excluded_audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Age
 (Optional)

**Note**: Audience suggestions guide automatic targeting by choosing additional audience settings. These serve as suggestions only, and delivery to those audiences is not guaranteed. | 
            Enabled or disabled | 
            `age_groups` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Gender
 (Optional) | 
            Enabled or disabled | 
            `gender` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Custom audience
 (Optional) | 
            Enabled or disabled | 
            `audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Interests & behaviors
  · Interests
 (Optional) | 
            Enabled or disabled | 
            `interest_category_ids`
`interest_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Interests & behaviors
  · Purchase intention
 (Optional) | 
            Enabled or disabled | 
            `purchase_intention_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
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
            Custom targeting
(`targeting_optimization_mode` 
as `MANUAL`) | 
            Retarget
· Custom audience
(Optional when an E-commerce catalog is used) | 
            Enabled or disabled. | 
            `shopping_ads_retargeting_type`
`shopping_ads_retargeting_actions_days`
`included_custom_actions`
`excluded_custom_actions` | 
            Specify valid values or not specified | 
         |
        
|     
            Retarget
· Custom audience
  · Include
    · Target anyone in catalog or custom audiences
(Optional when both a Catalog Include Audience and a custom audience are specified) | 
            Enabled or disabled | 
            `shopping_ads_retargeting_custom_audience_relation` | 
            Specify valid values or not specified | 
         |
        
|     
            Demographics
· Location | 
            Specify a valid value.
If a catalog is specified, the location should match or be the subset of the targeting location of your catalog. | 
            `location_ids` or `zipcode_ids` or both | 
            Specify a valid value.
If a catalog is specified, specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
         |
        
| 
            Demographics
· HFSS Product/Brand | 
            Enabled or disabled

                
                    
- You can enable this setting when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union.
                 | 
            `is_hfss` | 
            `true` or `false`.
                
                    
- You can set it to `true` when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union.
                 | 
         |
        
| 
            Demographics
· LHF (Less Healthy Foods) compliance | 
            Enabled or disabled

                
                    
- This setting must be enabled when your targeting locations include locations in the UK and HFSS Product/Brand is enabled.
                 | 
            `is_lhf_compliance` | 
            `true` or `false`.
                
                    
- You need to set it to `true` when your targeting locations include locations in the UK and `is_hfss` is `true`.
                 | 
         |
        
| 
            Demographics
· Age
 (Optional) | 
            Enabled or disabled | 
            `age_groups` | 
            Specify valid values or not specified | 
         |
        
| 
            Demographics
· Gender
 (Optional) | 
            Enabled or disabled | 
            `gender` | 
            Specify valid values or not specified | 
         |
        
| 
            Demographics
· Languages
 (Optional) | 
            Enabled or disabled | 
            `languages` | 
            Specify valid values or not specified | 
         |
        
| 
            Custom audience
· Include audience
 (Optional) | 
            Enabled or disabled | 
            `audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Custom audience
· Smart audience
 (Optional) | 
            Enabled or disabled | 
            `smart_audience_enabled` | 
            `true` or `false` | 
         |
        
| 
            Custom audience
· Exclude audience
 (Optional) | 
            Enabled or disabled | 
            `excluded_audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Interests
 (Optional) | 
            Enabled or disabled | 
            `interest_category_ids`
`interest_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Purchase intention
 (Optional) | 
            Enabled or disabled | 
            `purchase_intention_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Video interactions
  · Creator interactions
  · Hashtag interactions
 (Optional) | 
            Enabled or disabled | 
            `actions` | 
            `true` or `false` | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Smart interests & behaviors
 (Optional) | 
            Enabled or disabled | 
            `smart_interest_behavior_enabled` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Spending power
 (Optional) | 
            Enabled or disabled | 
            `spending_power` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Household income
 (Optional) | 
            Enabled or disabled | 
            `household_income` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Operating system
(Optional) | 
            Enabled or disabled | 
            `operating_systems` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· OS versions
(Optional) | 
            Enabled or disabled | 
            `min_android_version`
`min_ios_version` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Device model
(Optional) | 
            Enabled or disabled | 
            `device_model_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Connection type
(Optional) | 
            Enabled or disabled | 
            `network_types` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Carriers
(Optional) | 
            Enabled or disabled | 
            `carrier_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Internet service provider
(Optional) | 
            Enabled or disabled | 
            `isp_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Device price
(Optional) | 
            Enabled or disabled | 
            `device_price_ranges` | 
            Specify valid values or not specified | 
         |
        
| 
            Use saved audience
(Optional) | 
            Enabled or disabled | 
            `saved_audience_id` | 
            Specify valid values or not specified | 
         |
    

### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \\
--header 'Access-Token: {{Access-Token}}' \\
--header 'Content-Type: application/json' \\
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "promotion_type": "WEBSITE",
    "app_config": [
        {
            "app_id": "{{app_id}}"
        },
        {
            "app_id": "{{app_id}}"
        }
    ],
    "optimization_goal": "CONVERT",
    "pixel_id": "{{pixel_id}}",
    "optimization_event": "ADD_BILLING",
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": {{conversion_bid_price}},
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_spec": {
        "location_ids": [
            "{{location_id}}"
        ]
    }
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
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "app_config": [
            {
                "app_id": "{{app_id}}"
            },
            {
                "app_id": "{{app_id}}"
            }
        ],
        "attribution_event_count": "EVERY",
        "bid_type": "BID_TYPE_CUSTOM",
        "billing_event": "OCPM",
        "budget": 0,
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "catalog_id": "{{catalog_id}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": {{conversion_bid_price}},
        "create_time": "{{create_time}}",
        "dayparting": "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "engaged_view_attribution_window": "ONE_DAY",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": 0,
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ADD_BILLING",
        "optimization_goal": "CONVERT",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "pixel_id": "{{pixel_id}}",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "product_source": "CATALOG",
        "promotion_type": "WEBSITE",
        "promotion_website_type": "UNSET",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": true,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "targeting_optimization_mode": "AUTOMATIC",
        "targeting_spec": {
            "actions": [],
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "app_targeting_type": "PROSPECT",
            "brand_safety_type": "STANDARD_INVENTORY",
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_id}}"
            ],
            "spc_audience_age": "OVER_EIGHTEEN",
            "spending_power": "ALL"
        },
        "video_download_disabled": true,
        "view_attribution_window": "ONE_DAY"
    }
}

(/code)
```

## Create an ad
Create an ad using [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522).

    
        
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
            
- To have the system auto-generate the ad name, set this field to `""`(empty string).
- To customize the ad name, specify a non-empty string value. | 
         |
        
| 
            Product source details
· Products | 
            Any of the following options:
- All products
- Product set
- Specific products with a maximum of 20 products | 
            `product_specific_type`
`product_set_id`
`product_ids` | 
            Set `product_specific_type` to `ALL`, `PRODUCT_SET` or `CUSTOMIZED_PRODUCTS`.
- If `product_specific_type` is set to `ALL`, you don't need to specify `product_set_id` and `product_ids`.
- If `product_specific_type` is set to `PRODUCT_SET`, you need to specify `product_set_id`. `product_ids` is not needed.
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to specify a maximum of 20 available catalog products through `product_ids`. `product_set_id` is not needed.To retrieve the product ID (`product_id`) of each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). | 
         |
        
| 
            Deeplink | 
            Enabled with a custom deeplink.
The deeplink format can be an Apple’s universal link or Android App Link starting with `http://` or `https://`. | 
            `landing_page_url_list` | 
            Specify a deeplink in the format of an Apple’s universal link or Android App Link starting with `http://` or `https://` through `landing_page_url_list`. | 
         |
        
| 
            `deeplink`
`deeplink_type`
`fallback_type`
`page_list` | 
            Not specified | 
         |
        
| 
            Added URL parameters (Optional) | 
            Enabled or disabled | 
            `utm_params` | 
            Specify valid values or not specified.
- **Note**:  If you set `landing_page_url_list` to a URL that already includes URL parameters, you can optionally specify `utm_params` at the same time to store the URL parameters used in the URL.
In such cases, you need to ensure that `utm_params` exactly matches the used URL parameters. The URL parameters will not be automatically appended to the `landing_page_url_list` upon ad delivery. | 
         |
        
| 
            Creative assets 
· Identity | 
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
- `BC_AUTH_TT`**Note**:
- For non-Spark Ads identities (`CUSTOMIZED_USER`), specify values to `identity_type` and `identity_id` in the `ad_configuration` object.
- For Spark Ads identities (`AUTH_CODE`,`TT_USER`,`BC_AUTH_TT`), specify values to `identity_type` and `identity_id` within the `creative_info` object.
 | 
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
            Creative assets 
· Autoselect from catalog | 
            Any of the following options:
- Enabled (Recommended)Images and videos in your catalog will be used to automatically generate optimized Catalog Ads in all formats for your products.
- Multiple ad format combinations are supported. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ Catalog Ads with Website and App Optimization](#item-link-Customize the ad format combinations in Upgraded Smart+ Catalog Ads with Website and App Optimization).
- DisabledImages and videos in your catalog will not be used to automatically generate optimized Catalog Ads in all formats for your products. The system will automatically create single video ads using your specified content.
- For a single ad, you can include one to **50 ad creatives** that can consist of the following types:Videos
- TikTok video posts
- TikTok photo posts
- Carousel
- To learn about the combination of available ad creatives based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).
**Note**: Not using a catalog for creatives might restrict your ad performance potential.
 | 
            `catalog_creative_toggle`
`video_info`
`image_info`
`music_info`
`ad_text_list`
`tiktok_item_id`
`ad_format` | 
            
- To enable auto-selection of catalog creatives, set `catalog_creative_toggle` to `true`, specify a valid value for `ad_format` in each `creative_info` object, and specify a piece of music via `music_info`. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ Catalog Ads with Website and App Optimization](#item-link-Customize the ad format combinations in Upgraded Smart+ Catalog Ads with Website and App Optimization).

**Note**: `music_info` is required when `catalog_creative_toggle` is `true`.
- To disable auto-selection of catalog creatives, set `catalog_creative_toggle` to `false`.For a single ad, you can include one to **50 ad creatives** that can consist of the following types:Videos
- TikTok video posts
- TikTok photo posts
- Carousel
- For each creative, specify the corresponding value for `ad_format` in each `creative_info` object.
- To learn about configurations of the available ad creative combinations based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).  | 
         |
        
| 
            Add promo code or offer
(Optional) | 
            Disabled | 
            N/A | 
            N/A | 
         |
        
| 
            Call to action | 
            Any of the following options:
- Dynamic
- Standard**Note**: When you use a Spark Ads identity, you can only use dynamic call to action.
 | 
            `call_to_action_id`
`call_to_action_list` | 
            
- To use dynamic call to action, specify `call_to_action_id`.
- To use standard call to action, specify `call_to_action_list`.

**Note**: If you set `identity_type` within the `creative_info` object to `TT_USER`, `BC_AUTH_TT`, or `AUTH_CODE`, `call_to_action_id` is required.
 | 
         |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
        
| 
            Interactive add-ons
(Optional)
(When the ad creatives include videos or video posts) | 
            Disabled or enabled with up to one add-on in any of the following types:
- Display Card
- Countdown Sticker
- Gift Code Sticker
**Note**: By using interactive add-ons, your ad will no longer display product cards. 
 | 
            `interactive_add_on_list` | 
            Not specified or specify up to one ID of any of the following add-on types:
- Countdown Sticker
- Gift Code Sticker
- Display Card
**Note**: 
- You can only use add-ons when `creative_list` contains video creatives, including videos and TikTok video posts.
To create an interactive add-on (creative portfolio), use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to obtain the ID of a Display Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058#item-link-Display%20Card).
- To learn about how to obtain the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177). | 
         |
        
| 
            Third-party tracking settings
· Impression tracking URL for iOS
(Optional) | 
            Disabled or enabled | 
            `app_id`
`app_type`
`impression_tracking_url` | 
            Any of the following configurations:
- Not specified 
- Specify valid values:Set `app_id` to the App ID of an iOS app
- Set `app_type` to `APP_IOS`
- Set `impression_tracking_url` to the Impression tracking URL for iOS | 
         |
        
| 
            Third-party tracking settings
· Click tracking URL for iOS
(Optional) | 
            Disabled or enabled | 
            `app_id`
`app_type`
`click_tracking_url` | 
            Any of the following configurations:
- Not specified 
- Specify valid values:Set `app_id` to the App ID of an iOS app
- Set `app_type` to `APP_IOS`
- Set `click_tracking_url` to the Click tracking URL for iOS | 
         |
        
| 
            Third-party tracking settings
· Impression tracking URL for Android
(Optional) | 
            Disabled or enabled | 
            `app_id`
`app_type`
`impression_tracking_url` | 
            Any of the following configurations:
- Not specified 
- Specify valid values:Set `app_id` to the App ID of an Android app
- Set `app_type` to `APP_ANDROID`
- Set `impression_tracking_url` to the Impression tracking URL for Android | 
         |
        
| 
            Third-party tracking settings
· Click tracking URL for Android 
(Optional) | 
            Disabled or enabled | 
            `app_id`
`app_type`
`click_tracking_url` | 
            Any of the following configurations:
- Not specified 
- Specify valid values:Set `app_id` to the App ID of an Android app
- Set `app_type` to `APP_ANDROID`
- Set `click_tracking_url` to the Click tracking URL for Android | 
         |
    

### Customize the ad format combinations in Upgraded Smart+ Catalog Ads with Website and App Optimization
If you enable auto-selection of catalog creatives (`catalog_creative_toggle` is `true`), the system will automatically create ads using combinations of three possible formats: catalog carousel, catalog video, and single video.

The possible ad format combinations for your Upgraded Smart+ Catalog Ads with Website and App Optimization are illustrated in the following table.

    
        
| 
            Is the catalog carousel format available? | 
            Is the catalog video format available? | 
            Is the single video format available? | 
            Ad format combination for your Upgraded Smart+ Catalog Ads with Website and App Optimization | 
         |
    
    
        
| 
            ✅ | 
            ❌ | 
            ❌ | 
            Catalog carousel only | 
         |
        
| 
            ✅ | 
            ❌ | 
            ✅ | 
            Catalog carousel and single video | 
         |
        
| 
            ✅ | 
            ✅ | 
            ❌ | 
            Catalog carousel and catalog video | 
         |
        
| 
            ✅ | 
            ✅ | 
            ✅ | 
            Catalog carousel, catalog video, and single video | 
         |
    

To ensure certain ad formats are available in Upgraded Smart+ Catalog Ads with Website and App Optimization, follow the instructions in the following table.

    
        
| 
            Ad format | 
            Ad format description | 
            How to ensure the ad format is available | 
            How to configure the parameters | 
         |
    
    
        
| 
            catalog carousel | 
            Display 2–20 products in a slideshow format. This format will showcase product images of up to 20 products from your catalog at a time. | 
            The catalog needs to contain at least two products supported in Catalog Carousel Ads. | 
            Ensure that the catalog (`catalog_id`) contains at least two approved products. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least two.
- Carousel image selection scope: The product images for products in a catalog (`catalog_id`) will be dynamically chosen as images in the delivering Catalog Carousel Ads. The scope of product images to choose from is determined by the specified `product_specific_type` parameter:If `product_specific_type` is set to `ALL`, the system will dynamically choose Carousel images from all products in the catalog.
- If `product_specific_type` is set to `PRODUCT_SET`, the system will dynamically choose Carousel images from products in the specified product set (`product_set_id`).
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, the system will dynamically choose Carousel images from a customized product range consisting of up to 20 products (`product_ids`).
- Carousel image type:Use the main images of the products: By default, the main image URLs of the dynamically selected catalog products will be used as Carousel images. | 
         |
        
| 
            Specify a piece of music supported in Catalog Carousel Ads. | 
            Pass one music ID that is valid for use in Catalog Carousel Ads via `music_info`.

To obtain a valid music ID, you can use any of the following methods:
- Filter the pieces of music for Catalog Carousel Ads under an ad account by specifying `music_scene` as `CATALOG_CAROUSEL` in [/file/music/get/](https://ads.tiktok.com/marketing_api/docs?id=1740053909509122).
- Upload a piece of customized music for Catalog Carousel Ads to an ad account by using any of the following methods:Specify `music_scene` as `CATALOG_CAROUSEL` and pass `music_file` and `music_signature` in [/file/music/upload/](https://ads.tiktok.com/marketing_api/docs?id=1740052650395650).
- Specify `music_scene` as `CATALOG_CAROUSEL`, `upload_type` as `UPLOAD_BY_FILE_ID`, and pass `file_id` to [/file/music/upload/](https://ads.tiktok.com/marketing_api/docs?id=1740052650395650). | 
         |
        
| 
            catalog video | 
            Generate a dynamic video based on information from the product catalog | 
            The catalog needs to be bound to at least one video template or you need to configure a video URL for each catalog product.
The system will automatically select one of your video templates for each catalog product to generate the corresponding catalog video or use the video URL for the catalog product. | 
            Ensure that at least one video template is bound to your catalog (`catalog_id`) or a video URL (`video_url`) has been configured for each catalog product.
- To ensure a video URL has been configured for each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) and check the returned `video_url`.If you want to add video URLs for your catalog products, use [/catalog/product/update/](https://business-api.tiktok.com/portal/docs?id=1740562287852546).
- To ensure that at least one video template (video package) is bound to your catalog, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073).To learn about how to create video templates on TikTok Ads Manager, see [How to create video packages in a Catalog](https://ads.tiktok.com/help/article/how-to-create-video-packages-in-a-catalog?lang=en).
- To retrieve video templates for your catalog via API, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073). | 
         |
        
| 
            single video | 
            Use specified video creatives to promote your products. | 
            Specify additional videos | 
            Specify additional videos via `video_info` and cover images via `image_info`. | 
         |
    

### Example

#### Using catalog creatives
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \\
--header 'Access-Token: {{Access-Token}}' \\
--header 'Content-Type: application/json' \\
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "landing_page_url_list": [
        {
            "landing_page_url": "{{landing_page_url}}"
        }
    ],
    "creative_list": [
        {
            "creative_info": {
                "ad_format": "CATALOG_CAROUSEL",
                "music_info": {
                    "music_id": "{{music_id}}"
                }
            }
        }
    ],
    "ad_text_list": [
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        }
    ],
    "ad_configuration": {
        "product_specific_type": "ALL",
        "identity_type": "CUSTOMIZED_USER",
        "identity_id": "{{identity_id}}",
        "catalog_creative_toggle": true,
        "call_to_action_id": "{{call_to_action_id}}"
    }
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
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "catalog_creative_toggle": true,
            "dark_post_status": "OFF",
            "deeplink_utm_params": [],
            "identity_id": "{{identity_id}}",
            "identity_type": "CUSTOMIZED_USER",
            "phone_info": {},
            "product_info": {
                "product_image_list": []
            },
            "product_specific_type": "ALL",
            "tracking_info": {
                "app_tracking_info_list": [
                    {
                        "app_id": "{{app_id}}",
                        "app_type": "APP_ANDROID",
                        "click_tracking_url": "",
                        "impression_tracking_url": ""
                    },
                    {
                        "app_id": "{{app_id}}",
                        "app_type": "APP_IOS",
                        "click_tracking_url": "",
                        "impression_tracking_url": ""
                    }
                ]
            },
            "utm_params": []
        },
        "ad_name": "{{ad_name}}",
        "ad_text_list": [
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            }
        ],
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "auto_message_list": [],
        "call_to_action_list": [],
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "creative_list": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format": "CATALOG_CAROUSEL",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "CUSTOMIZED_USER",
                    "material_name": "catalog_carousel_or_single_image",
                    "music_info": {
                        "music_id": "{{music_id}}"
                    }
                },
                "material_operation_status": "ENABLE"
            }
        ],
        "custom_product_page_list": [],
        "deeplink_list": [],
        "disclaimer": {},
        "interactive_add_on_list": [],
        "landing_page_url_list": [
            {
                "landing_page_url": "{{landing_page_url}}"
            }
        ],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}

(/code)
```

#### Without using catalog creatives
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \\
--header 'Access-Token: {{Access-Token}}' \\
--header 'Content-Type: application/json' \\
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "landing_page_url_list": [
        {
            "landing_page_url": "{{landing_page_url}}"
        }
    ],
    "creative_list": [
        {
            "creative_info": {
                "ad_format": "SINGLE_VIDEO",
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                "identity_id": "{{identity_id}}",
                "identity_type": "BC_AUTH_TT"
            }
        }
    ],
    "ad_text_list": [
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        }
    ],
    "ad_configuration": {
        "product_specific_type": "ALL",
        "catalog_creative_toggle": false,
        "dark_post_status": "ON",
        "call_to_action_id": "{{call_to_action_id}}"
    }
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
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "catalog_creative_toggle": false,
            "dark_post_status": "ON",
            "deeplink_utm_params": [],
            "phone_info": {},
            "product_info": {
                "product_image_list": []
            },
            "product_specific_type": "ALL",
            "tracking_info": {
                "app_tracking_info_list": [
                    {
                        "app_id": "{{app_id}}",
                        "app_type": "APP_ANDROID",
                        "click_tracking_url": "{{click_tracking_url}}",
                        "impression_tracking_url": "{{impression_tracking_url}}"
                    },
                    {
                        "app_id": "{{app_id}}",
                        "app_type": "APP_IOS",
                        "click_tracking_url": "{{click_tracking_url}}",
                        "impression_tracking_url": "{{impression_tracking_url}}"
                    }
                ]
            },
            "utm_params": []
        },
        "ad_name": "{{ad_name}}",
        "ad_text_list": [
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            }
        ],
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "auto_message_list": [],
        "call_to_action_list": [],
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "creative_list": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format": "SINGLE_VIDEO",
                    "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "BC_AUTH_TT",
                    "image_info": [
                        {
                            "web_uri": "{{web_uri}}"
                        }
                    ],
                    "material_name": "{{material_name}}",
                    "video_info": {
                        "file_name": "{{file_name}}",
                        "video_id": "{{video_id}}"
                    }
                },
                "material_operation_status": "ENABLE"
            }
        ],
        "custom_product_page_list": [],
        "deeplink_list": [],
        "disclaimer": {},
        "interactive_add_on_list": [],
        "landing_page_url_list": [
            {
                "landing_page_url": "{{landing_page_url}}"
            }
        ],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}

(/code)
```
