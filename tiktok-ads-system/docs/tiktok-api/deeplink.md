# Deeplink

**Doc ID**: 1779541971843073
**Path**: Marketing API/Campaign Management/Guides/Ad/Deeplink

---

Deeplinks are a feature that directs a user to a certain page within the promoted App, optimizing user journeys and improving ad performance.

# Deeplink types and fallback URL
Two deeplink types are supported at the ad level: non-deferred deeplinks and deferred deeplinks.

## Non-deferred deeplink
This deeplink type leads installed users (users who have installed your App) directly to a certain page within the promoted App. Non-deferred deeplinks are useful for re-engagement with installed users. For example, you can set the deeplink to the discount page during the holiday season.

Supported formats: 
  - Custom URL scheme, in the format of `scheme://resource`. For instance, a Custom URL scheme of WhatsApp should follow the format `whatsapp://resource`.
  -  Apple’s universal link starting with `http://` or `https://`.
  -  Android App Link starting with `http://` or `https://`.

> **Note**

> 
- Non-deferred deeplinks are currently an allowlist-only feature for some scenarios. To check the scenarios where non-deferred deeplinks are an allowlist-only feature, see the "[Availability - Deeplink](#item-link-Deeplink)" section. If you would like to access it for these scenarios, please contact your TikTok representative. 
- Non-deferred deeplinks are not an allowlist-only feature for the Lead generation objective with optimization location as social media app, but the optimization location of social media app under the Lead generation objective is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. 

  
## Deferred deeplink
This deeplink type leads new users who have NOT installed the App to a certain page within the promoted App after they download and install the App.

To learn about the supported scenarios for non-deferred deeplinks and deferred deeplinks, see the "[Availability - Deeplink](#item-link-Deeplink)" section.

> **Note**

> 
- Deferred deeplinks are currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. Note that implementing deferred deeplinks require technical resources and development capabilities.
- Deferred deeplinks are not available in Dedicated Campaigns. 

## Fallback URL
Fallback URL is a URL that directs users who have not installed the App to a designated page (for instance, the homepage of your official website) when a deeplink is configured for an ad. To learn about the supported scenarios for fallback URLs, see the "[Availability - Fallback type](#item-link-Fallback type)" section.

## Availability
The following tables outline the supported scenarios for deeplinks, including non-deferred deeplinks and deferred deeplinks, and fallback URLs.

### Deeplink

  
| 
    Advertising objective | 
    Optimization location
(Promotion type) | 
    Corresponding API settings | 
    Non-deferred deeplink
 | 
    Deferred deeplink | 
   |
  
| 
    iOS Dedicated Campaign
 | 
    iOS non-Dedicated Campaign | 
    Android Campaign | 
    Web campaign | 
    iOS Dedicated Campaign | 
    iOS non-Dedicated Campaign | 
    Android Campaign | 
    Web campaign | 
   |

  
| 
    Reach | 
    - | 
    
- At the campaign level:`objective_type` is set to `REACH`
- At the ad group level:`promotion_type` is set to `WEBSITE_OR_DISPLAY` | 
    ❌ | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Video views | 
    - | 
    
- At the campaign level:`objective_type` is set to `VIDEO_VIEWS`
- At the ad group level:`promotion_type` is set to `WEBSITE_OR_DISPLAY` | 
    ❌ | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Lead generation | 
    Instant Form | 
    
