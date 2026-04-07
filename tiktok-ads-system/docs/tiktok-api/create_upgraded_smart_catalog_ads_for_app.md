# Create Upgraded Smart+ Catalog Ads for App

**Doc ID**: 1847303035303106
**Path**: Use Cases/Campaign creation/Create an Upgraded Smart+ Campaign/Create Upgraded Smart+ Catalog Ads for App

---

This article walks you through the steps to create Upgraded Smart+ Catalog Ads for App using the Sales objective.

Upgraded Smart+ Catalog Ads for App are Upgraded Smart+ Sales Campaigns that use catalog products to deliver ads. For such campaigns, you need to set `objective_type` to `WEB_CONVERSIONS` and `sales_destination` to `APP` at the campaign level. By utilizing Upgraded Smart+ Catalog Ads for App, you can grow your app user base in two primary ways: by acquiring new users (Prospecting) and re-engaging existing ones (Retargeting).

Based on your preference for creating a [Dedicated Campaign](https://business-api.tiktok.com/portal/docs?id=1740029173531649), you can create Upgraded Smart+ Catalog non-DC Ads for App, or Upgraded Smart+ Catalog DC Ads for App. For detailed instructions on creating each type, refer to their respective sections: "[Create Upgraded Smart+ Catalog non-DC Ads for App](#item-link-Create Upgraded Smart+ Catalog non-DC Ads for App)", "[Create Upgraded Smart+ Catalog DC Ads for App](#item-link-Create Upgraded Smart+ Catalog DC Ads for App)".

# Create Upgraded Smart+ Catalog non-DC Ads for App

Upgraded Smart+ Catalog non-DC Ads for App are Upgraded Smart+ Sales Campaigns with iOS 14 dedicated campaign setting disabled that use catalog products to deliver ads. For such campaigns, you can set the `campaign_type` parameter to `REGULAR_CAMPAIGN` or leave `campaign_type` unspecified.

## Prerequisite for creating Upgraded Smart+ Catalog non-DC Ads for App

Creating Upgraded Smart+ Catalog Ads for App requires setting up a catalog in your Business Center first.

To set up the catalog:

1. Create a catalog using [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961).

The catalog type can be any of the following:

- E-commerce
- hotel
- flight
- destination
- entertainment

2. Upload products to the catalog using [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) (JSON schema), [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) (CSV feed template), or [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377)(online data feed schedule).

3. Check the product handling results using [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889).
   
Pass in the `feed_log_id` obtained from Step 2. If the field `error_affected_products` in the response is not null, examine the issue details and return to Step 2 to reupload the product.

4. (Optional) Create a product set using [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257).
   
If you want to have products selected from a product set, creating a product set is necessary. Otherwise, you can skip this step.

5. (Optional) Invite members to Business Center and grant the admin permission using [/bc/member/invite/](https://business-api.tiktok.com/portal/docs?id=1739939455765505).
   
You can also choose `advertiser_role` that you want to assign to the members invited.

6. (Optional) Share a catalog with members and grant catalog management access using [/bc/asset/assign/](https://business-api.tiktok.com/portal/docs?id=1739438211077121).
   
Make sure to specify `CATALOG` in the `asset_type` field and `ADMIN` in the `catalog_role` field.

For all catalog APIs, see [here](https://business-api.tiktok.com/portal/docs?id=1739578477445121).

## Steps

### Create a campaign

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
      App | 
      `sales_destination` | 
      `APP` | 
     |
        
| 
            Catalog type | 
            Any of the following types:
- E-commerce
- Travel and entertainment | 
            `catalog_enabled` | 
            `true` | 
         |
        
| 
            `catalog_type` | 
            Any of the following values:
- `ECOMMERCE`
- `TRAVEL_ENTERTAINMENT` | 
         |
    
| 
      iOS 14 dedicated campaign | 
      **Disabled**

To learn about how to create Upgraded Smart+ Catalog Ads for App with iOS 14 Dedicated Campaign enabled, see [Create Upgraded Smart+ Catalog DC Ads for App](#item-link-Create Upgraded Smart+ Catalog DC Ads for App). | 
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
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
      Special ad categories (Optional) | 
      Disabled or enabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada.
 | 
      `special_industries` | 
      Not specified or specify a valid value | 
     |
    
| 
      Campaign budget strategy | 
      Any of the following types:
- **Automatic campaign budget**: Your budget will be automatically allocated and optimized across ad groups. All ad groups must share the same budget and optimization settings.
- **Custom ad group budget**: Precisely control spend for each ad group, using different budget and optimization settings for each. | 
      `budget_optimize_on` | 
      
- To set an automatic campaign budget, set this field to `true` or leave it unspecified.
- To set a custom ad group budget, set this field to `false`. | 
     |
    
| 
      Campaign budget mode | 
      
- When Campaign budget strategy is Automatic campaign budget, specify any of the following modes:Daily
- Lifetime
- When Campaign budget strategy is Custom ad group budget:Disabled | 
      `budget_mode` | 
      
- When `budget_optimize_on` is `true` or not specified, use any of the following values :`BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- When `budget_optimize_on` is `false`:Not specified | 
     |
    
| 
      Automatic budget increase (when Campaign budget strategy is Automatic campaign budget and campaign budget mode is daily) | 
      Any of the following options:
- Enabled
- Disabled | 
      `budget_auto_adjust_strategy` | 
      When `budget_optimize_on` is `true` or not specified and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`:
-  To enable the setting, use the following value:`AUTO_BUDGET_INCREASE`. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- To disable the setting: Not specified

**Note**: Enabling automatic budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Campaign budget | 
      
- When Campaign budget strategy is Automatic campaign budget, specify a valid budget
- When Campaign budget strategy is Custom ad group budget:Disabled | 
      `budget` | 
      
- When `budget_optimize_on` is `true` or not specified, specify a valid value.
- When `budget_optimize_on` is `false`:Not specified | 
     |
    
| 
      Realtime API (RTA) (Optional) | 
      Enabled or disabled

**Note**: The available placements at the ad group level might vary based on your RTA setting.
 | 
      `rta_id` | 
      Specify one of the RTA IDs associated with your ad account.

To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative.

**Note**: The available placement setting (`placement_type` and `placements`) at the ad group level might vary based on your `rta_id` configuration.
 | 
     |
    
| 
      Use RTA to automatically select products (Optional) | 
      
- When RTA is disabled, this setting is not supported.
- When RTA is enabled, you can either enable or disable this setting. | 
      `rta_product_selection_enabled` | 
      
- When `rta_id` is not specified:`false` or not specified
- When `rta_id` is specified, use any of the following configurations :`true`
- `false` or not specified | 
     |
    
| 
      Use RTA bid (Optional) | 
      
- When RTA is disabled, this setting is not supported.
- When RTA is enabled, you can either enable or disable this setting. | 
      `rta_bid_enabled` | 
      
- When `rta_id` is not specified:`false` or not specified
- When `rta_id` is specified, use any of the following configurations :`true`
- `false` or not specified | 
     |
  

#### Example
**Creating a CBO campaign**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": {{request_id}},
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "APP",
    "catalog_enabled": true,
    "catalog_type": "ECOMMERCE",
    "campaign_type": "REGULAR_CAMPAIGN",
    "campaign_name": "{{campaign_name}}",
    "budget": {{budget}}
}'
(/code)
```

Response
```xcodeblock
(code json)
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
        "sales_destination": "APP",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "smart_plus_adgroup_mode": "MULTIPLE"
    }
}
(/code)
```

### Create an ad group

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

**Note**:
- When RTA is disabled at the campaign level, you can specify any of the following catalog types:E-commerce
- hotel
- flight
- destination
- entertainment
- When RTA is enabled at the campaign level, you can specify any of the following catalog types:E-commerce
- entertainment
 | 
      `catalog_id`
`catalog_authorized_bc_id` | 
      Specify valid values.
The catalog (`catalog_id`) needs to have at least two approved products. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 2.

- To obtain catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610).
- To learn about how to create a catalog, see [ Prerequisite for creating Upgraded Smart+ Catalog non-DC Ads for App](#item-link-Prerequisite for creating Upgraded Smart+ Catalog non-DC Ads for App).

**Note**:
- When `rta_id` is not specified at the campaign level, the `catalog_type` of the catalog can be any of the following:`ECOM`
- `HOTEL`
- `FLIGHT`
- `DESTINATION`
- `ENTERTAINMENT`
- When `rta_id` is specified at the campaign level, the `catalog_type` of the catalog can be any of the following:`ECOM`
- `ENTERTAINMENT`
 | 
     |
    
| 
      Optimization and bidding 
· App | 
      Any of the following types:
- Android App
- iOS App

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
      `promotion_type`
`app_id` | 
      
- To specify an Android App:Specify an Android App via `app_id`.
- Set `promotion_type` to `APP_ANDROID`.
- To specify an iOS App:Specify an iOS App via `app_id`.
- Set `promotion_type` to `APP_IOS`.To obtain the list of Apps under your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).
- For Android Apps, the returned `platform` will be `ANDROID`.
- For iOS Apps, the returned `platform` will be `IOS`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding 
· Goal | 
      Any of the following types:
- ClickWe'll deliver your ads to the people most likely to click on your ad.
- InstallWe'll show your ads to the people who are most likely to install your app.
- In-app eventWe'll show your ads to the people who are most likely to perform certain actions within your app.
- ValueWe'll deliver your ads to users that are more likely to make a purchase in order to maximize your total purchase value.
**Note**:
- When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
      `optimization_goal` | 
      Any of the following values:
- `CLICK`
- `INSTALL` (with `optimization_event` as `ACTIVE`)To use `INSTALL`, you need to ensure third-party tracking has been set up for the selected App.To check whether third-party tracking (`tracking_url`) has been configured for an App, use [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297).
- To add third-party tracking for an existing App, use [/app/update/](https://business-api.tiktok.com/portal/docs?id=1740859300069378). To learn about how to obtain tracking links from a third-party partner, see [Mobile Measurement Partner Tracking](https://ads.tiktok.com/help/article/mobile-measurement-partner-mmp-tracking).
- `IN_APP_EVENT` (with `optimization_event` specified)To use `IN_APP_EVENT`, you need to ensure the specified event (`optimization_event`) is available for the selected App.
- `VALUE` (with `optimization_event` specified)When you set this field to `VALUE`, specify the placement parameters (`placement_type` or both `placement_type` and `placements`) at the same time.
- Learn more about [Value-Based Optimization](https://business-api.tiktok.com/portal/docs?id=1739381743067137).
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding 
· Select in-app event (when Goal is In-app event) | 
      Any of the following types:
- Standard Event
- Custom Conversion
**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign. | 
      `optimization_event`
`custom_conversion_id` | 
      When `optimization_goal` is `IN_APP_EVENT`, specify any of the following:
- A Standard Event through`optimization_event`
- A Custom Conversion along with the associated conversion event through `custom_conversion_id` and `optimization_event`

- To obtain the available optimization events (`optimization_event`) for the App, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977).
- To obtain the list of Custom Conversions associated with an App, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673).To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation.
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, the `optimization_event` and `custom_conversion_id`, if specified, must be the same for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding 
· Bid Strategy, (Optional) Target CPA, and (Optional) Target ROAS | 
      
- If Goal is Click, Install, or In-app event, the strategy can only be Maximum Delivery or Cost Cap.For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Value, the strategy can be Highest value or Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.
**Note**:
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      
- If `optimization_goal` is `CLICK`, `INSTALL`, or `IN_APP_EVENT`:Set `bid_type` to `BID_TYPE_CUSTOM` (Cost Cap) or `BID_TYPE_NO_BID` (Maximum Delivery). Do not specify `deep_bid_type` and `roas_bid`.If `optimization_goal` is `INSTALL` or `IN_APP_EVENT`and `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `CLICK` and `bid_type` is `BID_TYPE_CUSTOM`, specify `bid_price` at the same time.
- If `optimization_goal` is `VALUE`:Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
**Note**:
- The `bid_type` must be the same across ad groups within the same campaign.
- When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`conversion_bid_price`
- `bid_price`
- `deep_bid_type`
- `roas_bid`
- You can only set `bid_type` to `BID_TYPE_CUSTOM` or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
     |
    
| 
      Optimization and bidding 
· Billing event | 
      
- If Goal is Click, the billing event should be CPC.
- If Goal is Install, In-app event, or Value, the billing event should be oCPM.

**Note**:
- When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign.
 | 
      `billing_event` | 
      
- If `optimization_goal` is `CLICK`, set this field to `CPC`.
- If `optimization_goal` is `INSTALL`, `IN_APP_EVENT`, or `VALUE`, set this field to `OCPM`.

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
      
- When you select an automatic campaign budget mode:The ad group budget is disabled. The campaign-level budget will be used as the ad group budget.
- When you select a custom ad group budget strategy, you can use any of the following ad group budget modes:Lifetime
- Daily
**Note**:
- The ad group budget mode, if specified, must be the same across ad groups within the same campaign.
 | 
      `budget_mode`
`budget` | 
      
- When `budget_optimize_on` is `true` at the campaign level, `budget_mode` and `budget`are not supported.
- When `budget_optimize_on` is `false` at the campaign level:Set `budget_mode` to `BUDGET_MODE_TOTAL` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`

**Note**:
- The `budget_mode`, if specified, must be the same across ad groups within the same campaign.
 | 
     |
    
| 
      Budget and schedule 
· Automatic budget increase (when Goal is Value) | 
      Enabled or disabled

To enable this setting, the following conditions should be met:
- At the campaign level: CBO is disabled.
- At the ad group level:Ad group budget is Daily
- Goal is Value
- Bid Strategy is Target ROAS
- Time window of the bid strategy is Day 0 ROAS | 
      `budget_auto_adjust_strategy` | 
      Use any of the following values:
- `AUTO_BUDGET_INCREASE`: To enable automatic budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable automatic budget increase.
You can only set this field to `AUTO_BUDGET_INCREASE` when the following conditions are all met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level:`budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `optimization_goal` is `VALUE`.
- `deep_bid_type` is `VO_MIN_ROAS`.
- `vbo_window` is `ZERO_DAY`.

**Note**: Enabling automatic budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
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
      Audience targeting | 
      Any of the following modes:
- **Prospect**Find new customers who want to install your app
- **Retarget**Show ads to customers who are already using your app

**Note**: When Optimization goal is Install, this setting is not supported. | 
      `app_targeting_type` | 
      Any of the following values:
- `PROSPECT`
- `RETARGETING`

**Note**: When `optimization_goal` is `INSTALL`, `app_targeting_type` is not supported. | 
     |
    
| 
      Audience targeting optimization mode | 
      Any of the following modes:
- **Automatic targeting**You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
- **Custom targeting**You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App). | 
      `targeting_optimization_mode` | 
      Any of the following values:
- `AUTOMATIC`
- `MANUAL`To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App). | 
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
  

#### Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App

  
    
| 
      Targeting optimization mode | 
      Available targeting setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Automatic targeting
(`targeting_optimization_mode` as `AUTOMATIC` or not specified) | 
      Audience controls 
· Location | 
      The location should match or be the subset of the targeting location of your catalog. | 
      `location_ids` or `zipcode_ids` or both | 
      Specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
     |
    
| 
      Audience controls 
· Minimum age | 
      Any of the following options:
- 18
- 25 | 
      `spc_audience_age` | 
      Any of the following values:
- `OVER_EIGHTEEN` or unspecified
- `OVER_TWENTY_FIVE` | 
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
· Custom audience 
(Optional) | 
      Enabled or disabled | 
      `audience_ids` | 
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
      Audience controls 
· Gender 
(Optional) | 
      Enabled or disabled | 
      `gender` | 
      Specify valid values or not specified | 
     |
    
| 
      Custom targeting
(`targeting_optimization_mode` as `MANUAL`) | 
      Demographics · Location | 
      Specify a valid value.
If a catalog is specified, the location should match or be the subset of the targeting location of your catalog. | 
      `location_ids` or `zipcode_ids` or both | 
      Specify a valid value.
If a catalog is specified, specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
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
· Exclude audience (Optional) | 
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
· Operating system (Optional) | 
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
· Internet service provider (Optional) | 
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
  

