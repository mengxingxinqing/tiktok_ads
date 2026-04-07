# Get Upgraded Smart+ Ads

**Doc ID**: 1843317378982914
**Path**: API Reference/Upgraded Smart+/Ads/Get Upgraded Smart+ Ads

---

Use this endpoint to retrieve Upgraded Smart+ Ads within an ad account. 

## Request
**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/get/

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162). |
```

**Parameters**

```xtable
|Field{35%}|Data Type{15%}|Description{50%}|
|---|---|---|
|advertiser_id  {Required}|string|Advertiser ID.|
|fields|string[]|Fields that you want to get.

When not specified, all fields are returned by default.

For allowed fields, see the fields under `list` and fields under `ad_configuration` in the [Response](#item-link-Response) section excluding `advertiser_id` and `smart_plus_ad_id`, which are returned by default.|
|filtering|object|Filtering conditions.

Example: `filtering={"objective_type":"APP_PROMOTION"}`|
#| campaign_ids|string[]|Filter by campaign IDs.

Max size: 100.

To obtain campaign IDs, use [/smart_plus/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1843312818332930). |
#| adgroup_ids|string[]|A list of Ad group IDs.

Max size: 100.

To obtain ad group IDs, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).|
#| smart_plus_ad_ids|string[]|A list of Ad IDs.

Max size: 100.|
#| primary_status|string|Primary status.

For enum values, see [Enumeration-Primary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Primary%20Status).|
#| secondary_status|string|Filter by ad secondary status.

For enum values, see [Enumeration- Ad Status - Secondary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Ad%20status%20-%20secondary%20status).

The following secondary statuses are newly added for Upgraded Smart+ Ads:
- `AD_STATUS_DELIVERY_AND_REAUDIT`: Review of modifications in progress.
- `AD_STATUS_DELIVERY_AND_TRANSCODING_FAIL`: Transcoding of the video or videos in the ad failed.
- `AD_STATUS_REVIEW_PARTIALLY_APPROVED`: Ad in partial review and in delivery.
- `AD_STATUS_COLLECTION_TOGGLED_OFF`: Lead collection has ended.
- `AD_STATUS_PRIVACY_POLICY_REJECTED`: Ad rejected due to privacy policy violations.
- `AD_STATUS_PRIVACY_POLICY_AUDIT`: Ad in review for privacy policy compliance.|
#| objective_type|string|Filter by advertising objective.

Currently, we support `APP_PROMOTION`, `WEB_CONVERSIONS`, and `LEAD_GENERATION`.

For detailed explanation of enum values, see [Enumeration-Advertising Objectives](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Advertising%20Objective).|
#| sales_destination | string | Sales destination, the destination where you want to drive your sales.

Enum values:
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.|
#| optimization_goal|string|Optimization goal.

To find the enum values, see [Enumeration - Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal).|
#| creation_filter_start_time|string|The earliest ad creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time). This filter will retrieve ads created after this time.

Example: `2025-01-01 00:00:01`.

If `creation_filter_start_time` and `creation_filter_end_time` are not specified, the results will include ads created at any time.

**Important**: To ensure task efficiency and speed, consider setting a time range within six months for the creation time filters.|
#| creation_filter_end_time|string|The latest ad creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time). This filter will retrieve ads created before this time.

Example: `2025-02-01 00:00:01`.

If `creation_filter_start_time` and `creation_filter_end_time` are not specified, the results will include ads created at any time.

**Important**: To ensure task efficiency and speed, consider setting a time range within six months for the creation time filters.|
#| modified_after|string|The latest ad modification time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time). This filter will retrieve ads last modified after this time.

**Important**: To ensure task efficiency and speed, consider setting a time range within six months for the creation time filters.|
|page|number|Current page number.

Value range: ≥ 1.
Default value: 1.|
|page_size|number|Page size.

Value range: 1-100.
Default value: 10.|
```

### Example
```xcodeblock
(code curl http)
curl --location  --request GET 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/get/?advertiser_id={{advertiser_id}}&page=1&page_size=100' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```
## Response

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|-|-|-|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#|list|object[]|A list of ads. The returned fields are generated based on the `fields` specified in the request parameters. If not specified, all fields are returned by default.|
##|advertiser_id|string|Advertiser ID.|
##|campaign_id|string|Campaign ID.|
##|campaign_name|string|Campaign name.|
##|adgroup_id|string|Ad group ID.|
##|adgroup_name|string|Ad group name.|
##|smart_plus_ad_id|string|Ad ID.|
##|ad_name|string|Ad name.|
##|operation_status|string|Operation status.

