# Mapping between Catalog Management features in Catalog Manager and API configurations

**Doc ID**: 1782141580104705
**Path**: Marketing API/Catalog Management/Guides/Mapping between Catalog Management features in Catalog Manager and API configurations

---

This article provides the mapping between Catalog Management features in Catalog Manager, a part of TikTok Ads Manager, and the corresponding API configurations. If you are a Catalog Manager user seeking to integrate with TikTok API for Business, we recommend that you read this article beforehand to gain a clear understanding of how Catalog Management features in Catalog Manager are supported in the TikTok API for Business.

## Catalogs
The following table lists the features for creating and managing catalogs in Catalog Manager and the corresponding API configurations.

  
| 
    Catalog Manager module | 
    Catalog Manager feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Product Catalog page | 
    Create catalog 
- Catalog Name | 
    
 | 
    [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961)
 | 
    Request parameter
`name` | 
   |
  
| 
    Product Catalog page | 
    Create catalog
- Business Center account | 
     | 
    `/catalog/create/` | 
    Request parameter
`bc_id` | 
   |
  
| 
    Product Catalog page | 
    Create catalog
- Industry | 
     | 
    `/catalog/create/` | 
    Request parameter
`catalog_type` | 
   |
  
| 
    Product Catalog page | 
    Create catalog
- Default location | 
     | 
    `/catalog/create/` | 
    Request parameter
`region_code` | 
   |
  
| 
    Product Catalog page | 
    Create catalog
- Default Currency | 
     | 
    `/catalog/create/` | 
    Request parameter
`currency` | 
   |
  
| 
    Settings | 
    Catalog Name
