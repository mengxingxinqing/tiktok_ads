# Get campaigns

**Doc ID**: 1739315828649986
**Path**: API Reference/Campaign/Get campaigns

---

Use this endpoint to get all campaigns for an ad account. Optionally, you can use filters in your request to return only certain campaigns.

>**Note**
If you wish to query deleted campaigns in your request, either specify the value of `STATUS_DELETE `in the `primary_status` field or `CAMPAIGN_STATUS_DELETE` in the `secondary_status` field. Deleted data are by default not queried. 

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/campaign/get/|/v1.3/campaign/get/|
|Request parameter name|
- `create_start_time`
- `create_end_time`
-  In the `fields` field: the supported values are 
 `opt_status`
`industry_types`
`status`
- `status` |`creation_filter_start_time`
- `creation_filter_end_time`
- In the `fields` field: the supported values are renamed to
`operation_status`
 `special_industries`
`secondary_status`
- `secondary_status`|
|Request parameter data type |`advertiser_id`: number
`campaign_ids`: number[]|`advertiser_id`: string
`campaign_ids`: string[]|
|New request parameters | /  | `exclude_field_types_in_response` 
`campaign_product_source` 
`is_smart_performance_campaign` 
`optimization_goal`
`campaign_system_origins`
`buying_types`
`split_test_enabled`
`gmv_max_promotion_types`
`store_ids` 
`creative_campaign_type` 
`sales_destination`
`campaign_automation_type`|
|Response parameter name|`budget_optimize_switch`
- in the `list`object: 
`opt_status`
`campaign_app_profile_page_type`
`industry_types`
`status` 
- `status`
- `optimize_goal`|`budget_optimize_on`
- in the `list`object: 
`operation_status`
 `campaign_app_profile_page_state`
`special_industries`
`secondary_status`
- `secondary_status`
- `optimization_goal`|
|Response parameter data type|`advertiser_id`: number
`campaign_ids`: number
`budget_optimize_on`: number|`advertiser_id`: string
`campaign_ids`: string
`budget_optimize_on`: boolean|
|New response parameters | /  | `app_id`
`rf_campaign_type`
`campaign_product_source` 
`postback_window_mode`
 `is_search_campaign`
 `campaign_system_origin`
`is_advanced_dedicated_campaign`
`rta_id`
`rta_product_selection_enabled`
`disable_skan_campaign`
`bid_align_type`
`catalog_enabled`
`rta_bid_enabled`
 `virtual_objective_type`
 `sales_destination`
`po_number`
`campaign_automation_type`|
```

## Request

**Endpoint** 

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

```xtable
|Field{32%}|Data Type{13%}|Description{55%}|
|---|---|---|
|advertiser_id {Required}|string|Advertiser ID.|
|fields |string[]|Fields that you want to get. 

When not specified, all fields are returned by default. 

