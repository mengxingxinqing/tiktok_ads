# Create Upgraded Smart+ E-commerce Catalog Ads

**Doc ID**: 1847302895272962
**Path**: Use Cases/Campaign creation/Create an Upgraded Smart+ Campaign/Create Upgraded Smart+ Web Campaigns/Create Upgraded Smart+ E-commerce Catalog Ads

---

Upgraded Smart+ E-commerce Catalog Ads are Upgraded Smart+ Web Campaigns that use E-commerce catalog products to deliver ads. 

For such campaigns, you need to set `catalog_enabled` to `true` and `catalog_type` to `ECOMMERCE` at the campaign level. By utilizing Upgraded Smart+ E-commerce Catalog Ads, you can automatically generate ads in diverse formats such as catalog video, catalog carousel, and single video.

# Prerequisite
Creating Upgraded Smart+ E-commerce Catalog Ads requires setting up an E-commerce catalog in your Business Center first.

To set up the catalog:

1. Create an **E-commerce** catalog using [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961).
2. Upload products to the catalog using [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) (JSON schema), [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) (CSV feed template), or [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377)(online data feed schedule).
3. Check the product handling results.
	- For CSV feed and JSON schema, use [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889).
		- Pass in the `feed_log_id` obtained from Step 2. If the field `error_affected_products` in the response is not null, examine the issue details and return to Step 2 to reupload the product.
	- For online feed, use [/catalog/feed/log/](https://business-api.tiktok.com/portal/docs?id=1740665225631810).
		- Pass in the `feed_id` obtained from Step 2. If the field `error_count` in the response is not 0, examine your online feed and return to Step 2 to reupload the product.
4. (Optional) Create an E-commerce product set using [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257).

If you want to have products selected from a product set, creating a product set is necessary. Otherwise, you can skip this step.
5. (Optional) Invite members to Business Center and grant the admin permission using [/bc/member/invite/](https://business-api.tiktok.com/portal/docs?id=1739939455765505).

You can also choose `advertiser_role` that you want to assign to the members invited.
6. (Optional) Share a catalog with members and grant catalog management access using [/bc/asset/assign/](https://business-api.tiktok.com/portal/docs?id=1739438211077121).

Make sure to specify `CATALOG` in the `asset_type` field and `ADMIN` in the `catalog_role` field.

For all catalog APIs, see [here](https://business-api.tiktok.com/portal/docs?id=1739578477445121).

# Steps
## Create a campaign
Create a campaign using [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706) 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706).

  
   
| 
     **Setting** | 
     **Requirement** | 
     **Parameter** | 
     **How to configure the parameter** | 
    |
  
  
   
| 
     Advertising objective | 
     Sales | 
     `objective_type` | 
     `WEB_CONVERSIONS` | 
    |
   
| 
     Sales destination | 
     Website | 
     `sales_destination` | 
     `WEBSITE` | 
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
     `catalog_enabled` | 
     `true` | 
    |
   
| 
     Catalog type | 
     **E-commerce** | 
     `catalog_type` | 
     `ECOMMERCE` | 
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
**Creating a CBO campaign**

Request
```xcodeblock
(code json)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "WEBSITE",
    "catalog_enabled": true,
    "catalog_type": "ECOMMERCE",
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
        "modify_time": "{{modify_time}}",
        "objective_type": "WEB_CONVERSIONS",
        "operation_status": "ENABLE",
        "sales_destination": "WEBSITE",
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
     **Setting** | 
     **Requirement** | 
     **Parameter** | 
     **How to configure the parameter** | 
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
      Specify an** E-commerce catalog with at least two approved products** | 
      `catalog_id`
`catalog_authorized_bc_id` | 
      Specify valid values.

The catalog (`catalog_id`) needs to have at least two approved products. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 2.
- To obtain E-commerce catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610). For E-commerce catalogs, the `catalog_type` should be `ECOM`.
- To learn about how to create an E-commerce catalog, see [Prerequisite](#item-link-Prerequisite). | 
     |
    
| 
      Optimization and bidding
· Location | 
      Website | 
      `promotion_type` | 
      `WEBSITE` | 
     |
    
| 
      `promotion_target_type` | 
      Not specified | 
     |
    
| 
      Optimization and bidding
· Goal | 
      Any of the following types:
- Click
- Conversion
- Landing page view
- Value
**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
      `optimization_goal` | 
      Any of the following values:
- `CLICK`
- `CONVERT`
- `TRAFFIC_LANDING_PAGE_VIEW`
- `VALUE`
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding
· Event 
  · Data connection | 
      
- When Goal is Conversion or Value, specify a valid Pixel.
- When Goal is Click or Landing page view, Pixel is not supported. | 
      `pixel_id` | 
      
- Required when `optimization_goal` is set to `CONVERT` or `VALUE`.To obtain the list of Pixels within your ad account, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- Not supported when `optimization_goal` is set to `CLICK` or `TRAFFIC_LANDING_PAGE_VIEW`. | 
     |
    
| 
      Optimization and bidding
· Event 
  · Optimization event | 
      
- Required when Goal is Conversion or Value.When Goal is Value, specify the optimization event as Complete Payment.
- When Goal is Conversion, specify any of the following:Standard Event
- Custom Conversion
- Not supported when Goal is Click or Landing page view.
**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign. | 
      `optimization_event`
`custom_conversion_id` | 
      
- Required when `optimization_goal` is set to `CONVERT` or `VALUE`.When `optimization_goal` is set to `VALUE`, set this field to `SHOPPING`.
- When `optimization_goal` is set to `CONVERT`, specify any of the following:A Standard Event through `optimization_event` .To obtain the optimization events that have been configured for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
See [Conversion events - Pixel events](https://business-api.tiktok.com/portal/docs?id=1739361474981889#item-link-Pixel%20events) for enum values.
- A Custom Conversion along with the associated conversion event through `custom_conversion_id` and `optimization_event`.To obtain the list of Custom Conversions associated with a Pixel, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673).To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation. 
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.
- Not supported when `optimization_goal` is set to `CLICK`.
- Can be omitted when `optimization_goal` is set to `TRAFFIC_LANDING_PAGE_VIEW`. Then `optimization_event` will default to `LANDING_PAGE_VIEW`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, the `optimization_event` and `custom_conversion_id`, if specified, must be the same for ad groups within the same campaign. | 
     |
    
| 
      Optimization and bidding
· Bid Strategy, 
(Optional) Target CPA, 
and (Optional) Target ROAS | 
      
- If Goal is Click or Conversion, the strategy can be Maximum Delivery or Cost Cap.For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Landing page view, the strategy can only be Maximum Delivery.
- If Goal is Value, the strategy can be Highest value or Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.
**Note**:
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA  or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily. | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      
- If `optimization_goal` is `CLICK` or `CONVERT`, set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`. Do not specify `deep_bid_type` and `roas_bid`.If `optimization_goal` is `CONVERT` and `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `CLICK`, and `bid_type` is `BID_TYPE_CUSTOM`, specify `bid_price` at the same time.
- If `optimization_goal` is `TRAFFIC_LANDING_PAGE_VIEW`, set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `deep_bid_type` and `roas_bid`.
- If `optimization_goal` is `VALUE`, set `deep_bid_type` to `VO_HIGHEST_VALUE` or `VO_MIN_ROAS`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.If `deep_bid_type` is `VO_MIN_ROAS`, specify  `roas_bid` at the same time.
**Note**:
- The `bid_type` must be the same across ad groups within the same campaign.
-  When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`conversion_bid_price`
- `bid_price`
- `deep_bid_type`
- `roas_bid`
- You can only set `bid_type` to `BID_TYPE_CUSTOM`  or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
     |
    
| 
      Optimization and bidding
· Attribution settings | 
      Select from the supported attribution setting options for the specific scenario. | 
      
- `click_attribution_window`
- `view_attribution_window`
- `engaged_view_attribution_window`
- `attribution_event_count` | 
      To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - Website conversions](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-Website%20conversions). | 
     |
    
| 
      Optimization and bidding
· Billing event | 
      
- If Goal is Click, the billing event should be CPC.
- If Goal is Conversion, Landing page view, or Value, the billing event should be oCPM.
**Note**:
- When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign. | 
      `billing_event` | 
      
- If `optimization_goal` is `CLICK`, set this field to `CPC`.
- If `optimization_goal` is `CONVERT`, `TRAFFIC_LANDING_PAGE_VIEW`, or `VALUE`, set this field to `OCPM`.
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
- At the ad group level, a daily ad group budget is set. | 
      `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
      
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`.
**Note**: You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`  | 
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
- **Custom targeting**You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes](https://business-api.tiktok.com/portal/docs?id=1847839827327106). | 
      `targeting_optimization_mode` | 
      Any of the following values:
- `AUTOMATIC`
- `MANUAL`To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes](https://business-api.tiktok.com/portal/docs?id=1847839827327106). | 
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
      These settings only apply to **TikTok in-feed** and **search feed** ads. Any previous account-level settings in the brand safety hub will apply to your campaign. | 
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
  

### Example
Request
```xcodeblock
(code json)
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
    "promotion_type": "WEBSITE",
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
        "location_ids": ["1562822"]
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
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "attribution_event_count": "EVERY",
        "bid_type": "BID_TYPE_CUSTOM",
        "billing_event": "OCPM",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "catalog_id": "{{catalog_id}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": {{conversion_bid_price}},
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111", 
        "modify_time": "{{modify_time}}",
        "optimization_event": "ADD_BILLING",
        "optimization_goal": "CONVERT",
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
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "brand_safety_type": "EXPANDED_INVENTORY",
            "gender": "GENDER_UNLIMITED",
            "location_ids": ["1562822"],
            "spc_audience_age": "OVER_EIGHTEEN"
        },
        "video_download_disabled": false,
        "view_attribution_window": "ONE_DAY"
    }
}
(/code)
```

## Create an ad
Create an ad using [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522).

  
    
| 
     **Setting** | 
     **Requirement** | 
     **Parameter** | 
     **How to configure the parameter** | 
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
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to specify a maximum of 20 available E-commerce catalog products through `product_ids`. `product_set_id` is not needed.To retrieve the product ID (`product_id`) of each E-commerce catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402).
**Note**: To determine whether an E-commerce catalog product is available for use in ads, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). If the returned `ad_creation_eligible` for the product is `AVAILABLE`, you can use the product in ads. | 
     |
    
| 
      Destination URL | 
      Enabled | 
      `landing_page_url_list` | 
      Specify a valid URL.
Users will be directed to your product links, TikTok Instant Page, or the specified link depending on where they’re most likely to convert. | 
     |
    
| 
      `page_list` | 
      Not specified | 
     |
    
| 
      UTM parameters
(Optional) | 
      Enabled or disabled | 
      `utm_params` | 
      Specify valid values or not specified
If you set `landing_page_url_list` to a URL that already includes URL parameters, you can optionally specify `utm_params` at the same time to store the URL parameters used in the URL.
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
- `BC_AUTH_TT`
**Note**:
- For non-Spark Ads identities (`CUSTOMIZED_USER`), specify values to `identity_type` and `identity_id` in the `ad_configuration` object.
- For Spark Ads identities, specify values to `identity_type` and `identity_id` within the `creative_info` object. | 
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
- Multiple ad format combinations are supported. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ E-commerce Catalog Ads](#item-link-Customize the ad format combinations in Upgraded Smart+ E-commerce Catalog Ads).
- DisabledImages and videos in your catalog will not be used to automatically generate optimized Catalog Ads in all formats for your products.The system will automatically create single video ads using your specified content.
- Requirements:When using a non-Spark Ad identity:Specify 1-50 videos with cover images
- Specify 1-5 ad texts
- When using a Spark Ad identity:1-50 TikTok video posts
- **Note**: Not using a catalog for creatives might restrict your ad performance potential. | 
      `catalog_creative_toggle`
`video_info`
`image_info`
`music_info`
`ad_text_list`
`tiktok_item_id`
`ad_format` | 
      
- To enable auto-selection of catalog creatives, set `catalog_creative_toggle` to `true`, specify a valid value for `ad_format` in each `creative_info` object, and specify a piece of music via `music_info`. For detailed configuration options and requirements, see [Customize the ad format combinations in Upgraded Smart+ E-commerce Catalog Ads](#item-link-Customize the ad format combinations in Upgraded Smart+ E-commerce Catalog Ads).
- **Note**: `music_info` is required when `catalog_creative_toggle` is `true`.
- To disable auto-selection of catalog creatives, set `catalog_creative_toggle` to `false`, and specify any of the following:If `identity_type` in the `ad_configuration` object is `CUSTOMIZED_USER`:one to 50 videos (`video_info`) with cover images (`image_info`) and one to five ad texts (`ad_text_list`).
- set `ad_format` to `SINGLE_VIDEO`
- If `identity_type` within the `creative_info` object is `AUTH_CODE`, `TT_USER` or `BC_AUTH_TT`:one to 50 TikTok video posts through `tiktok_item_id`. Do not pass `video_info`, `image_info`, and `ad_text_list`.
- set `ad_format` to `SINGLE_VIDEO` | 
     |
        
| 
            Creative assets
· Catalog creative settings | 
            Disabled or enabled with one to three of the following types:
- **Video**
- **Image**
- **Video templates** | 
            `catalog_creative_toggle`
`catalog_media_settings` | 
            
- To disable catalog creative settings:Set `catalog_creative_toggle` to `false`.
- Leave `catalog_media_settings` unspecified.
- To enable catalog creative settings:Set `catalog_creative_toggle` to `true`.
- Provide one to three of the following values in `catalog_media_settings`:`VIDEO`
- `IMAGE`
- `TEMPLATE_VIDEO` | 
         |
        
| 
            When you enable **Video templates,** select one of the following video template settings:
- All video templates and video URLs
- A specific video template | 
            `catalog_template_video_id` | 
            When `TEMPLATE_VIDEO` is included in the `catalog_media_settings` value:
- To select the "All video templates and video URLs" option, leave this field unspecified.
- To select a specific video template, specify a valid value. | 
         |
    
| 
      Catalog product information
(Optional) | 
      Disabled | 
      N/A | 
      N/A | 
     |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
    
| 
      Call to action | 
      Any of the following options:
- Dynamic
- Standard
**Note**: When you use a Spark Ads identity, you can only use dynamic call to action. | 
      `call_to_action_id`
`call_to_action_list` | 
      
- To use dynamic call to action, specify `call_to_action_id`.
- To use standard call to action, specify `call_to_action_list`.
**Note**: If you set `identity_type` within the `creative_info` object to `TT_USER`, `BC_AUTH_TT`, or `AUTH_CODE`, `call_to_action_id` is required. | 
     |
    
| 
      Interactive add-ons | 
      Disabled | 
      `interactive_add_on_list` | 
      Not specified | 
     |
    
| 
      Tracking
· TikTok events tracking
  · App events
 (Optional) | 
      Enabled or disabled | 
      `tracking_app_id` | 
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
  

### Customize the ad format combinations in Upgraded Smart+ E-commerce Catalog Ads
If you enable auto-selection of catalog creatives (`catalog_creative_toggle` is `true`), the system will automatically create ads using combinations of three possible formats: catalog carousel, catalog video, and single video.

The possible ad format combinations for your Upgraded Smart+ E-commerce Catalog Ads are illustrated in the following table.

  
    
| 
      **Is the catalog carousel format available?** | 
      **Is the catalog video format available?** | 
      **Is the single video format available?** | 
      **Ad format combination for your Upgraded Smart+ E-commerce Catalog Ads** | 
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
  

To ensure certain ad formats are available in Upgraded Smart+ E-commerce Catalog Ads, follow the instructions in the following table.

    
        
| 
            **Ad format** | 
            **Ad format description** | 
            **How to ensure the ad format is available** | 
            **How to configure the parameters** | 
         |
    
    
        
| 
            catalog carousel | 
            Display 2–20 products in a slideshow format. This format will showcase product images of up to 20 products from your catalog at a time. | 
            Enable "Image" in your catalog creative settings, allowing the system to use images from your catalogs in the ad. | 
            Ensure `IMAGE` is included in the `catalog_media_settings` value. | 
         |
        
| 
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

**Note**: To obtain a valid music ID, you can use any of the following methods:

- Filter the pieces of music for Catalog Carousel Ads under an ad account by specifying `music_scene` as `CATALOG_CAROUSEL` in [/file/music/get/](https://business-api.tiktok.com/portal/docs?id=1740053909509122).
- Upload a piece of customized music for Catalog Carousel Ads to an ad account by using any of the following methods:Specify `music_scene` as `CATALOG_CAROUSEL` and pass `music_file` and `music_signature` in [/file/music/upload/](https://business-api.tiktok.com/portal/docs?id=1740052650395650).
- Specify `music_scene` as `CATALOG_CAROUSEL`, `upload_type` as `UPLOAD_BY_FILE_ID`, and pass `file_id` to [/file/music/upload/](https://business-api.tiktok.com/portal/docs?id=1740052650395650). | 
         |
        
| 
            catalog video | 
            Generate a dynamic video based on information from the product catalog | 
            Enable "Video templates" in your catalog creative settings, allowing the system to use video templates from your catalogs in the ad. | 
            Ensure `TEMPLATE_VIDEO` is included in the `catalog_media_settings` value. | 
         |
        
| 
            The catalog must have at least one video template.
- If you select a video template, the video template will be used to automatically generate the catalog video for each catalog product.
- If you don't select the video template, the system will automatically select one of your video templates for each catalog product to generate the corresponding catalog video.  | 
            Ensure that at least one video template is bound to your catalog (`catalog_id`).
- To ensure that at least one video template (video package) is bound to your catalog, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073).To learn about how to create video templates on TikTok Ads Manager, see [How to create video packages in a Catalog](https://ads.tiktok.com/help/article/how-to-create-video-packages-in-a-catalog).
- To retrieve video templates for your catalog via API, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073).

- If `catalog_template_video_id` is specified, the specified video template will be used to automatically generate the catalog video for each catalog product.
- If `catalog_template_video_id` is not specified, the system will automatically select one of your video templates for each catalog product to generate the corresponding catalog video. When a product has a video URL, that video will be used instead. | 
         |
        
| 
            Use videos from your catalog to promote your products. | 
            Enable "Video" in your catalog creative settings, allowing the system to use videos from your catalogs in the ad. | 
            Ensure `VIDEO` is included in the `catalog_media_settings` value. | 
         |
        
| 
            You need to configure a video URL for each catalog product. | 
            Ensure that a video URL (`video_url`) has been configured for each catalog product.
- To ensure a video URL has been configured for each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) and check the returned `video_url`.
- If you want to add video URLs for your catalog products, use [/catalog/product/update/](https://business-api.tiktok.com/portal/docs?id=1740562287852546). | 
         |
        
| 
            single video | 
            Use specified video creatives to promote your products. | 
            Specify additional videos | 
            Specify additional videos via `video_info` and cover images via `image_info`. | 
         |
    

### Example
Request
```xcodeblock
(code json)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
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
                "ad_format":"CATALOG_CAROUSEL",
                "music_info": {
                    "music_id": "{{music_id}}"
                }
            }
        },
        {
            "creative_info": {
                "ad_format":"SINGLE_VIDEO",
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ]
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
        "identity_type": "CUSTOMIZED_USER",
        "identity_id": "{{identity_id}}",
        "product_specific_type": "PRODUCT_SET",
        "product_set_id": "{{product_set_id}}",
        "utm_params": [
            {
                "key": "{{key}}",
                "value": "{{value}}"
            }
        ],
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
            "catalog_creative_toggle": true,
            "identity_id": "{{identity_id}}",
            "identity_type": "CUSTOMIZED_USER",
            "product_set_id": "{{product_set_id}}",
            "product_specific_type": "PRODUCT_SET",
            "tracking_info": {},
            "utm_params": [
                {
                    "key": "{{key}}",
                    "value": "{{value}}"
                }
            ]
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
        "call_to_action_list": [],
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "creative_.list": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"SINGLE_VIDEO",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "CUSTOMIZED_USER",
                    "image_info": [
                        {
                            "web_uri": "{{web_uri}}"
                        }
                    ],
                    "material_name": "",
                    "video_info": {
                        "file_name": "",
                        "video_id": "{{video_id}}"
                    }
                },
                "material_operation_status": "ENABLE"
            },
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"CATALOG_CAROUSEL",
                    "identity_authorized_bc_id": "0",
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
        "deeplink_list": [],
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
