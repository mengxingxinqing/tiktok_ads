# Automatic Enhancements

**Doc ID**: 1855450880142402
**Path**: Marketing API/Campaign Management/Guides/Ad/Automatic Enhancements

---

Automatic Enhancements is an advertising optimization product that provides creative optimization services. It utilizes TikTok's latest Symphony AIGC (AI-Generated Content) capabilities to automatically optimize videos and images that are uploaded when you create ad campaigns.

The following Automatic Enhancement options are available:

- **Translate and dub**: Connect with global audiences by delivering your ad in 50+ languages.
- **Music refresh**: Stay on-trend by swapping in music currently popular on TikTok.
- **Video quality**: Improve overall video quality with increased resolution and clarity.
- **Image quality**: Improve overall image quality with increased resolution and clarity.
- **Resize**: Resize your image to take advantage of full-screen capabilities.

## Availability
The availability of Automatic Enhancements, configured via the `creative_auto_enhancement_strategy_list` parameter, depends on the ad type (Upgraded Smart+ or Manual) and various campaign settings. The following tables detail the specific configurations that support this feature.

### For Upgraded Smart+ Ads
The following tables outline the scenarios where `creative_auto_enhancement_strategy_list` can be used to enable Automatic Enhancements via the [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522) endpoint.

> **Note**

> All Automatic Enhancement strategies are available for Upgraded Smart+ Ads where supported.

#### For App Promotion ads

    

        
            
| 
                **Campaign level** | 
                **Ad group level** | 
                **Ad level** | 
             |
            
| 
                **Advertising objective**
(`objective_type`) | 
                **App promotion type**
(`app_promotion_type`) | 
                **Use catalog**
(`catalog_enabled`) | 
                **Placement **
(`placement_type` and `placements`) | 
                **Are Automatic Enhancements 
(`creative_auto_enhancement_strategy_list`)  available?** | 
             |
            
| 
             |
        
        
            
| 
                App promotion
(`APP_PROMOTION`) | 
                App install
(`APP_INSTALL`) | 
                `false` | 
                Any of the following types:
- **Automatic Placement**To use Automatic Placement, do not specify `placement_type` and `placements`.
- **Select specific placements **with TikTok includedTo use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`. | 
                ✅ | 
             |
            
| 
                App retargeting
(`APP_RETARGETING`) | 
                `false` | 
                ❌ | 
             |
            
| 
                TikTok Minis
(`MINIS`) | 
                `true` | 
                **Select specific placements **with only TikTok placement included:
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL` and `placements` to `["PLACEMENT_TIKTOK"]`. | 
                ❌ | 
             |
            
| 
                `false` | 
                ❌ | 
             |
        
    

#### For Lead Generation ads

    

        
            
| 
                **Campaign level** | 
                **Ad group level** | 
                **Ad level** | 
             |
            
| 
                **Advertising objective**
(`objective_type`) | 
                **Use catalog**
(`catalog_enabled`) | 
                **Optimization Location**
(`promotion_type` and `promotion_target_type`) | 
                **Placement **
(`placement_type` and `placements`) | 
                **Are Automatic Enhancements (`creative_auto_enhancement_strategy_list`) available?** | 
             |
        
        
            
| 
                Lead generation
(`LEAD_GENERATION`) | 
                `false` | 
                Instant Form
(`promotion_type` as `LEAD_GENERATION`
and `promotion_target_type` as `INSTANT_PAGE`) | 
                Any of the following types:
- **Automatic Placement**To use Automatic Placement, do not specify `placement_type` and `placements`.
- **Select specific placements **with TikTok includedTo use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`. | 
                ✅ | 
             |
            
| 
                `false` | 
                Website
(`promotion_type` as `LEAD_GENERATION`
and `promotion_target_type` as `EXTERNAL_WEBSITE`) | 
                ✅ | 
             |
            
| 
                `true` | 
                **Select specific placements **with only TikTok placement included:
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL` and `placements` to `["PLACEMENT_TIKTOK"]`. | 
                ❌ | 
             |
            
| 
                `false` | 
                TikTok direct messages
(`promotion_type` as `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
and `promotion_target_type` not specified) | 
                ❌ | 
             |
            
| 
                `true` | 
                ❌ | 
             |
            
| 
                `false` | 
                Instant messaging apps
(`promotion_type` as `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
and `promotion_target_type` not specified) | 
                ✅ | 
             |
            
