# Mapping between campaign features in TikTok Ads Manager and API configurations

**Doc ID**: 1740673047618561
**Path**: Marketing API/Campaign Management/Guides/Mapping between campaign features in TikTok Ads Manager and API configurations

---

This article provides the mapping between TikTok Ads Manager (TTAM) features at the campaign, ad group, and ad levels and the corresponding API configurations. If you are a TikTok Ads Manager user seeking to integrate with TikTok API for Business, we recommend that you read this article beforehand to gain a clear understanding of how campaign features in TikTok Ads Manager are supported in the TikTok API for Business.

Note that the mappings presented below may not cover all possible scenarios. For settings related to features not listed in this document, refer to [Campaign Management](https://business-api.tiktok.com/portal/docs?id=1735713781404673).

## Campaign level
To create a campaign, use [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602).

The table below lists the settings on TTAM at the campaign level and the corresponding API configurations.

  
| 
    TTAM Module | 
    TTAM setting | 
    UI Reference | 
    API configuration | 
   |

  
| 
    Advertising objective
 | 
    Advertising objective | 
     | 
    ` objective_type` | 
   |
  
| 
    Advertising objective as Sales | 
    
 | 
    `virtual_objective_type`

Learn about how to [upgrade from Product Sales or Website Conversions to the Sales objective](https://business-api.tiktok.com/portal/docs?id=1834189985160193). | 
   |
  
| 
    Sales destination | 
    
 | 
    `sales_destination` | 
   |
  
| 
    Campaign type | 
    App promotion type
(when Advertising objective = App promotion) | 
    
 | 
    `app_promotion_type` | 
   |
    
| 
    Smart+ campaign | 
    
 | 
    Use [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) to create a Smart+ Campaign. | 
   |
  
| 
    iOS 14 dedicated campaign | 
    Use iOS 14 dedicated campaign | 
    
 | 
    `campaign_type` | 
   |
  
| 
    App | 
    
 | 
    `app_id` | 
   |
    
| 
    Use advanced dedicated campaign | 
     | 
    `is_advanced_dedicated_campaign` | 
   |
    
| 
    SKAN attribution | 
     | 
    `disable_skan_campaign` | 
   |
  
| 
    Use app profile page to optimize delivery | 
    
 | 
    `campaign_app_profile_page_state` | 
   |
  
| 
    Campaign type
(when Buying type = Reach & Frequency 
& Advertising objective = Reach) | 
    Campaign type | 
    
 | 
    `rf_campaign_type` | 
   |
  
| 
    Product source 
(when Buying type = Auction
 & Advertising objective = Product Sales) | 
    Product source | 
    
 | 
    `campaign_product_source` | 
   |
  
| 
    Setting
 | 
    Campaign name | 
    
 | 
    `campaign_name` | 
   |
  
| 
    Special ad categories | 
     | 
    `special_industries` | 
   |
  
| 
    Campaign budget optimization | 
     | 
    `budget_optimize_on` | 
   |
  
| 
    Set campaign budget | 
     | 
    `budget_mode`
`budget` | 
   |
  
| 
    Realtime API (RTA) | 
     | 
    `rta_id` | 
   |
  
| 
    Use RTA to automatically select products | 
     | 
    `rta_product_selection_enabled` | 
   |
  
| 
    Campaign list | 
    Campaign - On/Off | 
     | 
    `operation_status` |   
   |

## Ad group level
To create an ad group, use [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114).

The table below lists the settings on TTAM at the ad group level and the corresponding API configurations.

  
| 
    TTAM Module | 
    TTAM setting | 
    UI Reference | 
    API configuration | 
   |

  
| 
    Settings | 
    Ad group name
 | 
     | 
    `adgroup_name` | 
   |
  
| 
    Shopping ads type
(when Buying type = Auction & Advertising objective = Product Sales) | 
    Shopping ads type
 | 
     | 
    `shopping_ads_type` | 
   |
  
| 
    Identity
(When Shopping ads type = Live Shopping Ads) | 
     | 
    `identity_id`
`identity_type`
`identity_authorized_bc_id` | 
   |
  
| 
    Product source details
(when Buying type = Auction 
& Advertising objective = Product Sales 
& Shopping ads type = Video Shopping Ads) | 
    Catalog | 
     | 
    `product_source`
`catalog_id`
`catalog_authorized_bc_id` | 
   |
  
| 
    TikTok Shop | 
     | 
    `product_source`
`store_id`
`store_authorized_bc_id` | 
   |
  
| 
    Showcase | 
     | 
    `product_source`
`identity_id`
`identity_type`
`identity_authorized_bc_id` | 
   |
  
| 
    Optimization location | 
    Optimization location
 | 
     | 
    `promotion_type` | 
   |
  
| 
    Optimization location
 (when Advertising objective = lead generation)
 | 
     | 
    `promotion_target_type` | 
   |
  
| 
    Optimization location
 (when App promotion type = pre-registration)
 | 
     | 
    `promotion_website_type` | 
   |
  
| 
    App 
(when Advertising objective = App promotion) | 
     | 
    `app_id` | 
   |
  
| 
    TikTok Pixel | 
     | 
    `pixel_id` | 
   |
  
| 
    Optimization event | 
     | 
    `optimization_event` | 
   |
 
| 
    Select your Instant messaging app or use a customized URL
(when Optimization location is Instant messaging apps) 
- Messenger
- WhatsApp
- Instant Messaging URL | 
     | 
    `messaging_app_type`
`messaging_app_account_id`
`phone_region_code`
`phone_region_calling_code`
`phone_number` | 
   |
  
| 
    Deep funnel optimization
- Data connection
- Optimization event | 
     | 
    `deep_funnel_optimization_status`
`deep_funnel_event_source`
`deep_funnel_event_source_id`
`deep_funnel_optimization_event` | 
   |
  
| 
    Placements | 
    Automatic placement
Select placement | 
    Select placement" style="color:#808080" > | 
    `placement_type`
`placements` | 
   |
  
| 
    Include search results | 
     | 
    `search_result_enabled` | 
   |
  
| 
    
- In-feed
- Search feed
- TikTok Lite (Japan & Korea) | 
     | 
    `tiktok_subplacements` | 
   |
  
| 
    User comment | 
     | 
    `comment_disabled` | 
   |
  
| 
    Video download | 
     | 
    `video_download_disabled` | 
   |
  
| 
    Video sharing | 
     | 
    `share_disabled` | 
   |
  
| 
    Pangle block list | 
     | 
    `blocked_pangle_app_ids` | 
   |
  
| 
    Audience targeting | 
    Saved audience | 
     | 
    `saved_audience_id` | 
   |
  
| 
    Select targeting mode
- Custom targeting
- Automatic targeting | 
     | 
    `auto_targeting_enabled` | 
   |
  
| 
    Find prospective customers 
/Retarget audience
(when Shopping ads type = Video Shopping Ads & Product source = Catalog) | 
    
 | 
    `shopping_ads_retargeting_type`
`shopping_ads_retargeting_actions_days`
`included_custom_actions`
`excluded_custom_actions` | 
   |
   
| 
    Expand / Narrow 
(when Shopping ads type = Video Shopping Ads & Product source = Catalog & Retarget audience is selected) | 
     | 
    `shopping_ads_retargeting_custom_audience_relation` | 
   |
  
| 
    Demographics - Location | 
     | 
    `location_ids`
`zipcode_ids` | 
   |
  
| 
    Demographics - Languages | 
     | 
    `languages` | 
   |
  
| 
    Demographics - Gender | 
     | 
    `gender` | 
   |
  
| 
    Demographics - Age | 
     | 
    `age_groups` | 
   |
  
| 
    Demographics - Spending power | 
     | 
    `spending_power` | 
   |
  
| 
    Demographics - Household income | 
     | 
    `household_income` | 
   |
  
| 
    Audience
- Include
- Exclude | 
     | 
    `audience_ids`
`excluded_audience_ids` | 
   |
    
| 
    Smart audience | 
     | 
    `smart_audience_enabled` | 
   |
  
| 
    Interests & Behaviors - Interests | 
     | 
    `interest_category_ids`
`interest_keyword_ids` | 
   |
  
| 
    Interests & Behaviors - Purchase intention | 
     | 
    `purchase_intention_keyword_ids` | 
   |
  
| 
    Interests & Behaviors - Video interactions 
& Creator interactions 
& Hashtag interactions | 
     | 
    `actions` | 
   |
    
| 
    Smart interests & behaviors | 
     | 
    `smart_interest_behavior_enabled` | 
   |
  
| 
    Pangle audience packages | 
     | 
    `included_pangle_audience_package_ids`
`excluded_pangle_audience_package_ids` | 
   |
  
| 
    Device - OS versions | 
     | 
    `operating_systems`
`min_android_version`
`min_ios_version`
`ios14_targeting` | 
   |
  
| 
    Device - Device model | 
     | 
    `device_model_ids` | 
   |
  
| 
    Device - Connection type | 
     | 
    `network_types` | 
   |
  
| 
    Device - Carriers | 
     | 
    `carrier_ids` | 
   |
  
| 
    Device - Internet service provider | 
     | 
    `isp_ids` | 
   |
  
| 
    Device - Device price | 
     | 
    `device_price_ranges` | 
   |
  
| 
    Targeting expansion

 | 
     | 
    `targeting_expansion` | 
   |
  
| 
    Contextual Targeting | 
    Content Topics
 | 
     | 
    `contextual_tag_ids` | 
   |
  
| 
    Content exclusions | 
    Inventory filter | 
     | 
    `brand_safety_type`
`brand_safety_partner` | 
   |
  
| 
    Category exclusions | 
     | 
    `category_exclusion_ids` | 
   |
  
| 
    Vertical sensitivity control | 
     | 
    `vertical_sensitivity_id` | 
   |
  
| 
    Budget & Schedule | 
    Budget | 
     | 
    `budget_mode`
`budget` | 
   |
  
| 
    Schedule | 
     | 
    `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
   |
  
| 
    Dayparting | 
     | 
    `dayparting` | 
   |
  
| 
    Bidding & Optimization | 
    Optimization goal | 
     | 
    `optimization_goal` | 
   |
  
| 
    Message event set (when Optimization location is Instant messaging apps & Optimization goal is Conversations) | 
     | 
    `message_event_set_id` | 
   |
  
| 
    Frequency cap | 
     | 
    `frequency`
`frequency_schedule` | 
   |
  
| 
    Select an in-app event to optimize for
(when Optimization goal = Install with in-app event) | 
     | 
    `secondary_optimization_event` | 
   |
  
| 
    Bid strategy | 
     | 
    `bid_type`
`bid_price` | 
   |
  
| 
    USD/Conversion | 
     | 
    `conversion_bid_price` | 
   |
  
| 
    Bid strategy | 
     | 
    `deep_bid_type`
`roas_bid` | 
   |
  
| 
    Day 7 ROAS / Day 0 ROAS | 
     | 
    `vbo_window` | 
   |
  
| 
    USD/View | 
     | 
    `bid_display_mode` | 
   |
  
| 
    Retention goal | 
     | 
    `next_day_retention` | 
   |
  
| 
    Attribution settings
- Attribution window
- Event count |  
     | 
    `click_attribution_window`
`view_attribution_window`
`attribution_event_count` | 
   |
  
| 
    Billing event | 
     | 
    `billing_event` | 
   |
  
| 
    Delivery type | 
     | 
    `pacing` | 
   |
  
| 
    Campaign list | 
    Ad group - On/Off | 
     | 
    `operation_status` |   
   |

## Ad level
To create an ad, use [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354).

The table below lists the settings on TTAM at the ad level and the corresponding API configurations.

  
| 
    TTAM Module | 
    TTAM setting | 
    UI Reference | 
    API configuration | 
   |

  
| 
    Smart Creative ads | 
    Smart Creative ads | 
     | 
    To learn about how to create Smart Creative ads, refer to [Smart Creative](https://business-api.tiktok.com/portal/docs?id=1767322784934914). | 
   |
  
| 
    Ad name | 
    Ad name | 
     | 
    `ad_name` | 
   |
  
| 
    Identity | 
    Identity | 
     | 
    `identity_type`
`identity_id`
`identity_authorized_bc_id` | 
   |
  
| 
    Product details | 
    Products | 
     | 
    `catalog_id`
`product_specific_type`
`item_group_ids`
`product_set_id`
`sku_ids` | 
   |
  
| 
     | 
    `showcase_products` | 
   |
  
| 
    Ad details | 
    Ad format | 
     | 
    `ad_format` | 
   |
  
| 
    Ad format | 
     | 
    `vertical_video_strategy` | 
   |
  
| 
    Ad setup - Dynamic format | 
     | 
    `dynamic_format` | 
   |
  
| 
    Ad creative - Video | 
     | 
    `video_id` | 
   |
  
| 
    Ad creative - Image | 
    

 | 
    `image_ids` | 
   |
  
| 
    Ad creative - Music | 
     | 
    `music_id` | 
   |
  
| 
    Ad creative - Post
 | 
     | 
    `tiktok_item_id` | 
   |
  
| 
    Ad creative - Post - Music sharing | 
     | 
    `promotional_music_disabled` | 
   |
  
| 
    Ad creative - Post - Stitch and Duet | 
     | 
    `item_duet_status`
`item_stitch_status` | 
   |
  
| 
    Ad creative - Video - Only show as ad | 
     | 
    `dark_post_status` | 
   |
  
| 
    Ad creative - Catalog video | 
     | 
    `shopping_ads_video_package_id` | 
   |
  
| 
    Ad creative - Text | 
     | 
    `ad_text` | 
   |
  
| 
    Ad creative - Call to action | 
     | 
    `call_to_action`
`call_to_action_id` | 
   |
  
| 
    Interactive add-ons | 
     | 
    `card_id` | 
   |
  
| 
    Destination | 
    URL | 
     | 
    `landing_page_url` | 
   |
  
| 
    Custom Page | 
     | 
    `page_id` | 
   |
  
| 
    Add specific custom product page as destination | 
     | 
    `cpp_url` | 
   |
  
| 
    TikTok page type
 | 
     | 
    `tiktok_page_category` | 
   |
  
| 
    Phone number | 
     | 
    `phone_region_code`
`phone_region_calling_code`
`phone_number` | 
   |
  
| 
    Direct users to deeplink first 
& Deferred deeplink | 
    
 | 
    `deeplink`
`deeplink_type` | 
   |
  
| 
    Deferred deeplink 
(for Shopping Ads) | 
     | 
    `shopping_ads_deeplink_type` | 
   |
  
| 
    Website type
(for Shopping Ads) | 
     | 
    `shopping_ads_fallback_type` | 
   |
  
| 
    Fallback type | 
     | 
    `fallback_type` | 
   |
  
| 
    Dynamic destination | 
     | 
    `dynamic_destination` | 
   |
  
| 
    Build URL parameters | 
     | 
    `utm_params` | 
   |
  
| 
    Instant Product Page | 
     | 
    `instant_product_page_used` | 
   |
  
| 
    Welcome message | 
     | 
    `auto_message_id` | 
   |
  
| 
    This ad contains AI-generated content | 
     | 
    `aigc_disclosure_type` | 
   |
  
| 
    Disclaimer | 
    Disclaimer | 
     | 
    `disclaimer_type`
`disclaimer_text`
`disclaimer_clickable_texts` | 
   |
  
| 
    Tracking | 
    TikTok events tracking - Website events | 
     | 
    `tracking_pixel_id` | 
   |
  
| 
    TikTok events tracking - App events | 
     | 
    `tracking_app_id` | 
   |
  
| 
    TikTok events tracking - Offline events | 
     | 
    `tracking_offline_event_set_ids` | 
   |
  
| 
    TikTok events tracking - Message event set | 
     | 
    `tracking_message_event_set_id` | 
   |
  
| 
    TikTok events tracking - Track viewability with third-party partner | 
     | 
    `viewability_postbid_partner`
`viewability_vast_url` | 
   |
  
| 
    TikTok events tracking - Measure brand safety with third-party partner | 
     | 
    `brand_safety_postbid_partner`
`brand_safety_vast_url` | 
   |
  
| 
    Third party tracking settings - Impression tracking URL | 
     | 
    `impression_tracking_url` | 
   |
  
| 
    Third party tracking settings - Click tracking URL | 
     | 
    `click_tracking_url` | 
   |
  
| 
    Playable | 
    Add playable asset | 
     | 
    `playable_url` | 
   |
  
| 
    Campaign list | 
    Ad - On/Off | 
     | 
    `operation_status` |   
   |
