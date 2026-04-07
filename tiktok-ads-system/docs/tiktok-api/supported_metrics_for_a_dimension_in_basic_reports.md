# Supported metrics for a dimension in basic reports

**Doc ID**: 1759239462689793
**Path**: Marketing API/Reporting/Guides/Report types/Basic reports/Supported dimensions/Supported metrics for a dimension in basic reports

---

See the tables below to learn about the supported metrics when you use a dimension in basic reports. You can find out the detailed introductions of the metrics in [Basic report-Supported metrics](https://ads.tiktok.com/marketing_api/docs?id=1751443967255553).

## Supported metrics for `ad_type`
```xtable
| Field{30%} | Description{60%}|
|---|---|
| Core metrics ||
#| `spend` | Cost |
#| `cpc` | CPC (destination) |
#| `cpm` | CPM |
#| `impressions` | Impressions |
#| `gross_impressions`` | Gross Impressions (Includes Invalid Impressions) |
#| `clicks` | Clicks (destination) |
#| `ctr` | CTR (destination) |
#| `conversion` | Conversions |
#| `cost_per_conversion` | Cost per conversion |
#| `conversion_rate` | Conversion rate (CVR, clicks) |
#| `real_time_conversion` | Real-time conversions |
#| `real_time_cost_per_conversion` | Real-time cost per conversion |
#| `real_time_conversion_rate` | Real-time conversion rate (CVR, clicks) |
| Videos metrics ||
#| `video_play_actions` | Video views |
#| `video_watched_2s` | 2-second video views |
#| `video_watched_6s` | 6-second video views |
#| `average_video_play` | Average play time per video view |
#| `video_views_p25` | Video views at 25% |
#| `video_views_p50` | Video views at 50% |
#| `video_views_p75` | Video views at 75% |
#| `video_views_p100` | Video views at 100% |
#| `engaged_view` | 6-second focused views |
#| `engaged_view_15s` | 15-second focused views |
| Clicks metrics ||
#| `clicks_on_music_disc` | Music Clicks |
| Social metrics ||
#| `follows` | Paid Followers |
#| `likes` | Paid Likes |
#| `comments` | Paid Comments |
#| `shares` | Paid Shares |
#| `profile_visits` | Paid Profile Visits |
#| `profile_visits_rate` | Paid Profile Visit Rate |
| Website metrics ||
#| Landing page view ||
##| `total_landing_page_view` | Landing page views (website) |
##| `cost_per_landing_page_view` | Cost per landing page view (website) |
##| `landing_page_view_rate` | Landing page view rate (website) |
| Core metrics (SKAN) ||
#| `skan_conversion` | Conversions (SKAN) |
#| `skan_cost_per_conversion` | Cost per conversion (SKAN)

**Note**: This metric cannot be used together with the `ad_type` dimension in asynchronous basic reports. |
#| `skan_conversion_rate` | Conversion rate (SKAN, clicks)

**Note**: This metric cannot be used together with the `ad_type` dimension in asynchronous basic reports. |
| App metrics (SKAN) ||
#| App install ||
##| `skan_app_install` | App install (SKAN) |
##| `skan_cost_per_app_install` | Cost per app install (SKAN) |
#| App install (SKAN Privacy Withheld) ||
##| `skan_app_install_withheld` | App Installs (SKAN Privacy Withheld) |
```

## Supported metrics for `country_code`

``` xtable
| Field{35%} | Description {35%}| Supported in synchronous basic reports {15%}| Supported in asynchronous basic reports {15%}|
|---|---|---|---|
| Core metrics | | | |
#| `spend` | Cost | ✅ | ✅ |
#| `cpc` | CPC (destination) | ✅ | ✅ |
#| `cpm` | CPM | ✅ | ✅ |
#| `impressions` | Impressions | ✅ | ✅ |
#| `gross_impressions` | Gross Impressions (Includes Invalid Impressions) | ✅ | ✅ |
#| `clicks` | Clicks (destination) | ✅ | ✅ |
#| `ctr` | CTR (destination) | ✅ | ✅ |
#| `reach` | Reach | ✅ | ❌ |
#| `conversio`n | Cost per 1,000 people reached | ✅ | ✅ |
#| `cost_per_conversion` | Conversions | ✅ | ✅ |
#| `conversion_rate` | Conversion rate (CVR, clicks) | ✅ | ✅ |
#| `real_time_conversion` | Real-time conversions | ✅ | ✅ |
#| `real_time_cost_per_conversion` | Real-time cost per conversion | ✅ | ✅ |
#| `real_time_conversion_rate` | Real-time conversion rate (CVR, clicks) | ✅ | ✅ |
#| `result` | Results | ✅ | ❌ |
#| `cost_per_result` | Cost per result | ✅ | ❌ |
#| `result_rate` | Result rate | ✅ | ❌ |
#| `real_time_result` | Real-time results | ✅ | ❌ |
#| `real_time_cost_per_result` | Real-time cost per result | ✅ | ❌ |
#| `real_time_result_rate` | Real-time result rate | ✅ | ❌ |
#| `frequency` | Frequency | ✅ | ❌ |
| Videos metrics | | | |
#| `video_play_actions` | Video views | ✅ | ✅ |
#| `video_watched_2s` | 2-second video views | ✅ | ✅ |
#| `video_watched_6s` | 6-second video views | ✅ | ✅ |
#| `average_video_play` | Average play time per video view | ✅ | ✅ |
#| `video_views_p25` | Video views at 25% | ✅ | ✅ |
#| `video_views_p50` | Video views at 50% | ✅ | ✅ |
#| `video_views_p75` | Video views at 75% | ✅ | ✅ |
#| `video_views_p100` | Video views at 100% | ✅ | ✅ |
#| `engaged_view` | 6-second focused views | ✅ | ✅ |
#| `engaged_view_15s` | 15-second focused views | ✅ | ✅ |
| Clicks metrics | | | |
#| `clicks_on_music_disc` | Music Clicks | ✅ | ✅ |
| Social metrics | | | |
#| `follows` | Paid Followers | ✅ | ✅ |
#| `likes` | Paid Likes | ✅ | ✅ |
#| `comments` | Paid Comments | ✅ | ✅ |
#| `shares` | Paid Shares | ✅ | ✅ |
#| `profile_visits` | Paid Profile Visits | ✅ | ✅ |
#| `profile_visits_rate` | Paid Profile Visit Rate | ✅ | ✅ |
| LIVE metrics | | | |
#| `live_product_clicks` | LIVE Product Clicks | ✅ | ❌ |
| App metrics | | | |
#| App install by conversion time | |
##| `real_time_app_install` | App installs by conversion time | ✅ | ❌ |
##| `real_time_app_install_cost` | Cost per app install by conversion time | ✅ | ❌ |
#| App install | | | |
##| `app_install` | App install | ✅ | ❌ |
##| `cost_per_app_install` | Cost per app install | ✅ | ❌ |
#| Registration |  | | |
##| `registration` | Unique registrations (app) | ✅ | ❌ |
##| `cost_per_registration` | Unique cost per registration (app) | ✅ | ❌ |
##| `registration_rate` | Unique registration rate (app) | ✅ | ❌ |
#| Purchase | | | |
##| `purchase` | Unique purchases (app) | ✅ | ❌ |
##| `cost_per_purchase` | Unique cost per purchase (app) | ✅ | ❌ |
##| `purchase_rate` | Unique purchase rate (app) | ✅ | ❌ |
| Website metrics | | | |
#| Complete payment | | | |
##| `complete_payment` | Payments completed (website) | ✅ | ❌ |
##| `cost_per_complete_payment` | Cost per purchase (website) | ✅ | ❌ |
##| `complete_payment_rate` | Unique payment completion rate (website) (%) | ✅ | ❌ |
#| Landing page view  |  | | |
##| `total_landing_page_view` | Landing page views (website) | ✅ | ✅ |
##| `cost_per_landing_page_view` | Cost per landing page view (website) | ✅ | ✅ |
##| `landing_page_view_rate` | Landing page view rate (website) | ✅ | ✅ |
#| Page View {-to be deprecated} | | | |
##| `page_browse_view` | Page Browse | ✅ | ❌ |
##| `cost_per_page_browse_view` | Cost per Page Browse | ✅ | ❌ |
##| `page_browse_view_rate` | Page Browse Rate (%) | ✅ | ❌ |
#| Click button |  | | |
##| `button_click` | Button clicks (website) | ✅ | ❌ |
##| `cost_per_button_click` | Cost per button click (website) | ✅ | ❌ |
##| `button_click_rate` | Unique button click rate (website) | ✅ | ❌ |
#| Contact | | | |
##| `online_consult` | Contacts (website) | ✅ | ❌ |
##| `cost_per_online_consult` | Cost per contact (website) | ✅ | ❌ |
##| `online_consult_rate` | Unique contact rate (website) | ✅ | ❌ |
#| Submit form | | | |
##| `form` | Form submissions (website) | ✅ | ❌ |
##| `cost_per_form` | Cost per form submitted (website) | ✅ | ❌ |
##| `form_rate` | Unique form submission rate (website) (%) | ✅ | ❌ |
#| Download |  | | |
##| `download_start` | Downloads (website) | ✅ | ❌ |
##| `cost_per_download_start` | Cost per download (website) | ✅ | ❌ |
##| `download_start_rate` | Unique download rate (website) (%) | ✅ | ❌ |
```

## Supported metrics for `search_terms`
```xtable
| Field{30%} | Description{60%}|
|---|---|
| Core metrics |  |
#| `spend` | Cost |
#| `cpc` | CPC (destination) |
#| `cpm` | CPM |
#| `impressions` | Impressions 
**Note**: When you use the metric `impressions` together with the dimension `search_terms`, you might get the result 
`"<5"` rather than a number, for instance, `"1.0"`. |
#| `clicks` | Clicks (destination) |
#| `ctr` | CTR (destination) |
#| `conversion` | Conversions |
#| `cost_per_conversion` | Cost per conversion |
#| `conversion_rate` | Conversion rate (CVR, clicks) |
#| `real_time_conversion` | Real-time conversions |
#| `result` | Results |
#| `cost_per_result` | Cost per result |
#| `result_rate` | Result rate |
| Videos metrics |  |
#| `video_play_actions` | Video views |
#| `engaged_view` | 6-second focused views |
#| `engaged_view_15s` | 15-second focused views |
```

## Supported metrics for `page_id`
```xtable
| Field{30%} | Description{60%}|
|---|---|
| TikTok metrics |  |
#| `onsite_form` | Form submissions (TikTok) |
#| `onsite_download_start` | App store clicks (TikTok) |
#| `ix_page_view_count` | Page views (TikTok) |
#| `ix_button_click_count` | Outbound clicks (TikTok) |
#| `ix_product_click_count` | Product clicks (TikTok) |
| Instant experience metrics |  |
#| `ix_page_duration_avg` | Instant experience average view time |
#| `ix_page_viewrate_avg` | Instant experience average view percentage |
#| `ix_video_views` | Instant experience video views |
#| `ix_video_views_p25` | Instant experience video views at 25% |
#| `ix_video_views_p50` | Instant experience video views at 50% |
#| `ix_video_views_p75` | Instant experience video views at 75% |
#| `ix_video_views_p100` | Instant experience video views at 100% |
#| `ix_average_video_play` | Average Instant experience video view time |
| Core metrics |  |
#| `spend` | Cost |
#| `cpc` | CPC (Destination) |
#| `cpm` | CPM |
#| `impressions` | Impressions |
#| `gross_impressions` | Gross impressions (Includes Invalid Impressions) |
#| `clicks` | Clicks (Destination) |
#| `ctr` | CTR (Destination) |
#| `conversion` | Conversions |
#| `cost_per_conversion` | Cost per conversion |
#| `conversion_rate` | Conversion rate (CVR, clicks) |
#| `conversion_rate_v2` | Conversion rate (CVR) |
#| `real_time_conversion` | Real-time conversions |
#| `real_time_cost_per_conversion` | Real-time cost per conversion |
#| `real_time_conversion_rate` | Real-time conversion rate (CVR, clicks) |
#| `real_time_conversion_rate_v2` | Real-time conversion rate (CVR) |
```

## Supported metrics for `component_name`
```xtable
| Field{30%} | Description{60%}|
|---|---|
| Instant experience metrics |  |
#| `ix_page_duration_avg` | Instant experience average view time |
#| `ix_page_viewrate_avg` | Instant experience average view percentage |
#| `ix_video_views` | Instant experience video views |
#| `ix_video_views_p25` | Instant experience video views at 25% |
#| `ix_video_views_p50` | Instant experience video views at 50% |
#| `ix_video_views_p75` | Instant experience video views at 75% |
#| `ix_video_views_p100` | Instant experience video views at 100% |
#| `ix_average_video_play` | Average Instant experience video view time |
| Core metrics |  |
#| `spend` | Cost |
#| `cpc` | CPC (Destination) |
#| `cpm` | CPM |
#| `impressions` | Impressions |
#| `gross_impressions` | Gross impressions (Includes Invalid Impressions) |
#| `clicks` | Clicks (Destination) |
#| `ctr` | CTR (Destination) |
#| `conversion` | Conversions |
#| `cost_per_conversion` | Cost per conversion |
#| `conversion_rate` | Conversion rate (CVR, clicks) |
#| `conversion_rate_v2` | Conversion rate (CVR) |
#| `real_time_conversion` | Real-time conversions |
#| `real_time_cost_per_conversion` | Real-time cost per conversion |
#| `real_time_conversion_rate` | Real-time conversion rate (CVR, clicks) |
#| `real_time_conversion_rate_v2` | Real-time conversion rate (CVR) |
```

## Supported metrics for `room_id`
```xtable
| Field{40%} | Description{60%}|
|---|---|
| Core metrics |  |
#| `spend` | Cost |
#| `cpc` | CPC (Destination) |
#| `cpm` | CPM |
#| `impressions` | Impressions |
#| `clicks` | Clicks (Destination) |
#| `ctr` | CTR (Destination) |
#| `conversion` | Conversions |
#| `cost_per_conversion` | Cost per conversion |
#| `conversion_rate` | Conversion rate (CVR, clicks) |
#| `conversion_rate_v2` | Conversion rate (CVR) |
| TikTok metrics ||
#| Add to wishlist ||
##| `onsite_add_to_wishlist` | Adds to wishlist (TikTok) |
##| `cost_per_onsite_add_to_wishlist` | Cost per add to wishlist (TikTok) |
##| `onsite_add_to_wishlist_rate` | Unique add to wishlist rate (TikTok) |
##| `value_per_onsite_add_to_wishlist` | Value per add to wishlist (TikTok) |
##| `total_onsite_add_to_wishlist_value` | Add to wishlist value (TikTok) |
#| Product clicks ||
##| `ix_product_click_count` | Product clicks (TikTok) |
##| `cost_per_ix_product_click_count` | Cost per product clicks (TikTok) |
##| `ix_product_click_count_rate` | Product clicks rate (TikTok) (%) |
| Shop metrics ||
#| ROAS ||
##| `onsite_shopping_roas` | ROAS (Shop) |
#| Purchases ||
##| `onsite_shopping` | Purchases (Shop) |
##| `cost_per_onsite_shopping` | Cost per purchase (Shop) |
##| `onsite_shopping_rate` | Purchase rate (Shop) |
##| `value_per_onsite_shopping` | Average order value (Shop) |
##| `total_onsite_shopping_value` | Gross revenue (Shop) |
#| Checkouts initiated ||
##| `onsite_initiate_checkout_count` | Checkouts initiated (Shop) |
##| `cost_per_onsite_initiate_checkout_count` | Cost per checkout initiated (Shop) |
##| `onsite_initiate_checkout_count_rate` | Checkout initiation rate (Shop) (%) |
##| `value_per_onsite_initiate_checkout_count` | Value per checkout initiated (Shop) |
##| `total_onsite_initiate_checkout_count_value` | Checkout initiation value (Shop) |
#| Product page views ||
##| `onsite_on_web_detail` | Product page views (Shop) |
##| `cost_per_onsite_on_web_detail` | Cost per product page view (Shop) |
##| `onsite_on_web_detail_rate` | Product page view rate (Shop) |
##| `value_per_onsite_on_web_detail` | Value per product page view (Shop) |
##| `total_onsite_on_web_detail_value` | Product page view value (Shop) |
#| Add to cart ||
##| `onsite_on_web_cart` | Add to cart (Shop) |
##| `cost_per_onsite_on_web_cart` | Cost per add to cart (Shop) |
##| `onsite_on_web_cart_rate` | Add to cart rate (Shop) |
##| `value_per_onsite_on_web_cart` | Value per add to cart (Shop) |
##| `total_onsite_on_web_cart_value` | Add to cart value (Shop) |
```

## Supported metrics for `post_id`
``` xtable
| Field{40%} | Description{60%}|
|---|---|
| Core metrics ||
#| `spend` | Cost |
#| `cpc` | CPC (Destination) |
#| `cpm` | CPM |
#| `impressions` | Impressions |
#| `clicks` | Clicks (Destination) |
#| `ctr` | CTR (Destination) |
#| `conversion` | Conversions |
#| `cost_per_conversion` | Cost per conversion |
#| `conversion_rate` | Conversion rate (CVR, clicks) |
#| `conversion_rate_v2` | Conversion rate (CVR) |
| Videos metrics ||
#| `video_play_actions` | Video views |
#| `video_watched_2s` | 2-second video views |
#| `video_watched_6s` | 6-second video views |
#| `engaged_view` | 6-second focused views |
#| `video_views_p25` | Video views at 25% |
#| `video_views_p50` | Video views at 50% |
#| `video_views_p75` | Video views at 75% |
#| `video_views_p100` | Video views at 100% |
#| `average_video_play` | Average play time per video view |
| TikTok metrics ||
#| Add to wishlist ||
##| `onsite_add_to_wishlist` | Adds to wishlist (TikTok) |
##| `cost_per_onsite_add_to_wishlist` | Cost per add to wishlist (TikTok) |
##| `onsite_add_to_wishlist_rate` | Unique add to wishlist rate (TikTok) |
##| `value_per_onsite_add_to_wishlist` | Value per add to wishlist (TikTok) |
##| `total_onsite_add_to_wishlist_value` | Add to wishlist value (TikTok) |
#| Product clicks ||
##| `ix_product_click_count` | Product clicks (TikTok) |
##| `cost_per_ix_product_click_count` | Cost per product clicks (TikTok) |
##| `ix_product_click_count_rate` | Product clicks rate (TikTok) (%) |
| Shop metrics ||
#| ROAS ||
##| `onsite_shopping_roas` | ROAS (Shop) |
#| Purchases ||
##| `onsite_shopping` | Purchases (Shop) |
##| `cost_per_onsite_shopping` | Cost per purchase (Shop) |
##| `onsite_shopping_rate` | Purchase rate (Shop) |
##| `value_per_onsite_shopping` | Average order value (Shop) |
##| `total_onsite_shopping_value` | Gross revenue (Shop) |
#| Checkouts initiated ||
##| `onsite_initiate_checkout_count` | Checkouts initiated (Shop) |
##| `cost_per_onsite_initiate_checkout_count` | Cost per checkout initiated (Shop) |
##| `onsite_initiate_checkout_count_rate` | Checkout initiation rate (Shop) (%) |
##| `value_per_onsite_initiate_checkout_count` | Value per checkout initiated (Shop) |
##| `total_onsite_initiate_checkout_count_value` | Checkout initiation value (Shop) |
#| Product page views ||
##| `onsite_on_web_detail` | Product page views (Shop) |
##| `cost_per_onsite_on_web_detail` | Cost per product page view (Shop) |
##| `onsite_on_web_detail_rate` | Product page view rate (Shop) |
##| `value_per_onsite_on_web_detail` | Value per product page view (Shop) |
##| `total_onsite_on_web_detail_value` | Product page view value (Shop) |
#| Add to cart ||
##| `onsite_on_web_cart` | Add to cart (Shop) |
##| `cost_per_onsite_on_web_cart` | Cost per add to cart (Shop) |
##| `onsite_on_web_cart_rate` | Add to cart rate (Shop) |
##| `value_per_onsite_on_web_cart` | Value per add to cart (Shop) |
##| `total_onsite_on_web_cart_value` | Add to cart value (Shop) |
```
