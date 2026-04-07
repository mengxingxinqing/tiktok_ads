# Get a portfolio by ID

**Doc ID**: 1739092113671170
**Path**: API Reference/Creative Portfolios/Get a portfolio by ID

---

Use this endpoint to get an existing creative portfolio by its ID. You can get portfolios that are created with the [/creative/portfolio/create/](https://ads.tiktok.com/marketing_api/docs?id=1739091950439426) endpoint. 

## Comparing v1.2 and v1.3
The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
|Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/creative/portfolio/get/|/v1.3/creative/portfolio/get/ |
| Request parameter data type | `advertiser_id`: number 
`creative_portfolio_id`: number |`advertiser_id`: string 
`creative_portfolio_id`: string|
| Response parameter name | `advanced_show_time` 
 `advanced_guide_text_bottom` 
 `advanced_position` 
 `advanced_image_info` 
 `portfolio_type`| `badge_show_time` 
 `call_to_action_text` 
 `badge_position` 
 `badge_image_info` 
 `creative_portfolio_type`|
| Response parameter data type | `asset_ids`: number[] 
`portfolio_content`: object[]| `asset_ids`: string[]
`portfolio_content`: object|
| New response parameters |/|`creative_portfolio_id` 
`sticker_param` (including all the parameters within the object ) 
`tags`
`layouts`
`description` 
`category_label` 
`app_id` 
`card_show_price`
 `card_tags`
 `card_image_index`
`title`
`selling_points`
 `content_url`
 `pop_up_window_image_id`
`gesture_type`
`slide_length`
`slide_dimension`
`interactive_music_id`|
| Response parameters deprecated in v1.3|/|The following parameters are deprecated as a result of `GAME_GIFT` card types no longer being supported: 
 `profile_image`
 `display_name` 
 `gift_card_title`  
 `gift_card_detail`  
 `gift_card_code` 
 `thumbnail_url`|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/creative/portfolio/get/

**Method** GET

**Header**

``` xtable
|Field{35%}|Type{15%}|Description{50%}|
|---|---|---|
|Access-Token {required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
|Field{35%}|Type{15%}|Description{50%}|
|--- |--- |--- |
|advertiser_id {required}|string| Advertiser ID|
|creative_portfolio_id {required}|string| ID of the creative portfolio that you want to get. 
You can find the portfolio id (`creative_portfolio_id`) in the response of [/creative/portfolio/create/](https://ads.tiktok.com/marketing_api/docs?id=1739091950439426).|
```
### Example
```xcodeblock
(code curl http)
curl --location --request GET https://business-api.tiktok.com/open_api/v1.3/creative/portfolio/get/?advertiser_id={{advertiser_id}}&creative_portfolio_id={{creative_portfolio_id}}
--header 'Access-Token: {{Access-Token}}'
--header 'Content-Type: application/json'
(/code)
```

## Response

``` xtable
|Field{35%}|Type{15%}|Description{50%}|
|-|-|-|
|message |string|The return message. For example, see [Appendix-Return information](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|code |number|The return code. For details, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|data |object|The returned data.|
#|creative_portfolio_id|string|Creative portfolio ID.|
#|creative_portfolio_type|string|Creative portfolio type. 

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
**Note**: 
- Website info cards can only be used for auction ads with the `objective_type` as `WEB_CONVERSIONS` or `TRAFFIC` (with `promotion_type` set to `WEBSITE`).
- You can only use the Inventory Card portfolio in Automotive Ads.
- Product Cards can only be used in Video Shopping Ads.
- Product Tiles can only be used in Video Shopping Ads with product source as catalog.
- Using a Product Tiles portfolio to create ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Countdown Sticker can only be used for auction ads with the advertising objective (`objective_type`) as Reach (`REACH`), Traffic (`TRAFFIC`), Video views(`VIDEO_VIEW`), App promotion (`APP_PROMOTION`), Lead generation(`LEAD_GENERATION`), Website conversions (`WEB_CONVERSIONS`), or Product sales (`PRODUCT_SALES`), as well as for R&F (`RF_REACH`) ads.Reminder Countdown Sticker (`sticker_type` as `REMINDER_COUNTDOWN` or `LIVE_REMINDER_COUNTDOWN`) is an allowlist-only feature for Traffic (`TRAFFIC`), App promotion (`APP_PROMOTION`), Website conversions (`WEB_CONVERSIONS`) ads. If you would like to access it for ads with these objectives, please contact your TikTok representative. 
- Gift Code Sticker can only be used for auction ads with the advertising objective (`objective_type`) as Reach (`REACH`), Traffic (`TRAFFIC`), Video views(`VIDEO_VIEW`),  App promotion (`APP_PROMOTION`),  Lead generation(`LEAD_GENERATION`), Website conversions (`WEB_CONVERSIONS`), or Product sales (`PRODUCT_SALES`), as well as for R&F ads with the advertising objective(`objective_type`) as Reach (`RF_REACH`).
- Gestures can only be used for auction ads with the `objective_type` (advertising objective) as `REACH`, `TRAFFIC`, `VIDEO_VIEWS` (with `optimization_goal` as `ENGAGED_VIEW`), `APP_PROMOTION`, `WEB_CONVERSIONS`, as well as for R&F ads with the advertising objective (`objective_type`) as Reach (`RF_REACH`).  Using Gesture portfolios in campaigns with the advertising objective `APP_PROMOTION`, `TRAFFIC`, or `WEB_CONVERSIONS` are currently separate allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Superlikes can only be used for auction ads with the `objective_type` (advertising objective) as `REACH`, `TRAFFIC`, `VIDEO_VIEWS` (with `optimization_goal` as `ENGAGED_VIEW`), `ENGAGEMENT` (with `optimization_goal` as `PAGE_VISIT`), `APP_PROMOTION`, `WEB_CONVERSIONS`, as well as for R&F ads with the advertising objective (`objective_type`) as Reach (`RF_REACH`).  Using Superlike portfolios in campaigns with the advertising objective `APP_PROMOTION` or `TRAFFIC` are currently separate allowlist-only features. If you would like to access them, please contact your TikTok representative.  |
#|portfolio_content|object[]|The content of the creative portfolio.|
##|asset_content|string|A call-to-action text. 

For example, `"Learn More"`.|
##|asset_ids|string[]|A list of CTAs. 

For example, `[201781, 201535]`.|
##|card_type| string| Card type. 

Enum value: `IMAGE`(Display Card).|
##| gesture_type | string | Returned when `creative_portfolio_type` is `GESTURE`.

Gesture type.

Enum values:  
- `CLICK`: Click Gesture.  
- `STRAIGHT_SLIDE`: Straight Slide Gesture.  
- `CURVED_SLIDE`: Curved Slide Gesture.|
##|image_id | string| Returned only when `creative_portfolio_type` is `CARD`, `WEB_INFO_CARD`, `INVENTORY_CARD`, or `SUPER_LIKE`.

Image ID. |
##| pop_up_window_image_id | string | Returned in any of the following scenarios: 
- `creative_portfolio_type` is `GESTURE`.  
- `creative_portfolio_type` is `SUPER_LIKE` and a `pop_up_window_image_id` is specified during portfolio creation..
The gesture pop-up card in the Gesture or the ID of the pop-up window image in the Superlike.

  
- When `creative_portfolio_type` is `GESTURE`, this field represents the gesture pop-up card that will appear after the viewer follows the gesture.  
- When `creative_portfolio_type` is `SUPER_LIKE`, this field represents the pop-up window that will appear after the Superlike finishes floating across the screen and will take the audience to the ad landing page when they click on it.|
##| title | string| Returned only when `creative_portfolio_type` is `WEB_INFO_CARD`.

The title of the card. |
##| selling_points | string[]| Returned only when `creative_portfolio_type` is `WEB_INFO_CARD`.

The reasons why your products are worth buying. |
##| content_url | string| Returned only when `creative_portfolio_type` is `WEB_INFO_CARD`.

The website URL of your landing page. 

**Note**:
- Specifying the `content_url` in a website info card via API is currently not supported. You can only retrieve the `content_url` of website info cards created via the TikTok Ads Manager.
- For website info cards created via API, the value of this field will be an empty string (`""`). |
##|thumbnail_id | string| Returned only when `creative_portfolio_type` is `DOWNLOAD_CARD`, `PRODUCT_CARD`, `PRODUCT_TILE`, or `PREMIUM_BADGE`.

Thumbnail ID. |
##|call_to_action_text|string| Returned when `creative_portfolio_type` is `GESTURE` or `PREMIUM_BADGE`.

Interactive guide text for the Gesture or Pop-out Showcase.|
##|badge_show_time|integer| Returned when `creative_portfolio_type` is `GESTURE` or `PREMIUM_BADGE`.

The time when the Gesture icon within the Gesture or the Premium Badge within the Pop-out Showcase will appear in your video, in seconds.|
##|badge_position|object| Returned when `creative_portfolio_type` is `GESTURE` or `PREMIUM_BADGE`.

Information about the position of the Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.|
###|position_x| float| Relative X-axis value of the top-left corner of the Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.|
###|position_y| float| Relative Y-axis value of the top-left corner of the Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.|
###| angle  | number | Returned when `badge_position` is specified and any of the following conditions is met: 
- `creative_portfolio_type` is `GESTURE` and `gesture_type` is `STRAIGHT_SLIDE` or `CURVED_SLIDE`. 
- `creative_portfolio_type` is `PREMIUM_BADGE`.
The angle of the Straight Slide Gesture or Curved Slide Gesture icon within a Gesture or the Premium Badge within a Pop-out Showcase.|
##|badge_image_info|object|Returned when `creative_portfolio_type` is `PREMIUM_BADGE`.

Information about the badge image in the Pop-out Showcase.|
###|image_id|string|ID of the badge image in the Pop-out Showcase.|
##| slide_length  | number | Returned when `creative_portfolio_type` is `GESTURE` and `gesture_type` is `STRAIGHT_SLIDE`.

The length of the Straight Slide Gesture.|
##| slide_dimension  | object | Returned when `creative_portfolio_type` is `GESTURE` and `gesture_type` is `CURVED_SLIDE`.

The dimensions of the Curved Slide Gesture.|
###| dimension_width  | number | The width of the Curved Slide Gesture.|
###| dimension_height  | number | The height of the Curved Slide Gesture.|
##| interactive_music_id  | string | Returned when `creative_portfolio_type` is `GESTURE`.

The URL of the background music for the Gesture.|
##| layouts | string[] | Returned when `creative_portfolio_type`= `DOWNLOAD_CARD`.
The layout type of the Download Card. Enum values: 
- `TYPE_1`: Type 1, showing app description in the Download Card. 
-  `TYPE_2` : Type 2, not showing app description in the Download Card.   When both `TYPE_1` and `TYPE_2` have been passed in this field, one Type 1 Download card and one Type 2 Download card will be created . |
##| description | string | Returned in any of the following scenarios:
- `creative_portfolio_type` is `DOWNLOAD_CARD` and the value of `layouts` includes `TYPE_1`. 
- `creative_portfolio_type` is `INVENTORY_CARD`. 
Description of the app that you want to promote in the Download Card or text of the Inventory Card. |
##| tags | string[] | Returned when `creative_portfolio_type`= `DOWNLOAD_CARD`. 
Tags for the Download Card. Enum values: 
-  `CATEGORIES`：Showing the category of the app you want to promote in the Download Card. 
- `FILESIZE`：Showing the file size of the app you want to promote in the Download Card. 
- `RATING`：Showing the rating of the app you want to promote in the Download Card. 
- `RANKING`：Showing the ranking of the app you want to promote in the Download Card. 
-  `COMMENT_VOLUME`：Showing the number of comments for the app you want to promote in the Download Card.  |
##| category_label | string | Returned when `creative_portfolio_type`= `DOWNLOAD_CARD` and `category_label` is specified during card creation.  
Category name of the app you want to promote in the Download Card. |
##| app_id | string | Returned when `creative_portfolio_type`= `DOWNLOAD_CARD`. 
 ID of the app that you want to promote in the Download Card. It's the App ID from Events Manager. |
##| sticker_param | object | Details of the Countdown Sticker or Gift Code Sticker you want to create. You can see an example of Countdown Sticker in [Countdown Sticker](https://ads.tiktok.com/help/article?aid=10007423) and an example of Gift Code Sticker in [Gift Code Sticker](https://ads.tiktok.com/help/article/tiktok-interactive-add-on-gift-code-sticker?lang=zh). 

Returned only when `creative_portfolio_type`=`STICKER`.
**Note**: You can only create one Countdown Sticker or Gift Code Sticker at a time. |
###| sticker_type | string | Sticker type. 

Enum values: 
- `COUNTDOWN`: A Countdown Sticker with no reminder.
- `REMINDER_COUNTDOWN`: A Countdown Sticker with reminder for a non-LIVE event.
- `LIVE_REMINDER_COUNTDOWN`: A Countdown Sticker with reminder for a LIVE event. 
- `GIFTCODE`: A Gift Code Sticker that aims to gain new customers and engage existing customers by providing virtual gifts or coupon redemption codes. |
###| title | string | Sticker title. 

- For a Countdown Sticker, the maximum length is 54, in UTF-8 bytes, and the hashtag symbol (#) is not supported.
- For a Gift Code Sticker, the maximum length is 20 in UTF-8 bytes. |
###| giftcode | string | Gift code. 
This field is only applicable for Gift Code Stickers. The maximum length is 10 in UTF-8 bytes (10 letters and numbers). |
###| cutoff_time | string | Countdown deadline (when `sticker_type`= `COUNTDOWN` or `REMINDER_COUNTDOWN`) or LIVE start time (when `sticker_type`=`LIVE_REMINDER_COUNTDOWN`) for the Countdown Sticker, in the format of "2022-10-30 00:00:00" (UTC+0 Time). 
**Note**: The time your pass in via this field is regarded as UTC+0 time by default and you cannot modify the default time zone. |
###| color | string | Background color of the sticker. 

- For a Countdown Sticker, the supported enum values are `ORANGE`(orange), `BLACK`(black), `RED`(red), and`BLUE`(blue).
- For a Giftcode Sticker created through the API, only `BLACK` and `BLUE` will be returned. However, `ORANGE` and `RED` may be returned for a Gift Code Sticker created on TTAM when orange and red were supported for Gift Code Stickers.|
###| display_angle | integer | Sticker display angle. Value range: `[-180, +180]`. `+90` means to rotate the sticker clockwise by 90 degrees. 
**Note**: This field is not returned for a Gift Code Sticker created through the API. However, it may be returned for a Gift Code Sticker created on TTAM when the `display_angle` setting was supported for Gift Code Stickers.|
###| predefined_placement | string | 
- If the portfolio is a Gift Code Sticker and the predefined placement of the sticker corresponds to an enum value in [Predefined placements](https://business-api.tiktok.com/portal/docs?id=1739091950439426#item-link-Predefined%20placements), this field returns  x-axis and y-axis coordinates. 
- If the portfolio is a Countdown Sticker and the predefined placement of the sticker corresponds to an enum value in [Predefined placements](https://business-api.tiktok.com/portal/docs?id=1739091950439426#item-link-Predefined%20placements), this field returns  x-axis and y-axis coordinates, and size. 
For example:
If the x-axis coordinate, y-axis coordinate and size of the Countdown Sticker are 196, 148, and 0.8, respectively, which corresponds to the enum value `196x148x0.8` in [Predefined placements](https://business-api.tiktok.com/portal/docs?id=1739091950439426#item-link-Predefined%20placements), this field will be returned as `196x148x0.8`.

**Note**: If the sticker does not correspond to any enum value in [Predefined placements](https://business-api.tiktok.com/portal/docs?id=1739091950439426#item-link-Predefined%20placements),  this field returns `null`. |
###| position_x | integer | The x-axis coordinate relative to the top-left corner of the screen. |
###| position_y | integer | The y-axis coordinate relative to the top-left corner of the screen. |
###| size | string | Sticker size by percentage. Enum values: `0.6`(60%), `0.7`(70%), `0.8`(80%), `0.9`(90%), `1`(100%), `1.1`(110%). 
**Note**: This field is not returned for a Gift Code Sticker created through the API. However, it may be returned for a Gift Code Sticker created on TTAM when the `size` setting was supported for Gift Code Stickers.|
###| opacity | string | Sticker opacity. Enum values: `0.7`, `0.8`, `0.9`, `1`. The lower the value, the more transparent the sticker will be. 
**Note**: This field is not returned for a Gift Code Sticker created through the API. However, it may be returned for a Gift Code Sticker created on TTAM when the `opacity` setting was supported for Gift Code Stickers.|
###| reminder_time| string | The time set for the reminder. Returns value when `sticker_type`= `REMINDER_COUNTDOWN` or `LIVE_REMINDER_COUNTDOWN`.

For non-LIVE stickers (when `sticker_type`= `REMINDER_COUNTDOWN`), the enum values are:
- `ONE_MINUTE_EARLIER`: send the reminder one minute before the non-LIVE event.
- `ONE_HOUR_EARLIER `: send the reminder one hour before the non-LIVE event.
- `ONE_DAY_EARLIER`: send the reminder one day before the non-LIVE event.

For LIVE stickers (when `sticker_type`= `LIVE_REMINDER_COUNTDOWN`), the enum values are:
-  `ONE_MINUTE_AFTER`: send the reminder one minute after the LIVE event starts.
- `FIVE_MINUTES_AFTER`: send the reminder five minutes after the LIVE event starts.
- `TEN_MINUTES_AFTER`: send the reminder ten minutes after the LIVE event starts. |
###| landing_page_url| string | The landing page URL you will be redirected to when you click the reminder after the countdown for an non-LIVE event ends. Returns value when `sticker_type` is `REMINDER_COUNTDOWN`. |
###| live_tiktok_user_id | string | TikTok user ID of the LIVE event host. After specifying this field, you will be redirected to the host's LIVE room when you click the reminder for a LIVE event. 
Returns value when `sticker_type` is `LIVE_REMINDER_COUNTDOWN`.  |
##| card_show_price | boolean | Whether to show the price of products on the Product Card or not. 
##| card_tags | string[] | The product tags that are shown on the Product Card. 
Enum values: `BRAND` (Brand Name), `DESC` (Description). |
##| card_image_index | integer | Used to specify the image used in the Product Card or Product Tiles. 

 The number set via this field is used as index to query the Image URLs you have passed through `additional_image_urls` in [/catalog/product/upload/](https://ads.tiktok.com/marketing_api/docs?id=1740497429681153). 

 For instance, `card_image_index` = 1 means that you will use the image via the second image URL in `additional_image_urls`. |
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
        "portfolio_content": [
            {
                "asset_ids": [
                    "201781",
                    "201535"
                ],
                "asset_content": "learn_more"
            },
            {
                "asset_ids": [
                    "201902",
                    "201404"
                ],
                "asset_content": "download_now"
            }
        ]
    },
    "request_id": "2020123008315601023125104010685"
}
(/code)
```
