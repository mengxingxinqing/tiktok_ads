# Create a portfolio

**Doc ID**: 1739091950439426
**Path**: API Reference/Creative Portfolios/Create a portfolio

---

Use this endpoint to create a portfolio of creative assets.

>  **Note**

>  You can only create one portfolio each time you call the endpoint.

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
|Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/creative/portfolio/create/|/v1.3/creative/portfolio/create/ |
| Request parameter name | `portfolio_type` 
`advanced_show_time` 
 `advanced_guide_text_bottom` 
 `advanced_position` 
 `advanced_image_info` | `creative_portfolio_type`
`badge_show_time` 
 `call_to_action_text` 
 `badge_position` 
 `badge_image_info`|
| Request parameter data type | `advertiser_id`: number 
`asset_ids`: number[] |`advertiser_id`: string 
`asset_ids`: string[]|
| New request parameters|/ |  `sticker_param` (including all the parameters within the object ) 
`tags`
`layouts`
`description` 
`category_label` 
`app_id`
 `profile_image`
`call_to_action`
`mobile_app_id`
`country_code`
`product_source`
`identity_id`
`identity_type`
`identity_authorized_bc_id`
`catalog_id`
`catalog_authorized_bc_id`
`store_id`
`store_authorized_bc_id`
`product_specific_type`
`product_set_id`
`item_group_ids`
`sku_ids`
`dynamic_format`
`vertical_video_strategy`
`ad_text`
`card_show_price`
`card_tags`
`card_image_index`
`showcase_products` (including all the parameters within the object)
`title`
`selling_points`
`pop_up_window_image_id`
`gesture_type`
`slide_length`
`slide_dimension`
`interactive_music_id`|
| Response parameter data type | `creative_portfolio_id`: number | `creative_portfolio_id`: string|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/creative/portfolio/create/

**Method** POST

**Header**

``` xtable
|Field{35%}|Type{15%}|Description{50%}|
|---|---|---|
|Access-Token {required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162). |
|Content-Type {required}|string|Request message type**Allowed format: `"application/json"`  |
```

**Parameters**