#### Example

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "app_id": "{{app_id}}",
    "promotion_type": "APP_IOS",
    "optimization_goal": "IN_APP_EVENT",
    "optimization_event": "LOGIN",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "location_ids": [
            "{{location_ids}}"
        ],
        "operating_systems": [
            "IOS"
        ]
    },
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_TIKTOK"
    ]
}'
(/code)
```

Response
```xcodeblock
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "app_config": [],
        "app_id": "{{app_id}}",
        "attribution_event_count": "ONCE",
        "bid_type": "BID_TYPE_NO_BID",
        "billing_event": "OCPM",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "catalog_id": "{{catalog_id}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": {{conversion_bid_price}},
        "create_time": "{{create_time}}",
        "dayparting": "{{dayparting}}",
        "deep_bid_type": "AEO",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": {{min_budget}},
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "LOGIN",
        "optimization_event_type": "STANDARD_EVENT",
        "optimization_goal": "IN_APP_EVENT",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "product_source": "CATALOG",
        "promotion_type": "APP_IOS",
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
            "brand_safety_type": "EXPANDED_INVENTORY",
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_ids}}"
            ],
            "min_ios_version": "8.0",
            "operating_systems": [
                "IOS"
            ],
            "spc_audience_age": "OVER_EIGHTEEN",
            "spending_power": "ALL"
        },
        "video_download_disabled": false,
        "view_attribution_window": "ONE_DAY"
    }
}
(/code)
```

### Create an ad

Create an ad using [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522).

  
    
| 
      Setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Ad name (Optional) | 
      By default, the system will auto-generate the ad name.
You can customize the ad name by specifying a valid ad name. | 
      `ad_name` | 
      
- To have the system auto-generate the ad name, set this field to `""`(empty string).
- To customize the ad name, specify a non-empty string value. | 
     |
    
| 
      Product source details 
· Products | 
      
- When "Use RTA to automatically select products" is enabled at the campaign level: All products
- When "Use RTA to automatically select products" is disabled, use any of the following options:All products
- Product set
- Specific products with a maximum of 20 products | 
      `product_specific_type`
`product_set_id`
`product_ids` | 
      
- When `rta_product_selection_enabled` is `true` at the campaign level: `ALL`
- When `rta_product_selection_enabled` is `false` or not specified at the campaign level, set `product_specific_type` to `ALL`, `PRODUCT_SET` or `CUSTOMIZED_PRODUCTS`.If `product_specific_type` is set to `ALL`, you don't need to specify `product_set_id` and `product_ids`.
- If `product_specific_type` is set to `PRODUCT_SET`, you need to specify `product_set_id`. `product_ids` is not needed.
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to specify a maximum of 20 available catalog products through `product_ids`. `product_set_id` is not needed.To retrieve the product ID (`product_id`) of each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). | 
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
- `BC_AUTH_TT`
**Note**:
- For non-Spark Ads identities (`CUSTOMIZED_USER`), specify values to `identity_type` and `identity_id` in the `ad_configuration` object.
- For Spark Ads identities, specify values to `identity_type` and `identity_id` within the `creative_info` object.
 | 
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
            Creative assets 
· Autoselect from catalog | 
            Any of the following options:
- Enabled (Recommended)Images and videos in your catalog will be used to automatically generate optimized Catalog Ads in all formats for your products.
- Multiple ad format combinations are supported. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App](#item-link-Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App).
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
            
- To enable auto-selection of catalog creatives, set `catalog_creative_toggle` to `true`, specify a valid value for `ad_format` in each `creative_info` object, and specify a piece of music via `music_info`. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App](#item-link-Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App).

**Note**: `music_info` is required when `catalog_creative_toggle` is `true`.
- To disable auto-selection of catalog creatives, set `catalog_creative_toggle` to `false`.For a single ad, you can include one to **50 ad creatives** that can consist of the following types:Videos
- TikTok video posts
- TikTok photo posts
- Carousel
- For each creative, specify the corresponding value for `ad_format` in each `creative_info` object.
- To learn about configurations of the available ad creative combinations based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).  | 
         |
    
| 
      Call to action | 
      Dynamic | 
      `call_to_action_id` | 
      Specify a valid value | 
     |
    
| 
      `call_to_action_list` | 
      Not specified | 
     |
    
| 
      Interactive add-ons (Optional) (When the ad creatives include videos or video posts ) | 
      Disabled or enabled with up to one add-on in any of the following types:
- Display Card
- Countdown Sticker
- Gift Code Sticker | 
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
      Destination | 
      
- When the promoted App is an Android App: Google Play
- When the App is an iOS App: App Store | 
      `landing_page_url_list`
`page_list` | 
      
- When `promotion_type` at the ad group level is `APP_ANDROID`, you can only set the Destination as Google Play.Do not specify `landing_page_url_list` and `page_list`.
- When `promotion_type` at the ad group level is `APP_IOS`, you can only set the Destination as App Store.Do not specify `landing_page_url_list` and `page_list`. | 
     |
    
| 
      Deferred deeplink (Optional) (When Destination is Google Play/App Store) | 
      Disabled or enabled with a valid deeplink.
A deferred deeplink sends the user to a specific page when they open your app for the first time after installing. It must be used with a third-party tracking link. | 
      `deeplink_type` | 
      Not specified or specify `DEFERRED_DEEPLINK` | 
     |
    
| 
      `deeplink` | 
      
- When `deeplink_type` is not specified:Not specified
- When `deeplink_type` is `DEFERRED_DEEPLINK`:Specify a custom deeplink | 
     |
    
| 
      Build URL parameters (Optional) | 
      
- When Deferred deeplink is disabled, this setting is not supported.
- When Deferred deeplink is enabled, you can either enable or disable this setting. | 
      `deeplink_utm_params` | 
      
- When `deeplink_type` is not specified:Not specified
- When `deeplink_type` is `DEFERRED_DEEPLINK`, use any of the following configurations :Specify a valid value or not specified
If you set `deeplink` to a URL that already includes URL parameters, you can optionally specify `deeplink_utm_params` at the same time to store the URL parameters used in the URL.
In such cases, you need to ensure that `deeplink_utm_params` exactly matches the used URL parameters. The URL parameters will not be automatically appended to the `deeplink` upon ad delivery. | 
     |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
  

#### Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App

If you enable auto-selection of catalog creatives (`catalog_creative_toggle` is `true`), the system will automatically create ads using combinations of three possible formats: catalog carousel, catalog video, and single video.

The possible ad format combinations for your Upgraded Smart+ Catalog Ads for App are illustrated in the following table.

    
        
| 
            Is the catalog carousel format available? | 
            Is the catalog video format available? | 
            Is the single video format available? | 
            Ad format combination for your Upgraded Smart+ Catalog Ads for App | 
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
    

To ensure certain ad formats are available in Upgraded Smart+ Catalog Ads for App, follow the instructions in the following table.

    
        
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
    

#### Example
**Using catalog creatives only**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
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
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "catalog_creative_info": {},
            "catalog_creative_toggle": true,
            "dark_post_status": "ON",
            "deeplink_utm_params": [],
            "fallback_type": "UNSET",
            "identity_id": "{{identity_id}}",
            "identity_type": "CUSTOMIZED_USER",
            "phone_info": {},
            "product_info": {
                "product_image_list": []
            },
            "product_specific_type": "ALL",
            "tracking_info": {
                "app_tracking_info_list": [],
                "tracking_app_id": "{{tracking_app_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}"
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
                    "material_name": "{{material_name}}",
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
        "landing_page_url_list": [],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```

