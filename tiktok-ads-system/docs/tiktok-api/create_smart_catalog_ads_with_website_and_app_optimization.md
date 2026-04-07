# Create Smart+ Catalog Ads with Website and App Optimization

**Doc ID**: 1842232769643905
**Path**: Use Cases/Campaign creation/Create ads with Website and App Optimization/Create Smart+ Catalog Ads with Website and App Optimization

---

This article walks you through the steps to create Smart+ Catalog Ads with Website and App Optimization.

## Prerequisite
* Creating Smart+ Catalog Ads using hotel, flight, destination, or entertainment catalogs are currently separate allowlist-only features. If you would like to access them, contact your TikTok representative. You need to apply for a separate allowlist for each catalog type to be used in Smart+ Catalog Ads.
* Creating Smart+ Catalog Ads with Website and App Optimization (with `sales_destination` set to `WEB_AND_APP`) is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
* Creating Smart+ Catalog Ads requires setting up an E-commerce, a hotel, a flight, a destination, or an entertainment catalog in your Business Center first.

To set up the catalog:
- 1. Create an E-commerce, a hotel, a flight, a destination, or an entertainment catalog using [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961).
- 2. Upload products to the catalog using [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) (JSON schema), [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) (CSV feed template), or [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377)(online data feed schedule).
- 3. Check the product handling results using [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889). 

Pass in the `feed_log_id` obtained from Step ii. If the field `error_affected_products` in the response is not null, examine the issue details and return to Step ii to reupload the product.
- 4. (Optional) Create a product set using [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257).