Enum values:
- `ENABLE` : The ad is enabled (in 'ON' status).
- `DISABLE`: The ad is disabled (in 'OFF' status).
- `FROZEN`: The ad is terminated and cannot be enabled.|
##|secondary_status|string|Ad secondary status. 

For enum values, see [Enumeration-Ad Status - Secondary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Ad%20status%20-%20secondary%20status).

The following secondary statuses are newly added for Upgraded Smart+ Ads:
- `AD_STATUS_DELIVERY_AND_REAUDIT`: Review of modifications in progress.
- `AD_STATUS_DELIVERY_AND_TRANSCODING_FAIL`: Transcoding of the video or videos in the ad failed.
- `AD_STATUS_REVIEW_PARTIALLY_APPROVED`: Ad in partial review and in delivery.
- `AD_STATUS_COLLECTION_TOGGLED_OFF`: Lead collection has ended.
- `AD_STATUS_PRIVACY_POLICY_REJECTED`: Ad rejected due to privacy policy violations.
- `AD_STATUS_PRIVACY_POLICY_AUDIT`: Ad in review for privacy policy compliance.|
##|create_time|string|The time when the ad was created, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).

Example: `2025-01-01 00:00:01`.|
##|modify_time|string|The time when the ad was last modified, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).

Example: `2025-01-01 00:00:01`.|
##|creative_list|object[]|A list of creatives.|
###|ad_material_id|string|An ad-specific material ID generated when a particular creative is used in an ad. 

This ID differs from the creative ID you receive when uploading the creative to your ad account’s Creative Library.|
###|material_operation_status|string|The status of the creative. 

Enum values: 
- `ENABLE`: The creative is enabled (in 'ON' status).
- `DISABLE`: The creative is disabled (in 'OFF' status).|
###|creative_info|object|Creative information.|
####|ad_format|string|The ad format.

Enum values: 
- `SINGLE_VIDEO`: Single Video.
- `CAROUSEL_ADS`: Standard Carousel.
- `CATALOG_CAROUSEL`: Catalog Carousel.|
####|material_name|string|Material name.|
####|video_info|object|Video information.|
#####|video_id|string|Video ID.|
#####|file_name|string|Video name.|
####|image_info|object[]|Image information.|
#####|web_uri|string|Image ID.|
####|music_info|object|Music information.|
#####|music_id|string|The ID of the piece of music to use in the Carousel Ads.|
####|aigc_disclosure_type|string|Whether to turn on the AIGC (Artificial Intelligence Generated Content) self-disclosure toggle to indicate the ad contains AI-generated content. After the toggle is turned on, your ad will carry an "Advertiser labeled as Al-generated" label when viewed in full.

Enum values:
- `SELF_DISCLOSURE`: To turn on the toggle to declare that the ad contains AI-generated content.
- `NOT_DECLARED`: To not declare that the ad contains AI-generated content.|
####|tiktok_item_id|string|The ID of the TikTok post to be used as an ad (Spark Ads).|
####|identity_type|string|Returned for Spark Ads created without using catalog creatives.

Identity type.

Enum values: `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`.

For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097).|
####|identity_id|string|Returned for Spark Ads created without using catalog creatives.

Identity ID.|
####|identity_authorized_bc_id|string|Returned when `identity_type` within `creative_info` is `BC_AUTH_TT`.

The ID of the Business Center that a TikTok Account User in Business Center identity is associated with.|
##|ad_text_list|object[]|A list of ad texts.

Ad texts are shown to your audience as part of your ad creatives, to deliver the message you intend to communicate to them.|
###|ad_text|string|Ad text.|
##|auto_message_list|object[]|Returned only when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` at the ad group level.

Details of the automatic message to use in a TikTok Direct Messaging Ad.|
###|auto_message_id|string|The ID of the automatic message to use in a TikTok Direct Messaging Ad.

