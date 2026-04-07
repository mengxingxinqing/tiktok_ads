# Realtime API

**Doc ID**: 1805437148769281
**Path**: Marketing API/Campaign Management/Guides/Campaign/Realtime API

---

This article introduces how to enable Realtime API (RTA) for your ads.

# Introduction
You can utilize real-time audience data directly in your ad creation workflow to streamline the ad creation process and help you create more tailored campaigns through real-time targeting capabilities. The RTA enables you to integrate real-time audience data to customize ad auction and targeting, thereby delivering better performance.
 
**You can use Campaign Management API to set up campaigns that utilize the RTA functionality. This helps you save time and focus on optimizing your overall advertising strategy.**

# Prerequisites
- You've gained access to TikTok API for Business. See [Get Started - Step by step workflow](https://ads.tiktok.com/marketing_api/docs?id=1735713609895937&rid=7llhcla7zmh) for details. 
  - To enable Realtime API, you need relevant permissions. See [API Reference](https://ads.tiktok.com/marketing_api/docs?id=1735713875563521) to find out permissions required for endpoints (including the endpoints listed in the "Steps" section) and see [Update app permissions](https://ads.tiktok.com/marketing_api/docs?id=1738855280338946&rid=7llhcla7zmh) to find out how to configure permissions.  
- Enabling RTA for your ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. You will need to complete the onboarding process to be able to receive and respond to RTA requests sent to your system first.
- Using RTA bids for your ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.

# Steps
Based on your preference for the advertising objective, you can enable RTA for App Promotion campaigns, Web Conversions campaigns, or Product Sales campaigns. For detailed instructions on each scenario, refer to their respective sections: "[Enable RTA for App Promotion campaigns](#item-link-Enable RTA for App Promotion campaigns)", "[Enable RTA for Web Conversions campaigns](#item-link-Enable RTA for Web Conversions campaigns)", and "[Enable RTA for Product Sales campaigns](#item-link-Enable RTA for Product Sales campaigns)".

## Enable RTA for App Promotion campaigns
1. Create a campaign using [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602). Note that the following requirements must be met.

```xtable
| Setting {20%}| Requirement {25%}| Parameters{25%} | How to configure the parameters{30%} |
|---|---|---|---|
| Advertising objective | App Promotion | `objective_type` | `APP_PROMOTION` |
| App promotion type | Any of the following types:
- App install 
- App retargeting   | `app_promotion_type` | Any of the following values: 
- `APP_INSTALL`
- `APP_RETARGETING`|
| Smart+ Campaign | Disabled 

 You cannot use [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) to create Smart+ Campaigns with RTA enabled. | / | / |
| Realtime API (RTA) | Enabled | `rta_id` | Pass one of the RTA IDs associated with your ad account.

  To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative. |
| Use RTA bid (Optional) | Enabled or disabled | `rta_bid_enabled` | `true` or `false` (or not passed)

**Note**: Using RTA bids for your ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. |
```

2. Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). Note that the following requirements must be met.

```xtable
| Setting {20%}| Requirement {25%}| Parameters{25%} | How to configure the parameters{30%} |
|---|---|---|---|
| Placement | **Select Placement** with TikTok placement | `placement_type`
`placements`  | Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and set `placements` to `["PLACEMENT_TIKTOK"]`. |
| Include search results 
(Optional)| Enabled (recommended) or Disabled | `search_result_enabled`|`true` or `false`|
| Audience targeting
  • Audience 
    ◦ Include 
    ◦ Exclude | Disabled | `audience_ids`
 `excluded_audience_ids` | Not passed |
```

3. Create an ad using [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354).

## Enable RTA for Web Conversions campaigns
1. Create a campaign using [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602). Note that the following requirements must be met.

```xtable
| Setting {20%}| Requirement {25%}| Parameters{25%} | How to configure the parameters{30%} |
|---|---|---|---|
| Advertising objective |Website Conversions | `objective_type` | `WEB_CONVERSIONS` |
| Smart+ Campaign | Disabled 

 You cannot use [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) to create Smart+ Campaigns with RTA enabled. | / | / |
| Realtime API (RTA) | Enabled | `rta_id` | Pass one of the RTA IDs associated with your ad account.

  To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative. |
| Use RTA bid (Optional) | Enabled or disabled | `rta_bid_enabled` | `true` or `false` (or not passed)

**Note**: Using RTA bids for your ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. |
```

2. Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). 

To learn about how to configure ad group level and ad level parameters for Web Conversions campaigns, see [Create Website Conversions ads](https://business-api.tiktok.com/portal/docs?id=1775548501843970).

3. Create an ad using [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354).

## Enable RTA for Product Sales campaigns
1. Create a campaign using [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602). Note that the following requirements must be met.

```xtable
| Setting {20%}| Requirement {25%}| Parameters{25%} | How to configure the parameters{30%} |
|---|---|---|---|
| Advertising objective | Product Sales | `objective_type` | `PRODUCT_SALES` |
| Smart+ Campaign| Disabled 

You cannot use  [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) to create Smart+ Campaigns with RTA enabled. | / | / |
| Campaign product source | Catalog | `campaign_product_source` | `CATALOG` |
| Realtime API (RTA) | Enabled | `rta_id` | Pass one of the RTA IDs associated with your ad account. 

To obtain the list of `RTA` IDs associated with your ad account, contact your TikTok representative. |
| Use RTA to automatically select products 
(Optional)| Enabled or disabled | `rta_product_selection_enabled` | `true` or `false` (or not passed) |
```

2. Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). Note that the following requirements must be met.

  
  
| 
    Setting | 
    Requirement | 
    Parameters | 
    How to configure the parameters | 
   |
  

  
| 
    Shopping ads type | 
    Video Shopping Ads | 
    `shopping_ads_type` | 
    `VIDEO` | 
   |
  
| 
    Optimization location 
(Promotion type) | 
    Any of the following options:
- App
- Web | 
    `promotion_type` | 
    Any of the following values:
- `APP_ANDRIOD` or `APP_IOS`
- `WEBSITE` | 
   |
  
| 
    Product source | 
    Catalog | 
    `product_source` | 
    `CATALOG` | 
   |
  
| 
    `catalog_id`
`catalog_authorized_bc_id` | 
    Pass valid values.

To obtain the IDs of catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610). | 
   |
  
| 
    Placement | 
    **Select Placement** with TikTok placement | 
    `placement_type`
`placements` | 
    Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and set `placements` to `["PLACEMENT_TIKTOK"]`. | 
   |
  
| 
    Include search results | 
    Disabled | 
    `search_result_enabled` | 
    `false` | 
   |
  
| 
  	Audience targeting | 
  	
      		
- Audience: Find prospective customers, including those who have not interacted with your products.
      		
- Retarget audience is not supported.
    	 | 
  	`shopping_ads_retargeting_type`
`shopping_ads_retargeting_actions_days`
`included_custom_actions`
`excluded_custom_actions`
`shopping_ads_retargeting_custom_audience_relation` | 
  	Set ` shopping_ads_retargeting_type` to `OFF`. 

 Do not pass `shopping_ads_retargeting_actions_days`, `included_custom_actions`, `excluded_custom_actions`, and `shopping_ads_retargeting_custom_audience_relation`. Once passed, the parameters `shopping_ads_retargeting_actions_days`, `included_custom_actions`, `excluded_custom_actions`, and `shopping_ads_retargeting_custom_audience_relation` will be ignored. | 
    |
  
| 
    Audience targeting
  • Demographics - Location | 
    Specify locations within the targeting country or region of the catalog | 
    `location_ids` | 
    Pass the IDs of locations within the targeting country or region of the catalog (`catalog_id`).

To obtain the location IDs that you can target, use [/tool/region/](https://business-api.tiktok.com/portal/docs?id=1737189539571713). | 
   |

3. Create an ad using [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). Note that the following requirements must be met. 

```xtable
| Setting {20%}| Requirement {25%}| Parameters{25%} | How to configure the parameters{30%} |
|---|---|---|---|
| Products |
- When "Use RTA to automatically select products" is enabled at the campaign level: **All products**
- When "Use RTA to automatically select products" is disabled, use any of the following options:**All products**
- **Product set**
- **Specific products** | `product_specific_type` | 
- When `rta_product_selection_enabled` is true at the campaign level: `ALL`
- When `rta_product_selection_enabled` is false or not passed at the campaign level, use any of the following values:`ALL`
- `PRODUCT_SET`
- `CUSTOMIZED_PRODUCTS` |
```
