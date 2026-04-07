# Migrate to GMV Max Campaigns

**Doc ID**: 1837161048383489
**Path**: Use Cases/Campaign creation/Create Shopping Ads/Migrate to GMV Max Campaigns

---

**If you are creating TikTok Shop Ads, read this document to find out the changes and actions you should take.**

## Background
Starting Q3, 2025, [GMV Max](https://business-api.tiktok.com/portal/docs?id=1822009058467842) will be the default and only supported campaign type for TikTok Shop Ads. If you create ads using the Product Sales objective and TikTok Shop as your sales destination, you will no longer be able to use the API to create, edit, or duplicate LIVE Shopping Ads, Product Shopping Ads, or Video Shopping Ads. Learn more [about GMV Max migration for TikTok Shop Ads](https://ads.tiktok.com/help/article/gmv-max-migration-tiktok-shop-ads).

## What's changing

### Impact by TikTok Shop Ads types
The following table outlines the impact by TikTok Shop Ads types and their corresponding configurations.

  
  
| 
    Type of TikTok Shop Ad
 | 
    Impacted? | 
    Configuration | 
   |
  
| 
    Campaign level | 
    Ad group level | 
   |

  
| 
    [Video Shopping Ads (with TikTok Shop as product source)](https://business-api.tiktok.com/portal/docs?id=1750361719059457) | 
    ✅ | 
    `objective_type` is `PRODUCT_SALES`
`campaign_product_source` is `STORE` | 
    `product_source` is `STORE` 
`shopping_ads_type` is `VIDEO`
`promotion_type` is `VIDEO_SHOPPING` | 
   |
  
| 
    [Product Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1785886237030401) | 
    ✅ | 
    `objective_type` is `PRODUCT_SALES`
`campaign_product_source` is `STORE` | 
    `product_source` is `STORE`
`shopping_ads_type` is `RODUCT_SHOPPING_ADS`
`promotion_type` is `PSA_PRODUCT` | 
   |
  
| 
    [Live Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1754162402455554) (with TikTok Shop specified) | 
    ✅ | 
    `objective_type` is `PRODUCT_SALES`
`campaign_product_source` is `STORE` | 
    `product_source` is `STORE`
`shopping_ads_type` is `LIVE`
`promotion_type` is `LIVE_SHOPPING`
`store_id` is specified | 
   |
  
| 
    [Video Shopping Ads (with Showcase as product source)](https://business-api.tiktok.com/portal/docs?id=1759232259360770)
 | 
    ❌ | 
    `objective_type` is `PRODUCT_SALES`
`campaign_product_source` is `STORE` | 
    `product_source` is `SHOWCASE`
`shopping_ads_type` is `VIDEO`
`promotion_type` is `VIDEO_SHOPPING` | 
   |
  
| 
    [Live Shopping Ads](https://business-api.tiktok.com/portal/docs?id=1754162402455554) (with TikTok Shop not specified) | 
    ❌ | 
    `objective_type` is `PRODUCT_SALES`
`campaign_product_source` is `STORE` | 
    `product_source` is `STORE`
`shopping_ads_type` is `LIVE`
`promotion_type` is `LIVE_SHOPPING`
`store_id` is not specified | 
   |

### Impact by endpoint

  
| 
    Module | 
    Endpoints | 
    Details | 
    Error message | 
   |

  
| 
    Ad group | 
    [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114)
[/adgroup/update/](https://business-api.tiktok.com/portal/docs?id=1739586761631745) | 
    Starting Q3, 2025, you cannot use these endpoints to create or update any [impacted TikTok Shop Ads types](#item-link-Impact by TikTok Shop Ads types). | 
    `Custom shop ads are no longer available` | 
   |
  
| 
    [/adgroup/budget/update/](https://business-api.tiktok.com/portal/docs?id=1739591133130817) | 
    Starting Q3, 2025, you cannot use this endpoint to update the budgets of any impacted TikTok Shop Ads types. | 
    `This ad can't be turned on because custom shop ads are no longer available` | 
   |
  
| 
    [/adgroup/status/update/](https://business-api.tiktok.com/portal/docs?id=1739591716326402) | 
    Starting Q3, 2025, you cannot use this endpoint to change the statuses of any impacted TikTok Shop Ads types. | 
    `Custom shop ads are no longer available` | 
   |
  
| 
    Ad 
 | 
    [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354)
[/ad/update/](https://business-api.tiktok.com/portal/docs?id=1739953405142018) | 
    Starting Q3, 2025, you cannot use these endpoints to create or update any impacted TikTok Shop Ads types. | 
    `This ad can't be edited because custom shop ads are no longer available` | 
   |
  
| 
    [/ad/status/update/](https://business-api.tiktok.com/portal/docs?id=1739953422970882)
 | 
    Starting Q3, 2025, you cannot use this endpoint to change the statuses of any impacted TikTok Shop Ads types. | 
    `Custom shop ads are no longer available` | 
   |

## What actions you should take
- Migrate to [GMV Max API](https://business-api.tiktok.com/portal/docs?id=1822000911166465) and start creating new GMV Max Campaigns. To find out the detailed steps for creating such campaigns via API, see [Create GMV Max Campaigns](https://business-api.tiktok.com/portal/docs?id=1822009058467842).

## Why GMV Max API?
- **Automation at scale**: Increase the effectiveness of your Shop Ads Campaigns at scale. The GMV Max API allows you to increase **operational efficiency** and reduce manual workload.
- **Deep customization**: Build tailored advertising solutions that fit your unique advertising needs. With flexible API endpoints, you can **customize your campaign settings** based on your specific needs. Adapt quickly to market changes and optimize for the best results, all through programmatic control.
- **Seamless API integration**: Connect directly to the TikTok Shop ecosystem with robust, developer-friendly APIs. **Manage your entire campaign lifecycle**—from creation and optimization to reporting—within your own systems and workflows. Enjoy real-time data access and streamlined campaign management, powered by API-driven efficiency.