``` xtable
|Field{35%}|Type{15%}|Description{50%}|
|--- |--- |--- |
|advertiser_id {required}|string|The advertiser ID |
|creative_portfolio_type|string|Type of the portfolio. 

Enum values: 
- `CTA`: call-to-action text.
- `CARD`: card (Display Card). 
- `WEB_INFO_CARD`: Website info card.
- `DOWNLOAD_CARD`: Download Card.
- `INVENTORY_CARD`: Inventory Card.
-  `PRODUCT_CARD`: Product Card. 
- `PRODUCT_TILE`: Product Tiles.
- `STICKER`: Countdown Sticker or Gift Code Sticker. 
- `PREMIUM_BADGE`: Pop-up Showcase.
- `GESTURE`: Gesture.
- `SUPER_LIKE`: Superlike. A Superlike engages the audience with a surprise visual element after they like a video ad. With Superlke, heart-shaped and customized icons float across the screen when the audience likes or double-taps on the ads.
Default value: `CTA`. 

Note**: 
- You can only create one creative portfolio of any type at a time.
- Website info cards can only be used for auction ads with the `objective_type` as `WEB_CONVERSIONS` or `TRAFFIC` (with `promotion_type` set to `WEBSITE`).
- You can only use the Inventory Card portfolio in Automotive Ads.
- Product Cards can only be used in Video Shopping Ads.
- Product Tiles can only be used in Video Shopping Ads with product source as catalog.
- Before creating a Product Tiles portfolio, ensure that you have a catalog containing at least four products that have passed the review. To verify whether you have a catalog with enough eligible products for the Product Tile portfolio, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) and confirm that the `audit_status` of at least four products is `approved`.
- Using a Product Tiles portfolio to create ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Countdown Sticker can only be used for auction ads with the advertising objective (`objective_type`) as Reach (`REACH`), Traffic (`TRAFFIC`), Video views(`VIDEO_VIEW`), App promotion (`APP_PROMOTION`), Lead generation(`LEAD_GENERATION`), Website conversions (`WEB_CONVERSIONS`), or Product sales (`PRODUCT_SALES`), as well as for R&F (`RF_REACH`) ads. If you want to use Countdown Stickers in Lead Generation ads, you can only set the Optimization location as Website at the ad group level. To learn about how to create such ads, see [Create a Lead Generation ad with optimization location as Website](https://business-api.tiktok.com/portal/docs?id=1774482976097281). 
- Reminder Countdown Sticker (`sticker_type` as `REMINDER_COUNTDOWN` or `LIVE_REMINDER_COUNTDOWN`) is an allowlist-only feature for Traffic (`TRAFFIC`), App promotion (`APP_PROMOTION`), Website conversions (`WEB_CONVERSIONS`) ads. If you would like to access it for ads with these objectives, please contact your TikTok representative. 
- Gift Code Sticker can only be used for auction ads with the advertising objective (`objective_type`) as Reach (`REACH`), Traffic (`TRAFFIC`), Video views(`VIDEO_VIEW`),  App promotion (`APP_PROMOTION`),  Lead generation(`LEAD_GENERATION`), Website conversions (`WEB_CONVERSIONS`), or Product sales (`PRODUCT_SALES`), as well as for R&F ads with the advertising objective(`objective_type`) as Reach (`RF_REACH`).
- Gestures can only be used for auction ads with the `objective_type` (advertising objective) as `REACH`, `TRAFFIC`, `VIDEO_VIEWS` (with `optimization_goal` as `ENGAGED_VIEW`), `APP_PROMOTION`, `WEB_CONVERSIONS`, as well as for R&F ads with the advertising objective (`objective_type`) as Reach (`RF_REACH`).  Using Gesture portfolios in campaigns with the advertising objective `APP_PROMOTION`, `TRAFFIC`, or `WEB_CONVERSIONS` are currently separate allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Superlikes can only be used for auction ads with the `objective_type` (advertising objective) as `REACH`, `TRAFFIC`, `VIDEO_VIEWS` (with `optimization_goal` as `ENGAGED_VIEW`), `ENGAGEMENT` (with `optimization_goal` as `PAGE_VISIT`), `APP_PROMOTION`, `WEB_CONVERSIONS`, as well as for R&F ads with the advertising objective (`objective_type`) as Reach (`RF_REACH`).  Using Superlike portfolios in campaigns with the advertising objective `APP_PROMOTION` or `TRAFFIC` are currently separate allowlist-only features. If you would like to access them, please contact your TikTok representative. |
|portfolio_content|object[]|The content of the portfolio.|
#|asset_content {+Conditional}|string|Required when `creative_portfolio_type` is `CTA`. 

A call-to-action text. 

For example, `"Learn More"`.  |
#|asset_ids {+Conditional}|string[]|Required when `creative_portfolio_type` is `CTA`. 

A list of CTAs. 

For example, `[201781, 201535]`. 

To create a CTA portfolio, you need to get a group of auto-optimized CTAs by using `/creative/cta/recommend/`. Fetch the data in the response and include it as values to this field. 

**Note**: Auto-optimized CTAs can only be used in the advertiser accounts that they were created for.
 |
#|card_type {+Conditional}|string | Required when `creative_portfolio_type` is `CARD`. 

Card type. 

Enum value: `IMAGE` (Display Card). |
#| gesture_type {+Conditional} | string | Required when `creative_portfolio_type` is `GESTURE`.

Gesture type.

Enum values:  
- `CLICK`: Click Gesture.  
- `STRAIGHT_SLIDE`: Straight Slide Gesture.  
- `CURVED_SLIDE`: Curved Slide Gesture.|
#|image_id {+Conditional}|string| Required when `creative_portfolio_type` is `CARD`, `WEB_INFO_CARD`, `INVENTORY_CARD`, or `SUPER_LIKE`.

Image ID. 

- The image for a Display Card (`CARD`) must be 750 pixels in width and 421 pixels in height.
- The recommended dimensions for a Website info card (`WEB_INFO_CARD`) are 800 pixels in width and 800 pixels in height.
- The image for an Inventory Card (`INVENTORY_CARD`) must be 800 pixels in width and 600 pixels in height.
- For Superlike (`SUPER_LIKE`), specify the image of a customized icon that floats across the screen together with heart-shaped icons when the audience likes or double-taps on the ads. The image needs to meet the following specification requirements:Recommended dimensions: 200 pixels in width and 200 pixels in height.
- Image format: JPG, JPEG, or PNG.
- File size: within 50KB.
You can get the image ID via [/file/image/ad/upload/](https://ads.tiktok.com/marketing_api/docs?id=1739067433456642) or [/file/image/ad/search/](https://ads.tiktok.com/marketing_api/docs?id=1740052016789506). |
#| pop_up_window_image_id {+Conditional}| string | 
- Required when `creative_portfolio_type` is `GESTURE`.  
- Optional when `creative_portfolio_type` is `SUPER_LIKE`.
The ID of the pop-up window image in the Superlike or the gesture pop-up card in the Gesture.
 
- When `creative_portfolio_type` is `GESTURE`, this field represents the gesture pop-up card that will appear after the viewer follows the gesture.  
- When `creative_portfolio_type` is `SUPER_LIKE`, this field represents the pop-up window that will appear after the Superlike finishes floating across the screen and will take the audience to the ad landing page when they click on it.
 Supported specifications: 
- Recommended dimensions: 620 pixels in width and 788 pixels in height. 
- Image format: JPG, JPEG, PNG, or GIF.
- File size: within 3MB. 
  To upload an image and obtain the image ID, use [/file/image/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1739067433456642). |
#|title {+Conditional}|string | Required when `creative_portfolio_type` is `WEB_INFO_CARD`.

The title of the card.

Length limit: 25 characters.|
#|selling_points {+Conditional}|string[] |Required when `creative_portfolio_type` is `WEB_INFO_CARD`.

The reasons why your products are worth buying.

Max size: 5.
Length limit for each selling point as a string within the string array: 25 characters. |
#|call_to_action_text{+Conditional}|string| Required when `creative_portfolio_type` is `GESTURE` or `PREMIUM_BADGE`.

Interactive guide text for the Gesture or Pop-out Showcase.
  
- When `creative_portfolio_type` is `GESTURE`, this field represents the interactive guide text for the Gesture.
Example text for different Gesture types:      For a Click Gesture: `Click here for more details` 
- For a Straight Slide Gesture: `Slide in a straight line` 
- For a Curved Slide Gesture: `Slide along the curve`   
- When `creative_portfolio_type` is `PREMIUM_BADGE`, this field represents the interactive guide text for the Pop-out Showcase.  Example text: `Click here for details`  
Length limit: 27 characters. Each English letter counts as one character while each Chinese, Japanese, or Korean word counts as two.
Emojis and special characters `{`, `}`, `@`, and `#` are not supported.
Do not include bar codes, stock codes, or any social media information.|
#|badge_show_time{+Conditional}|integer| Required when `creative_portfolio_type` is `GESTURE` or `PREMIUM_BADGE`.