- At the campaign level:`objective_type` is set to `LEAD_GENERATION`
- At the ad group level:`promotion_type` is set to `LEAD_GENERATION`
- `promotion_target_type` is set to `INSTANT_PAGE` or not passed
To learn about how to create such ads, see [Create a Lead Generation ad with promotion type as Instant Form](https://business-api.tiktok.com/portal/docs?id=1774482920012801). | 
    ❌ | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Lead generation | 
    Social media app | 
    
- At the campaign level:`objective_type` is set to `LEAD_GENERATION`
- At the ad group level:`promotion_type` is set to `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
To learn about how to create such ads, see [Create a Lead Generation ad with promotion type as social media app](https://business-api.tiktok.com/portal/docs?id=1774482999036930). | 
    ❌ | 
    Allowlist | 
    Allowlist | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Traffic | 
    App | 
    
- At the campaign level:`objective_type` is set to `TRAFFIC`
- At the ad group level:`promotion_type` is set to `APP_ANDROID` or `APP_IOS` | 
    ❌ | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Traffic | 
    Website 
(CPC only) | 
    
- At the campaign level:`objective_type` is set to `TRAFFIC`
- At the ad group level:`promotion_type` is set to `WEBSITE`
- `billing_event` is set to `CPC` | 
    GA | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    App promotion -
 App install 
(Click, 
Mobile App Install, 
App Event Optimization, 
Value-Based Optimization) | 
    App | 
    
- At the campaign level:`objective_type` is set to `APP_PROMOTION`
- `app_promotion_type` is set to `APP_INSTALL`
- At the ad group level:`promotion_type` is set to `APP_ANDROID` or `APP_IOS`
- `optimization_goal` is set to `CLICK`, `INSTALL`, `IN_APP_EVENT` or `VALUE` | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    Allowlist | 
    Allowlist | 
    ❌ | 
   |
  
| 
    App promotion - 
App retargeting | 
    App | 
    
- At the campaign level:`objective_type` is set to `APP_PROMOTION`
- `app_promotion_type` is set to `APP_RETARGETING`
- At the ad group level:`promotion_type` is set to `APP_ANDROID` or `APP_IOS` | 
    ❌ | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Product sales (Catalog) - 
App retargeting | 
    App | 
    
- At the campaign level:`objective_type` is set to `PRODUCT_SALES`
- `campaign_product_source` is set to `CATALOG`
- At the ad group level:`shopping_ads_type` is set to `VIDEO`
- `promotion_type` is set to `APP_ANDROID` or `APP_IOS`
- `product_source` is set to `CATALOG`
- `shopping_ads_retargeting_type` is set to `LAB1`, `LAB2`, or `LAB3` | 
    ❌ | 
    GA
 | 
    GA | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |
  
| 
    Product sales (Catalog) - 
App prospecting | 
    App | 
    
- For deferred deeplinks, the following requirements must be met:At the campaign level:`objective_type` is set to `PRODUCT_SALES`
- `campaign_product_source` is set to `CATALOG`
- At the ad group level:`shopping_ads_type` is set to `VIDEO`
- `promotion_type` is set to `APP_ANDROID` or `APP_IOS`
- `product_source` is set to `CATALOG`
- `shopping_ads_retargeting_type` is set to `OFF` or not passed
- For non-deferred deeplinks, see [Optimize Destination visit in Video Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1782087855154177).
**Note**: The optimization goal Destination visit is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. | 
    ❌ | 
    GA | 
    GA | 
    ❌ | 
    ❌ | 
    Allowlist | 
    Allowlist | 
    ❌ | 
   |
  
| 
    Product Sales (Catalog) | 
    Website | 
	
- At the campaign level:`objective_type` is set to `PRODUCT_SALES`
- `campaign_product_source` is set to `CATALOG`
- At the ad group level:`shopping_ads_type` is set to `VIDEO`
- `promotion_type` is set to `WEBSITE`
- `product_source` is set to `CATALOG`
- `optimization_goal` is set to `CLICK` 
To learn about how to configure specific destination and deeplink settings for website-promoting Video Shopping Ads, see [Configure destination and deeplink settings for website-promoting Video Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1774519076905985). | 
    ❌ | 
    ❌ | 
    ❌ | 
    Allowlist | 
    ❌ | 
    ❌ | 
    ❌ | 
    ❌ | 
   |

### Fallback type
```xtable
| Advertising objective {20%} | Optimization location{20%}  | Fallback type {60%} |
|---|---|---|
| Reach | - | ❌

By default, fall back to the promoted web page that is specified through `landing_page_url` at the ad level. |
| Video views | - | ❌ 

By default, fall back to the promoted web page that is specified through `landing_page_url` at the ad level. |
| Lead generation | Social media app | 
-  Website: the promoted Apple’s universal link or Android App Link that starts with `http:// ` or `https:// ` and is specified through `landing_page_url` at the ad level. |
| Traffic | App | 
-  App store: the App Store or Google Play page for the promoted App (`app_id`).
-  Website: the promoted web page that is specified through `landing_page_url` at the ad level. |
| Traffic | Website (CPC only) | ❌

By default, fall back to the promoted web page that is specified through `landing_page_url` at the ad level. |
| App promotion - 
App install 
 (Click, 
Mobile App Install, 
App Event Optimization, 
Value Based Optimization)| App | ❌ 

By default, fall back to the App Store or Google Play page for the promoted App specified through `app_id` at the ad group level. |
| App promotion - 
App retargeting | App | ❌ 

By default, fall back to the App Store or Google Play page for the promoted App specified through `app_id` at the ad group level. |
| Product sales (Catalog) - 
App retargeting | App | 
-  App store: the App Store or Google Play page for the promoted App (`app_id`).
-  Product link: the web page link (`landing_page_url`) you've provided for each product in the catalog.
-  Custom link: the promoted web page that is specified through `landing_page_url` at the ad level. 
**Note**: Product link is not supported in any of the following scenarios at the ad level: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO` .
- `ad_format` is set to `CATALOG_CAROUSEL`. |
| Product sales (Catalog) - 
App prospecting | App | 
- When you use deferred deeplinks, fallback type is not supported.By default, fall back to the App Store or Google Play page for the promoted App specified through `app_id` at the ad group level. 
- When you use non-deferred deeplinks, the supported fallback types are:  App store: the App Store or Google Play page for the promoted App (`app_id`). 
-  Product link: the web page link (`landing_page_url`) you've provided for each product in the catalog. 
-  Custom link: the promoted web page that is specified through `landing_page_url` at the ad level.
**Note**: Product link is not supported in any of the following scenarios at the ad level: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`. 
- `ad_format` is set to `CATALOG_CAROUSEL`. |
| Product sales (Catalog) | Website | 
-  Product link: the web page link (`landing_page_url`) you've provided for each product in the catalog. 
-  Custom link: the promoted web page that is specified through `landing_page_url` at the ad level.  
**Note**: Product link is not supported in any of the following scenarios at the ad level: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO` .
- `ad_format` is set to `CATALOG_CAROUSEL`. |
```
## Supported deeplink and fallback type settings for specific scenarios
The following table illustrates the supported deeplink and fallback type settings for a certain scenario, and how to configure the corresponding API configurations for the deeplink and fallback URL settings.

  
| 
    Scenario | 
    Deeplink and fallback URL settings | 
    How to configure the API settings | 
   |
  
| 
    Advertising objective | 
    Optimization location | 
    Deeplink | 
    Fallback type | 
   |

  
| 
    Reach | 
    -
 | 
    Non-deferred deeplink | 
    ❌ | 
	
- Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`. | 
   |
  
| 
    Video views | 
    - | 
    Non-deferred deeplink | 
    ❌ | 
    
- Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`. | 
   |
  
| 
    Lead generation | 
    Social media app | 
    Non-deferred deeplink | 
    Website | 
    
- To specify the deeplink type as non-deferred deeplink:Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`.
- To specify the fallback type as website:Set `fallback_type` to `WEBSITE`.
- Pass `landing_page_url`. | 
   |
  
| 
    Traffic | 
    App | 
    Non-deferred deeplink | 
    
- App store
- Website | 
    
- To specify the deeplink type as non-deferred deeplink:Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`.
-  If you set `optimization_goal` to `DESTINATION_VISIT` at the ad group level, you need to pass `deeplink_format_type` at the same time. To learn about how to use the optimization goal Destination Visit in a Traffic ad, see [Optimize Destination visit in Traffic ads](https://business-api.tiktok.com/portal/docs?id=1782086241778690).
- To specify the fallback type, pass `fallback_type`.If you want to specify fallback type as App store, set `fallback_type` to `APP_INSTALL`, and do not pass `landing_page_url`.
- If you want to specify fallback type as Website, set `fallback_type` to `WEBSITE`, and pass `landing_page_url`. | 
   |
  
| 
    Traffic | 
    Website (CPC only) | 
    Non-deferred deeplink | 
    ❌ | 
    
- Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`. | 
   |
  
| 
    App promotion - 
App install 
(Click, 
Mobile App Install, 
App Event Optimization, 
Value Based Optimization) | 
    App | 
    Deferred deeplink | 
    ❌ | 
    
- Set `deeplink_type` to `DEFERRED_DEEPLINK`.
- Pass `deeplink`. | 
   |
  
| 
    App promotion - 
App retargeting | 
    App | 
    Non-deferred deeplink | 
    ❌ | 
    
- Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`. | 
   |
  
| 
    Product sales (Catalog) - 
App retargeting | 
    App | 
    Non-deferred product deeplink | 
    
- App store
- Product link
- Custom link | 
    
- To specify the deeplink type as non-deferred product deeplink:Set `shopping_ads_deeplink_type` to `SHOPPING_ADS`.
- Set `deeplink_type` to `NORMAL`.
**Note**: `shopping_ads_deeplink_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- To specify the fallback type, pass `fallback_type` and `shopping_ads_fallback_type`.If you want to specify fallback type as App store, set `fallback_type` to `APP_INSTALL`, set `shopping_ads_fallback_type` to `DEFAULT`, and do not pass `landing_page_url`.
- If you want to specify fallback type as product link, set `fallback_type` to `WEBSITE`, set `shopping_ads_fallback_type` to `SHOPPING_ADS`, and do not pass `landing_page_url`.

**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- If you want to specify fallback type as custom link, set `fallback_type` to `WEBSITE`, set `shopping_ads_fallback_type` to `CUSTOM`, and pass `landing_page_url`.
 | 
   |
  
| 
    Non-deferred custom deeplink | 
    
- App store
- Product link
- Custom link | 
    
- To specify the deeplink type as non-deferred custom deeplink:Set `shopping_ads_deeplink_type` to `NORMAL`.
- Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`.
- To specify the fallback type, pass `fallback_type` and `shopping_ads_fallback_type`.If you want to specify fallback type as App store, set `fallback_type` to `APP_INSTALL`, set `shopping_ads_fallback_type` to `DEFAULT`, and do not pass `landing_page_url`.
- If you want to specify fallback type as product link, set `fallback_type` to `WEBSITE`, set `shopping_ads_fallback_type` to `SHOPPING_ADS`, and do not pass `landing_page_url`.

**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- If you want to specify fallback type as custom link, set `fallback_type` to `WEBSITE`, set `shopping_ads_fallback_type` to `CUSTOM`, and pass `landing_page_url`.
 | 
   |
  
| 
    Product sales (Catalog) - 
App prospecting | 
    App | 
    Deferred product deeplink | 
    ❌ | 
   
- Set `shopping_ads_deeplink_type` to `SHOPPING_ADS`.
- Set `deeplink_type` to `DEFERRED_DEEPLINK`.
**Note**: `shopping_ads_deeplink_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`. | 
   |
  
| 
    Deferred custom deeplink | 
    ❌ | 
    
- Set `shopping_ads_deeplink_type` to `CUSTOM`.
- Set `deeplink_type` to `DEFERRED_DEEPLINK`.
- Pass `deeplink`. | 
   |
  Non-deferred product deeplink | 
    
- App store
- Product link
- Custom link | 
    
- To specify the deeplink type as non-deferred product deeplink:Set `shopping_ads_deeplink_type` to `SHOPPING_ADS`.
- Set `deeplink_type` to `NORMAL`.
- Set `fallback_type` to `UNSET`.
**Note**: `shopping_ads_deeplink_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- To specify the fallback type, pass `shopping_ads_fallback_type`.If you want to specify fallback type as App store, set `shopping_ads_fallback_type` to `DEFAULT`, and do not pass `landing_page_url`.
- If you want to specify fallback type as product link, set `shopping_ads_fallback_type` to `SHOPPING_ADS`, and do not pass `landing_page_url`.

**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- If you want to specify fallback type as custom link, set `shopping_ads_fallback_type` to `CUSTOM`, and pass `landing_page_url`.
 | 
   |
  
| 
    Non-deferred custom deeplink | 
    
- App store
- Product link
- Custom link | 
    
- To specify the deeplink type as non-deferred custom deeplink:Set `shopping_ads_deeplink_type` to `NORMAL` and pass `deeplink`.
- Set `deeplink_type` to `NORMAL`.
- Set `fallback_type` to `UNSET`.
- To specify the fallback type, pass `shopping_ads_fallback_type`.If you want to specify fallback type as App store, set `shopping_ads_fallback_type` to `DEFAULT`, and do not pass `landing_page_url`.
- If you want to specify fallback type as product link, set `shopping_ads_fallback_type` to `SHOPPING_ADS`, and do not pass `landing_page_url`.

**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- If you want to specify fallback type as custom link, set `shopping_ads_fallback_type` to `CUSTOM`, and pass `landing_page_url`.
 | 
   |
  
| 
    Product sales (Catalog) | 
    Website | 
    Non-deferred product deeplink | 
    Product link | 
    
- To specify the deeplink type as non-deferred product deeplink:Set `shopping_ads_deeplink_type` to `SHOPPING_ADS`.
- Set `deeplink_type` to `NORMAL`.
**Note**: `shopping_ads_deeplink_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`.
- To specify the fallback URL as product link:Set `shopping_ads_fallback_type` to `SHOPPING_ADS`.
**Note**: `shopping_ads_fallback_type` cannot be set to `SHOPPING_ADS` in any of the following scenarios: 
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO`.
- `ad_format` is set to `CATALOG_CAROUSEL`. | 
   |
  
| 
    Non-deferred custom deeplink | 
    Custom link | 
     
- To specify the deeplink type as non-deferred custom deeplink:Set `shopping_ads_deeplink_type` to `CUSTOM`.
- Set `deeplink_type` to `NORMAL`.
- Pass `deeplink`.
- To specify the fallback URL as custom link:Set `shopping_ads_fallback_type` to `CUSTOM`.
- Pass `landing_page_url`. | 
   |