Currently, the only supported automatic message type is welcome message.
- To obtain a list of welcome messages within your ad account, use [/creative/auto_message/get/](https://business-api.tiktok.com/portal/docs?id=1822106498804738).
- To create a welcome message within your ad account, use [/creative/auto_message/create/](https://business-api.tiktok.com/portal/docs?id=1822106113771521).
To learn more about how to create TikTok Direct Messaging Ads with welcome messages, see [Create an Upgraded Smart+ Lead Generation Campaign with optimization location as TikTok direct messages](https://business-api.tiktok.com/portal/docs?id=1847302969710913).|
##|call_to_action_list|object[]|Call-to-action list.|
###|call_to_action|string|Call-to-action text.

For enum values, see [Enumeration - Call-to-action](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Call-to-action).|
##|interactive_add_on_list|object[]|A list of interactive add-on (creative portfolio) IDs.|
###|card_id|string|The ID of an interactive add-on.|
##|page_list|object[]|A list of pages.|
###|page_id|string|Page ID.|
##|landing_page_url_list|object[]|A list of landing page URLs.|
###|landing_page_url|string|Landing page URL.|
##|custom_product_page_list|object[]|Details of the custom product page to use in the ad.|
###|custom_product_page_url|string|The Custom Product Page (CPP) URL.

CPPs are product pages with customized screenshots, promotional text, and app previews that can be used to highlight specific content or features of the promoted app, or reach specific audiences.

Example: `https://apps.apple.com/us/app/tiktok/id835599320?ppid=12345a6b-c789-12d3-e4f5-g6h78i91jk2l`.|
##|deeplink_list|object[]|A list of deeplinks.|
###|deeplink|string|Deeplink, the specific location where you want your audience to go if they have your app installed.|
###|deeplink_type|string|The deeplink type. 

Enum values:
- `NORMAL`: non-deferred deeplink.
- `DEFERRED_DEEPLINK`: deferred deeplink.|
##| disclaimer | object | Disclaimer information. |
###| disclaimer_type | string | The type of disclaimer in the ad. 

Enum values: 
- `TEXT_LINK`: clickable disclaimers.
- `TEXT_ONLY`: text-only disclaimers. |
###| disclaimer_text | object | The text-only disclaimer in the ad. |
####| text | string | The disclaimer text. |
###| disclaimer_clickable_texts | object[] | The clickable disclaimer or clickable disclaimers in the ad. |
####| text | string | The disclaimer text. |
####| url | string | The URL for the clickable disclaimer. 
When users tap each text, they will be redirected to the URL and see more disclaimer details. |
##|ad_configuration|object|Additional configurations.|
###|identity_type|string|Returned in any of the following scenarios:
- For non-Spark Ads on non-TikTok placements. Non-Spark Ads on the TikTok placement are no longer supported.
- For Spark Ads created using catalog creatives from an E-commerce catalog. Learn more about how you can create such ads in [Create Upgraded Smart+ E-commerce Catalog Ads](https://business-api.tiktok.com/portal/docs?id=1847302895272962).
Identity type.
- Enum values for non-Spark Ads on non-TikTok placements: `CUSTOMIZED_USER`.
- Enum values for Upgraded Smart+ E-commerce Catalog Spark Ads (with `catalog_creative_toggle` as `true`): `TT_USER`, `BC_AUTH_TT`.
For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097).|
###|identity_id|string|Returned in any of the following scenarios:
- For non-Spark Ads on non-TikTok placements. Non-Spark Ads on the TikTok placement are no longer supported.
- For Spark Ads created using catalog creatives from an E-commerce catalog. Learn more about how you can create such ads in [Create Upgraded Smart+ E-commerce Catalog Ads](https://business-api.tiktok.com/portal/docs?id=1847302895272962).
Identity ID.|
###|identity_authorized_bc_id|string|Returned when `identity_type` within `ad_configuration` is `BC_AUTH_TT`.

ID of the Business Center that a TikTok Account User in Business Center identity is associated with.|
###|dark_post_status|string|The status of the "Ads-only mode" for your creatives.

Enum values:
- `ON`: Enable the ads-only mode to limit your posts to paid traffic.
- `OFF`: Disable the ads-only mode. The post will appear on your TikTok profile and will be eligible to receive organic traffic.|
###|product_specific_type|string|Different dimensions to choose products.

Enum values:
- `ALL`: Allow TikTok to dynamically choose from all products.
- `PRODUCT_SET`: Specify a product set. TikTok will dynamically choose products from this set.
- `CUSTOMIZED_PRODUCTS`: Specify a customized number of products.|
###|product_set_id|string|The ID of a product set.|
###|product_ids|string[]|The product IDs of catalog products.|
###|catalog_creative_toggle|boolean|Whether to enable auto-selection of creatives from your catalog.

Supported values: `true`, `false`.|
###|catalog_creative_info|object|Additional settings for catalog creatives to use in your ads.|
####|catalog_media_settings|string[]|The types of creatives from your E-commerce catalog to use in the ad.

Enum values:
- `VIDEO`: Video.
- `IMAGE`: Image.
- `TEMPLATE_VIDEO`: Video templates.|
####|catalog_template_video_id|string|The ID of a video template in your catalog to use in the ad.|
###| creative_auto_add_toggle | boolean | Whether to auto-add newly generated assets during delivery.
During your campaign, the system will generate new creative assets from your existing campaign assets and creative library. By using TikTok's latest trending elements (hooks, music, text, and more), you'll get high-quality, ready-to-use content that delivers alongside your other selected assets.
New assets will be added to your campaign automatically and won't appear on your TikTok profile. You can turn off this feature anytime.

Supported values: `true`, `false`. |
###| creative_auto_enhancement_strategy_list | string[] | The list of automatic enhancement strategies to apply to your ads.
Automatic enhancements are real-time edits applied to your ads during your campaign. They can improve performance by creating more engaging and impactful visuals, sound, and more.

Enum values:
- `TRANSLATE_AND_DUB`: Translate and dub. Connect with global audiences by delivering your ad in 50+ languages.
- `MUSIC_REFRESH`: Music refresh. Stay on-trend by swapping in music currently popular on TikTok.
- `VIDEO_QUALITY`: Video quality. Improve overall visual quality with increased resolution and clarity.
- `IMAGE_QUALITY`: Image quality. Improve overall visual quality with increased resolution and clarity.
- `IMAGE_RESIZE`: Resize. Resize your image to take advantage of full-screen capabilities.
- `CALL_TO_ACTION_ENHANCEMENT`: CTA enhancement. Tailor and optimize your call to action based on specific use cases to enhance performance.
- `AIGC_CARD`: Generate ad card. Increase engagement by showcasing key messages and visuals designed to drive clicks and conversions.
**Note**: Currently, you cannot enable the strategies `CALL_TO_ACTION_ENHANCEMENT` and `AIGC_CARD` through `creative_auto_enhancement_strategy_list` via API.
|
###|deeplink_utm_params|object[]|A list of deeplink URL parameters. URL parameters are snippets of code that can be added to the end of the URLs to help you track clicks across different channels and understand how visitors interact with a website through third-party analytics platforms. They consist of key-value pairs that are specified through `key` and `value`.|
####|key|string|The deeplink URL parameter.

It can be a custom parameter or a UTM parameter.

The supported UTM parameters are:
- `utm_source`: The app, site, etc., that brings traffic to your website. For example: TikTok.
- `utm_medium`: The advertising or marketing medium. For example: cpm, cpc, banner, video.
- `utm_content`: The creative content used for promotion. For example: ad name, CTA text, asset, color, etc.
- `utm_campaign`: The individual campaign name, slogan, or promo code. For example: BlackFridayProm.|
####|value|string|The value of the deeplink URL parameter.

It can be a custom value or the name of a macro.

The supported macros are:
- `__CAMPAIGN_NAME__`: This will be replaced by your campaign name.
- `__CAMPAIGN_ID__`: This will be replaced by your campaign ID.
- `__AID_NAME__`: This will be replaced by your ad group name.
- `__AID__`: This will be replaced by your ad group ID.
- `__CID_NAME__`: This will be replaced by your ad name.
- `__CID__`: This will be replaced by your ad ID.
- `__PLACEMENT__`: This will be replaced by your placement.|
###|end_card_cta|string|Call-to-action for the end card (`image_ids`) of an [Automotive Carousel Ad for Inventory](https://business-api.tiktok.com/portal/docs?id=1843325008693250) or Upgraded Smart+ [Automotive Carousel Ad for Models](https://business-api.tiktok.com/portal/docs?id=1843325022799873), or [the catalog solution for Upgraded Smart+ TikTok Direct Messaging Ads](https://business-api.tiktok.com/portal/docs?id=1847302969710913#item-link-For%20the%20catalog%20solution).

Enum values:
- `SEARCH_INVENTORY` (Recommended): Search inventory.
- `LEARN_MORE`: Learn more.
- `SHOP_NOW`: Shop now.
- `SIGN_UP`: Sign up.
- `CONTACT_US`: Contact us.
- `BOOK_NOW`: Book now.
- `READ_MORE`: Read more.
- `VIEW_MORE`: View now.
- `ORDER_NOW`: Order now.
- `SEND_MESSAGE`: Send message.This value is only available for [the catalog solution for Upgraded Smart+ TikTok Direct Messaging Ads](https://business-api.tiktok.com/portal/docs?id=1847302969710913#item-link-For%20the%20catalog%20solution).|
###|product_display_field_list|string[]|A list of product details to display in your [Automotive Carousel Ad for Inventory](https://business-api.tiktok.com/portal/docs?id=1843325008693250).

Enum values:
- `DEALER_NAME`: the `dealer_name` field of vehicles.
- `MAKE`: the `make` field of vehicles.
- `MODEL`: the `model` field of vehicles.
- `YEAR`: the `year` field of vehicles.
- `MILEAGE`: the `mileage` field of vehicles.
- `PRICE`: the `price` field of vehicles.
- `SALE_PRICE`: the `sale_price` field of vehicles.
- `EXTERIOR_COLOR`: the `exterior_color` field of vehicles.
- `TRIM`: the `trim` field of vehicles.
- `ADDRESS_CITY`: the `city` field of vehicles.
- `VEHICLE_STATE`: the `state_of_vehicle` field of vehicles.
The title of each vehicle is displayed automatically. For instance, if you set this field to `["MILEAGE","YEAR"]`, the ad will display the `mileage`, `price` and `title` fields of each vehicle.

To retrieve the product detail fields of your vehicles in an Auto-Inventory catalog and check whether you need to update the details, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402).|
###|auto_disclaimer_types|string[]|The type of disclaimer to show in the [Automotive Carousel Ad for Models](https://business-api.tiktok.com/portal/docs?id=1843325022799873).

Enum values:
- `EMISSION`: Emission disclaimer.
- `DISCOUNT`: Discount or offer disclaimer.|
###|utm_params|object[]|A list of URL parameters. 

URL parameters are snippets of code that can be added to the end of the URLs to help you track clicks across different channels and understand how visitors interact with a website through third-party analytics platforms. They consist of key-value pairs that are specified through `key` and `value`.|
####|key|string|The URL parameter.

The parameter can be a custom parameter or a UTM parameter.

The supported UTM parameters are:
- `utm_source`: The app, site, etc., that brings traffic to your website. For example: TikTok.
- `utm_medium`: The advertising or marketing medium. For example: cpm, cpc, banner, video.
- `utm_content`: The creative content used for promotion. For example: ad name, CTA text, asset, color, etc.
- `utm_campaign`: The individual campaign name, slogan, or promo code. For example: BlackFridayProm.Note that UTM parameters are case-sensitive.|
####|value|string|The value of the URL parameter.

The value can be a custom value or the name of a macro.

The supported macros are:
- `__CAMPAIGN_NAME__`: This will be replaced by your campaign name.
- `__CAMPAIGN_ID__`: This will be replaced by your campaign ID.
- `__AID_NAME__`: This will be replaced by your ad group name.
- `__AID__`: This will be replaced by your ad group ID.
- `__CID_NAME__`: This will be replaced by your ad name.
- `__CID__`: This will be replaced by your ad ID.
- `__PLACEMENT__`: This will be replaced by your placement.|
###|fallback_type|string|Fallback type.

The destination when the user is unable to access the deeplink because the app has not been installed.

Enum value:
- `WEBSITE`: The promoted web page as fallback URL. You need to simultaneously specify the fallback URL through `landing_page_url_list`.
To learn more about how to configure a fallback URL in TikTok Instant Messaging Ads, see [Create an Upgraded Smart+ Lead Generation Campaign with optimization location as instant messaging apps](https://business-api.tiktok.com/portal/docs?id=1847302988449921).|
###|product_info|object|Product information.

This information will be used in different ad variations to create personalized ad delivery with the goal of improving ad performance. Based on past data, ads with complete information often have more clicks and conversions. Results may vary.|
####| product_titles | string[] | A list of product names. |
####| product_image_list | object[] | A list of product images. |
#####| web_uri | string | The image ID of a product image. |
####| selling_points | string[] | A list of selling points. |
####| catalog_tag_list | string[] | Returned in any of the following scenarios:
- Scenario 1: At the campaign level `objective_type` is `WEB_CONVERSIONS` and `catalog_type` is `ECOMMERCE`.
- Scenario 2: At the campaign level, `objective_type` is `LEAD_GENERATION` and `catalog_enabled` is `true`.
- At the ad group level, an Auto-Inventory catalog is specified through `catalog_id`.Details of the product information for catalog ads.
- For scenario 1, the specified product information will be automatically displayed from your catalog to drive results. The enum values are:`PRICE`: Price.
- `STRIKETHROUGH_PRICE`: Strikethrough price.
- `DISCOUNT`: Discount.
- `FREE_SHIPPING`: Free shipping.
- For scenario 2, the corresponding text for the specified product information will be displayed on the inventory card. The enum values are:`DEALER_NAME`: Dealer name.
- `CURRENT_MILEAGE`: Current mileage.
- `LEAD_PRICE`: Price.
- `LEAD_SALE_PRICE`: Sale price.
- `EXTERIOR_COLOR`: Exterior color.
- `TRIM`: Trim.
- `ADDRESS_CITY`: City.
- `VEHICLE_STATE`: Vehicle state. |
####| promo_info_list | object[] | Returned only for [regular Upgraded Smart+ Web Campaigns](https://business-api.tiktok.com/portal/docs?id=1847302878676994).

Details of promo codes and offers.

Your offer details for promo codes, offers, or events will be highlighted to boost engagement and ad performance. Promo codes require shoppers to enter a code at checkout. Offers apply automatically and no code is needed. |
#####| discount_type | string | Returned only when `promo_info_list` is specified.

Discount type.

Enum values:
- `PERCENTAGE`: Percentage off discount.
- `CASH`: Cash off discount. |
#####| discount_value | float | Returned when `promo_info_list` is specified.

Discount value.|
#####| discount_currency | string | Returned when `discount_type` is `CASH`.

Discount currency.

For enum values, see [List of values for `discount_currency` or `minimum_purchase_currency`](#item-link-List of values for discount_currency or minimum_purchase_currency). |
#####| promo_code | string | The promo code. |
#####| minimum_purchase_type | string | Minimum purchase type.

Enum values:
- `QUANTITY`: Minimum quantity.
- `SUBTOTAL`: Minimum subtotal. |
#####| minimum_purchase_value | float | Returned only when `minimum_purchase_type` is specified.

Minimum purchase value. |
#####| minimum_purchase_currency | string | Returned only when `minimum_purchase_type` is `SUBTOTAL`.

Minimum purchase currency.

For enum values, see [List of values for `discount_currency` or `minimum_purchase_currency`](#item-link-List of values for discount_currency or minimum_purchase_currency). |
#####| valid_start_time | string | Valid start time (UTC+0) for the promo code or offer, in the format of `YYYY-MM-DD HH:MM:SS`. |
#####| valid_end_time | string | Valid end time (UTC+0) for the promo code or offer, in the format of `YYYY-MM-DD HH:MM:SS`. |
###| product_info_enabled | string | The product information mode.

Enum values:
- `UNSET`: To disable product information mode.
- `NON_CATALOG`: To enable the non-catalog version of product information.
- `CATALOG`: To enable the catalog version of product information. |
###|call_to_action_id|string|The ID of the call-to-action portfolio to use in your ad.|
###|phone_info|object|Returned only when `promotion_type` is set to `LEAD_GEN_CLICK_TO_CALL` at the ad group level.

Details of the phone number that the ad audience can directly reach out to you (the advertiser) through when they click the call-to-action button within the ad.

Learn about how to [create an Upgraded Smart+ Lead Generation Campaign with optimization location as phone call](https://business-api.tiktok.com/portal/docs?id=1847302998941697).|
####|phone_region_code|string|The region code for the phone number that the audience can click on the ad to call.

Example: `US`.|
####|phone_region_calling_code|string|The region calling code for the phone number that the audience can click on the ad to call.

Example: `+1`.|
####|phone_number|string|The phone number that the audience can click on the ad to call.

Example: `12638282`.|
###|tracking_info|object|Tracking information.|
####|impression_tracking_url|string|Default Impression Tracking URL.|
####|click_tracking_url|string|Click Tracking URL.|
####|tracking_app_id|string|The ID of the app that is measured.|
####|tracking_message_event_set_id|string|The ID of the message event set that you want to measure in the Instant Messaging Ad.|
####| app_tracking_info_list | object[] | Details of Third-party tracking settings. |
#####| app_type | string | Returned when `app_tracking_info_list` is specified.

App type.

Enum values:
- `APP_ANDROID`: Android App.
- `APP_IOS`: iOS App. |
#####| app_id | string | Returned when `app_tracking_info_list` is specified.

The App ID of the App.
- When `app_type` is `APP_ANDROID`, this field represents the App ID for an Android App.
- When `app_type` is `APP_IOS`, this field represents the App ID for an iOS App. |
#####| impression_tracking_url | string | Impression tracking URL.
- When `app_type` is `APP_ANDROID`, this field represents an impression tracking URL for Android.
- When `app_type` is `APP_IOS`, this field represents an impression tracking URL for iOS. |
#####| click_tracking_url | string | Click tracking URL.
- When `app_type` is `APP_ANDROID`, this field represents a click tracking URL for Android.
- When `app_type` is `APP_IOS`, this field represents a click tracking URL for iOS. |
#|page_info|object|Pagination information.|
##|page|number|Current page number.|
##|page_size|number|Page size.|
##|total_number|number|Total number of results.|
##|total_page|number|Total pages of results.|
```
### List of values for `discount_currency` or `minimum_purchase_currency`
The following table lists the enum values for `discount_currency` or `minimum_purchase_currency`.
```xtable
|Value for discount_currency or minimum_purchase_currency {50%}|Currency{50%}|
|---|---|
|`AED`|UAE Dirham|
|`ARS`|Argentine Peso|
|`AUD`|Australian Dollar|
|`BDT`|Bangladesh Taka|
|`BHD`|Bahraini Dinar|
|`BOB`|Bolivian Boliviano|
|`BRL`|Brazilian Real|
|`BYN`|Belarusian Ruble|
|`CAD`|Canadian Dollar|
|`CHF`|Swiss Franc|
|`CLP`|Chilean Peso|
|`CNY`|Chinese Yuan|
|`COP`|Colombian Peso|
|`CRC`|Costa Rican Colón|
|`CZK`|Czech Republic Koruna|
|`DKK`|Danish Krone|
|`DZD`|Algerian Dinar|
|`EGP`|Egyptian Pound|
|`EUR`|Euro|
|`GBP`|British Pound|
|`GTQ`|Guatemalan Quetzal|
|`HKD`|Hong Kong Dollar|
|`HNL`|Honduran Lempira|
|`HUF`|Hungarian Forint|
|`IDR`|Indonesian Rupiah|
|`ILS`|New Israeli Shekel|
|`INR`|Indian Rupee|
|`IQD`|Iraqi Dinar|
|`ISK`|Icelandic Króna|
|`JOD`|Jordanian Dinar|
|`JPY`|Japanese Yen|
|`KES`|Kenyan Shilling|
|`KHR`|Cambodian Riel|
|`KRW`|South Korean Won|
|`KWD`|Kuwaiti Dinar|
|`KZT`|Tenge|
|`LBP`|Lebanese Pound|
|`LKR`|Sri Lanka Rupee|
|`MAD`|Moroccan Dirham|
|`MOP`|Pataca|
|`MXN`|Mexican Peso|
|`MYR`|Malaysian Ringgit|
|`NGN`|Nigerian Naira|
|`NIO`|Nicaraguan Cordoba|
|`NOK`|Norwegian Krone|
|`NZD`|New Zealand Dollar|
|`OMR`|Rial Omani|
|`PEN`|Peruvian Sol|
|`PHP`|Philippine Piso|
|`PKR`|Pakistan Rupee|
|`PLN`|Polish ZŁOty|
|`PYG`|Paraguayan Guarani|
|`QAR`|Qatari Rial|
|`RON`|Romanian Leu|
|`RSD`|Serbian Dinar|
|`RUB`|Russian Ruble|
|`SAR`|Saudi Riyal|
|`SEK`|Krona|
|`SGD`|Singapore Dollar|
|`THB`|Thai Baht|
|`TRY`|Turkish Lira|
|`TWD`|New Taiwan Dollar|
|`UAH`|Hryvnia|
|`USD`|US Dollar|
|`UYU`|Peso Uruguayo|
|`VEF`|Venezuelan Bolívar|
|`VND`|Vietnamese Dong|
|`ZAR`|South African Rand|
```

### Example
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "list": [
            {
                "ad_configuration": {
                    "call_to_action_id": "{{call_to_action_id}}",
                    "catalog_creative_toggle": false,
                    "product_ids": [
                        "{{product_id}}",
                        "{{product_id}}",
                        "{{product_id}}",
                        "{{product_id}}"
                    ],
                    "product_specific_type": "CUSTOMIZED_PRODUCTS"
                },
                "ad_name": "",
                "ad_text_list": [],
                "adgroup_id": "{{adgroup_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "create_time": "{{create_time}}",
                "creative_list": [
                    {
                        "ad_material_id": "{{ad_material_id}}",
                        "creative_info": {
                            "ad_format":"SINGLE_VIDEO",
                            "identity_authorized_bc_id": "0",
                            "identity_id": "{{identity_id}}",
                            "identity_type": "TT_USER",
                            "tiktok_item_id": "{{tiktok_item_id}}"
                        },
                        "material_operation_status": "ENABLE"
                    }
                ],
                "landing_page_url_list": [
                    {
                        "landing_page_url": "{{landing_page_url}}"
                    }
                ],
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "secondary_status": "AD_STATUS_DONE",
                "smart_plus_ad_id": "{{smart_plus_ad_id}}"
            },
            {
                "ad_configuration": {
                    "call_to_action_id": "{{call_to_action_id}}",
                    "catalog_creative_toggle": false,
                    "identity_id": "{{identity_id}}",
                    "identity_type": "CUSTOMIZED_USER",
                    "product_set_id": "{{product_set_id}}",
                    "product_specific_type": "PRODUCT_SET",
                    "utm_params": [
                        {
                            "field": "{{field}}",
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
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "create_time": "{{create_time}}",
                "creative_list": [
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
                    }
                ],
                "landing_page_url_list": [
                    {
                        "landing_page_url": "{{landing_page_url}}"
                    }
                ],
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "secondary_status": "AD_STATUS_AUDIT",
                "smart_plus_ad_id": "{{smart_plus_ad_id}}"
            },
            {
                "ad_configuration": {
                    "call_to_action_id": "{{call_to_action_id}}"
                },
                "ad_name": "{{ad_name}}",
                "ad_text_list": [],
                "adgroup_id": "{{adgroup_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "advertiser_id": "{{advertiser_id}}",
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "create_time": "{{create_time}}",
                "creative_list": [
                    {
                        "ad_material_id": "{{ad_material_id}}",
                        "creative_info": {
                            "ad_format":"SINGLE_VIDEO",
                            "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                            "identity_id": "{{identity_id}}",
                            "identity_type": "BC_AUTH_TT",
                            "tiktok_item_id": "{{tiktok_item_id}}"
                        },
                        "material_operation_status": "ENABLE"
                    },
                    {
                        "ad_material_id": "{{ad_material_id}}",
                        "creative_info": {
                            "ad_format":"SINGLE_VIDEO",
                            "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                            "identity_id": "{{identity_id}}",
                            "identity_type": "BC_AUTH_TT",
                            "tiktok_item_id": "{{tiktok_item_id}}"
                        },
                        "material_operation_status": "ENABLE"
                    }
                ],
                "interactive_add_on_list": [
                    {
                        "card_id": "{{card_id}}"
                    }
                ],
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "page_list": [
                    {
                        "page_id": "{{page_id}}"
                    }
                ],
                "secondary_status": "AD_STATUS_AUDIT",
                "smart_plus_ad_id": "{{smart_plus_ad_id}}"
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 100,
            "total_number": 3,
            "total_page": 1
        }
    }
}
(/code)
```