| 
                `false` | 
                Phone call
(`promotion_type` as `LEAD_GEN_CLICK_TO_CALL`
and `promotion_target_type` not specified) | 
                ❌ | 
             |
        
    

#### For Sales ads

    

        
            
| 
                **Campaign level** | 
                **Ad group level** | 
                **Ad level** | 
             |
            
| 
                **Advertising objective**
(`objective_type`) | 
                **Sales destination**
(`sales_destination`) | 
                **Use catalog**
(`catalog_enabled`) | 
                **Catalog type**
(`catalog_type`) | 
                **Placement **
(`placement_type` and `placements`) | 
                **Are Automatic Enhancements (`creative_auto_enhancement_strategy_list`) available?** | 
             |
        
        
            
| 
                Sales
(`WEB_CONVERSIONS`) | 
                Website
(`WEBSITE`) | 
                `false` | 
                Not specified | 
                Any of the following types:
- **Automatic Placement**To use Automatic Placement, do not specify `placement_type` and `placements`.
- **Select specific placements **with TikTok includedTo use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`. | 
                ✅ | 
             |
            
| 
                `true` | 
                E-commerce
(`ECOMMERCE`) | 
                ✅ | 
             |
            
| 
                `true` | 
                Travel and entertainment
(`TRAVEL_ENTERTAINTAINMENT`) | 
                ❌ | 
             |
            
| 
                `true` | 
                Mini series
(`MINI_SERIES`) | 
                ✅ | 
             |
            
| 
                App
(`APP`) | 
                `true` | 
                E-commerce
(`ECOMMERCE`) | 
                ✅ | 
             |
            
| 
                Website and app
(`WEB_AND_APP`) | 
                `false` | 
                Not specified | 
                ✅ | 
             |
            
| 
                `true` | 
                E-commerce
(`ECOMMERCE`) | 
                ✅ | 
             |
            
| 
                `true` | 
                Travel and entertainment
(`TRAVEL_ENTERTAINTAINMENT`) | 
                ❌ | 
             |
        
    

### For Manual Ads
The following tables detail the scenarios where `creative_auto_enhancement_strategy_list` can be used to enable Automatic Enhancements via the [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354) endpoint.

> **Note**

> For Manual Ads, only the following strategies are configurable via `creative_auto_enhancement_strategy_list`:
> *   Video quality (`VIDEO_QUALITY`)
> *   Music refresh (`MUSIC_REFRESH`)
> *   Image quality (`IMAGE_QUALITY`)
> *   Resize (`IMAGE_RESIZE`)

#### For App Promotion ads

  

    
        
| 
            **Campaign level** | 
            **Ad group level** | 
            **Ad level** | 
         |
        
| 
            **Advertising objective**
(`objective_type`) | 
            **App promotion type**
(`app_promotion_type`) | 
            **Placement **
(`placement_type` and `placements`) | 
            **Are Automatic Enhancements (`creative_auto_enhancement_strategy_list`)  available?** | 
         |
        
| 
         |
    
    
        
| 
            App promotion
(`APP_PROMOTION`) | 
            App install
(`APP_INSTALL`) | 
            Any of the following types:  
- **Automatic Placement**  To use Automatic Placement, do not specify `placement_type` and `placements`.   
- **Select specific placements **with TikTok included  To use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`.    | 
            ✅ | 
         |
        
| 
            App retargeting
(`APP_RETARGETING`) | 
            ✅ | 
         |
        
| 
            App pre-registration
(`APP_PREREGISTRATION`) | 
            ✅ | 
         |
    

  
#### For Lead Generation ads

    

        
            
| 
                **Campaign level** | 
                **Ad group level** | 
                **Ad level** | 
             |
            
| 
                **Advertising objective**
(`objective_type`) | 
                **Use catalog**
(`catalog_enabled`) | 
                **Optimization Location**
(`promotion_type` and `promotion_target_type`) | 
                **Placement **
(`placement_type` and `placements`) | 
                **Are Automatic Enhancements (`creative_auto_enhancement_strategy_list`) available?** | 
             |
        
    
        
| 
            Lead generation
(`LEAD_GENERATION`) | 
            `false` | 
            Instant Form