- Update | 
     | 
    [/catalog/update/](https://business-api.tiktok.com/portal/docs?id=1740306544966657) | 
     | 
   |
  
| 
    Product Catalog page | 
    Catalog
- Delete | 
     | 
    [/catalog/delete/](https://business-api.tiktok.com/portal/docs?id=1740310064588801) | 
     | 
   |
  
| 
    Catalog List | 
    Catalog List | 
    
 | 
    [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) | 
     | 
   |
  
| 
    Product Catalog page | 
    Transfer catalog to Business Center account | 
    

 | 
    [/catalog/capitalize/](https://business-api.tiktok.com/portal/docs?id=1740490222539778) | 
     | 
   |

## Products
The following table lists the features for adding and managing products in Catalog Manager and the corresponding API configurations.

  
| 
    Catalog Manager module | 
    Catalog Manager feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Products
 | 
    Add products - Manually Add
- Main image | 
    
 | 
    [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) | 
    Request parameter
`image_url` | 
   |
  
| 
    Products
 | 
    Add products - Manually Add
- Video URL (Optional) | 
     | 
	`/catalog/product/upload/` | 
    Request parameter
`video_url` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Basic Info - Title | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`title` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Basic Info - SKU ID | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`sku_id` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Basic Info - Description | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`description` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Basic Info - Brand | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`brand` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Basic Info - Link | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`landing_page_url` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Basic Info - Condition | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`condition` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Sales Info - Availability | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`availability` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- Sales Info - Price | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`price` | 
   |

  
| 
    Products | 
    Add products - Manually Add
- App Links (Optional) -Android URL | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`android_url` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- App Links (Optional) - Android Package ID | 
     | 
   `/catalog/product/upload/` | 
    Request parameter
`android_package` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- App Links (Optional) - Android App Name | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`android_app_name` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- App Links (Optional) - iOS URL | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`ios_url` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- App Links (Optional) - iOS App Store ID | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`ios_app_store_id` | 
   |
  
| 
    Products | 
    Add products - Manually Add
- App Links (Optional) - iOS App Name | 
     | 
    `/catalog/product/upload/` | 
    Request parameter
`ios_app_name` | 
   |
  
| 
    Products | 
    Add products - Data Feed Schedule
- Data Feed Name Create New Product Source | 
    
 | 
    [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377) | 
    Request parameter
`feed_name` | 
   |
  
| 
    Products | 
    Add products - Data Feed Schedule 
- Data Feed URL | 
     | 
	`/catalog/feed/create/` | 
    Request parameter
`uri` | 
   |
  
| 
    Products | 
    Add products - Data Feed Schedule 
- Data Feed URL Login DetailsUsername | 
     | 
    `/catalog/feed/create/` | 
    Request parameter
`username` | 
   |
  
| 
    Products | 
    Add products - Data Feed Schedule
- Data Feed URL Login DetailsPassword | 
     | 
    `/catalog/feed/create/` | 
    Request parameter
`password` | 
   |
  
| 
    Products | 
    Add products - Data Feed Schedule

- Automatic Upload | 
     | 
    `/catalog/feed/create/` | 
    Request parameters
`interval_type`
`interval_count`
`timezone`
`day_of_month`
`hour`
`minute` | 
   |
  
| 
    Products | 
    Add products - Data Feed Schedule 
- Update Method | 
     | 
    `/catalog/feed/create/` | 
    Request parameter
`update_mode` | 
   |
  
| 
    Products
 | 
    Add products - Data Feed Schedule 
- Data Feed NameUpload to Existing Product Source | 
    
 | 
    [/catalog/feed/update/](https://business-api.tiktok.com/portal/docs?id=1740665197662210) | 
     | 
   |
  
| 
    Product Sources | 
    Product Source list | 
     | 
    [/catalog/feed/get/](https://business-api.tiktok.com/portal/docs?id=1740665183073281) | 
     | 
   |
  
| 
    Product Sources | 
    Product Source
- Delete | 
     | 
    [/catalog/feed/delete/](https://business-api.tiktok.com/portal/docs?id=1740665210863617) | 
     | 
   |
  
| 
    Product Sources | 
    Select a product source- Settings 

- ScheduleSet up a feed schedule | 
     | 
    [/catalog/feed/switch/](https://business-api.tiktok.com/portal/docs?id=1750349624999937) | 
     | 
   |
  
| 
    Products | 
    Add products - Upload File | 
    
 | 
    [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) | 
     | 
   |
  
| 
    Products | 
    Edit products | 
     | 
    [/catalog/product/update/](https://business-api.tiktok.com/portal/docs?id=1740562287852546) | 
     | 
   |
  
| 
    Products | 
    Delete products | 
     | 
    [/catalog/product/delete/](https://business-api.tiktok.com/portal/docs?id=1740562489236481) | 
     | 
   |
  
| 
    Products | 
    Product list | 
     | 
    [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) | 
     | 
   |
  
| 
    Product Sources | 
    Upload log | 
     | 
    [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889) | 
     | 
   |

## Product sets 
The following table lists the features for creating and managing product sets in Catalog Manager and the corresponding API configurations.

  
| 
    Catalog Manager module | 
    Catalog Manager feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Product Sets | 
    Create Product Set
- Use FiltersProduct set name | 
    
 | 
    [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257) | 
    Request parameter
`product_set_name` | 
   |
  
| 
    Product Sets | 
    Create Product Set
- Use FiltersFilter rules | 
     | 
    `/catalog/set/create/` | 
    Request parameter
`conditions` | 
   |
  
| 
    Product Sets | 
    Product set
- Edit | 
     | 
    [/catalog/set/update/](https://business-api.tiktok.com/portal/docs?id=1740572974725122) | 
     | 
   |
  
| 
    Product Sets | 
    Product set
- Delete | 
     | 
    [/catalog/set/delete/](https://business-api.tiktok.com/portal/docs?id=1740573143966722) | 
     | 
   |
  
| 
    Product Sets | 
    Product set list | 
     | 
    [/catalog/set/get/](https://business-api.tiktok.com/portal/docs?id=1740570556295169) | 
     | 
   |
  
  
| 
    Product Sets | 
    Product list for product sets | 
     | 
    [/catalog/set/product/get/](https://business-api.tiktok.com/portal/docs?id=1740571478441986) | 
     | 
   |

## Event Sources
The following table lists the features for managing event sources in Catalog Manager and the corresponding API configurations.

  
| 
    Catalog Manager module | 
    Catalog Manager feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Event Sources | 
    
- Connect App Event Sources
- Connect Pixel Event Sources | 
    

 | 
    [/catalog/eventsource/bind/](https://business-api.tiktok.com/portal/docs?id=1740492491200513) | 
     | 
   |
  
| 
    Event Sources | 
    
- Disconnect App Event Sources
- Disconnect Pixel Event Sources | 
     | 
    [/catalog/eventsource/unbind/](https://business-api.tiktok.com/portal/docs?id=1740492512449538)
 | 
     | 
   |
  
| 
    Event Sources | 
    Event source list | 
    
 | 
    [/catalog/eventsource_bind/get/](https://business-api.tiktok.com/portal/docs?id=1740492531343362) | 
     | 
   |

## Videos
The following table lists the features for uploading and managing video packages in Catalog Manager and the corresponding API configurations.

  
| 
    Catalog Manager module | 
    Catalog Manager feature | 
    UI Reference | 
    API endpoint | 
    API configurations | 
   |

  
| 
    Videos | 
    Custom templates & fonts
- My TemplatesUpload | 
     | 
    [/catalog/template/upload/](https://business-api.tiktok.com/portal/docs?id=1740665346584577) | 
     | 
   |
  
| 
    Videos | 
    Custom templates & fonts
- My TemplatesCreate | 
     | 
    [/catalog/video_package/create/](https://business-api.tiktok.com/portal/docs?id=1740665273039873) | 
     | 
   |
  
| 
    Videos | 
    Videos
- NameEdit | 
     | 
    [/catalog/video_package/update/](https://business-api.tiktok.com/portal/docs?id=1740665303669761) | 
     | 
   |
  
| 
    Videos | 
    Videos
- ActionsDelete | 
     | 
    [/catalog/video_package/delete/](https://business-api.tiktok.com/portal/docs?id=1740665332455426)
 | 
     | 
   |
  
| 
    Videos | 
    Videos
- ActionsView | 
     | 
    [/catalog/template_preview/create/](https://business-api.tiktok.com/portal/docs?id=1740665368159233)
 | 
     | 
   |
  
| 
    Videos | 
    Videos 
- List | 
     | 
    [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073) | 
     | 
   |
