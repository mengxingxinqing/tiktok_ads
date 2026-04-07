# Configure destination and deeplink settings for website-promoting Video Shopping Ads

**Doc ID**: 1774519076905985
**Path**: Use Cases/Campaign creation/Create Shopping Ads/Create Video Shopping Ads/Create Catalog Ads/Configure destination and deeplink settings for website-promoting Video Shopping Ads

---

This article introduces how to configure specific destination and deeplink settings for Video Shopping Ads that promote websites.

> **Note**

> 
- Using deeplink in Shopping Ads that promote websites is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Using dynamic destination in Shopping Ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.

1. **Create a campaign** using [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602). 

The parameter requirements listed in the section [Create Video Shopping Ads with products from catalogs-1. Create a campaign](https://ads.tiktok.com/marketing_api/docs?id=1750361698613249#item-link-1.%20Create%20a%20campaign) must be met.

2. **Create and manage catalogs.** 
Follow the steps outlined in the section [Create Video Shopping Ads with products from catalogs-2. Create and manage catalogs](https://ads.tiktok.com/marketing_api/docs?id=1750361698613249#item-link-2.%20Create%20and%20manage%20catalogs).

3. **Create an ad group** using [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114). 
Note that in addition to the requirements listed in the section [Create Video Shopping Ads with products from catalogs-3. Create an ad group](https://ads.tiktok.com/marketing_api/docs?id=1750361698613249#item-link-3.%20Create%20an%20ad%20group), the following requirements must be met at the same time.

``` xtable
| Setting {20%} | Requirement {25%} | Parameter {20%} | How to configure the parameter {35%} |
|---|---|---|
| Promotion type 
(Optimization location) | Website| `promotion_type`| `WEBSITE`|
| Optimization goal | Click | `optimization_goal` | `CLICK` |
| Billing event | CPC | `billing_event` | `CPC` |
```
4. **Create an ad** using [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354). 
In addition to the requirements listed in the section [Create Video Shopping Ads with products from catalogs-4. Create an ad](https://ads.tiktok.com/marketing_api/docs?id=1750361698613249#item-link-4.%20Create%20an%20ad), you have the flexibility to select from various settings based on your preference for destination and deeplink. There are a total of six combinations available, offering different types of deeplinks and fallback URLs:
- Custom deeplink: Use the deeplink you provide in the ad.
- Product deeplink: Use the deeplink (`ios_url` and `android_url`) you've provided for each product in the catalog.
- Custom link: Fall back to the web page link you provide.
- Product link: Fall back to the web page link (`landing_page_url`) you've provided for each product in the catalog.

To learn more about deeplinks, see [Deeplink](https://business-api.tiktok.com/portal/docs?id=1779541971843073).

You need to select **one** setting from the following options:

  
| 
    Setting | 
    Parameters | 
    How to configure the parameters | 
   |
  
| 
    Destination | 
    Deeplink | 
    Fallback URL | 
   |

  
| 
    Website - Custom link
 | 
    Custom deeplink
 | 
    Custom link | 
    `dynamic_destination` | 
    `UNSET` or do not pass the parameter | 
   |
  
| 
    `shopping_ads_deeplink_type`
`deeplink`
`deeplink_type` | 
    To specify the deeplink type as non-deferred custom deeplink:
- Set `shopping_ads_deeplink_type` to `CUSTOM`,
- Pass `deeplink`,
- AND set `deeplink_type` to `NORMAL`. | 
   |
  
| 
    `shopping_ads_fallback_type`
`landing_page_url` | 
    To specify the fallback URL as custom link:
- Set `shopping_ads_fallback_type` to `CUSTOM`,
- AND pass `landing_page_url`. | 
   |
  
| 
    Website - Custom link | 
    ❌ | 
    Custom link | 
    `dynamic_destination` | 
    `UNSET` or do not pass the parameter | 
   |
  
| 
    `shopping_ads_fallback_type`
`landing_page_url` | 
    To specify the fallback URL as custom link:
- Set `shopping_ads_fallback_type` to `CUSTOM`,
- AND pass `landing_page_url`. | 
   |
  
| 
    Website - Product link
 | 
    product deeplink
 | 
    Product link | 
    `dynamic_destination` | 
    `UNSET` or do not pass the parameter | 
   |
  
| 
    `shopping_ads_deeplink_type`
`deeplink_type` | 
    To specify the deeplink type as non-deferred product deeplink:
- Set `shopping_ads_deeplink_type` to `SHOPPING_ADS`,
- AND set `deeplink_type` to `NORMAL`.
**Note**: `shopping_ads_deeplink_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
-  `ad_format` is set to `CATALOG_CAROUSEL`. | 
   |
  
| 
    `shopping_ads_fallback_type` | 
    `SHOPPING_ADS`

**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
-  `ad_format` is set to `CATALOG_CAROUSEL`. | 
   |
  
| 
    Website - Product link | 
    ❌
 | 
    Product link | 
    `dynamic_destination` | 
    `UNSET` or do not pass the parameter | 
   |
  
| 
    `shopping_ads_fallback_type` | 
    `SHOPPING_ADS`

**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
-  `ad_format` is set to `CATALOG_CAROUSEL`. | 
   |
  
| 
    Instant Product Page
 | 
    Custom deeplink | 
    Custom link | 
    `dynamic_destination` | 
    `UNSET` or do not pass the parameter | 
   |
  
| 
    `instant_product_page_used` | 
    `true` | 
   |
  
| 
    `deeplink`
`deeplink_type`
 | 
    To specify the deeplink type as non-deferred custom deeplink:
- Pass `deeplink`,
- AND set `deeplink_type` to `NORMAL`. | 
   |
  
| 
    `shopping_ads_fallback_type`
`landing_page_url` | 
    To specify the fallback URL as custom link:
- Set `shopping_ads_fallback_type` to `CUSTOM`,
- AND pass `landing_page_url`. | 
   |
  
| 
    Instant Product Page
 | 
    ❌ | 
    Custom link | 
    `dynamic_destination` | 
    `UNSET` or do not pass the parameter | 
   |
  
| 
    `instant_product_page_used` | 
    `true` | 
   |
  
| 
    `shopping_ads_fallback_type`
`landing_page_url`
`deeplink_type` | 
    To specify the fallback URL as custom link:
- Set `shopping_ads_fallback_type` to `CUSTOM`,
- Pass `landing_page_url`,
- AND set `deeplink_type` to `NORMAL`. | 
   |