**Using non-catalog creatives only**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "creative_list": [
        {
            "creative_info": {
                "ad_format": "SINGLE_VIDEO",
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "identity_type": "BC_AUTH_TT",
                "identity_id": "{{identity_id}}",
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}"
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
        "call_to_action_id": "{{call_to_action_id}}"
    }
}'
(/code)
```

Response
```xcodeblock
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "catalog_creative_info": {},
            "catalog_creative_toggle": false,
            "dark_post_status": "ON",
            "deeplink_utm_params": [],
            "fallback_type": "UNSET",
            "phone_info": {},
            "product_info": {
                "product_image_list": []
            },
            "product_specific_type": "ALL",
            "tracking_info": {
                "app_tracking_info_list": [],
                "tracking_app_id": "{{tracking_app_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}"
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
        "landing_page_url_list": [],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```

# Create Upgraded Smart+ Catalog DC Ads for App

Upgraded Smart+ Catalog DC Ads for App are Upgraded Smart+ Sales Campaigns with iOS 14 dedicated campaign setting enabled that use catalog products to deliver ads. For such campaigns, you need to set the `campaign_type` parameter to `IOS14_CAMPAIGN`.

## Prerequisite for creating Upgraded Smart+ Catalog DC Ads for App

Creating Upgraded Smart+ Catalog Ads for App requires setting up a catalog in your Business Center first.

To set up the catalog:

1. Create a catalog using [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961).

The catalog type can be any of the following:

- E-commerce
- hotel
- flight
- destination
- entertainment

2. Upload products to the catalog using [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) (JSON schema), [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) (CSV feed template), or [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377)(online data feed schedule).

3. Check the product handling results using [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889).
   
Pass in the `feed_log_id` obtained from Step 2. If the field `error_affected_products` in the response is not null, examine the issue details and return to Step 2 to reupload the product.

4. (Optional) Create a product set using [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257).
   
If you want to have products selected from a product set, creating a product set is necessary. Otherwise, you can skip this step.

5. (Optional) Invite members to Business Center and grant the admin permission using [/bc/member/invite/](https://business-api.tiktok.com/portal/docs?id=1739939455765505).
   
You can also choose `advertiser_role` that you want to assign to the members invited.

6. (Optional) Share a catalog with members and grant catalog management access using [/bc/asset/assign/](https://business-api.tiktok.com/portal/docs?id=1739438211077121).
   
Make sure to specify `CATALOG` in the `asset_type` field and `ADMIN` in the `catalog_role` field.

For all catalog APIs, see [here](https://business-api.tiktok.com/portal/docs?id=1739578477445121).

## Steps

### Create a campaign

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
      App | 
      `sales_destination` | 
      `APP` | 
     |
        
| 
            Catalog type | 
            Any of the following types:
- E-commerce
- Travel and entertainment | 
            `catalog_enabled` | 
            `true` | 
         |
        
| 
            `catalog_type` | 
            Any of the following values:
- `ECOMMERCE`
- `TRAVEL_ENTERTAINMENT` | 
         |
    
| 
      iOS 14 dedicated campaign | 
      **Enabled**

To learn about how to create Upgraded Smart+ Catalog Ads for App with iOS 14 Dedicated Campaign disabled, see [Create Upgraded Smart+ Catalog non-DC Ads for App](#item-link-Create Upgraded Smart+ Catalog non-DC Ads for App). | 
      `campaign_type` | 
      `IOS14_CAMPAIGN` | 
     |
    
| 
      App | 
      Specify a valid iOS App | 
      `app_id` | 
      Specify a valid value.
To obtain the list of Apps under your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).
For iOS Apps, the returned `platform` will be `IOS`. | 
     |
    
| 
      SKAN attribution (Optional) | 
      Disabled or enabled | 
      `disable_skan_campaign` | 
      Any of the following values:
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition).
- `false` or not specified: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.

**Note**: Disabling SKAN attribution for Dedicated Campaigns is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Use app profile page to optimize delivery | 
      Disabled | 
      `campaign_app_profile_page_state` | 
      `OFF` (or not specified) | 
     |
    
| 
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
      Special ad categories (Optional) | 
      Disabled or enabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada. | 
      `special_industries` | 
      Not specified or specify a valid value | 
     |
    
| 
      Campaign budget strategy | 
      Any of the following types:
- **Automatic campaign budget**: Your budget will be automatically allocated and optimized across ad groups. All ad groups must share the same budget and optimization settings.
- **Custom ad group budget**: Precisely control spend for each ad group, using different budget and optimization settings for each. | 
      `budget_optimize_on` | 
      
- To set an automatic campaign budget, set this field to `true` or leave it unspecified.
- To set a custom ad group budget, set this field to `false`. | 
     |
    
| 
      Campaign budget mode | 
      
- When Campaign budget strategy is Automatic campaign budget, specify any of the following modes:Daily
- Lifetime
- When Campaign budget strategy is Custom ad group budget:Disabled | 
      `budget_mode` | 
      
- When `budget_optimize_on` is `true` or not specified, use any of the following values :`BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- When `budget_optimize_on` is `false`:Not specified | 
     |
    
| 
      Automatic budget increase (when Campaign budget strategy is Automatic campaign budget and campaign budget mode is daily) | 
      Any of the following options:
- Enabled
- Disabled | 
      `budget_auto_adjust_strategy` | 
      When `budget_optimize_on` is `true` or not specified and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`:
-  To enable the setting, use the following value:`AUTO_BUDGET_INCREASE`. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- To disable the setting: Not specified
**Note**: Enabling automatic budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Campaign budget | 
      
- When Campaign budget strategy is Automatic campaign budget, specify a valid budget
- When Campaign budget strategy is Custom ad group budget:Disabled | 
      `budget` | 
      
- When `budget_optimize_on` is `true` or not specified, specify a valid value.
- When `budget_optimize_on` is `false`:Not specified | 
     |
    
| 
      Realtime API (RTA) (Optional) | 
      Enabled or disabled

**Note**: The available placements at the ad group level might vary based on your RTA setting. | 
      `rta_id` | 
      Specify one of the RTA IDs associated with your ad account.

To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative.

**Note**: The available placement setting (`placement_type` and `placements`) at the ad group level might vary based on your `rta_id` configuration. | 
     |
    
| 
      Use RTA to automatically select products (Optional) | 
      
- When RTA is disabled, this setting is not supported.
- When RTA is enabled, you can either enable or disable this setting. | 
      `rta_product_selection_enabled` | 
      
- When `rta_id` is not specified:`false` or not specified
- When `rta_id` is specified, use any of the following configurations :`true`
- `false` or not specified | 
     |
    
| 
      Use RTA bid (Optional) | 
      
- When RTA is disabled, this setting is not supported.
- When RTA is enabled, you can either enable or disable this setting. | 
      `rta_bid_enabled` | 
      
- When `rta_id` is not specified:`false` or not specified
- When `rta_id` is specified, use any of the following configurations :`true`
- `false` or not specified | 
     |
  

#### Example
**Creating a CBO campaign**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "APP",
    "catalog_enabled": true,
    "catalog_type": "ECOMMERCE",
    "campaign_type": "IOS14_CAMPAIGN",
    "app_id": "{{app_id}}",
    "campaign_name": "{{campaign_name}}",
    "budget": {{budget}}
}'
(/code)
```

Response
```xcodeblock
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "advertiser_id": "{{advertiser_id}}",
        "app_id": "{{app_id}}",
        "bid_align_type": "SAN",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "budget_optimize_on": true,
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "campaign_type": "IOS14_CAMPAIGN",
        "catalog_enabled": true,
        "catalog_type": "ECOMMERCE",
        "create_time": "{{create_time}}",
        "disable_skan_campaign": false,
        "is_advanced_dedicated_campaign": true,
        "is_promotional_campaign": false,
        "modify_time": "{{modify_time}}",
        "objective_type": "WEB_CONVERSIONS",
        "operation_status": "ENABLE",
        "sales_destination": "APP",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "smart_plus_adgroup_mode": "MULTIPLE"
    }
}
(/code)
```

### Create an ad group

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

**Note**:
- When RTA is disabled at the campaign level, you can specify any of the following catalog types:E-commerce
- hotel
- flight
- destination
- entertainment
- When RTA is enabled at the campaign level, you can specify any of the following catalog types:E-commerce
- entertainment
 | 
      `catalog_id`
`catalog_authorized_bc_id` | 
      Specify valid values.
The catalog (`catalog_id`) needs to have at least two approved products. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 2.

- To obtain catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610).
- To learn about how to create a catalog, see [Prerequisite for creating Upgraded Smart+ Catalog DC Ads for App](#item-link-Prerequisite for creating Upgraded Smart+ Catalog DC Ads for App).

**Note**:
- When `rta_id` is not specified at the campaign level, the `catalog_type` of the catalog can be any of the following:`ECOM`
- `HOTEL`
- `FLIGHT`
- `DESTINATION`
- `ENTERTAINMENT`
- When `rta_id` is specified at the campaign level, the `catalog_type` of the catalog can be any of the following:`ECOM`
- `ENTERTAINMENT`
 | 
     |
    
| 
      Optimization and bidding 
· App | 
      iOS App

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
      `promotion_type` | 
      `APP_IOS`

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding 
· Goal | 
      Any of the following types:
- ClickWe'll deliver your ads to the people most likely to click on your ad.
- InstallWe'll show your ads to the people who are most likely to install your app.
- In-app eventWe'll show your ads to the people who are most likely to perform certain actions within your app.
- ValueWe'll deliver your ads to users that are more likely to make a purchase in order to maximize your total purchase value.

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
      `optimization_goal` | 
      Any of the following values:
- `CLICK`
- `INSTALL` (with `optimization_event` as `ACTIVE`)To use `INSTALL`, you need to ensure third-party tracking has been set up for the selected App.To check whether third-party tracking (`tracking_url`) has been configured for an App, use [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297).
- To add third-party tracking for an existing App, use [/app/update/](https://business-api.tiktok.com/portal/docs?id=1740859300069378). To learn about how to obtain tracking links from a third-party partner, see [Mobile Measurement Partner Tracking](https://ads.tiktok.com/help/article/mobile-measurement-partner-mmp-tracking).
- `IN_APP_EVENT` (with `optimization_event` specified)To use `IN_APP_EVENT`, you need to ensure the specified event (`optimization_event`) is available for the selected App.
- `VALUE` (with `optimization_event` specified)When you set this field to `VALUE`, specify the placement parameters (`placement_type` or both `placement_type` and `placements`) at the same time.
- Learn more about [Value-Based Optimization](https://business-api.tiktok.com/portal/docs?id=1739381743067137).
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding 
· Select in-app event (when Goal is In-app event) | 
      Any of the following types:
- Standard Event
- Custom Conversion
**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign. | 
      `optimization_event`
`custom_conversion_id` | 
      When `optimization_goal` is `IN_APP_EVENT`, specify any of the following:
- A Standard Event through`optimization_event`
- A Custom Conversion along with the associated conversion event through `custom_conversion_id` and `optimization_event`

- To obtain the available optimization events (`optimization_event`) for the App, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977).
- To obtain the list of Custom Conversions associated with an App, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673).To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation.
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, the `optimization_event` and `custom_conversion_id`, if specified, must be the same for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding 
· Bid Strategy, (Optional) Target CPA, and (Optional) Target ROAS | 
      
- If Goal is Click, Install, or In-app event, the strategy can only be Maximum Delivery or Cost Cap.For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Value, the strategy can be Highest value or Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.
**Note**:
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      
- If `optimization_goal` is `CLICK`, `INSTALL`, or `IN_APP_EVENT`:Set `bid_type` to `BID_TYPE_CUSTOM` (Cost Cap) or `BID_TYPE_NO_BID` (Maximum Delivery). Do not specify `deep_bid_type` and `roas_bid`.If `optimization_goal` is `INSTALL` or `IN_APP_EVENT`and `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `CLICK` and `bid_type` is `BID_TYPE_CUSTOM`, specify `bid_price` at the same time.
- If `optimization_goal` is `VALUE`:Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
**Note**:
- The `bid_type` must be the same across ad groups within the same campaign.
- When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`conversion_bid_price`
- `bid_price`
- `deep_bid_type`
- `roas_bid`
- You can only set `bid_type` to `BID_TYPE_CUSTOM` or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
     |
    
| 
      Optimization and bidding 
· Billing event | 
      
- If Goal is Click, the billing event should be CPC.
- If Goal is Install, In-app event, or Value, the billing event should be oCPM.

**Note**:
- When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign. | 
      `billing_event` | 
      
- If `optimization_goal` is `CLICK`, set this field to `CPC`.
- If `optimization_goal` is `INSTALL`, `IN_APP_EVENT`, or `VALUE`, set this field to `OCPM`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `billing_event`for ad groups within the same campaign. | 
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
      
- When you select an automatic campaign budget mode:The ad group budget is disabled. The campaign-level budget will be used as the ad group budget.
- When you select a custom ad group budget strategy, you can use any of the following ad group budget modes:Lifetime
- Daily
**Note**:
- The ad group budget mode, if specified, must be the same across ad groups within the same campaign. | 
      `budget_mode`
`budget` | 
      
- When `budget_optimize_on` is `true` at the campaign level, `budget_mode` and `budget`are not supported.
- When `budget_optimize_on` is `false` at the campaign level:Set `budget_mode` to `BUDGET_MODE_TOTAL` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`

**Note**:
- The `budget_mode`, if specified, must be the same across ad groups within the same campaign. | 
     |
    
| 
      Budget and schedule 
· Automatic budget increase (when Goal is Value) | 
      Enabled or disabled

To enable this setting, the following conditions should be met:
- At the campaign level: CBO is disabled.
- At the ad group level:Ad group budget is Daily
- Goal is Value
- Bid Strategy is Target ROAS
- Time window of the bid strategy is Day 0 ROAS | 
      `budget_auto_adjust_strategy` | 
      Use any of the following values:
- `AUTO_BUDGET_INCREASE`: To enable automatic budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable automatic budget increase.
You can only set this field to `AUTO_BUDGET_INCREASE` when the following conditions are all met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level:`budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `optimization_goal` is `VALUE`.
- `deep_bid_type` is `VO_MIN_ROAS`.
- `vbo_window` is `ZERO_DAY`.
**Note**: Enabling automatic budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
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
- At the ad group level, a daily ad group budget is set. | 
      `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
      
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`.
**Note**: You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
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
      Audience targeting | 
      **Prospect**
- Find new customers who want to install your app | 
      `app_targeting_type` | 
      `PROSPECT` | 
     |
    
| 
      Audience targeting optimization mode | 
      Any of the following modes:
- **Automatic targeting**You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
- **Custom targeting**You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App). | 
      `targeting_optimization_mode` | 
      Any of the following values:
- `AUTOMATIC`
- `MANUAL`To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Catalog Ads for App). | 
     |
    
| 
      Placements and brand safety 
· Placement | 
      TikTok | 
      `placement_type` | 
      `PLACEMENT_TYPE_NORMAL` | 
     |
    
| 
      `placements` | 
      `["PLACEMENT_TIKTOK"]` | 
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
  

#### Example

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "app_id": "{{app_id}}",
    "promotion_type": "APP_IOS",
    "optimization_goal": "IN_APP_EVENT",
    "optimization_event": "LOGIN",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "app_targeting_type": "PROSPECT",
        "location_ids": [
            "{{location_ids}}"
        ],
        "operating_systems": [
            "IOS"
        ]
    },
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_TIKTOK"
    ]
}'
(/code)
```

Response
```xcodeblock
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "app_config": [],
        "app_id": "{{app_id}}",
        "attribution_event_count": "ONCE",
        "bid_type": "BID_TYPE_NO_BID",
        "billing_event": "OCPM",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "catalog_id": "{{catalog_id}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": {{conversion_bid_price}},
        "create_time": "{{create_time}}",
        "dayparting": "{{dayparting}}",
        "deep_bid_type": "AEO",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": {{min_budget}},
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "LOGIN",
        "optimization_event_type": "STANDARD_EVENT",
        "optimization_goal": "IN_APP_EVENT",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "product_source": "CATALOG",
        "promotion_type": "APP_IOS",
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
            "brand_safety_type": "EXPANDED_INVENTORY",
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_ids}}"
            ],
            "min_ios_version": "14.0",
            "operating_systems": [
                "IOS"
            ],
            "spc_audience_age": "OVER_EIGHTEEN",
            "spending_power": "ALL"
        },
        "video_download_disabled": false,
        "view_attribution_window": "ONE_DAY"
    }
}
(/code)
```

### Create an ad

Create an ad using [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522).

  
    
| 
      Setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Ad name (Optional) | 
      By default, the system will auto-generate the ad name.
You can customize the ad name by specifying a valid ad name. | 
      `ad_name` | 
      
- To have the system auto-generate the ad name, set this field to `""`(empty string).
- To customize the ad name, specify a non-empty string value. | 
     |
    
| 
      Product source details 
· Products | 
      
- When "Use RTA to automatically select products" is enabled at the campaign level: All products
- When "Use RTA to automatically select products" is disabled, use any of the following options:All products
- Product set
- Specific products with a maximum of 20 products | 
      `product_specific_type`
`product_set_id`
`product_ids` | 
      
- When `rta_product_selection_enabled` is `true` at the campaign level: `ALL`
- When `rta_product_selection_enabled` is `false` or not specified at the campaign level, set `product_specific_type` to `ALL`, `PRODUCT_SET` or `CUSTOMIZED_PRODUCTS`.If `product_specific_type` is set to `ALL`, you don't need to specify `product_set_id` and `product_ids`.
- If `product_specific_type` is set to `PRODUCT_SET`, you need to specify `product_set_id`. `product_ids` is not needed.
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to specify a maximum of 20 available catalog products through `product_ids`. `product_set_id` is not needed.To retrieve the product ID (`product_id`) of each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). | 
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
- `BC_AUTH_TT`
**Note**:
- For non-Spark Ads identities (`CUSTOMIZED_USER`), specify values to `identity_type` and `identity_id` in the `ad_configuration` object.
- For Spark Ads identities, specify values to `identity_type` and `identity_id` within the `creative_info` object.
 | 
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
            Creative assets 