If you want to have products selected from a product set, creating a product set is necessary. Otherwise, you can skip this step.
- 5. (Optional) Invite members to Business Center and grant the admin permission using [/bc/member/invite/](https://business-api.tiktok.com/portal/docs?id=1739939455765505). 

 You can also choose `advertiser_role` that you want to assign to the members invited.
- 6. (Optional) Share a catalog with members and grant catalog management access using [/bc/asset/assign/](https://business-api.tiktok.com/portal/docs?id=1739438211077121). 

 Make sure to specify `CATALOG` in the `asset_type` field and `ADMIN` in the `catalog_role` field. 

For all catalog APIs, see [here](https://business-api.tiktok.com/portal/docs?id=1739578477445121).

## Steps

Note that the following requirements must be met. To find a complete list of parameters, see [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362).

> **Note**

> Smart+ Catalog ad groups cannot be used in [/split_test/create/](https://business-api.tiktok.com/portal/docs?id=1742666471475201) to create split test groups.

  
    
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
      Sales destination | 
      Website and app | 
      `objective_type` | 
      `WEB_CONVERSIONS` | 
     |
   
| 
      `sales_destination` | 
      `WEB_AND_APP` | 
     |
    
| 
      Smart+ Campaign | 
      **Smart+ Campaign** | 
      `spc_type` | 
      `WEB_ALL_IN_ONE` | 
     |
    
| 
      iOS 14 Dedicated Campaign | 
      Disabled | 
      `campaign_type` | 
      `REGULAR_CAMPAIGN` or not passed. | 
     |
    
| 
      `app_id` | 
      Not passed | 
     |
    
| 
      `campaign_app_profile_page_state` | 
      Not passed | 
     |
    
| 
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Pass a valid value | 
     |
    
| 
      Special ad categories (Optional) | 
      Enabled or disabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada. | 
      `special_industries` | 
      Pass valid values or not passed | 
     |
    
| 
      Campaign Budget Optimization (CBO) | 
      N/A

CBO is enabled by default for Smart+ Web Campaigns. | 
      N/A | 
      N/A

**Note**: If you retrieve Smart+ Web Campaigns via [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986), the returned `budget_optimize_on` will be `true`. | 
     |
    
| 
      Product source details
· Use Catalog | 
      **Enabled with an E-commerce, a hotel, a flight, a destination, or an entertainment catalog with at least two approved products** | 
      `web_all_in_one_catalog_status` | 
      `OPEN` | 
     |
    
| 
      `product_source` | 
      `CATALOG` | 
     |
    
| 
      `catalog_id`
`catalog_authorized_bc_id` | 
      Pass valid values.
The catalog (`catalog_id`) needs to have at least two approved products. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 2.

To obtain E-commerce, hotel, flight, destination, or entertainment catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). The `catalog_type` should be `ECOM`, `HOTEL`, `FLIGHT`, `DESTINATION`, or `ENTERTAINMENT`.

To learn about how to create an E-commerce, a hotel, a flight, a destination, or an entertainment catalog, see [Prerequisite](#item-link-Prerequisite). | 
     |
    
| 
      Product source details
· Products | 
      Any of the following options:
- All products
- Product set
- Specific products with a maximum of 20 products
**Note**: When you select a destination catalog or an entertainment catalog, this option is not supported. | 
      `product_specific_type`
`product_set_id`
`product_ids` | 
      Set `product_specific_type` to `ALL`, `PRODUCT_SET` or `CUSTOMIZED_PRODUCTS`.
- If `product_specific_type` is set to `ALL`, you don't need to pass `product_set_id` and `product_ids`.
- If `product_specific_type` is set to `PRODUCT_SET`, you need to pass `product_set_id`. `product_ids` is not needed.
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, you need to pass a maximum of 20 available E-commerce, hotel, or flight catalog products through `product_ids`. `product_set_id` is not needed.To retrieve the product ID (`product_id`) of each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402). | 
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
- App ID of Android app and that of an iOS appTo obtain the list of App IDs within your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786) and check the returned `app_id`. | 
     |
    
| 
      `app_id` | 
      Pass valid values | 
     |
    
| 
      Optimization goal | 
      Any of the following types:
- Conversion
- Value | 
      `optimization_goal` | 
      Any of the following values:
- `CONVERT`
- `VALUE` | 
     |
    
| 
      Optimization location
· Web data connection | 
      Specify a valid Pixel | 
      `pixel_id` | 
      Specify a valid value
To obtain the list of Pixels within your ad account, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978). | 
     |
    
| 
      `promotion_type` | 
      `WEBSITE` | 
     |
    
| 
      Optimization event | 
      Specify a valid optimization event
- When optimization goal is Value, specify the optimization event as Complete Payment. | 
      `optimization_event` | 
      Specify a valid value.

**Note**: When `optimization_goal` is set to `VALUE`, set this field to `SHOPPING`.

To learn about the supported event types, see [List of values for `optimization_event` for Smart+ Catalog Ads](#item-link-List of values for optimization_event for Smart+ Catalog Ads).
You need to ensure the specified optimization event is active for both the Pixel and the app or apps.
- To obtain the optimization events that have been configured for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- To obtain the active optimization events for an app, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977). | 
     |
    
| 
      Bid Strategy | 
      
- If optimization goal is Conversion, the strategy can be Maximum Delivery or Target CPA.
- If optimization goal is Value, the strategy can only be Highest value. | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      
- If `optimization_goal` is `CONVERT`, set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`. Do not pass `deep_bid_type`.If `bid_type` is `BID_TYPE_CUSTOM`, pass `conversion_bid_price` at the same time.
- If `optimization_goal` is `VALUE`, set `deep_bid_type` to `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not pass `conversion_bid_price` and `bid_price`. | 
     |
    
| 
      Attribution settings | 
      Select from the supported attribution setting options for the specific scenario. | 
      `click_attribution_window`
- `view_attribution_window`
- `engaged_view_attribution_window`
- `attribution_event_count` | 
      To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - Website conversions](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-Website%20conversions). | 
     |
    
| 
      Billing event | 
      oCPM | 
      `billing_event` | 
      `OCPM` | 
     |
    
| 
      Budget mode | 
      Dynamic daily budget | 
      `budget_mode` | 
      `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
     |
    
| 
      Schedule type | 
      Any of the following types:
- Run campaign continuously after the scheduled start time
- Run campaign between the scheduled start time and end time | 
      `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
      