For allowed fields, see the fields under `list` in the [Response](#item-link-Response) section.|
| exclude_field_types_in_response| string[]|The type of fields that you want to remove from the response.

Allowed enum values: `NULL_FIELD`: Fields with null values.|
|filtering |object|Filters on the data. 

Example: `filtering={"campaign_automation_type":"UPGRADED_SMART_PLUS"}`|
#| campaign_automation_type | string | Campaign automation type.

Enum values:
- `MANUAL`: Manual Campaigns.
- `SMART_PLUS`: Smart+ Campaigns.
- `UPGRADED_SMART_PLUS`: Upgraded Smart+ Campaigns, a new automated campaign type. To learn more about Upgraded Smart+ Campaigns, see [Upgraded Smart+ Campaign](https://business-api.tiktok.com/portal/docs?id=1853452461203458). |
#|campaign_ids |string[]|Filter by campaign IDs.

Max size: 100. |
#|campaign_name |string|Filter by campaign name. Fuzzy match is supported.|
#| campaign_system_origins| string[] | Filter by campaign origins (campaign sources). 
 
 Enum values: 
- `PROMOTE`: The campaign is a Promote campaign created through the TikTok mobile App.
- `TT_ADS_PLATFORM`: The campaign is a non-Promote campaign created through the API or in TikTok Ads Manager.  Default value: `["TT_ADS_PLATFORM"]`.

Only the following settings can be retrieved for a Promote campaign: 
- `advertiser_id`
- `campaign_id` 
- `create_time`
- `campaign_name`
-  `operation_status`
-  `secondary_status` 
To learn more about the availability of and the supported filters for Promote campaigns, see [Promote campaigns](https://business-api.tiktok.com/portal/docs?id=1785880454546433). |
#|primary_status |string|Primary status. 

For enum values, see [Enumeration-Primary Status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
#|secondary_status|string|Filter by campaign secondary status.  

For enum values, see [Enumeration- Campaign Status - Secondary Status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 

**Note**: 
- This field is not returned in the sandbox environment because the campaign is not actually delivered.
- See [Supported secondary statuses for a primary status](https://ads.tiktok.com/marketing_api/docs?id=1757239620352002) to learn about the valid values you can pass in via `secondary_status` for the primary status you specify.|
#|objective_type |string|Filter by advertising objective.

 See [Enumeration-Advertising Objective](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138) for enum values.|
#| sales_destination | string | Sales destination, the destination where you want to drive your sales.

Enum values: 
- `TIKTOK_SHOP`: TikTok Shop. Drive sales on your TikTok Shop.
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app. |
#| buying_types | string[] | Filter by buying types. 

Enum values: 
-  `AUCTION`: Auction ads. 
- `RESERVATION_RF`: Reservation Reach & Frequency ads and TikTok Pulse ads.
- `RESERVATION_TOP_VIEW`: Reservation TopView ads.
Default value: `["AUCTION", "RESERVATION_RF"]`.

 To learn more about the availability of TopView ads in the API, see [TopView](https://business-api.tiktok.com/portal/docs?id=1804258360285186). 

**Note**: The enum value `RESERVATION_TOP_VIEW` cannot be combined with other values. To filter TopView ads, set this field to `["RESERVATION_TOP_VIEW"]`. |
#|is_smart_performance_campaign|boolean|Filter by whether the campaign is an automated campaign type.

Supported values: 
- `true`: The campaign is either a Smart+ Campaign or a Smart Performance Web Campaign. 
- `false`: The campaign is a standard campaign type. 
**Note**: If you do not specify this field, you will get all campaigns. |
#| creative_campaign_type | string[] | Filter by whether the campaign is a Smart+, Search Ads Campaign, or neither.

Enum values: 
- `SPC`: To filter Smart+ Campaigns.
- `SEARCH_CAMPAIGN`: To filter Search Ads Campaigns.
- `OTHER`: To filter non-Smart+ non-Search Ads Campaigns.
If you do not specify this field, you will get all campaigns. |
#|split_test_enabled|boolean|Filter by whether split test has been enabled for the campaign or not.
`true`: Only get campaigns with enabled split test, `false`: Only get disabled campaigns.
**Note**: If you do not specify this field, you will get all campaigns. |
#| campaign_product_source | string | Filter by product source of the campaign.

Enum values: 
- `CATALOG` : Catalog. 
- `STORE`: TikTok Shop, or TikTok Showcase.If you pass in this field, the results will only include campaigns with the Product Sales advertising objective (`objective_type` =`PRODUCT_SALES`). The `objective_type` filter, if specified at the same time, can only be set as `PRODUCT_SALES`.   |
#|optimization_goal|string|Optimization goal. 

Enum values:  [Enumeration - Optimization Goal](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138#item-link-Optimization%20Goal).|
#|campaign_type |string|Use this field to filter regular campaigns or iOS 14 campaigns. 

Enum values: `REGULAR_CAMPAIGN`,`IOS14_CAMPAIGN`. 

To learn about how to create an iOS 14 campaign, see [Create an iOS 14 campaign](https://ads.tiktok.com/marketing_api/docs?id=1737719523561474).|
#|creation_filter_start_time|string|Filter by lower range of campaign creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time zone). Campaigns created later than this time will be returned.

Suggestion: A time range within 6 months is suggested when applying a creation time filter, to ensure that the success and speed of the task won't be affected.|
#|creation_filter_end_time|string|Filter by higher range of campaign creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time zone). Campaigns created earlier than this time will be returned.

Suggestion: A time range within 6 months is suggested when applying a creation time filter, to ensure that the success and speed of the task won't be affected.|
#| gmv_max_promotion_types {-Deprecated}| string[] | GMV Max Campaign type.

Enum values: 
- `PRODUCT_GMV_MAX`: [Product GMV Max Campaign](https://business-api.tiktok.com/portal/docs?id=1822009220448257). 
- `LIVE_GMV_MAX`: [Live GMV Max Campaign](https://business-api.tiktok.com/portal/docs?id=1822009242546258).
**Note**: To filter GMV Max Campaigns, use [/gmv_max/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1826463372290177).|
#| store_ids  {-Deprecated}| string[] | Valid only when the value of `gmv_max_promotion_types` contains `LIVE_GMV_MAX` or `PRODUCT_GMV_MAX`.

 A list of TikTok Shop IDs.

Max size: 10.

**Note**: To filter GMV Max Campaigns, use [/gmv_max/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1826463372290177).|
|page |number|Current page number.

 Default value: 1.
Value range: ≥ 1.|
|page_size |number|Page size.

 Default value: 10.
Value range: 1-1,000. |
```

### Example

```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/campaign/get/?advertiser_id={{advertiser_id}}' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

## Response

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|code |number|The response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|message |string|The response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|request_id |string|The log ID of a request, which uniquely identifies the request.|
|data |object|Returned data. The returned list is sorted by campaign ID (`campaign_id`) in reverse order by default. |
#|list |object[]|A list of campaigns. The returned fields are generated based on the `fields` specified in the request parameters. All fields are returned by default.|
##|advertiser_id |string| Advertiser ID. |
##|campaign_id |string| Campaign ID. |
##| campaign_system_origin| string | Returned for Promote campaigns only. 
Not returned for non-Promote campaigns. 

The origin (source) of the campaign. 

Enum values: 
- `PROMOTE`: The campaign is a Promote campaign created through the TikTok mobile App. 
Only the following settings can be retrieved for a Promote campaign (`campaign_system_origin` is `PROMOTE`): 
- `advertiser_id`
- `campaign_id` 
- `create_time`
- `campaign_name`
-  `operation_status`
-  `secondary_status` |
##|create_time |string| Time at which the campaign was created. |
##|modify_time |string| Time at which the campaign was modified. |
##|objective_type|string| Advertising objective. 

For enum values, see [Enumeration-Advertising Objectives](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
##| app_promotion_type | string | App promotion type. 

Enum values: 
- `APP_INSTALL`: App install. Get new users to install your app.
- `APP_RETARGETING`: App retargeting. Re-engage existing users to take action in your app. 
- `APP_PREREGISTRATION`: App pre-registration. Get new users to pre-register before your app launches.
- `APP_POSTS_PROMOTION`: App posts promotion. Promote TikTok posts to increase app awareness and measure conversions.
**Note**: Currently, creating App posts promotion campaigns via API is not supported. You can only update or retrieve such campaigns via API.  |
##|virtual_objective_type|string|The new objective type.

Enum value: `SALES`.

Use this field to create a campaign with the Sales objective, the combined objective for Website Conversions and Product Sales objectives. Learn more about [the Sales objective](https://business-api.tiktok.com/portal/docs?id=).|
##|sales_destination|string|Sales destination, the destination where you want to drive your sales.

Enum values: 
- `TIKTOK_SHOP`: TikTok Shop. Drive sales on your TikTok Shop.
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.|
##| is_search_campaign | boolean | Whether the campaign is a Search Ads Campaign. With Search Ads Campaigns, you can select keywords and serve ads within TikTok's search result page. 

Supported values: `true`, `false`.  |
##| campaign_automation_type | string | Campaign automation type.

Enum values:
- `MANUAL`: Manual Campaigns.
- `SMART_PLUS`: Smart+ Campaigns.
- `UPGRADED_SMART_PLUS`: Upgraded Smart+ Campaigns, a new automated campaign type. To learn more about Upgraded Smart+ Campaigns, see [Upgraded Smart+ Campaign](https://business-api.tiktok.com/portal/docs?id=1853452461203458). |
##| is_smart_performance_campaign | boolean | Whether the campaign is an automated campaign type.

Supported values:
- `true`: The campaign is a legacy Smart+ Campaign.
- `false`: The campaign is a Manual Campaign or an Upgraded Smart+ Campaign.To determine whether a campaign is a Manual Campaign or an Upgraded Smart+ Campaign, check the returned `campaign_automation_type`.When `campaign_automation_type` is `MANUAL`, the campaign is a Manual Campaign.
- When `campaign_automation_type` is `UPGRADED_SMART_PLUS`, the campaign is an Upgraded Smart+ Campaign. |
##|campaign_type|string| Campaign Type, indicates the campaign is a regular campaign or iOS 14 campaign. 

Enum values: `REGULAR_CAMPAIGN`, `IOS14_CAMPAIGN`. |
##| app_id | string | The Application ID of the promoted app.

 You can get `app_id` by using the [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786) endpoint. |
##| is_advanced_dedicated_campaign | boolean | Whether the campaign is an Advanced Dedicated Campaign. Advanced Dedicated Campaigns leverage advanced delivery models that benefit from real-time signals. 

Enum values: `true`, `false`. |
##| disable_skan_campaign | boolean| Whether to disable SKAN (SKAdNetwork) attribution, Apple's conversion attribution solution for iOS campaigns.

Enum values:
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition). 
- `false`: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.|
##| bid_align_type | string | The attribution type for the Dedicated Campaign. The type determines which attribution network the target CPA (`conversion_bid_price`) or ROAS (`roas_bid`) at the ad group level is based on. 

Enum values: 
- `SAN`: SAN. 
- `SKAN`: SKAN.|
##|campaign_app_profile_page_state|string| Indicates the status of App Profile Page. 

Enum values: `INVALID`, `UNSET`, `ON`, `OFF`. |
##|rf_campaign_type |string|When `objective_type` is specified as `RF_REACH`, this field specifies the specific Reservation campaign type.

Enum values:
- `STANDARD`: Reach & Frequency campaign. 
-  `PULSE`: TikTok Pulse campaign. 
- `TOPVIEW`: TopView campaign.|
##| campaign_product_source | string | Returned only when `objective_type` for the campaign is `PRODUCT_SALES` and the product source is configured for the campaign.
Product source of the campaign.
Enum values: 
- `CATALOG` : Catalog.
- `STORE`: TikTok Shop, or TikTok Showcase.    |
##|catalog_enabled|boolean|Whether to use your catalog to automatically advertise relevant products or services to people based on their unique interests, intent and actions.|
##|campaign_name |string| Campaign name. |
##|special_industries| string[] |Special ad categories. 

Enum values:
- `HOUSING`: Ads for real estate listings, homeowners insurance, mortgage loans or other related opportunities.
- `EMPLOYMENT`: Ads for job offers, internship, professional certification programs or other related opportunities.
- `CREDIT`: Ads for credit card offers, auto loans, long-term financing or other related opportunities.
**Note**: 
- Using special ad categories in Shopping Ads with campaign product source as Catalog and in Shopping Ads with campaign product source as non-Catalog are currently separate allowlist-only features. If you would like to access them, please contact your TikTok representative.
- This field is generally available to advertisers registered in America or Canada. Advertisers who are not registered in America or Canada but want to target these countries with special ad categories need to apply for an additional allowlist.|
##|budget_optimize_on|boolean| Returned only for campaigns with Campaign Budget Optimization (CBO) enabled.   

Whether CBO is enabled. 

Enum values: `true` (enabled).

For details about CBO, see [Campaign Budget Optimization](https://ads.tiktok.com/marketing_api/docs?id=1739381757818881).

**Note**: For Smart+ Campaigns or Smart Performance Web Campaigns, the value of this field will be `true` because CBO is enabled by default for these campaigns.|
##|bid_type |string| Bidding strategy on the campaign level. |
##|deep_bid_type |string| Bidding strategy for in-app events. 

For enum values and their descriptions, see [Enumeration - Deep-level Bidding Strategy](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
##|roas_bid |float| ROAS goal for Value Optimization.|
##|optimization_goal |string| Optimization goal. |
##|budget_mode |string| Budget mode. 

Enum values:
- `BUDGET_MODE_INFINITE`: Unlimited budget.
- `BUDGET_MODE_TOTAL`: Lifetime budget.
- `BUDGET_MODE_DAY` : Daily budget.
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.|
##|budget |float| Campaign budget |
##| rta_id | string | Realtime API (RTA) ID, the RTA strategy identifier. |
##| rta_bid_enabled | boolean | Whether to use RTA bid. 

 Supported values: 
-  `true`: enabled.
-  `false`: not enabled.  |
##| rta_product_selection_enabled | boolean | Whether to use RTA to automatically select products.

Enum values: 
- `true`: enabled.
- `false`: not enabled. |
##|operation_status |string| Operation status.

Enum values:
- `ENABLE` : The campaign is enabled (in 'ON' status).
- `DISABLE`: The campaign is disabled (in 'OFF' status).  |
##|secondary_status|string|Campaign status (Secondary status). 

For enum values, see [Enumeration- Campaign Status - Secondary Status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
**Note**: This field is not returned in the sandbox environment because the campaign is not actually delivered.|
##| postback_window_mode| string | The mode that determines which SKAN 4.0 postback you want to secure. 

Enum values: 
-  `POSTBACK_WINDOW_MODE1`: This option secures the first postback, which corresponds to the 0-2 day attribution window. The data can take up to 4 days to return, and the campaign will wait for 4 days to release the campaign quota. 
- `POSTBACK_WINDOW_MODE2`: This mode secures the first two postbacks, which correspond to the 3-7 day attribution window. The data can take up to 13 days to return, and the campaign will wait for 13 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE3`: This mode secures all three postbacks, which correspond to the 8-35 day attribution window. The data can take up to 41 days to return, and the campaign will wait for 41 days to release the campaign quota. 
**Note**: If you have set up Mobile Measurement Partner (MMP) Tracking with **Adjust**, **Airbridge**, **Appsflyer**,  **Branch**, **Kochava**, or **Singular** for your App and your MMP SDK version is updated to a SKAN 4.0 supported SDK, you can transition your App to SKAN 4.0 on Events Manager. To learn about how to set up MMP tracking for your App, see [How to Set Up App Attribution in TikTok Ads Manager](https://ads.tiktok.com/help/article/set-up-app-attribution-tiktok-ads-manager?lang=en). To learn more about how to transition your App to SKAN 4.0, see [About SKAN 4.0 and TikTok](https://ads.tiktok.com/help/article/about-skan-4-0-and-tiktok?lang=en) and [How to transition to SKAN 4.0](https://ads.tiktok.com/help/article/how-to-transition-to-skan-4-0). |
##|is_new_structure|boolean|Whether the campaign is a new structure (for the same campaign, the structure of campaign, ad groups and ads are the same).|
##|objective|string| Campaign type (application or landing page). 

Enum values: `APP`(application), `LANDING_PAGE`(Landing page). |
##|po_number|string|PO (purchase order) number.
PO numbers are useful for invoice tracking and reconciliation.

[Learn more about PO numbers on monthly invoices](https://ads.tiktok.com/help/article/update-po-number-on-monthly-invoices).|
#|page_info |object | Pagination information. |
##|page |number | Current page number. |
##|page_size |number | Paging size. |
##|total_number |number | Total number of results. |
##|total_page |number |Total pages of results. |
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
        "list": [
            {
                "secondary_status": "CAMPAIGN_STATUS_ENABLE",
                "advertiser_id": "{{advertiser_id}}",
                "is_smart_performance_campaign": false,
                "campaign_name": "{{campaign_name}}",
                "is_new_structure": true,
                "campaign_type": "REGULAR_CAMPAIGN",
                "campaign_id": "{{campaign_id}}",
                "roas_bid": 0,
                "budget_mode": "BUDGET_MODE_TOTAL",
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "objective": "LANDING_PAGE",
                "objective_type": "TRAFFIC",
                "budget": {{budget}},
                "create_time": "{{create_time}}",
                "deep_bid_type": null
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 10,
            "total_page": 1,
            "total_number": 1
        }
    }
}
(/code);
```
