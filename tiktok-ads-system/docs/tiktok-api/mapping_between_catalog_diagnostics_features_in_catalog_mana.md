# Mapping between Catalog Diagnostics features in Catalog Manager and API configurations

**Doc ID**: 1780803525320706
**Path**: Marketing API/Catalog Management/Guides/Troubleshoot catalogs with diagnostics/Mapping between Catalog Diagnostics features in Catalog Manager and API configurations

---

This article provides the mapping between Catalog Diagnostics features in Catalog Manager, a part of TikTok Ads Manager, and the corresponding API configurations. If you are a Catalog Manager user seeking to integrate with TikTok API for Business, we recommend that you read this article beforehand to gain a clear understanding of how Catalog Diagnostics features in Catalog Manager are supported in the TikTok API for Business.

## Diagnostics for catalog products
The following table lists the features for diagnosing catalog products in Catalog Manager and the corresponding API configurations.

  
| 
    Catalog Manager 
module | 
    Catalog Manager 
feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Diagnostics
 | 
    Issue type (filter) | 
     | 
    [/diagnostic/catalog/](https://business-api.tiktok.com/portal/docs?id=1771117232728066) | 
    Request parameter 
`issue_level` | 
   |
  
| 
    Diagnostics | 
    Issue category (filter) | 
     | 
    `/diagnostic/catalog/` | 
    Request parameter 
 `issue_category` | 
   |
  
| 
    Diagnostics | 
    Date | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter  
diagnostic_date` | 
   |
  
| 
    Diagnostics | 
    Issue type | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter  
issue_title` | 
   |
  
| 
    Diagnostics | 
    Issue level | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter  
issue_level` | 
   |
  
| 
    Diagnostics | 
    Reason and suggestion | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter 
reason_and_suggestion` | 
   |
  
| 
    Diagnostics | 
    Issue category | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter 
issue_category` | 
   |
  
| 
    Diagnostics | 
    Affected items | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter 
affected_product_count` | 
   |
  
| 
    Diagnostics | 
    % affected | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter  
affected_product_percentage` | 
   |
  
| 
    Diagnostics | 
    Affected items 
- View examples | 
     | 
    `/diagnostic/catalog/ | 
    Response parameter 
example_affected_products` | 
   |
  
| 
    Diagnostics | 
    Download | 
     | 
    [/diagnostic/catalog/product/task/create/](https://business-api.tiktok.com/portal/docs?id=1771117279175682)
[/diagnostic/catalog/product/task/get/](https://business-api.tiktok.com/portal/docs?id=1771117294731266) | 
     | 
   |

## Diagnostics for catalog event sources
The following table lists the features for diagnosing catalog event sources in Catalog Manager and the corresponding API configurations.
   	

  
| 
    Catalog Manager 
module | 
    Catalog Manager 
feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Event sources | 
    App ID or Pixel ID | 
    
 | 
    [/diagnostic/catalog/eventsource/issue/](https://business-api.tiktok.com/portal/docs?id=1780799405041665) | 
    The request parameters:`event_source_type`
- `app_id`
- `pixel_code` | 
   |
  
| 
    Event sources | 
    Issues and suggestions 
- View Content
- Add to Cart
- Complete Payment | 
     | 
    `/diagnostic/catalog/eventsource/issue/` | 
    Request parameter 
`event_type` | 
   |
  
| 
    Event sources | 
    Issues and suggestions 
- Issues | 
     | 
    `/diagnostic/catalog/eventsource/issue/` | 
    Response parameter 
`diagnostic_result` | 
   |
  
| 
    Event sources | 
    Issues and suggestions 
- Issue level | 
     | 
    `/diagnostic/catalog/eventsource/issue/` | 
    Response parameter 
`level` | 
   |
  
| 
    Event sources | 
    Issues and suggestions
- Solutions | 
     | 
    `/diagnostic/catalog/eventsource/issue/` | 
    Response parameter 
`diagnostic_solution` | 
   |
  
| 
    Event sources | 
    App ID or Pixel ID | 
    
  | 
    [/diagnostic/catalog/eventsource/metric/](lhttps://business-api.tiktok.com/portal/docs?id=1780802101608450) | 
    The request parameters:
- `event_source_type`
- `app_id`
- `pixel_code` | 
   |
  
| 
    Event sources | 
    Events received from data sources 
- View Content
- Add to Cart
- Complete Payment | 
     | 
    `/diagnostic/catalog/eventsource/metric/` | 
    Request parameter 
`event_type` | 
   |
  
| 
    Event sources | 
    Events received from data sources 
- Yesterday
- Last 7 days
- Last 30 days | 
     | 
    `/diagnostic/catalog/eventsource/metric/` | 
    Request parameter 
`time_range` | 
   |
  
| 
    Event sources | 
    Events received from data sources 
- All events
- Events with content IDs
- Events matching content IDs | 
     | 
    `/diagnostic/catalog/eventsource/metric/` | 
    Response parameter 
`available_type` | 
   |
  
| 
    Event sources | 
    Events received from data sources 
- Date | 
     | 
    `/diagnostic/catalog/eventsource/metric/` | 
    Response parameter 
`date` | 
   |
  
| 
    Event sources | 
    Events received from data sources 
- Number | 
     | 
    `/diagnostic/catalog/eventsource/metric/` | 
    Response parameter 
`count` | 
   |
  
| 
    Event sources | 
    Events received from data sources 
- Percentage | 
     | 
    `/diagnostic/catalog/eventsource/metric/` | 
    Response parameter 
`percentage` | 
   |