- To run the campaign continuously after the scheduled start time, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not pass `schedule_end_time`.
- To run the campaign between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`. | 
     |
    
| 
      Dayparting (Optional) | 
      Any of the following types:
- All day
- Select specific time | 
      `dayparting` | 
      Any of the following configurations:
- Specify an all-0 value, an all-1 value, or not specified
- Specify a value that's not an all-0 value or an all-1 value | 
     |
    
| 
      Audience targeting
· Location | 
      The location should match or be the subset of the targeting location of your catalog. | 
      `location_ids` or `zipcode_ids` | 
      Pass IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) and check the returned `country`. | 
     |
    
| 
      Audience targeting
· Minimum age | 
      Any of the following types:
- 18
- 25 | 
      `spc_audience_age` | 
      Any of the following values:
- `18+`
- `25+` | 
     |
	
| 
      `exclude_age_under_eighteen` | 
      `true` | 
     |
    
| 
      Audience targeting
· Languages (Optional) | 
      Enabled or disabled | 
      `languages` | 
      Pass valid values or not passed | 
     |
    
| 
      Audience targeting
· Gender (Optional) | 
      Supported with allowlist

**Note**: Gender targeting in Smart+ Campaigns is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. | 
      `gender` | 
      Pass valid values or not passed | 
     |
    
| 
      Audience targeting
· Exclude audience (Optional) | 
      Enabled or disabled | 
      `excluded_audience_ids` | 
      Pass valid values or not passed | 
     |
    
| 
      Placement | 
      TikTok placement including search result or Automatic placement | 
      `placement_type`
`placements` | 
      Not passed

**Note**: Automated placement selection is a key feature of Smart+ Campaigns. The system will automatically configure placements based on your other settings and select high-quality traffic from various placements to deliver better results. If provided, the parameters `placement_type` and `placements` will be ignored. To retrieve the exact placement setting of Smart+ Catalog Ads, use [/campaign/spc/get/](https://business-api.tiktok.com/portal/docs?id=1767334299811842). | 
     |
    
| 
      User comment (Optional) | 
      Enabled or disabled | 
      `comment_disabled` | 
      Pass valid values or not passed | 
     |
    
| 
      Video download (Optional) | 
      Enabled or disabled | 
      `share_disabled` | 
      Pass valid values or not passed | 
     |
    
| 
      Video sharing (Optional) | 
      Enabled or disabled | 
      `video_download_disabled` | 
      Pass valid values or not passed | 
     |
    
| 
      Pangle block list (Optional) | 
      Enabled or disabled | 
      `blocked_pangle_app_ids` | 
      Pass valid values or not passed | 
     |
    
| 
      Brand safety and suitability | 
      N/A 
These settings only apply to TikTok in-feed ads. Any previous account-level settings in the brand safety hub will apply to your campaign. | 
      N/A | 
      Any previous account-level settings in the Brand Safety Hub will apply to your Smart+ Campaign.
To set the Brand Safety Hub settings of an ad account first, use [/tiktok_inventory_filters/update/](https://business-api.tiktok.com/portal/docs?id=1830112569774274). | 
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
      `landing_page_url` | 
      Specify a deeplink.
The deeplink format can be Apple’s universal link or Android App Link starting with `http://` or `https://`. | 
     |
    
| 
	   URL parameters (Optional) | 
      Enabled or disabled | 
      `utm_params` | 
      Specify valid values or not specified

You can manually add URL parameters to the custom link by directly setting `landing_page_url` to a URL that already includes URL parameters.
- However, if you use a custom link in your ad and specify `utm_params` at the same time, the URL parameters will not be automatically appended to the custom link (`landing_page_url`) upon ad delivery. In such cases, you need to ensure that you specify a `landing_page_url` with the URL parameters already appended, and that `utm_params` exactly matches the used URL parameters. Otherwise, an error will occur. | 
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
- `BC_AUTH_TT`
**Note**:
- For Spark Ads identities (`AUTH_CODE`, `TT_USER`, or `BC_AUTH_TT`), pass values to `identity_type` and `identity_id` within the `media_info` object.
- For non-Spark Ads identities (`CUSTOMIZED_USER`), pass values to `identity_type` and `identity_id` outside of the `media_info` object. | 
     |
    
| 
      `identity_id` | 
      Pass a valid value
To get the list of identities under your ad account, use [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057). | 
     |
    
| 
      `identity_authorized_bc_id` | 
      Pass a valid value when `identity_type` is `BC_AUTH_TT` | 
     |
    
| 
      Ad creative
· Auto-selection of creatives from your catalog | 
      Any of the following options:
- Enabled (Recommended)Catalog creatives will be used to generate ads.
- Multiple ad format combinations are supported. For detailed configuration options and requirements, see [Customize the ad format combinations in Smart+ Catalog Ads](#item-link-Customize the ad format combinations in Smart+ Catalog Ads).
- DisabledCatalog creatives will not be used to generate ads. The system will automatically create single video ads using your specified content.
- Requirements:Specify non-catalog creatives based on identity type:For Custom User identity, specify one to 30 videos with cover images and one to five ad texts.
- For Authorized User identity, or Spark Ads PULL with TikTok User or TikTok Account User in Business Center identity, specify one to 30 TikTok video posts.
- Specify 1-5 ad texts**Note**: Not using a catalog for creatives might restrict your ad performance potential. | 
      `catalog_creative_toggle`
`video_info`
`image_info`
`music_info`
`title_list`
`tiktok_item_id` | 
      
- To enable auto-selection of catalog creatives:Set `catalog_creative_toggle` to `true`
- Specify a piece of music via `music_info`.
- Set `identity_type` to `CUSTOMIZED_USER`.
- Specify one to five ad texts (`title_list`).
- For detailed configuration options and requirements, see [Customize the ad format combinations in Smart+ Catalog Ads](#item-link-Customize the ad format combinations in Smart+ Catalog Ads).**Note**: `music_info` is required when `catalog_creative_toggle` is `true`.
- To disable auto-selection of catalog creatives, set `catalog_creative_toggle` to `false`, and specify non-catalog creatives based on identity type:If `identity_type` is `CUSTOMIZED_USER`, specify one to 30 videos (`video_info`) with cover images (`image_info`) and one to five ad texts (`title_list`).
- If `identity_type` is not `CUSTOMIZED_USER`, specify one to 30 TikTok video posts (`tiktok_item_id`). Do not specify ad texts (`title_list`). | 
     |
    
| 
      Interactive add-ons
· Auto-selection of interactive add-ons (Optional) | 
      Any of the following options:
- Enabled (Recommended)The most suitable interactive add-ons will be automatically applied.
- Disabled
**Note**: When you use an E-commerce catalog, you can only disable this setting. | 
      `automatic_add_on_enabled`
`card_list` | 
      If the single video or catalog video ad format is available, you can either enable (recommended) or disable auto-selection of interactive add-ons in the generated ads.
- To enable auto-selection of interactive add-ons, set `automatic_add_on_enabled` to `true`, and do not pass `card_list`. The system will automatically generate a Hotel Card, Flight Card, Destination Card, or Movie Card portfolio based on the specified catalog type via the returned `card_list`.
- To disable auto-selection of interactive add-ons, set `automatic_add_on_enabled` to `false`, and do not pass `card_list`. The returned `card_list` will be null.
**Note**: When you specify an E-commerce catalog through `catalog_id`, you can only set `automatic_add_on_enabled` to `false`.

To learn about Hotel Card, Flight Card, Destination Card, or Movie Card portfolios, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058). | 
     |
    
| 
      Call to action | 
      Any of the following options:
- Dynamic
- Standard | 
      `call_to_action_id`
`call_to_action_list` | 
      
- To use dynamic call to action, pass `call_to_action_id`.
- To use standard call to action, pass `call_to_action_list`. | 
     |
    
| 
      Disclaimer (Optional) | 
      Disabled or enabled | 
      `disclaimer_info` | 
      Not specified or specify valid values | 
     |
    
| 
      Third-party tracking settings
· Impression tracking URL for iOS (Optional) | 
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
· Click tracking URL for iOS (Optional) | 
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
· Impression tracking URL for Android (Optional) | 
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
· Click tracking URL for Android (Optional) | 
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
  

### List of values for `optimization_event` for Smart+ Catalog Ads

The following tables list the events supported for Smart+ Catalog Ads with Website and App Optimization.
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
### Customize the ad format combinations in Smart+ Catalog Ads
If you enable auto-selection of catalog creatives (`catalog_creative_toggle` is `true`), the system will automatically create ads using combinations of three possible formats: catalog carousel, catalog video, and single video.

The possible ad format combinations for your Smart+ Catalog Ads are illustrated in the following table.

```xtable
| Is the catalog carousel format available? {20%}| Is the catalog video format available? {20%}| Is the single video format available? {20%}| Ad format combination for your Smart+ Catalog Ads{40%} |
|---|---|---|---|
| ✅ | ❌ | ❌ | Catalog carousel only |
| ✅ | ❌ | ✅ | Catalog carousel and single video |
| ✅ | ✅ | ❌ | Catalog carousel and catalog video |
| ✅ | ✅ | ✅ | Catalog carousel, catalog video, and single video |
```

To ensure certain ad formats are available in Smart+ Catalog Ads, follow the instructions in the following table.

  
  
| 
    Ad format | 
    Ad format description | 
    How to ensure the ad format is available | 
    How to configure the parameters | 
   |
  

  
| 
    catalog carousel | 
    Display 2–20 products in a slideshow format. This format will showcase product images of up to 20 products from your catalog at a time | 
    The catalog needs to contain at least two images supported in Catalog Carousel Ads. | 
    Ensure that the catalog (`catalog_id`) contains at least two approved products. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least two.
- Carousel image selection scope: The product images for products in a catalog (`catalog_id`) will be dynamically chosen as images in the delivering Catalog Carousel Ads. The scope of product images to choose from is determined by the specified `product_specific_type` parameter:If `product_specific_type` is set to `ALL`, the system will dynamically choose Carousel images from all products in the catalog.
- If `product_specific_type` is set to `PRODUCT_SET`, the system will dynamically choose Carousel images from products in the specified product set (`product_set_id`).
- If `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`, the system will dynamically choose Carousel images from a customized product range consisting of up to 20 products (`product_ids`).
- Carousel image type:Use the main images of the products: By default, the main image URLs of the dynamically selected catalog products will be used as Carousel images. | 
   |
  
| 
    Specify a piece of music supported in Catalog Carousel Ads | 
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
- To ensure that at least one video template (video package) is bound to your catalog, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073).To learn about how to create video templates on TikTok Ads Manager, see [How to create video packages in a Catalog](https://ads.tiktok.com/help/article/how-to-create-video-packages-in-a-catalog).
- To retrieve video templates for your catalog via API, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073). | 
   |
  
