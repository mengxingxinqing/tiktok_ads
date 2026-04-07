# Preview an ad or a creative

**Doc ID**: 1739403070695426
**Path**: API Reference/Creative Tools/Preview an ad or a creative

---

Use this endpoint to preview an ad or a creative.

## Comparing v1.2 and v1.3
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/creative/ads_preview/create/|/v1.3/creative/ads_preview/create/|
|Request parameter name|`material_type` 
 `dpa_video_package_id`
 `placement` |`preview_type` 
 `shopping_ads_video_package_id`
`placements`|
|Request parameter data type | `advertiser_id`: number  
`bc_id`: number 
 `ad_id`: number
 `catalog_id`: number 
 `product_ids`: number[] 
 `call_to_action_id`: number | `advertiser_id`: string  
 `bc_id`: string 
 `ad_id`: string
 `catalog_id`: string 
 `product_ids`: string[] 
 `call_to_action_id`: string |
|New request parameters|/|`identity_id`
 `identity_type`
`identity_authorized_bc_id`
 `objective_type`
`shopping_ads_type`
 `promotion_type`
`dynamic_format`
`card_id`
`card_type`
`product_set_id`
`sku_ids`
`product_specific_type`
`item_group_ids`
`vertical_video_strategy`
`card_tags`
`card_show_price`
`card_image_id`
`page_id`
`dynamic_destination`
`instant_product_page_used`
`catalog_authorized_bc_id`
`placement`(in **Preview existing ads** and **Preview ads that you plan to create**)
`preview_format`
`ad_format`
`image_id`
`carousel_image_index`(in **Preview ads that you plan to create**)
`music_id`(in **Preview ads that you plan to create**)
`is_smart_performance_campaign`(in **Preview ads that you plan to create**)
`image_ids`(in **Preview ads that you plan to create**) 
`product_source`
`store_id`
`store_authorized_bc_id`
`showcase_products`
`vehicle_ids`
`auto_disclaimer_types`
`end_card_cta`
`tiktok_subplacement`(in **Preview ads that you plan to create**)|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/

**Method** POST

**Header**