The time when the Gesture icon within the Gesture or the Premium Badge within the Pop-out Showcase will appear in your video, in seconds.

The first three seconds and the last five seconds of the video cannot be used as the start of the pop-up.

Example: 5.|
#|badge_position{+Conditional}|object| Required when `creative_portfolio_type` is `GESTURE` or `PREMIUM_BADGE`.

Information about the position of the Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.|
##|position_x{+Conditional}| float| Required when `badge_position` is specified.

Relative X-axis value of the top-left corner of the Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.

Value range: 0-1.|
##|position_y{+Conditional}| float| Required when `badge_position` is specified.

Relative Y-axis value of the top-left corner of the Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.

Value range: 0-1.|
##| angle {+Conditional} | number |Required when `badge_position` is specified and any of the following conditions is met:  
- `creative_portfolio_type` is `GESTURE` and `gesture_type` is `STRAIGHT_SLIDE` or `CURVED_SLIDE`.  
- `creative_portfolio_type` is `PREMIUM_BADGE`.
The angle of the Straight Slide Gesture or Curved Slide Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.

Value range:  
- When `creative_portfolio_type` is `GESTURE` and `gesture_type` is `STRAIGHT_SLIDE` or `CURVED_SLIDE`, the recommended angle is a value within the range 30-150 or 210-330.  
- When `creative_portfolio_type` is `PREMIUM_BADGE`: 0-360.|
#|badge_image_info{+Conditional}|object|Required when `creative_portfolio_type` is `PREMIUM_BADGE`.

Information about the badge image in the Pop-out Showcase.|
##|image_id{+Conditional}|string|Required when `badge_image_info` is specified.

ID of the badge image in the Pop-out Showcase.

Specification requirements:  
- Dimensions: 448 pixels in width and 448 pixels in height.  
- Image format: JPG, JPEG, or PNG.  
- File size: within 1 MB.|
#| slide_length {+Conditional} | number | Required when `creative_portfolio_type` is `GESTURE` and `gesture_type` is `STRAIGHT_SLIDE`.

The length of the Straight Slide Gesture.|
#| slide_dimension {+Conditional} | object | Required when `creative_portfolio_type` is `GESTURE` and `gesture_type` is `CURVED_SLIDE`.

The dimensions of the Curved Slide Gesture.|
##| dimension_width {+Conditional} | number | Required when `slide_dimension` is specified.

The width of the Curved Slide Gesture.|
##| dimension_height {+Conditional} | number | Required when `slide_dimension` is specified.

The height of the Curved Slide Gesture.|
#| interactive_music_id {+Conditional} | string | Required when `creative_portfolio_type` is `GESTURE`.

The URL of the background music for the Gesture.

Specification requirements:  
- File size: within 1 MB.  
- File format: MP3.  
- Recommended duration: six seconds.
Example: `https://sf16-sg-default.akamaized.net/obj/tiktok-obj/0123456789.mp3`.

To ensure a smooth ad experience, use the video ad background music as the Gesture background music.

