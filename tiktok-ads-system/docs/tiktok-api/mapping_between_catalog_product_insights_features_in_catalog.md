# Mapping between Catalog Product Insights features in Catalog Manager and API configurations

**Doc ID**: 1805642902406145
**Path**: Marketing API/Catalog Management/Guides/Obtain Catalog Product Insights/Mapping between Catalog Product Insights features in Catalog Manager and API configurations

---

This article provides the mapping between Catalog Product Insights features in Catalog Manager, a part of TikTok Ads Manager, and the corresponding API configurations. If you are a Catalog Manager user seeking to integrate with TikTok API for Business, we recommend that you read this article beforehand to gain a clear understanding of how Catalog Product Insights features in Catalog Manager are supported in the TikTok API for Business.

  
  
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
    Insights > Your trending products | 
    Category (filter) | 
     | 
    [/catalog/insight/product/get/](https://business-api.tiktok.com/portal/docs?id=1805640886872066) | 
    Request parameter
`category_ids` | 
   |
  
| 
    Insights > Your trending products | 
    Brand (filter) | 
     | 
    `/catalog/insight/product/get/` | 
    Request parameter
`brands` | 
   |
  
| 
    Insights > Your trending products | 
    Availability (filter) | 
     | 
    `/catalog/insight/product/get/` | 
    Request parameter
`availabilities` | 
   |
  
| 
    Insights > Your trending products | 
    Rank | 
     | 
    `/catalog/insight/product/get/` | 
    No corresponding parameter. 
Indicated by the position of the product within the `product_insights` object array in the response. | 
   |
  
| 
    Insights > Your trending products | 
    Product | 
     | 
    `/catalog/insight/product/get/` | 
    Response parameters
`image_url` 
`description` | 
   |
  
| 
    Insights > Your trending products | 
    SKU ID | 
     | 
    `/catalog/insight/product/get/` | 
    Response parameter
`sku_id` | 
   |
  
| 
    Insights > Your trending products | 
    Category | 
     | 
    `/catalog/insight/product/get/` | 
    Response parameter
`category_info` | 
   |
  
| 
    Insights > Your trending products | 
    Brand | 
     | 
    `/catalog/insight/product/get/` | 
    Response parameter
`brand` | 
   |
  
| 
    Insights > Your trending products | 
    Price | 
     | 
    `/catalog/insight/product/get/` | 
    Response parameter
`price` | 
   |
  
| 
    Insights > Your trending products | 
    Availability | 
     | 
    `/catalog/insight/product/get/` | 
    Response parameter
`availability` | 
   |
  
| 
    Insights > Trending categories on TikTok | 
    Category (filter) | 
     | 
    `/catalog/insight/product/get/` | 
    Request parameter
`category_ids` | 
   |
  
| 
    Insights > Trending categories on TikTok | 
    Rank | 
     | 
    [/catalog/insight/category/get/](https://business-api.tiktok.com/portal/docs?id=1805640900563969) | 
    No corresponding parameter. 
Indicated by the position of the category within the `category_insights` object array in the response. | 
   |
  
| 
    Insights > Trending categories on TikTok | 
    Category | 
     | 
    `/catalog/insight/category/get/` | 
    Response parameters
`category_id` 
`level_info` | 
   |
  
| 
    Insights > Trending categories on TikTok | 
    Your matching products | 
     | 
    `/catalog/insight/category/get/` | 
    Response parameter
`total_products_count` | 
   |
  
| 
    Insights > Trending categories on TikTok | 
    Available now | 
     | 
    `/catalog/insight/category/get/` | 
    Response parameter
`product_availability_rate` | 
   |
