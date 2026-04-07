# Available product information settings in Upgraded Smart+ Campaigns

**Doc ID**: 1860735968798721
**Path**: Appendix/Available product information settings in Upgraded Smart+ Campaigns

---

The availability of the "product information" feature in Upgraded Smart+ Campaigns, configured via the `product_info` parameter, depends on various campaign settings.

The following tables outline the scenarios where `product_info` can be used to enable the "product information" feature via the [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522) or [/smart_plus/ad/update/](https://business-api.tiktok.com/portal/docs?id=1843317411665921) endpoint.

## For App Promotion ads

    
        
| 
            Campaign level | 
            Ad level | 
         |
        
| 
            Advertising objective
(`objective_type`) | 
            App promotion type
(`app_promotion_type`) | 
            Use catalog
(`catalog_enabled`) | 
            Is there any product information setting
(`product_info`) available? | 
            Specific product information settings
(parameters within `product_info`) available | 
         |
        
| 
            Add product information
· Selling points
(`selling_points`) | 
            Required setting for
`product_info_enabled` | 
         |
    
    
        
| 
            App promotion
(`APP_PROMOTION`) | 
            App install
(`APP_INSTALL`) | 
            `false` | 
            ✅ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            App retargeting
(`APP_RETARGETING`) | 
            `false` | 
            ✅ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            TikTok Minis
(`MINIS`) | 
            `false` | 
            ✅ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            `true` | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
    

## For Sales ads

 

    
        
| 
            Campaign level | 
            Ad level | 
         |
        
| 
            Advertising objective
(`objective_type`) | 
            Sales destination
(`sales_destination`) | 
            Use catalog
(`catalog_enabled`) | 
            Catalog type
(`catalog_type`) | 
            Is there any product information setting
(`product_info`) available? | 
            Specific product information settings
(parameters within `product_info`) available | 
         |
        
| 
            Add product information
· Product name
(`product_titles`) | 
            Add product information
· Product image
(`product_image_list`) | 
            Add product information
· Selling points
(`selling_points`) | 
            Automatic enhancements and display options
· Product card settings
  · Product information
(`catalog_tag_list`) | 
            Add promo code or offer
(`promo_info_list`) | 
            Required setting for
`product_info_enabled` | 
         |
    
    
        
| 
            Sales
(`WEB_CONVERSIONS`) | 
            Website
(`WEBSITE`) | 
            `false` | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            `true` | 
            E-commerce
(`ECOMMERCE`) | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            `true` | 
            Travel and entertainment
(`TRAVEL_ENTERTAINTAINMENT`) | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            `true` | 
            Mini series
(`MINI_SERIES`) | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            App
(`APP`) | 
            `true` | 
            E-commerce
(`ECOMMERCE`) | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            Website and app
(`WEB_AND_APP`) | 
            `false` | 
            Not specified | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            `true` | 
            E-commerce
(`ECOMMERCE`) | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            `true` | 
            Travel and entertainment
(`TRAVEL_ENTERTAINTAINMENT`) | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
    

The availability of the "product information" feature in Upgraded Smart+ Campaigns, configured via the `product_info` parameter, depends on various campaign settings.

The following tables outline the scenarios where `product_info` can be used to enable the "product information" feature via the [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522) or [/smart_plus/ad/update/](https://business-api.tiktok.com/portal/docs?id=1843317411665921) endpoint.

## For App Promotion ads

    
        
| 
            Campaign level | 
            Ad level | 
         |
        
| 
            Advertising objective
(`objective_type`) | 
            App promotion type
(`app_promotion_type`) | 
            Use catalog
(`catalog_enabled`) | 
            Is there any product information setting
(`product_info`) available? | 
            Specific product information settings
(parameters within `product_info`) available | 
         |
        
| 
            Add product information
· Selling points
(`selling_points`) | 
            Required setting for
`product_info_enabled` | 
         |
    
    
        
| 
            App promotion
(`APP_PROMOTION`) | 
            App install
(`APP_INSTALL`) | 
            `false` | 
            ✅ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            App retargeting
(`APP_RETARGETING`) | 
            `false` | 
            ✅ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            TikTok Minis
(`MINIS`) | 
            `false` | 
            ✅ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            `true` | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
    

## For Sales ads

 

    
        
| 
            Campaign level | 
            Ad level | 
         |
        
| 
            Advertising objective
(`objective_type`) | 
            Sales destination
(`sales_destination`) | 
            Use catalog
(`catalog_enabled`) | 
            Catalog type
(`catalog_type`) | 
            Is there any product information setting
(`product_info`) available? | 
            Specific product information settings
(parameters within `product_info`) available | 
         |
        
| 
            Add product information
· Product name
(`product_titles`) | 
            Add product information
· Product image
(`product_image_list`) | 
            Add product information
· Selling points
(`selling_points`) | 
            Automatic enhancements and display options
· Product card settings
  · Product information
(`catalog_tag_list`) | 
            Add promo code or offer
(`promo_info_list`) | 
            Required setting for
`product_info_enabled` | 
         |
    
    
        
| 
            Sales
(`WEB_CONVERSIONS`) | 
            Website
(`WEBSITE`) | 
            `false` | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ✅ | 
            `NON_CATALOG` | 
         |
        
| 
            `true` | 
            E-commerce
(`ECOMMERCE`) | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            `true` | 
            Travel and entertainment
(`TRAVEL_ENTERTAINTAINMENT`) | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            `true` | 
            Mini series
(`MINI_SERIES`) | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            App
(`APP`) | 
            `true` | 
            E-commerce
(`ECOMMERCE`) | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            Website and app
(`WEB_AND_APP`) | 
            `false` | 
            Not specified | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            `true` | 
            E-commerce
(`ECOMMERCE`) | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            `true` | 
            Travel and entertainment
(`TRAVEL_ENTERTAINTAINMENT`) | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
    

## For Lead Generation ads

    
        
| 
            Campaign level | 
            Ad group level | 
            Ad level | 
         |
        
| 
            Advertising objective
(`objective_type`) | 
            Use catalog
(`catalog_enabled`) | 
            Optimization Location
(`promotion_type` and `promotion_target_type`) | 
            Type of catalog
(`catalog_id`) | 
            Is there any product information setting
(`product_info`) available? | 
            Specific product information settings (parameters within `product_info`) available | 
         |
        
| 
            Add product information
· Product name
(`product_titles`) | 
            Add product information
· Product image
(`product_image_list`) | 
            Add product information
· Selling points
(`selling_points`) | 
            Video product information
(`catalog_tag_list`) | 
            Add promo code or offer
(`promo_info_list`) | 
            Required setting for
`product_info_enabled` | 
         |
    
    
        
| 
            Lead generation
(`LEAD_GENERATION`) | 
            `false` | 
            Instant Form
(`promotion_type` as `LEAD_GENERATION`
and `promotion_target_type` as `INSTANT_PAGE`) | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ❌ | 
            `NON_CATALOG` | 
         |
        
| 
            `false` | 
            Website
(`promotion_type` as `LEAD_GENERATION`
and `promotion_target_type` as `EXTERNAL_WEBSITE`) | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ❌ | 
            `NON_CATALOG` | 
         |
        
| 
            `true` | 
            Auto-Inventory | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            Auto-Model | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            `false` | 
            TikTok direct messages
(`promotion_type` as `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
and `promotion_target_type` not specified) | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ❌ | 
            `NON_CATALOG` | 
         |
        
| 
            `true` | 
            Auto-Inventory | 
            ✅ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ✅ | 
            ❌ | 
            `CATALOG` | 
         |
        
| 
            Auto-Model | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            ❌ | 
            Not specified | 
         |
        
| 
            `false` | 
            Instant messaging apps
(`promotion_type` as `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
and `promotion_target_type` not specified) | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ❌ | 
            `NON_CATALOG` | 
         |
        
| 
            `false` | 
            Phone call
(`promotion_type` as `LEAD_GEN_CLICK_TO_CALL`
and `promotion_target_type` not specified) | 
            Not specified | 
            ✅ | 
            ✅ | 
            ✅ | 
            ✅ | 
            ❌ | 
            ❌ | 
            `NON_CATALOG` | 
         |