To upload a music file to the creative library and obtain the music URL (`url`), use [/file/music/upload/](https://business-api.tiktok.com/portal/docs?id=1740052650395650).|
#| layouts {+Conditional} | string[] | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`. 

The layout type of the Download Card. 

Enum values: 
- `TYPE_1`: Type 1, showing app description in the Download Card. 
-  `TYPE_2` : Type 2, not showing app description in the Download Card.  You can pass in one or two layout types, and when you pass in both `TYPE_1` and `TYPE_2` in this field, you will create one Type 1 Download Card and one Type 2 Download Card. |
#| description {+Conditional} | string | Required in any of the following scenarios:
- `creative_portfolio_type` is `DOWNLOAD_CARD` and the value of `layouts` includes `TYPE_1`. 
- `creative_portfolio_type` is `INVENTORY_CARD`.
Description of the app that you want to promote in the Download Card or text of the Inventory Card. 

For an Inventory Card (`INVENTORY_CARD`), the length limit is 40 characters.|
#| tags {+Conditional} | string[] | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`. 

Tags for the Download Card. Enum values: 
- `CATEGORIES`：Showing the category of the app you want to promote in the Download Card. 
- `FILESIZE`：Showing the file size of the app you want to promote in the Download Card. 
-  `RATING`：Showing the rating of the app you want to promote in the Download Card. 
-  `RANKING`：Showing the ranking of the app you want to promote in the Download Card. 
- `COMMENT_VOLUME`：Showing the number of comments for the app you want to promote in the Download Card. 
**Note**: 
- You can pass in multiple tags at one time, but when you pass in more than two tags, only two tags will show in the Download Card according to the following tag priority: `CATEGORIES` > `FILESIZE` > `RATING` > `RANKING`>`COMMENT_VOLUME`. 
- For Type 1 Download Card, you need to pass in at least one tag. 
- For Type 2 Download Card, you need to pass in at least two tags. |
#| category_label {+Conditional} | string | Required when `creative_portfolio_type` is  `DOWNLOAD_CARD` and the value of `tags` includes `CATEGORIES`.

 Category name of the app you want to promote in the Download Card. 

See [Enumerations-Creative Management-Category Labels](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138) for the enum values, and you need to pass the value as string. |
#| app_id {+Conditional} | string | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`. 

ID of the app that you want to promote in the Download Card. It's the App ID from Events Manager. |
#| profile_image {+Conditional} | string | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`.

Profile image URL. |
#| call_to_action {+Conditional} | string | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`. 

Call-to-action text in the Download Card. |
#| mobile_app_id {+Conditional} | string | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`.

Mobile App ID, used to extract tag information from Google Play or App Store. 
- For an iOS app, please find the ID number in the app’s App Store URL as the string of numbers directly after `id`. 
For instance, in `https://apps.apple.com/us/app/hyperpure/id1203646221` the ID would be `1203646221`. 
- For an Android app, please find the package name in the app’s Google Play store URL after `id`. 
For instance, in `https://play.google.com/store/apps/details?id=com.innersloth.spacemafia` the ID would be `com.innersloth.spacemafia`. |
#| country_code {+Conditional} | string[] | Required when `creative_portfolio_type` is `DOWNLOAD_CARD`. 

Country or location code of the region you want to target. 

For enum values, see [Appendix - Location code](https://ads.tiktok.com/marketing_api/docs?id=1737585867307010). |
#| sticker_param {+Conditional} | object | Required when `creative_portfolio_type` is  `STICKER`. 

Details of the Countdown Sticker or Gift Code Sticker you want to create. 

You can see an example of Countdown Sticker in [Countdown Sticker](https://ads.tiktok.com/help/article?aid=10007423) and an example of Gift Code Sticker in [Gift Code Sticker](https://ads.tiktok.com/help/article/tiktok-interactive-add-on-gift-code-sticker?lang=en). 

**Note**: You can only create one Countdown Sticker or Gift Code Sticker at a time. |
##| sticker_type | string | Sticker type. 

Default value: `COUNTDOWN`. 

Enum values: 
- `COUNTDOWN`: A Countdown Sticker with no reminder.
- `REMINDER_COUNTDOWN`: A Countdown Sticker with reminder for a non-LIVE event.
- `LIVE_REMINDER_COUNTDOWN`: A Countdown Sticker with reminder for a LIVE event.
- `GIFTCODE`: A Gift Code Sticker that aims to gain new customers and engage existing customers by providing virtual gifts or coupon redemption codes.  |
##| title {+Conditional} | string | Required when `creative_portfolio_type` is set to `STICKER`. 

Sticker title. 

- For a Countdown Sticker, the maximum length is 54, in UTF-8 bytes, and the hashtag symbol (#) is not supported.
- For a Gift Code Sticker, the maximum length is 20 in UTF-8 bytes.|
##| giftcode {+Conditional}| string |Required when `sticker_type` is set to `GIFTCODE`. 
Not supported when `sticker_type` is not set to `GIFTCODE`. 

Gift code. 

The maximum length is 10 in UTF-8 bytes.|
##| cutoff_time {+Conditional}| string | Required when `sticker_type` is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`. 
Not supported when `sticker_type` is set to `GIFTCODE`. 

Countdown deadline (when `sticker_type` is `COUNTDOWN` or `REMINDER_COUNTDOWN`) or LIVE start time (when `sticker_type` is `LIVE_REMINDER_COUNTDOWN`) for the Countdown Sticker, in the format of "2022-10-30 00:00:00" (UTC+0 Time). 

**Note**: The time you pass in via this field is regarded as UTC+0 time by default and you cannot modify the default time zone. |
##| color {+Conditional}| string | Required when `creative_portfolio_type` is set to `STICKER`. 

Background color of the sticker. 

- For a Countdown Sticker, the supported enum values are `ORANGE`(orange), `BLACK`(black), `RED`(red), and `BLUE`(blue).
- For a Gift Code Sticker, the supported enum values are `BLACK`(black) and `BLUE`(blue). |
##| display_angle {+Conditional}| integer | Required when `sticker_type` is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`. 
Not supported when `sticker_type` is set to `GIFTCODE`. 

Sticker display angle. 

Value range: `[-180, +180]`. 

`+90` means to rotate the sticker clockwise by 90 degrees. |
##| predefined_placement {+Conditional}| string | 
- When `sticker_type` is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`, you need to pass in the field `predefined_placement`, or the fields `position_x`, `position_y` and `size`. 
- When `sticker_type` is set to `GIFTCODE`, you need to pass in the field `predefined_placement`,  or the fields `position_x`, `position_y`.  Use this field to predefine: 
- the x-axis and y-axis coordinates for a Gift Code Sticker
- OR the x-axis and y-axis coordinates, and the size for a Countdown Sticker. 

- For instance, if you set `predefined_placement`  to `55x143x0.9`, then for the **Countdown Sticker**, the x-axis coordinate will be 55, the y-axis coordinate will be 143, and the size will be 90%.
- Similarly, if you set `predefined_placement`  to `86x179`, then for the **Gift Code Sticker**, the x-axis coordinate will be 86, and the y-axis coordinate will be 179.
To learn about the enum values of this field, see the section "Predefined placements". 
 
**Note**: 
-  If you specify the `predefined_placement` for a Countdown Sticker and also provide values for `position_x`, `position_y`, and `size` parameters simultaneously, the values of `position_x`, `position_y`, and `size` will be ignored.
- If you specify the `predefined_placement` parameter for a Gift Code Sticker and also provide values for `position_x`and `position_y` parameters simultaneously, the values of `position_x` and `position_y` will be ignored. |
##| position_x {+Conditional}| integer | 
- When `sticker_type` is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`, you need to pass in the field `predefined_placement`, or the fields `position_x`, `position_y` and `size`.  
- When `sticker_type` is set to `GIFTCODE`, you need to pass in the field `predefined_placement`,  or the fields `position_x`, `position_y`. 
The x-axis coordinate relative to the top-left corner of the screen.  

- For Countdown Sticker: 
The value range of this field varies depending on the sticker size:  When `size` is set to `0.6`,  the value range is [50, 301].
- When `size` is set to `0.7`,  the value range is [50, 253].
- When `size` is set to `0.8`,  the value range is [50, 205].
- When `size` is set to `0.9`,  the value range is [50, 157].
- When `size` is set to `1`,  the value range is [50, 109].
- When` size` is set to `1.1`,  the value range is [50, 61].
- For Gift Code Sticker: 
The value range is [79, 145].**Note**: If you pass in both `predefined_placement` and `position_x` for a Countdown Sticker or Gift Code sticker, `position_x` will be ignored.|
##| position_y {+Conditional}| integer |
- When `sticker_type` is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`, you need to pass in the field `predefined_placement`, or the fields `position_x`, `position_y` and `size`.  
- When `sticker_type` is set to `GIFTCODE`, you need to pass in the field `predefined_placement`,  or the fields `position_x`, `position_y`. 
The y-axis coordinate relative to the top-left corner of the screen. 

- For Countdown Sticker: 
The value range of this field varies depending on the sticker size:  When `size` is set to `0.6`,  the value range is [141, 639].
- When `size` is set to `0.7`,  the value range is [141, 606].
- When `size` is set to `0.8`,  the value range is [141, 573].
- When `size` is set to `0.9`,  the value range is [141, 540].
- When `size` is set to `1`,  the value range is [141, 506].
- When` size` is set to `1.1`,  the value range is [141, 473].
- For Gift Code Sticker: 
The value range is [169, 683]. **Note**: If you pass in both `predefined_placement` and `position_y` for a Countdown Sticker or Gift Code sticker, `position_y` will be ignored.|
##| size {+Conditional}| string |
- When `sticker_type` is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`, you need to pass in the field `predefined_placement`, or the fields `position_x`, `position_y` and `size`.  
- When `sticker_type` is set to `GIFTCODE`, the field size is not supported. 
 Sticker size by percentage. 
 
 Enum values: `0.6`(60%), `0.7`(70%), `0.8`(80%), `0.9`(90%), `1`(100%), `1.1`(110%). 

**Note**: If you pass in both `predefined_placement` and `size` for a Countdown Sticker, `size` will be ignored. |
##| opacity {+Conditional}| string | 
- Required when sticker_type is set to `COUNTDOWN`, `REMINDER_COUNTDOWN`, or `LIVE_REMINDER_COUNTDOWN`.
- Not supported when `sticker_type` is set to `GIFTCODE`.  
 Sticker opacity. 
 
 Enum values: `0.7`, `0.8`, `0.9`, `1`.  
 
The lower the value, the more transparent the sticker will be. |
##| reminder_time {+Conditional} | string | The time set for the reminder. Required when `sticker_type` is `REMINDER_COUNTDOWN` or `LIVE_REMINDER_COUNTDOWN`.

For non-LIVE stickers (when `sticker_type`= `REMINDER_COUNTDOWN`), the enum values are:
- `ONE_MINUTE_EARLIER`: send the reminder one minute before the non-LIVE event.
- `ONE_HOUR_EARLIER `: send the reminder one hour before the non-LIVE event.
- `ONE_DAY_EARLIER`: send the reminder one day before the non-LIVE event.

For LIVE stickers (when `sticker_type` is `LIVE_REMINDER_COUNTDOWN`), the enum values are:
-  `ONE_MINUTE_AFTER`: send the reminder one minute after the LIVE event starts.
- `FIVE_MINUTES_AFTER`: send the reminder five minutes after the LIVE event starts.
- `TEN_MINUTES_AFTER`: send the reminder ten minutes after the LIVE event starts. |
##| landing_page_url{+Conditional} | string | Required when `sticker_type` is `REMINDER_COUNTDOWN`.
 
The landing page URL you will be redirected to when you click the reminder after the countdown for a non-LIVE event ends.  |
##| live_tiktok_user_id{+Conditional} | string |Required when `sticker_type` is `LIVE_REMINDER_COUNTDOWN`. 
 
 TikTok user ID of the LIVE event host.
 
 After specifying this field, you will be redirected to the host's LIVE room when you click the reminder for a LIVE event. |
#| product_source {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` or `PRODUCT_TILE`. 
 When `creative_portfolio_type` is `PRODUCT_TILE`, this field can only be set to `CATALOG`. 

Product source where you want to get products for promotion. 
 
Enum values: `UNSET`, `CATALOG`(Catalog), `STORE` (TikTok Shop), `SHOWCASE` (TikTok Showcase). 

 
If you set this field as `STORE`, you need to pass in `item_group_ids` at the same time. 
 
**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad group level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| identity_id {+Conditional} | string | Required when `creative_portfolio_type`is `PRODUCT_CARD` or `PRODUCT_TILE`. 
 
 Identity ID. |
#| identity_type {+Conditional} | string | Required when `creative_portfolio_type`is `PRODUCT_CARD` or `PRODUCT_TILE`. 
When `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is `STORE`, the supported values for this field are `AUTH_CODE`, `TT_USER`, and `BC_AUTH_TT`.
 
 Identity type. 
 
Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`. 
 
For details about identities, see [Identities](https://ads.tiktok.com/marketing_api/docs?id=1738958351620097). |
#| identity_authorized_bc_id {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` or `PRODUCT_TILE` and `identity_type` is `BC_AUTH_TT`.  
 
ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
#| catalog_id {+Conditional} | string | Required when `creative_portfolio_type`is `PRODUCT_CARD` and `product_source` is `CATALOG`, or when `creative_portfolio_type` is set to `PRODUCT_TILE`.
 
Catalog ID. 
 
**Note**:
-  You can use [/store/list/](https://ads.tiktok.com/marketing_api/docs?id=1752267762718722) to get the `catalog_id`, `store_id` and `store_authorized_bc_id` for available stores under an ad account.
-  If you have created a Product Card and want to use it during ad creation, ensure that at the **ad group level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| catalog_authorized_bc_id {+Conditional} | string | Required when `creative_portfolio_type`is `PRODUCT_CARD` and `product_source` is set as `CATALOG`, or when `creative_portfolio_type` is set to `PRODUCT_TILE`.
 
ID of the Business Center that is authorized to access the catalog (`catalog_id`). 
 
**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad group level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| store_id {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `STORE`. 
 Not supported when `creative_portfolio_type` is set to `PRODUCT_TILE`.
 
ID of the TikTok Shop. 
 
**Note**: 
-  To get the TikTok Shop ID, you can use [/bc/asset/get/](https://ads.tiktok.com/marketing_api/docs?id=1739432717798401):  When in the response `asset_type` is `TIKTOK_SHOP`, the returned `asset_id` is the TikTok Shop ID.  
-  If you have created a Product Card and want to use it during ad creation, ensure that at the **ad group level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product.  |
#| store_authorized_bc_id {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `STORE`. 
 Not supported when `creative_portfolio_type` is set to `PRODUCT_TILE`.
 
 ID of the Business Center that is authorized to access the store (`store_id`). 
 
**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad group level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| product_specific_type {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `CATALOG`, or when `creative_portfolio_type` is set to `PRODUCT_TILE`.
 
The way that you specify the products. 
 
Enum values:  
- `ALL`: All products. Allow TikTok to dynamically choose from all catalog products. You don't need to specify any of `sku_ids`, `item_group_ids` and `product_set_id` at the same time.
- `PRODUCT_SET`: Product set. Select a product set. TikTok will dynamically choose products from this set. You need to specify `item_group_ids` or `product_set_id` at the same time. 
- `CUSTOMIZED_PRODUCTS`: Specific products. Select up to 20 products from your catalog. You need to specify `sku_ids` at the same time.
**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| product_set_id {+Conditional} | string | When `creative_portfolio_type` is `PRODUCT_CARD` or `PRODUCT_TILE` and `product_specific_type` is `PRODUCT_SET`, you need to pass in either `product_set_id` or `item_group_ids`. 
 
ID of the Product Set. You can call [/catalog/set/get/](https://ads.tiktok.com/marketing_api/docs?id=1740570556295169) to get a list of Product Sets in a catalog under your Business Center. 
 
**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| item_group_ids {+Conditional} | string[] | Required when `creative_portfolio_type`is `PRODUCT_CARD` and `product_source` is set as `STORE`. 
 
When `creative_portfolio_type` is  `PRODUCT_CARD` or `PRODUCT_TILE` and `product_specific_type` is `PRODUCT_SET`, you need to pass in either `product_set_id` or `item_group_ids`. 

Product SPU IDs. 

Max size: 20. 

**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| sku_ids {+Conditional} | string[] | Required when `creative_portfolio_type` is `PRODUCT_CARD` or `PRODUCT_TILE` and `product_specific_type` is set as `CUSTOMIZED_PRODUCTS`.

 Product SKU IDs.

 Max size: 20. 

**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad level** you pass to the same field the value that is used for creating the Product Card. Otherwise, when the ad is delivered, the product thumbnail in the Product Card may not be of the promoted product. |
#| dynamic_format {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `CATALOG`.
 Not supported when `creative_portfolio_type` is set to `PRODUCT_TILE`. 

When `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `STORE`, you cannot set `dynamic_format` as `DYNAMIC_CREATIVE`. You can choose not to pass in the field or set it as `UNSET`. 

Whether to enable Dynamic Format. Dynamic Format combines video creative, product cards, and landing pages into different variations based on a shopper's purchase intent, maximizing conversions for you.

Enum values: `UNSET`, `DYNAMIC_CREATIVE` (Use Dynamic Format to create creatives). 

**Note**:
-  `dynamic_format` cannot be enabled for retargeting ads (i.e. when `shopping_ads_retargeting_type` in the ad group is not `OFF`). When `dynamic_format` is `DYNAMIC_CREATIVE`, we will automatically create cards. This means that you won't need to pass all card related fields (`card_show_price`, `card_tags`, `card_image_index`).
-  If you have created a Product Card and want to use it during ad creation, ensure that at the **ad level** you pass to the same field the value that is used for creating the Product Card. |
#| vertical_video_strategy {+Conditional} | string | Required when `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `CATALOG`.
 Not supported when `creative_portfolio_type` is set to `PRODUCT_TILE`.

 When `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `STORE`, you can choose not to pass in the field or set it as `SINGLE_VIDEO`.

The video type that you use for Product Sales scenarios. 

Enum values: `UNSET` (unset), `SINGLE_VIDEO` (single video), `CATALOG_VIDEOS` (catalog video). 

 It must be `UNSET` if `dynamic_format` is `DYNAMIC_CREATIVE`. 

**Note**: If you have created a Product Card and want to use it during ad creation, ensure that at the **ad level** you pass to the same field the value that is used for creating the Product Card. |
#| ad_text | string | Valid when `creative_portfolio_type` is `PRODUCT_CARD`. 

An ad text. It is shown to your audience as part of your ad creative, to deliver the message you intend to communicate to them. 
 
If you don't know how to create effective ad texts, you can try the [Smart Text](https://ads.tiktok.com/marketing_api/docs?id=1739084248002626) feature, which generates ad text recommendations based on the industry and language.
 
**Note**:
-  Ad text must be 1-100 characters long and cannot contain emoji. 
-  Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character.  |
#| card_show_price {+Conditional} | boolean | Required when `creative_portfolio_type` is `PRODUCT_CARD`. 

 Whether to show the price of products on the Product Card or not. |
#| card_tags {+Conditional} | string[] | Required when `creative_portfolio_type` is  `PRODUCT_CARD`. 

The product tags that you want to show on the Product Card. 

Enum values: `BRAND` (Brand Name), `DESC` (Description). |
#| card_image_index | integer | Valid when `creative_portfolio_type` is `PRODUCT_CARD` or `PRODUCT_TILE`. 

You can use this field to specify the image used in the Product Card or Product Tiles. The number you set via this field will be used as index to query the Image URLs you have passed through `additional_image_urls` in [/catalog/product/upload/](https://ads.tiktok.com/marketing_api/docs?id=1740497429681153). 

For instance, `card_image_index` is 1 means that you will use the image via the second image URL in `additional_image_urls`. |
#| showcase_products {+Conditional}| object[] | Required when `creative_portfolio_type` is `PRODUCT_CARD` and `product_source` is set as `SHOWCASE`. 

See [Create Video Shopping Ads with products from Showcase](https://ads.tiktok.com/marketing_api/docs?id=1759232259360770) to learn more.

The list of Showcase products that you want to use in your ad. 

Max size: 20.

You can get the available Showcase products via [/showcase/product/get/](https://ads.tiktok.com/marketing_api/docs?id=1759233576199169). |
##| item_group_id | string | SPU ID of the product. |
##| store_id | string | The ID of the store that the product (`item_group_id`) belongs to.

 Note that the only supported store type is TikTok Shop. |
##| catalog_id | string | The ID of the catalog that the product (`item_group_id`) belongs to. |
```
### Example

#### Creating a Product Card Portfolio with products from a catalog

```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/portfolio/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "advertiser_id": "{{advertiser_id}}",
    "creative_portfolio_type": "PRODUCT_CARD",
    "portfolio_content": [{
        "product_source": "CATALOG",
        "catalog_id": "{{catalog_id}}",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "product_specific_type": "PRODUCT_SET",
        "ad_text": "{{ad_text}}",
        "identity_id": "{{identity_id}}",
        "identity_type": "{{identity_type}}",
        "dynamic_format": "UNSET",
        "vertical_video_strategy": "SINGLE_VIDEO",
        "card_show_price": true,
        "card_tags": ["BRAND"],
        "item_group_ids": ["{{item_group_ids}}"],
        "card_image_index": 0
    }]
}'
(/code)
```

#### Creating a Product Card Portfolio with products from TikTok Shopping
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/portfolio/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "advertiser_id": "{{advertiser_id}}",
    "creative_portfolio_type": "PRODUCT_CARD",
    "portfolio_content": [{
        "product_source": "STORE",
        "identity_id": "{{identity_id}}",
        "identity_type": "{{identity_type}}",
        "store_id": "{{store_id}}",
        "store_authorized_bc_id": "{{store_authorized_bc_id}}",
        "item_group_ids": ["{{item_group_ids}}"],
        "card_show_price": true,
        "card_tags": ["BRAND"]
    }]
}'
(/code)
```
#### Creating a Product Tiles portfolio
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/creative/portfolio/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "creative_portfolio_type": "PRODUCT_TILE",
    "portfolio_content": [
        {
            "product_source": "CATALOG",
            "identity_id": "{{identity_id}}",
            "identity_type": "CUSTOMIZED_USER",
            "catalog_id": "{{catalog_id}}",
            "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
            "product_specific_type": "CUSTOMIZED_PRODUCTS",
            "sku_ids": [
                "{{sku_id}}",
                "{{sku_id}}",
                "{{sku_id}}",
                "{{sku_id}}"
            ],
            "card_image_index": 0
        }
    ]
}'
(/code)
```

## Response

``` xtable
|Field{35%}|Type{15%}|Description{50%}|
|-|-|-|
|message |string|The return message. For example, see [Appendix-Return information](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|code |number|The return code. For details, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|data |object|The returned data|
#| creative_portfolio_id | string | ID of the creative portfolio that has just been created|
|request_id |string|Request log ID|
```

### Example

``` xcodeblock
(code JSON python)
HTTPS/1.1 200 OK
{
    "message": "OK",
    "code": 0,
    "data": {
        "creative_portfolio_id": "6911933716445006853"
    },
    "request_id": "2020123008310401023125104012852"
}
(/code)
```

## Predefined placements
The two tables below list the enum values for the field `predefined_placement` and the corresponding examples.
### For a Countdown Sticker
```xtable
|Enum values{50%}|Example{50%}|
|---|---|---|
| `196x148x0.8` | Top right
 |
| `57x148x0.8` | Top left
  |
| `196x564x0.8` | Bottom right
  |
| `57x564x0.8` | Bottom left 
 |
| `129x370x0.8` | Center
  |
|`55x143x0.9`||
|`157x141x0.9`||
|`110x236x0.9`||
|`112x327x0.9`||
|`105x533x0.9`||
|`53x533x0.9`||
|`143x533x0.9`||
|`55x143x0.9`||
|`157x141x0.9`||
|`110x236x0.9`||
|`112x327x0.9`||
|`105x533x0.9`||
|`53x533x0.9`||
|`143x533x0.9`||
```

### For a Gift Code Sticker
```xtable
|Enum values{50%}|Example{50%}|
|---|---|---|
| `141x176`  | Top right
 |
| `86x176`  | Top left
 |
| `141x678` | Bottom right
 |
| `86x678`  | Bottom left
 |
| `112x432`  | Center
 |
|`86x179`||
|`113x179`||
|`113x308`||
|`113x462`||
|`113x676`||
|`88x676`||
|`138x676`||
|`86x179`||
|`113x179`||
|`113x308`||
|`113x462`||
|`113x676`||
|`88x676`||
|`138x676`||
```