(`promotion_type` as `LEAD_GENERATION`
and `promotion_target_type` as `INSTANT_PAGE`) | 
            Any of the following types:  
- **Automatic Placement**  To use Automatic Placement, do not specify `placement_type` and `placements`.   
- **Select specific placements **with TikTok included  To use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`.    | 
            ✅ | 
         |
        
| 
            `false` | 
            Website
(`promotion_type` as `LEAD_GENERATION`
and `promotion_target_type` as `EXTERNAL_WEBSITE`) | 
            ✅ | 
         |
        
| 
            `true` | 
            **Select specific placements **with only TikTok placement included:  
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL` and `placements` to `["PLACEMENT_TIKTOK"]`.  | 
            ❌ | 
         |
        
| 
            `false` | 
            TikTok direct messages
(`promotion_type` as `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
and `promotion_target_type` not specified) | 
            ✅ | 
         |
        
| 
            `false` | 
            Instant messaging apps
(`promotion_type` as `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
and `promotion_target_type` not specified) | 
            ✅ | 
         |
        
| 
            `false` | 
            Phone call
(`promotion_type` as `LEAD_GEN_CLICK_TO_CALL`
and `promotion_target_type` not specified) | 
            ✅ | 
         |
    

#### For Sales ads

    

    
        
| 
            **Campaign level** | 
            **Ad group level** | 
            **Ad level** | 
         |
        
| 
            **Advertising objective**
(`virtual_objective_type` 
and `objective_type`) | 
            **Sales destination**
(`sales_destination`) | 
            **Use catalog**
(`catalog_enabled` 
and `campaign_product_source`) | 
            **Placement**
(`placement_type` and `placements`) | 
            **Are Automatic Enhancements (`creative_auto_enhancement_strategy_list`)  available?** | 
         |
    
    
        
| 
            Sales
(`virtual_objective_type` as `SALES` and `objective_type` as `WEB_CONVERSIONS`) | 
            Website
(`WEBSITE`) | 
            Not specified | 
            Any of the following types:
- **Automatic Placement**To use Automatic Placement, do not specify `placement_type` and `placements`.
- **Select specific placements **with TikTok includedTo use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`. | 
            ✅ | 
         |
        
| 
            Any of the following configurations:
- `catalog_enabled` is set to `true`
- `campaign_product_source` is set to `CATALOG` | 
            ❌ | 
         |
        
| 
            Sales
(`virtual_objective_type` as `SALES` and `objective_type` as  `PRODUCT_SALES`) | 
            App
(`APP`) | 
            `campaign_product_source` as `CATALOG` | 
            ❌ | 
         |
        
| 
            Sales
(`virtual_objective_type` as `SALES` and `objective_type` as  `PRODUCT_SALES`) | 
            Website and app
(`WEB_AND_APP`) | 
            `campaign_product_source` as `false` | 
            ✅ | 
         |
        
| 
            `campaign_product_source` as `true` | 
            ❌ | 
         |
    

#### For other ads

    
        
| 
            **Campaign level** | 
            **Ad group level** | 
            **Ad level** | 
         |
        
| 
            **Advertising objective**
(`objective_type`) | 
            **Campaign type**
(`rf_campaign_type`) | 
            **Placement **
(`placement_type` and `placements`) | 
            **Are Automatic Enhancements (`creative_auto_enhancement_strategy_list`)  available?** | 
         |
    
    
        
| 
            Traffic
(`TRAFFIC`) | 
            N/A | 
            Any of the following types:
- **Automatic Placement**To use Automatic Placement, do not specify `placement_type` and `placements`.
- **Select specific placements **with TikTok includedTo use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include `PLACEMENT_TIKTOK` in the value for `placements`. | 
            ✅ | 
         |
        
| 
            Auction Reach
(`REACH`) | 
            N/A | 
            ✅ | 
         |
        
| 
            Reach & Frequency
(`RF_REACH`) | 
            Reach & Frequency
(`STANDARD`) | 
            ❌ | 
         |
        
| 
            Reach & Frequency
(`RF_REACH`) | 
            TikTok Pulse
(`PULSE`) | 
            ❌ | 
         |
        
| 
            Video views
(`VIDEO_VIEWS`) | 
            N/A | 
            ✅ | 
         |
        
| 
            Community interaction
(`ENGAGEMENT`) | 
            N/A | 
            ✅ | 
         |