| 
    single video | 
    Use specified video creatives to promote your products | 
    Specify additional videos | 
    Specify one to 30 videos (`video_info`) with cover images (`image_info`) and one to five ad texts (`title_list`). | 
   |

### Example

Request
```xcodeblock
(code http)
curl --location   --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/spc/create/' \
--header 'Access-Token: {{AccessToken}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "virtual_objective_type": "SALES",
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "WEB_AND_APP",
    "spc_type": "WEB_ALL_IN_ONE",
    "campaign_name": "{{campaign_name}}",
    "web_all_in_one_catalog_status": "OPEN",
    "product_source": "CATALOG",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "product_specific_type": "ALL",
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
    "promotion_type": "WEBSITE",
    "optimization_event": "SHOPPING",
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": {{conversion_bid_price}},
    "billing_event": "OCPM",
    "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "location_ids": [
        "1880251"
    ],
    "spc_audience_age": "18+",
    "exclude_age_under_eighteen": true,
    "landing_page_urls": [
        {
            "landing_page_url": "{{landing_page_url}}"
        }
    ],
    "catalog_creative_toggle": true,
    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER",
    "media_info_list": [
        {
            "media_info": {
                "music_info": {
                    "music_id": "{{music_id}}"
                }
            }
        }
    ],
    "title_list": [
        {
            "title": "{{title}}"
        }
    ],
    "automatic_add_on_enabled": true,
    "call_to_action_list": [
        {
            "call_to_action": "LEARN_MORE"
        }
    ]
}'
(/code)
```