```xtable
|Field|Data Type|Description|
|--- |--- |--- |
|Content-Type {Required}|string|Request content type. Allowed Value: `application/json`.  |
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

### Preview ads that you plan to create

This allows you to preview your ad before creating it. 

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|-|-|-|
| advertiser_id {Required} | string | Advertiser ID. 

**Note**: You need to have Operator or Admin permission for the ad account. To check your permission for an ad account, use [/bc/asset/get/](https://business-api.tiktok.com/portal/docs?id=1739432717798401). The returned `advertiser_role` should be `ADMIN` or `OPERATOR`. |
| preview_type {Required} | string | Preview type.
To preview ads by ads creation parameters, use `ADS_CREATION`. |
| objective_type {Required}|string| Advertising objective. For enum values and descriptions, see [Objectives](https://ads.tiktok.com/marketing_api/docs?id=1737585562434561). 
**Note**: Currently the supported objectives are: `REACH`,`TRAFFIC`,  `VIDEO_VIEWS`, `ENGAGEMENT`, `APP_PROMOTION`, `LEAD_GENERATION`, `WEB_CONVERSIONS`, `PRODUCT_SALES`, and `RF_REACH`. |
| is_smart_performance_campaign| boolean|Whether the campaign is a Smart+ Campaign.
Default value: `false`.
**Note**: This field can only be set to `false` when any of the following conditions is met:
- `ad_fomat` is set to `CAROUSEL_ADS` or `CATALOG_CAROUSEL`.
- `placement` is set to `PLACEMENT_PANGLE` or `ALL`. 
- `objective_type` is set to `TRAFFIC`, `REACH`, `VIDEO_VIEWS`, or `PRODUCT_SALES`.  |
| placement | string |The app where you want to deliver your ads. 
 When `ad_format` is set to `CAROUSEL_ADS` or `CATALOG_CAROUSEL`,  specify this field as `PLACEMENT_TIKTOK`, or do not pass this field.

 Enum values: 
- `PLACEMENT_TIKTOK`: Supported only when `objective_type` is `REACH`,`TRAFFIC`,  `VIDEO_VIEWS`, `ENGAGEMENT`, `APP_PROMOTION`, `LEAD_GENERATION`, `WEB_CONVERSIONS`,  or `PRODUCT_SALES`.
- `PLACEMENT_PANGLE`: Supported only when `objective_type` is `TRAFFIC`, `LEAD_GENERATION` (only when `promotion_type` is `LEAD_GENERATION`), `APP_PROMOTION`, or `WEB_CONVERSIONS`. 
- `PLACEMENT_GLOBAL_APP_BUNDLE`: Suppported only when `objective_type` is `REACH`.
- `ALL`: Supported only when `objective_type` is `TRAFFIC`, `LEAD_GENERATION` (only when `promotion_type` is `LEAD_GENERATION`), `APP_PROMOTION`, or `WEB_CONVERSIONS`. |
|tiktok_subplacement|string|Valid only when the following conditions are both met:
- `objective_type` is `REACH`.
- `placement` is `PLACEMENT_TIKTOK`.
The subplacements within TikTok for your ads, allowing you to choose where your ads will appear.

Enum values:
- `LEMON8`: Lemon8, a community app for lifestyle content, focusing on real-life experiences, tips, guides, and product reviews. By including Lemon8 as a subplacement, your ads will appear in its For You feed, Search feed, and Immersive Video feed. [Learn more about Lemon8](https://ads.tiktok.com/help/article/about-lemon8-in-tiktok-ads-manager). 
- `UNSET`: Unset.|
| preview_format | string | Based on the `placement` you've selected, the allowed preview formats are different.
- When `placement` is `PLACEMENT_TIKTOK`, the allowed preview formats are:  `IN_FEED`: In-feed. Ads will be placed in the For You feed and might also be placed in Profile Page and Following feeds.
- `SEARCH_RESULTS`: Search result. 
- `SEARCH_FEED`: Search feed. 
- `TIKTOK_LITE`: TikTok Lite, a streamlined version of TikTok that features a smaller app size and faster video loading speed. The TikTok Lite subplacement is currently available for Japan or South Korea as targeting locations.
- `PRODUCT_SEARCH`: Search (Shopping Center). Show your products in the Shop Tab search results, as well as general search results in the TikTok App. Learn more about [Shop Tab placements for Shop Ads](https://ads.tiktok.com/help/article/about-onsite-shopping-placements).
- `PRODUCT_SHOP_CENTER`: Recommendations (Shopping Center). Show your products to people who are likely to buy them in a Recommended for you section. 
- When `placement` is `PLACEMENT_TIKTOK` and `tiktok_subplacement` is `LEMON8`, the allowed preview formats are:`IN_FEED`: In-feed. The ad will be displayed in a full-screen format, providing an immersive and undistracted viewing experience.
- `IN_FEED_TWO_COLUMNS`: In feed (two columns). The ad will be displayed in a two-column layout within the For You feed, allowing multiple content pieces to be displayed side by side. 
- When `placement` is `PLACEMENT_GLOBAL_APP_BUNDLE`, the allowed preview formats are:`APP_OPEN`: App Open. The ad will be displayed when the Capcut app is opened, marking the beginning of each user session. This premium full-screen placement ensures visibility as the first screen users see.
- `IN_FEED`: In-feed. The ad will be displayed in a full-screen format, providing an immersive and undistracted viewing experience.
- `IN_FEED_TWO_COLUMNS`: In feed (two columns). The ad will be displayed in a two-column layout within the For You feed, allowing multiple content pieces to be displayed side by side. Default value: `IN_FEED`. 

**Note**: 
- The values `SEARCH_FEED` and `TIKTOK_LITE` are valid only when the following conditions are met: `objective_type` is `REACH`, `VIDEO_VIEWS`, or `ENGAGEMENT`.
- `placement` is `PLACEMENT_TIKTOK`.
- The values `PRODUCT_SEARCH` and `PRODUCT_SHOP_CENTER` are only available for Video Shopping Ads and Product Shopping Ads. 
- When `placement` is `PLACEMENT_PANGLE`, this field is not supported.|
| shopping_ads_type {+Conditional}  | string | Required when `objective_type` is `PRODUCT_SALES` and `catalog_id` is not specified.

Shopping ads type. 

Enum values: 
- `VIDEO`: Video Shopping Ads. 
- `LIVE`: Live Shopping Ads.
- `PRODUCT_SHOPPING_ADS`: Product Shopping Ads.  
When `ad_format` is set to `CATALOG_CAROUSEL`, specify this field as `VIDEO`, or do not pass this field.|
| product_source {+Conditional} | string | Required only for Video Shopping Ads and Product Shopping Ads. 

Product source where you want to get products for promotion. 

Enum values: `STORE` (TikTok Shop),`SHOWCASE`(TikTok Showcase). 
- For Video Shopping Ads, you can set this field to `STORE` or `SHOWCASE`.
- For Product Shopping Ads, set this field to `STORE`. |
| store_id {+Conditional} | string | 
- Required in any of the following scenarios:`shopping_ads_type` is `VIDEO` and `product_source` is `STORE`.
- `shopping_ads_type` is `PRODUCT_SHOPPING_ADS` and `product_source` is `STORE`. 
- Optional when `shopping_ads_type` is `LIVE`.  
ID of the TikTok Shop.

 To get the TikTok Shop ID, use [/bc/asset/get/](https://business-api.tiktok.com/portal/docs?id=1739432717798401) and set `asset_type` to `TIKTOK_SHOP`. The returned `asset_id` will be the TikTok Shop ID. |
| store_authorized_bc_id {+Conditional} | string | Required when `store_id` is passed.

 ID of the Business Center that is authorized to access the TikTok Shop (`store_id`). |
| showcase_products {+Conditional} | object[] | Required when `shopping_ads_type` is `VIDEO` and `product_source` is `SHOWCASE`.

 See [Create Video Shopping Ads with products from Showcase](https://business-api.tiktok.com/portal/docs?id=1759232259360770) to learn more. 

The list of Showcase products that you want to use in your ad. 

 Max size: 20.

 You can get the available Showcase products via [/showcase/product/get/](https://business-api.tiktok.com/portal/docs?id=1759233576199169). |
#| item_group_id {+Conditional} | string | Required when `showcase_products` is passed. 

SPU ID of the product. |
#| store_id {+Conditional} | string | Required when `showcase_products` is passed. 

The ID of the TikTok Shop that the product (`item_group_id`) belongs to.|
| promotion_type {+Conditional} |string|Promotion type. You can decide where you'd like to promote your products using this field. 

 Enum values: 
- `APP_ANDROID`: Android application.
- `APP_IOS`: iOS application.
- `WEBSITE`: landing page.
- `LEAD_GENERATION`: Instant Form or Website.
- `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`: TikTok direct messages.
- `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`: instant messaging apps.
-  `LEAD_GEN_CLICK_TO_CALL`: phone call.  
**Note**: The following enum values are valid only when `objective_type` is `LEAD_GENERATION`: 
- `LEAD_GENERATION`
- `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` 
-  `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE` 
- `LEAD_GEN_CLICK_TO_CALL` |
| identity_id {Required} | string | Identity ID.

If you are not using Spark Ads, `identity_id` and `identity_type` (`CUSTOMIZED_USER`) can be used for better management of ad information. |
| identity_type {Required} | string| Identity type. 

Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`. 
Use `CUSTOMIZED_USER` for custom identity and use `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT` in Spark Ads. 
For details about identities, see [Identities](https://ads.tiktok.com/marketing_api/docs?id=1738958351620097).

- When `ad_format` is `CATALOG_CAROUSEL`, you can only set this field to `CUSTOMIZED_USER`.
-  If `objective_type` is `LEAD_GENERATION`:  When `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`, Spark Ads must be used and `identity_type` must be `TT_USER` or `BC_AUTH_TT`. 
-  When `promotion_type` is not `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`, both Spark Ads & non-Spark Ads are supported, so `identity_type` can be set to any of the enum values.  
-  If `objective_type` is `ENGAGEMENT`, only Spark Ads are supported and `identity_type` must be `AUTH_CODE`, `TT_USER` or `BC_AUTH_TT`. |
| identity_authorized_bc_id {+Conditional} |string|Required when `identity_type` is `BC_AUTH_TT`. 
ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
| ad_format{Required} |string|Ad format.

-  For single video ads, set this field to `SINGLE_VIDEO`. 
-  For single image ads, set this field to `SINGLE_IMAGE`. Supported only on Pangle.
- For TikTok Standard Carousel ads, set this field to `CAROUSEL_ADS`. To use this ad format, you need to set `objective_type` to `REACH`, `WEB_CONVERSIONS`, `APP_PROMOTION`, `LEAD_GENERATION` or `TRAFFIC`. 
- For TikTok Catalog Carousel ads, set this field to `CATALOG_CAROUSEL`.
See [here](https://business-api.tiktok.com/portal/docs?id=1766217791987713) to learn about the steps of creating TikTok Carousel Ads. 
-  For Live Shopping Ads, set this field to `LIVE_CONTENT`. |
| video_id {+Conditional} | string | Video ID. 
Required when `ad_format` is `SINGLE_VIDEO`.
 Not supported when `ad_format` is `SINGLE_IMAGE`, `CAROUSEL_ADS` or `CATALOG_CAROUSEL`.

- To create video [Spark Ads](https://ads.tiktok.com/marketing_api/docs?id=1739470744631298) using Spark Ads Push or create video Non-Spark Ads, use `video_id`. You can find video IDs using [/file/video/ad/search/](https://ads.tiktok.com/marketing_api/docs?id=1740050472224769). 
- To create video Spark Ads using Spark Ads Pull, use `tiktok_item_id` to specify the TikTok post ID. |
| image_ids{+Conditional} | string[] | Required in any of the following scenarios:
-  `ad_format` is `SINGLE_IMAGE`.
-  `ad_format` is `CAROUSEL_ADS` and you want to create Standard Carousel Spark Ads via Spark Ads Push or Standard Carousel Non-Spark Ads.  
- `ad_format` is `CATALOG_CAROUSEL`, `catalog_enabled` is set to `true`, and an Auto-Model catalog is specified through `catalog_id`.
A list of image IDs (images used in an ad or as a video cover). 

- When `ad_format` is set to `CAROUSEL_ADS`, the size range for this field is [1, 35], and the sequence of the image IDs specified via this field is the order in which the images are shown in the Carousel Ads.  
 See [Create Carousel Ads](https://ads.tiktok.com/marketing_api/docs?id=1766217791987713) to learn about the requirements for images that can be used in TikTok Carousel Ads. 
- When `ad_format` is set to `CATALOG_CAROUSEL` and `catalog_enabled` is set to `true`, the value of this field will be used as the summary photo in the Automotive Ads for Models (only one value is allowed).
To learn about the requirements for the summary photo that can be used in Automotive Ads for Models, see [Automotive Ads for Models](https://business-api.tiktok.com/portal/docs?id=1829635758164994).
- When `ad_format` is set to `SINGLE_IMAGE`, you can only assign one image ID to this field.
  To learn about the requirements for images that can be used in single image ads, see [Create single image ads](https://business-api.tiktok.com/portal/docs?id=1777633230937090).|
| end_card_cta {+Conditional}|string[]|Required when the following conditions are met:
- `objective_type` is `LEAD_GENERATION`.
- `catalog_enabled` is `true`.
- An Auto-Model catalog is specified through `catalog_id`.
- `ad_format` is `CATALOG_CAROUSEL`.
Call-to-action for the end card (`image_ids`) of an [Automotive Carousel Ad for Models](https://business-api.tiktok.com/portal/docs?id=1829635758164994#item-link-Ad%20format%20as%20Catalog%20Carousel).

Enum values:
- `SEARCH_INVENTORY` (Recommended): Search inventory.
- `LEARN_MORE`: Learn more.
- `SHOP_NOW`: Shop now.
- `SIGN_UP`: Sign up.
- `CONTACT_US`: Contact us.
- `BOOK_NOW`: Book now.
- `READ_MORE`: Read more.
- `VIEW_MORE`: View now.
- `ORDER_NOW`: Order now. |
| music_id{+Conditional}| string|  Required in any of the following scenarios:
- `ad_format` is `CAROUSEL_ADS` and you create Standard Carousel Spark Ads via Spark Ads Push or Standard Carousel Non-Spark Ads. 
- `ad_format` is `CATALOG_CAROUSEL`.  
The ID of the piece of music that you want to use in the TikTok Carousel Ad.|
|tiktok_item_id {+Conditional}|string|
- Required when `identity_type` is `AUTH_CODE` or `BC_AUTH_TT` and you want to create Spark Ads through Spark Ads Pull.
- Not supported when `identity_type` is `CUSTOMIZED_USER`. 
The ID of the TikTok post to be used as Spark Ad. 
 
To learn more about Spark Ads, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298). 
 
 Pass in the `item_id` you get from the response of the [/tt_video/info/](https://ads.tiktok.com/marketing_api/docs?id=1738376324021250) or [/identity/video/get/](https://ads.tiktok.com/marketing_api/docs?id=1740218475032577) endpoint. 

**Note**: By using Spark Ads, you confirm that you have the rights to use the music in the videos for commercial purposes.|
| carousel_image_index | integer | Valid only when you set `ad_format` to `CATALOG_CAROUSEL`, and a list of additional images has been configured for the specified products. 
 
The index that specifies the additional images to be used in the VSA Carousel ad. If this field is not passed, the main images of catalog products will be used in the VSA Carousel ad.
 Value range: [0, 9]. 
-  The number you set via this field represents the position of the product image within the additional image list (`additional_image_urls`) for each catalog product. For instance, `carousel_image_index` = **1** means that you will use all the images specified via the **second** image URL in each `additional_image_urls` value as images in the Carousel Ad. You can retrieve the additional images configured for a product via `additional_image_urls` returned by [/catalog/product/get/](https://ads.tiktok.com/marketing_api/docs?id=1740564136678402). 
-  If you set a number greater than the total number of additional Image URLs specified for the product, this field will be ignored, and the main image (`image_url`) for the product will be used. You can retrieve the main image for a product via `image_url` returned by [/catalog/product/get/](https://ads.tiktok.com/marketing_api/docs?id=1740564136678402).  |
| ad_text {+Conditional}| string | An ad text. It is shown to your audience as part of your ad creative, to deliver the message you intend to communicate to them. If you don't know how to create effective ad texts, you can try the [Smart Text](https://ads.tiktok.com/marketing_api/docs?id=1739084248002626) feature, which generates ad text recommendations based on the industry and language. 
- This field is required if your ad is non-Spark Ads. 
- Ad text must be 1-100 characters long and cannot contain emoji.
- Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character.|
| call_to_action {+Conditional} | string | Call-to-action text. 

For TikTok ads, either this field or `call_to_action_id` must be specified. If both are specified, this field will be ignored. 
For enum values, see [Enumeration - Call-to-Action](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
For live shopping ads, the call to action must be `WATCH_LIVE`. 

**Note**
- If `objective_type` is `REACH`or `VIDEO_VIEW`, and `landing_page_url` or `page_id` has been specified, then either `call_to_action` or `call_to_action_id` is required. 
- If `objective_type` is `APP_PROMOTION`, `WEB_CONVERSIONS`, or `TRAFFIC`, then either `call_to_action` or `call_to_action_id` is required.
- If `objective_type` is `LEAD_GENERATION`:  When `promotion_type` is `LEAD_GENERATION`, either `call_to_action` or `call_to_action_id` is required.
-  When `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`, `call_to_action` is required and must be set to `SEND_MESSAGE`.
-  When `promotion_type` is `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`, `call_to_action` is required and cannot be set to `CALL_NOW`. 
-  When `promotion_type` is `LEAD_GEN_CLICK_TO_CALL`, `call_to_action` is required. 
- If `objective_type` is `PRODUCT_SALES`, `call_to_action` is required.|
| call_to_action_id {+Conditional} | string | The ID of the CTA portfolio that you want to use in your ads. A CTA portfolio is a group of auto-optimized CTAs. If both this field and `call_to_action` are specified, `call_to_action` will be ignored. For details about auto-optimized CTAs, see [CTA recommendations > Dynamic CTAs](https://ads.tiktok.com/marketing_api/docs?id=1740307296329730).
**Note**
- If `objective_type` is `REACH`or `VIDEO_VIEW`, and `landing_page_url` or `page_id` has been specified, then either `call_to_action` or `call_to_action_id` is required. 
- If `objective_type` is `APP_PROMOTION`, `WEB_CONVERSIONS`, or `TRAFFIC`, then either `call_to_action` or `call_to_action_id` is required.
-  If `ad_format` is `CAROUSEL_ADS` or `CATALOG_CAROUSEL`, `call_to_action_id` is not supported.
- If `objective_type` is `LEAD_GENERATION`:  When `promotion_type` is `LEAD_GENERATION`, either `call_to_action` or `call_to_action_id` is required.
-  When `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`, `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`, or `LEAD_GEN_CLICK_TO_CALL`, `call_to_action_id` is not supported.|
| card_id | string | Creative portfolio ID. 

Pass the ID of one of the following creative portfolio types:
- Display Card.
-  Website info card.
- Product Card.
- Product Tiles.
- Countdown Sticker. 
- Gift Code Sticker.
- Gesture.
- Superlike. 
To create a creative portfolio, use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).

- To learn about how to get the ID of a Display Card, Website info card, Product Card, or Product Tiles portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058).
- To learn about how to get the ID of a Countdown Sticker or Giftcode Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177).
- To learn about how to get the ID of a Gesture or Superlike portfolio, see [Premium Add-ons](https://business-api.tiktok.com/portal/docs?id=1749019676181505).
**Note**: You can use this field in the following scenarios. 
-  When `objective_type`= `REACH`, `promotion_type`= `WEBSITE`, `placements`= `PLACEMENT_TIKTOK`, and `ad_format` = `SINGLE_VIDEO`.
- When `objective_type`= `TRAFFIC`, `promotion_type`= `WEBSITE`, `placements`= `PLACEMENT_TIKTOK`, and `ad_format` = `SINGLE_VIDEO`.
- When `objective_type`= `VIDEO_VIEWS`, `placements`= `PLACEMENT_TIKTOK`, and `ad_format` = `SINGLE_VIDEO`.
- When `objective_type`=  `ENGAGEMENT`, you can only specify a Countdown Sticker portfolio through this field.
- When `objective_type`= `APP_PROMOTION`, `promotion_type`= `WEBSITE`,  `placements`= `PLACEMENT_TIKTOK`,  and `ad_format` = `SINGLE_VIDEO`.
- When `objective_type`= `LEAD_GENERATION`, you can only specify a Display Card portfolio through this field. 
- When `objective_type`=`WEB_CONVERSIONS`, `placements`= `PLACEMENT_TIKTOK`, and `ad_format` = `SINGLE_VIDEO`.
- When `objective_type`=`PRODUCT_SALES`, `placements`= `PLACEMENT_TIKTOK`, and `ad_format` = `SINGLE_VIDEO`.|
| landing_page_url {+Conditional} | string | Landing page URL. 
**Note**If `objective_type` is  `APP_PROMOTION`, `WEB_CONVERSIONS` or `TRAFFIC`, and `promotion_type` is `WEBSITE`, then either `page_id` or `landing_page_url` is required.
- If `objective_type` is `APP_PROMOTION` or `TRAFFIC`, and `promotion_type` is `APP_ANDROID`/`APP_IOS` , then neither `page_id` nor `landing_page_url` can be used.|
| page_id {+Conditional} | string | Used to preview TikTok Instant Page. 
**Note**If `objective_type` is  `APP_PROMOTION`, `WEB_CONVERSIONS` or `TRAFFIC`, and `promotion_type` is `WEBSITE`, then either `page_id` or `landing_page_url` is required.
- If `objective_type` is  `APP_PROMOTION`, or `TRAFFIC`, and `promotion_type` is `APP_ANDROID`/`APP_IOS` , then neither `page_id` nor `landing_page_url` can be used.
-  If `ad_format` is `CATALOG_CAROUSEL`, this field is not supported.|
| catalog_id {+Conditional} | string | Product catalog ID. Products whose links are shown in the ad are from this catalog. 
When `ad_format` is `CATALOG_CAROUSEL`, this field is required.

**Note**: You need to have Ad promotion or Catalog management permission for the catalog. To check your permission for a catalog, use [/bc/asset/get/](https://business-api.tiktok.com/portal/docs?id=1739432717798401). The returned `catalog_role` should be `ADMIN` or `AD_PROMOTE`.|
|product_specific_type{+Conditional} |string|Different dimensions to choose products. 

When `ad_format` is `CATALOG_CAROUSEL`, this field is required. The Carousel images will be dynamically chosen from the images for the specified catalog products, and the specified product range needs to include at least two products.

Enum values: 
- `ALL`: Allow TikTok to dynamically choose from all catalog products.
- `PRODUCT_SET`: Specify a product set. TikTok will dynamically choose products from this set.
- `CUSTOMIZED_PRODUCTS`:Specify up to 20 products from your catalog. 

- If this field is set to `ALL`, you don't need to input `sku_ids` or  `item_group_ids`  or `product_set_id`.  
- If this field is set to `PRODUCT_SET`, you need to pass in either `item_group_ids` or `product_set_id`.
- If this field is set to `CUSTOMIZED_PRODUCTS`, you need to pass in `sku_ids` or `vehicle_ids`.
**Note**:
- When `shopping_ads_type` is `PRODUCT_SHOPPING_ADS` and `product_source` is `STORE`, you can set this field to `ALL` or `CUSTOMIZED_PRODUCTS`. If this field is set to `ALL`, you don't need to input `sku_ids`,`vehicle_ids`, `item_group_ids`, and `product_set_id`. 
- If this field is set to `CUSTOMIZED_PRODUCTS`, `item_group_ids` is required.  
- When `shopping_ads_type` is `VIDEO` and `product_source` is `STORE`, specify the products through `item_group_ids`. 
- When `shopping_ads_type` is `VIDEO` and `product_source` is `SHOWCASE`, specify the products through `showcase_products`.
- When `shopping_ads_type` is `LIVE`, you don't need to specify the products. |
|item_group_ids {+Conditional}|string[]|
- If `catalog_id` is specified and `product_specific_type` is set to `PRODUCT_SET`, you need to pass in either `item_group_ids` or `product_set_id`.
- Required in any of the following scenarios:`shopping_ads_type` is `VIDEO` and `product_source` is `STORE`. 
-  `shopping_ads_type` is `PRODUCT_SHOPPING_ADS`,`product_source` is `STORE`, and `product_specific_type` is `CUSTOMIZED_PRODUCTS`.
Product SPU IDs. |
|product_set_id {+Conditional}|string|If `catalog_id` is specified and `product_specific_type` is set to `PRODUCT_SET`, you need to pass in either `item_group_ids` or `product_set_id`.

The ID of the product set.|
| sku_ids {+Conditional}|string[]| Required when the following conditions are both met:
- An E-commerce catalog is specified through `catalog_id`.
- `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`.
IDs of the SKUs.

Max size: 20. |
| vehicle_ids{+Conditional}|string[]|Required when the following conditions are both met:
- An Auto-Model catalog is specified through `catalog_id`.
- `product_specific_type` is set to `CUSTOMIZED_PRODUCTS`.
IDs of vehicles.

Max size: 20. |
| auto_disclaimer_types | string[] |Valid only when the following conditions are met:
- `objective_type` is `LEAD_GENERATION`.
- `catalog_enabled` is true.
- An Auto-Model catalog is specified through `catalog_id`.
- `ad_format` is `CATALOG_CAROUSEL`.
The type of disclaimer to show in the [Automotive Carousel Ads for Models](https://business-api.tiktok.com/portal/docs?id=1829635758164994#item-link-Ad%20format%20as%20Catalog%20Carousel).

Enum values:
- `EMISSION`: Emission disclaimer.
- `DISCOUNT`: Discount or offer disclaimer.
Max size: 1. |
| catalog_authorized_bc_id | string | Same as `bc_id`. Please use this field when previewing catalog items. |
|dynamic_format|string|Not supported when `ad_format` is `CAROUSEL_ADS` or `CATALOG_CAROUSEL`.
Dynamic format. 
Enum values: 
- `UNSET`: Unset.
- `DYNAMIC_CREATIVE`: smart creative. To display different videos, product cards and destinations to each person based on purchase intent, maximizing conversions.  |
|vertical_video_strategy|string|Not supported when `ad_format` is `CAROUSEL_ADS` or `CATALOG_CAROUSEL`.

Video strategy.

Enum values:
- `SINGLE_VIDEO`: Use a video creative to promote your products.
- `CATALOG_VIDEOS`: Generate a dynamic video based on information from the product catalog.
- `LIVE_STREAM`: Use livestream to promote your products. Supported only for Live Shopping Ads with ad format as Real-time LIVE.
- `UNSET`: Unset.It must be `UNSET` if `dynamic_format` = `DYNAMIC_CREATIVE`.|
|shopping_ads_video_package_id|string| Product video package ID. 
Use the [/catalog/video/get/](https://ads.tiktok.com/marketing_api/docs?id=1740574099715073) endpoint to get video package IDs.|
|shopping_ads_fallback_type {+Conditional}|string| In the Shopping Ads retargeting scenario, the fallback website type when the deeplink fails to be triggered.

Enum values:
- `DEFAULT`:  Unset.
- `CUSTOM`: Custom link. Fall back to the web page link you provide. You need to pass in `landing_page_url` at the same time.
-  `SHOPPING_ADS`:  Product link. Fall back to the web page link you've provided for each product in the catalog. 
The `SHOPPING_ADS` value is not supported when the following conditions are met: 
-  `shopping_ads_type` is set to `VIDEO` (Video Shopping Ads)
-  `product_source` is set to `CATALOG`
- `ad_format` is set to `SINGLE_VIDEO` and `vertical_video_strategy` is set to `SINGLE_VIDEO` or `ad_format` is set to `CATALOG_CAROUSEL` 
To learn about the supported scenarios for fallback types, see the "[Deeplink - Availability - Fallback type](https://business-api.tiktok.com/portal/docs?id=1779541971843073#item-link-Fallback type)" section.|
|dynamic_destination|string|Not supported when `ad_format` is `CAROUSEL_ADS` or `CATALOG_CAROUSEL`.
Dynamic destination strategy.
Enum values:
- `DLP`: Dynamic Landing Page. Displaying different destinations including a custom website or Instant Product Page to each person based on their profile, behavior, and intent to maximize ad conversion.
-  `UNSET`: Unset. |
|instant_product_page_used|boolean|Not supported when `ad_format` is `CAROUSEL_ADS` or `CATALOG_CAROUSEL`.
Whether to use TikTok Instant Product Page, an auto-generated TikTok instant page that displays a range of products and provides a native experience landing page. 
- When `dynamic_destination `= `DLP`, you don't need this parameter. 
- When `dynamic_destination` = `UNSET`, you can set this field to `true` to use TikTok Instant Product Page, and you don't need to pass in `page_id`.|
```

#### Example
##### Preview Video Shopping Ads with product source as TikTok Shop
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "shopping_ads_type": "VIDEO",
    "product_source": "STORE",
    "placement": "PLACEMENT_TIKTOK",
    "identity_id": "{{identity_id}}",
    "identity_type": "TT_USER",
    "ad_format": "SINGLE_VIDEO",
    "item_group_ids": ["{{item_group_id_1}}", "{{item_group_id_2}}"],
    "vertical_video_strategy": "SINGLE_VIDEO",
    "video_id": "{{video_id}}",
    "ad_text": "{{ad_text}}"
}'
(/code)
```
##### Preview Video Shopping Ads with product source as Showcase
```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "shopping_ads_type": "VIDEO",
    "product_source": "SHOWCASE",
    "placement": "PLACEMENT_TIKTOK",
    "identity_id": "{{identity_id}}",
    "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
    "identity_type": "BC_AUTH_TT",
    "showcase_products" : [
        {
            "item_group_id": "{{item_group_id_1}}",
            "store_id": "{{store_id_1}}"
        },
        {
            "item_group_id": "{{item_group_id_2}}",
            "store_id": "{{store_id_2}}"
        }
    ],
    "ad_format": "SINGLE_VIDEO",
    "vertical_video_strategy": "SINGLE_VIDEO",
    "video_id": "{{video_id}}",
    "call_to_action": "BOOK_NOW",
    "ad_text": "{{ad_text}}",
    "card_id": "{{card_id}}"
}'
(/code)
```
##### Preview Product Shopping Ads

```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "shopping_ads_type": "PRODUCT_SHOPPING_ADS",
    "product_source": "STORE",
    "store_id": "{{store_id}}",
    "placement": "PLACEMENT_TIKTOK",
    "product_specific_type": "ALL",
    "item_group_ids": ["{{item_group_id_1}}", "{{item_group_id_2}}"]
}'
(/code)
```
##### Preview Live Shopping Ads with ad format as Single Video

```xcodeblock
(code curl http)
curl --location  --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "shopping_ads_type": "LIVE",
    "placement": "PLACEMENT_TIKTOK",
    "identity_id": "{{identity_id}}",
    "identity_type": "TT_USER",
    "ad_format": "LIVE_CONTENT",
    "vertical_video_strategy": "SINGLE_VIDEO",
    "video_id": "{{video_id}}",
    "ad_text": "{{ad_text}}"
}'
(/code)
```
##### Preview Live Shopping Ads with ad format as Real-time LIVE

```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "placement": "PLACEMENT_TIKTOK",
    "identity_id": "{{identity_id}}",
    "identity_type": "TT_USER",
    "shopping_ads_type": "LIVE",
    "ad_format": "LIVE_CONTENT",
    "vertical_video_strategy": "LIVE_STREAM"
}'
(/code)
```

##### Preview using ALL placements
```xcodeblock
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER",
    "objective_type": "TRAFFIC",
    "ad_format": "SINGLE_VIDEO",
    "promotion_type": "WEBSITE",
    "ad_text": "{{ad_text}}",
    "call_to_action": "SHOP_NOW",
    "placement": "ALL",
    "video_id": "{{video_id}}"
}'
(/code)
```
##### Preview using a single placment
```xcodeblock
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER",
    "objective_type": "TRAFFIC",
    "ad_format": "SINGLE_VIDEO",
    "promotion_type": "WEBSITE",
    "ad_text": "{{ad_text}}",
    "call_to_action": "SHOP_NOW",
    "placement": "PLACEMENT_TIKTOK",
    "preview_format": "SEARCH_RESULTS",
    "video_id": "{{video_id}}"
}'
(/code)
```

##### Preview non-VSA Carousel Ads you plan to create
```xcodeblock
(code curl http)
curl --location 'https://business-api.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "APP_PROMOTION",
    "is_smart_performance_campaign": false,
    "promotion_type": "APP_ANDROID",
    "placement": "PLACEMENT_TIKTOK",
    "ad_format": "CAROUSEL_ADS",
    "ad_text": "{{ad_text}}",
    "call_to_action": "DOWNLOAD_NOW",
    "instant_product_page_used": false,  
    "image_ids": ["{{image_id}}", "{{image_id}}"],
    "music_id": "{{music_id}}",
    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER"
}'
(/code)
```

##### Preview VSA Carousel Ads you plan to create
```xcodeblock
(code curl http)
# VSA Carousel Ads with images from All products
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "placement": "PLACEMENT_TIKTOK",
    "preview_format": "IN_FEED",
    "ad_format": "CATALOG_CAROUSEL",
    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER",
    "call_to_action": "SHOP_NOW",
    "music_id": "{{music_id}}",
    "catalog_id": "{{catalog_id}}",
    "product_specific_type": "ALL",
    "carousel_image_index": 2,
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "ad_text": "{{ad_text}}",
}'

# VSA Carousel Ads with images from Customized products
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "placement": "PLACEMENT_TIKTOK",
    "preview_format": "IN_FEED",
    "ad_format": "CATALOG_CAROUSEL",

    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER",
        "call_to_action": "SHOP_NOW",
    "music_id": "{{music_id}}",
    "catalog_id": "{{catalog_id}}",
    "product_specific_type": "CUSTOMIZED_PRODUCTS",
    "sku_ids": [
        "{{sku_id}}",
        "{{sku_id}}"
    ],
    "carousel_image_index": 0,
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "ad_text": "AD_TEXT Testing"
}'

# VSA Carousel Ads with images from Product Set
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "objective_type": "PRODUCT_SALES",
    "placement": "PLACEMENT_TIKTOK",
    "preview_format": "IN_FEED",
    "ad_format": "CATALOG_CAROUSEL",
    "identity_id": "{{identity_id}}",
    "identity_type": "CUSTOMIZED_USER",
    "call_to_action": "SHOP_NOW",
    "music_id": "{{music_id}}",
    "catalog_id": "{{catalog_id}}",
    "product_specific_type": "PRODUCT_SET",
    "product_set_id": "{{product_set_id}}",
    "carousel_image_index": 0,
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "ad_text": "AD_TEXT Testing"
}'
(/code)
```

### Preview existing ads

```xtable
|Field|Data Type|Description|
|---|---|---|
|advertiser_id {Required}|string| Advertiser ID. 

**Note**: 
- You need to have Operator or Admin permission for the ad account. To check your permission for an ad account, use [/bc/asset/get/](https://business-api.tiktok.com/portal/docs?id=1739432717798401). The returned `advertiser_role` should be `ADMIN` or `OPERATOR`. 
- If the ad uses a catalog, you need to have Ad promotion or Catalog management permission for the catalog. To check your permission for a catalog, use [/bc/asset/get/](https://business-api.tiktok.com/portal/docs?id=1739432717798401). The returned `catalog_role` should be `ADMIN` or `AD_PROMOTE`.|
|preview_type {Required}|string| Type of the ad you want to preview. To preview existing regular ads, please use `AD`. 
 
**Note**: Currently the supported objectives are: `REACH`, `TRAFFIC`, `VIDEO_VIEWS` , `ENGAGEMENT`, `APP_PROMOTION`, `LEAD_GENERATION`, `WEB_CONVERSIONS`, `PRODUCT_SALES`, and `RF_REACH`. |
|ad_id {Required}|string| ID of the ad that you want to preview.|
|device|string[]| List of device models. 

Use [/tool/device_model/](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369) to get the enum values of device models.|
|language|string| Language for the ad. 

Enum values: `ENGLISH`, `CHINESE`, `JAPANESE`. 
Default value:`ENGLISH`.|
| placement | string |The app where you want to deliver your ads.  

Enum values: 
- `PLACEMENT_TIKTOK`: Supported only when `objective_type` is  `REACH`, `TRAFFIC`,  `VIDEO_VIEWS`, `ENGAGEMENT`, `APP_PROMOTION`, `LEAD_GENERATION`,`WEB_CONVERSIONS`, or `PRODUCT_SALES`. 
- `PLACEMENT_PANGLE`: Supported only when `objective_type` is `TRAFFIC`,  `APP_PROMOTION`, `LEAD_GENERATION` (only when `promotion_type` is `LEAD_GENERATION`), or `WEB_CONVERSIONS`. 
- `ALL`: Supported only when `objective_type` is `TRAFFIC`,  `APP_PROMOTION`, `LEAD_GENERATION` (only when `promotion_type` is `LEAD_GENERATION`), or `WEB_CONVERSIONS`. 
**Note**: You need to pass in this field if you want to set non-TikTok placement for your ad. Otherwise, this field will be set as TikTok placement (`PLACEMENT_TIKTOK`) by default.|
```
#### Example

```xcodeblock
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "AD",
    "ad_id": "{{ad_id}}"
}'
(/code)
```

### Preview an existing interactive add-on

```xtable
|Field|Data Type|Description|
|-|-|-|
| advertiser_id {Required} | string | Advertiser ID. |
| preview_type {Required} | string |Preview type. 
To preview an existing interactive add-on, use `CARD`. |
| card_id | string | Creative portfolio ID. 

Pass the ID of one of the following creative portfolio types:
- Display Card.
- Countdown Sticker.
- Gift Code Sticker.
To create a creative portfolio, use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to get the ID of a Display Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058). 
- To learn about how to get the ID of a Countdown Sticker or Giftcode Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177).  |
```
#### Example
```xcodeblock
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "CARD",
    "card_id": "{{card_id}}"
}'
(/code)
```

### Preview existing instant page

```xtable
|Field|Data Type|Description|
|-|-|-|
| advertiser_id {Required} | string | Advertiser ID. |
| preview_type {Required} | string | Type of the ad that you want to preview. To preview instant product landing page, use `PAGE`. |
| page_id {+Conditional} | string | Page ID. 

- To create instant pages, use [Instant Page Editor SDK](https://business-api.tiktok.com/portal/docs?id=1740307202170881).
- After you create an instant page, call [/page/get/](https://business-api.tiktok.com/portal/docs?id=1820826387779586) to get the page ID.. |
```

#### Example

```xcodeblock
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "PAGE",
    "page_id": "{{page_id}}"
}'
(/code)
```

### Preview videos

```xtable
|Field|Data Type|Description|
|-|-|-|
| advertiser_id{Required} | string | Advertiser ID. |
| preview_type{Required} | string | Type of the ad that you want to preview. To preview video ads based on parameters, use `SINGLE_VIDEO`. |
| video_id{Required} | string | Video ID. Different placements have different creative specifications. See the [Ad Formats](https://ads.tiktok.com/help/article/image-ads-specification?redirected=1) chapter on TikTok Business Help Center for details. |
| thumbnail | string | ID of the thumbnail. You can get suggested thumbnails by using the [Get suggested thumbnails](https://ads.tiktok.com/marketing_api/docs?id=1740051189071873) endpoint. |
| profile_image | string | ID of the profile image. |
| display_name{Required} | string | Brand name. Number of characters allowed: 1-40 English characters, or 1-20 Chinese/Japanese/Korean characters.|
| ad_text{Required} | string | Ad text. Number of characters allowed: 1-100. |
| call_to_action{+Conditional} | string | Call-to-action text. For TikTok ads, either this field or `call_to_action_id` must be specified. If both are specified, this field will be ignored. For enum values, see [Enumeration - Call-to-action](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). For live shopping events, the call to action must be `WATCH_LIVE`.|
| call_to_action_id{+Conditional} | string | The ID of the CTA portfolio that you want to use in your ads. A CTA portfolio is a group of auto-optimized CTAs. If both this field and `call_to_action` are specified, this field will be used, and `call_to_action` will be ignored. For details about auto-optimized CTAs, see [CTA recommendations > Dynamic CTAs](https://ads.tiktok.com/marketing_api/docs?id=1740307296329730).|
| placements{Required} | string[] | Placement. For enum values, see [Enumeration - Placement](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). Different placements have different creative specifications. See the [Ad Formats](https://ads.tiktok.com/help/article/image-ads-specification?redirected=1) chapter on TikTok Business Help Center for details.|
|device|string[]| List of device models. Use [Get device models](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369) to get the enum values of device models.|
|language|string| Language for the ad. Enum values: `ENGLISH`, `CHINESE`, `JAPANESE`. Default: `ENGLISH`.|
```

#### Example
```xcodeblock
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "SINGLE_VIDEO",
    "video_id": "{{video_id}}",
    "display_name": "{{display_name}}",
    "ad_text": "{{ad_text}}",
    "call_to_action": "APPLY_NOW",
    "placements": [
        "PLACEMENT_TIKTOK"
    ],
    "device": [
        "{{device}}"
    ],
    "language": "CHINESE"
}'
(/code)
```

### Preview images

```xtable
|Field|Data Type|Description|
|-|-|-|
| advertiser_id{Required} | string | Advertiser ID. |
| preview_type{Required} | string | Type of the ad that you want to preview. To preview image ads based on parameters, use `SINGLE_IMAGE`. |
| image_id{Required} | string | Image ID. Different placements have different creative specifications. See the [Ad Formats](https://ads.tiktok.com/help/article/image-ads-specification?redirected=1) chapter on TikTok Business Help Center for details.|
| display_name{Required} | string | Brand name. Number of characters allowed: 1-40 English characters, or 1-20 Chinese/Japanese/Korean characters.|
| ad_text{Required} | string | Ad text. Number of characters allowed: 1-100. |
| call_to_action{+Conditional} | string | Call-to-action text. For TikTok ads, either this field or `call_to_action_id` must be specified. If both are specified, this field will be ignored. For enum values, see [Enumeration - Call-to-action](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). For live shopping events, the call to action must be `WATCH_LIVE`.|
| call_to_action_id{+Conditional} | string | The ID of the CTA portfolio that you want to use in your ads. A CTA portfolio is a group of auto-optimized CTAs. If both this field and `call_to_action` are specified, this field will be used, and `call_to_action` will be ignored. For details about auto-optimized CTAs, see [CTA recommendations > Dynamic CTAs](https://ads.tiktok.com/marketing_api/docs?id=1740307296329730).|
| placements{Required}| string[] | Placement. For enum values, see [Enumeration - Placement](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). Different placements have different creative specifications. See the [Ad Formats](https://ads.tiktok.com/help/article/image-ads-specification?redirected=1) chapter on TikTok Business Help Center for details.|
|device|string[]| List of device models. Use [Get device models](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369) to get the enum values of device models.|
|language|string| Language for the ad. Enum values: `ENGLISH`, `CHINESE`, `JAPANESE`. Default: `ENGLISH`.|
```

#### Example
```xcodeblock
(/code)
(code curl http)
curl --location 'https://ads.tiktok.com/open_api/v1.3/creative/ads_preview/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "SINGLE_IMAGE",
    "image_id": "{{image_id}}",
    "ad_text": "{{ad_text}}",
    "display_name": "{{display_name}}",
    "call_to_action": "CONTACT_US",
    "placements": [
        "PLACEMENT_PANGLE"
    ],
    "device": [
        "{{device}}"
    ],
    "language": "CHINESE"
}'
(/code)
```

## Response

```xtable
|Field|Data Type|Description|
|-|-|-|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1701890984602626).|
|message |string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1701890984602626).|
|data|json|Returned data.|
#| preview_link | string | Preview link.

Validity period: 
- 30 days when `preview_type` is `ADS_CREATION` or `AD`.
- 24 hours when `preview_type` is `CARD`, `PAGE`, `SINGLE_VIDEO` or `SINGLE_IMAGE`. |
#|iframe|string| iframe code snippet with the preview link. You can embed the iframe code to your HTML file.|
#| tips | list | Adjustment advice. Modify the materials according to the prompts to obtain a better display effect. |
##| placement{+ Conditional} | string | Incorrect placement. For enum values, see [Enumeration - Placement](https://ads.tiktok.com/marketing_api/docs?id=1701890985340929). If it is a general prompt message (applicable to all placements), then this field will not be returned. |
##| messages | string[] | Messages. |
|request_id|string|Request ID.|
```

### Example

```xcodeblock
(code Success-Response python)
HTTPS/1.1 200 OK
{
    "message": "OK",
    "code": 0,
    "data": {
        "tips": [
            {
                "messages": [
                    "The resolution should be 1280*720 at least."
                ],
                "placement": "PLACEMENT_TIKTOK"
            }
        ],
        "preview_link": "https://ads.tiktok.com/ad_preview_tool?ad_preview_id=5681cba0fcd211eab33c351a98xxxxx",
        "iframe": ""
    },
    "request_id": "202009221251300101151531921B1D3F96"
}
(/code)
```