· Autoselect from catalog | 
            Any of the following options:
- Enabled (Recommended)Images and videos in your catalog will be used to automatically generate optimized Catalog Ads in all formats for your products.
- Multiple ad format combinations are supported. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App](#item-link-Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App).
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
            
- To enable auto-selection of catalog creatives, set `catalog_creative_toggle` to `true`, specify a valid value for `ad_format` in each `creative_info` object, and specify a piece of music via `music_info`. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App](#item-link-Customize the ad format combinations in Upgraded Smart+ Catalog Ads for App).

**Note**: `music_info` is required when `catalog_creative_toggle` is `true`.
- To disable auto-selection of catalog creatives, set `catalog_creative_toggle` to `false`.For a single ad, you can include one to **50 ad creatives** that can consist of the following types:Videos
- TikTok video posts
- TikTok photo posts
- Carousel
- For each creative, specify the corresponding value for `ad_format` in each `creative_info` object.
- To learn about configurations of the available ad creative combinations based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).  | 
         |
    
| 
      Call to action | 
      Dynamic | 
      `call_to_action_id` | 
      Specify a valid value | 
     |
    
| 
      `call_to_action_list` | 
      Not specified | 
     |
    
| 
      Interactive add-ons (Optional) (When the ad creatives include videos or video posts ) | 
      Disabled or enabled with up to one add-on in any of the following types:
- Display Card
- Countdown Sticker
- Gift Code Sticker | 
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
      Destination | 
      
- When the promoted App is an Android App: Google Play
- When the App is an iOS App: App Store | 
      `landing_page_url_list`
`page_list` | 
      
- When `promotion_type` at the ad group level is `APP_ANDROID`, you can only set the Destination as Google Play.Do not specify `landing_page_url_list` and `page_list`.
- When `promotion_type` at the ad group level is `APP_IOS`, you can only set the Destination as App Store.Do not specify `landing_page_url_list` and `page_list`. | 
     |
    
| 
      Deferred deeplink (When Destination is Google Play/App Store) | 
      Disabled | 
      `deeplink_type` | 
      Not specified | 
     |
    
| 
      `deeplink` | 
      Not specified | 
     |
    
| 
      Build URL parameters | 
      Disabled | 
      `deeplink_utm_params` | 
      Not specified | 
     |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
  

#### Example
**Using catalog creatives only**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
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
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "catalog_creative_info": {},
            "catalog_creative_toggle": true,
            "dark_post_status": "ON",
            "deeplink_utm_params": [],
            "fallback_type": "UNSET",
            "identity_id": "{{identity_id}}",
            "identity_type": "CUSTOMIZED_USER",
            "phone_info": {},
            "product_info": {
                "product_image_list": []
            },
            "product_specific_type": "ALL",
            "tracking_info": {
                "app_tracking_info_list": [],
                "tracking_app_id": "{{tracking_app_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}"
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
                    "material_name": "{{material_name}}",
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
        "landing_page_url_list": [],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```

**Using non-catalog creatives only**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "creative_list": [
        {
            "creative_info": {
                "ad_format": "SINGLE_VIDEO",
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "identity_type": "BC_AUTH_TT",
                "identity_id": "{{identity_id}}",
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}"
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
        "call_to_action_id": "{{call_to_action_id}}"
    }
}'
(/code)
```

Response
```xcodeblock
(code json)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "catalog_creative_info": {},
            "catalog_creative_toggle": false,
            "dark_post_status": "ON",
            "deeplink_utm_params": [],
            "fallback_type": "UNSET",
            "phone_info": {},
            "product_info": {
                "product_image_list": []
            },
            "product_specific_type": "ALL",
            "tracking_info": {
                "app_tracking_info_list": [],
                "tracking_app_id": "{{tracking_app_id}}",
                "tracking_pixel_id": "{{tracking_pixel_id}}"
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
        "landing_page_url_list": [],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```