Response

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "roas_bid": null,
        "app_download_url": null,
        "media_info_list": [
            {
                "media_info": {
                    "aigc_disclosure_type": null,
                    "identity_type": "CUSTOMIZED_USER",
                    "image_info": null,
                    "tiktok_item_id": null,
                    "identity_authorized_bc_id": "0",
                    "music_info": {
                        "music_id": "{{music_id}}"
                    },
                    "identity_id": "{{identity_id}}",
                    "video_info": null
                },
                "ad_material_id": "{{ad_material_id}}",
                "material_operation_status": "ENABLE"
            }
        ],
        "call_to_action_id": null,
        "title_list": [
            {
                "title": "{{title}}"
            }
        ],
        "campaign_id": "{{campaign_id}}",
        "app_promotion_type": null,
        "bid_price": null,
        "tracking_app_id": null,
        "create_time": "{{create_time}}",
        "deep_funnel_optimization_status": null,
        "identity_type": "CUSTOMIZED_USER",
        "utm_params": null,
        "sales_destination": "WEB_AND_APP",
        "app_id": null,
        "spc_audience_age": "18+",
        "disable_skan_campaign": null,
        "identity_id": "{{identity_id}}",
        "click_tracking_url": null,
        "budget": {{budget}},
        "bid_align_type": null,
        "schedule_end_time": "{{schedule_end_time}}",
        "deep_funnel_event_source": null,
        "product_specific_type": "ALL",
        "pixel_id": "{{pixel_id}}",
        "adgroup_secondary_status": "ADVERTISER_ACCOUNT_PUNISH",
        "deeplink": "",
        "click_attribution_window": "SEVEN_DAYS",
        "virtual_objective_type": "SALES",
        "is_advanced_dedicated_campaign": false,
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "deep_funnel_event_source_id": null,
        "exclude_age_under_eighteen": true,
        "product_ids": null,
        "optimization_event": "SHOPPING",
        "engaged_view_attribution_window": "ONE_DAY",
        "promotion_type": "WEBSITE",
        "landing_page_urls": [
            {
                "tiktok_item_id": null,
                "landing_page_url": "{{landing_page_url}}",
                "video_id": null
            }
        ],
        "deep_funnel_optimization_event": null,
        "carousel_image_labels": null,
        "automatic_add_on_enabled": true,
        "carousel_image_index": null,
        "app_type": null,
        "bid_type": "BID_TYPE_CUSTOM",
        "advertiser_id": "{{advertiser_id}}",
        "attribution_event_count": "EVERY",
        "app_name": null,
        "modify_time": "{{modify_time}}",
        "comment_disabled": false,
        "campaign_type": "REGULAR_CAMPAIGN",
        "call_to_action_list": [
            {
                "call_to_action": "LEARN_MORE"
            }
        ],
        "shopping_ads_video_package_id": "",
        "impression_tracking_url": null,
        "campaign_app_profile_page_state": null,
        "product_source": "CATALOG",
        "is_smart_performance_campaign": true,
        "excluded_audience_ids": null,
        "product_set_id": null,
        "promotion_target_type": null,
        "spc_type": "WEB_ALL_IN_ONE",
        "disclaimer_info": null,
        "zipcode_ids": null,
        "app_tracking_info_list": [
            {
                "app_type": "APP_ANDROID",
                "app_id": "{{app_id}}",
                "click_tracking_url": "{{click_tracking_url}}",
                "impression_tracking_url": "{{impression_tracking_url}}"
            },
            {
                "app_type": "APP_IOS",
                "app_id": "{{app_id}}",
                "click_tracking_url": "",
                "impression_tracking_url": ""
            }
        ],
        "share_disabled": false,
        "gender": "GENDER_UNLIMITED",
        "scheduled_budget": 0,
        "vbo_window": null,
        "card_list": [
            {
                "card_id": "{{card_id}}"
            }
        ],
        "shopping_ads_fallback_type": null,
        "view_attribution_window": "ONE_DAY",
        "app_config": [
            {
                "app_id": "{{app_id}}"
            },
            {
                "app_id": "{{app_id}}"
            }
        ],
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_PANGLE"
        ],
        "deeplink_type": null,
        "catalog_creative_toggle": true,
        "brand_safety_type": "EXPANDED_INVENTORY",
        "schedule_type": "SCHEDULE_START_END",
        "objective_type": "WEB_CONVERSIONS",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "billing_event": "OCPM",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "campaign_name": "{{campaign_name}}",
        "blocked_pangle_app_ids": null,
        "product_info": null,
        "languages": [],
        "skip_learning_phase": true,
        "conversion_bid_price": 1.2,
        "operation_status": "ENABLE",
        "special_industries": null,
        "campaign_secondary_status": "ADVERTISER_ACCOUNT_PUNISH",
        "deep_bid_type": null,
        "page_list": null,
        "video_download_disabled": false,
        "schedule_start_time": "{{schedule_start_time}}",
        "web_all_in_one_catalog_status": "OPEN",
        "catalog_id": "{{catalog_id}}",
        "optimization_goal": "CONVERT",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "location_ids": [
            "1880251"
        ],
        "promotion_website_type": "UNSET"
    }
}
(/code)
```
