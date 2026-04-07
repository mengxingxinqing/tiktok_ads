# Upgraded Smart+ ad creative combinations by identity and ad type

**Doc ID**: 1847839781968897
**Path**: Appendix/Upgraded Smart+ ad creative combinations by identity and ad type

---

The following table outlines the various combinations of ad creative combinations based on identity type and ad type.

To learn more about Spark Ads, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298).

    
        
| 
            **Identity Type** | 
            **Ad Type** | 
            **Available creative combination** | 
            **Details** | 
            **Configurations** | 
         |
    
    
        
| 
            Custom User
(`identity_type` in the `ad_configuration` object is `CUSTOMIZED_USER`) | 
            non-Spark Ads | 
            Videos only creatives | 
            
- one to 50 videos with cover images
- one to five ad texts | 
            
- Specify one to 50 videos (`video_info`) with cover images (`image_info`)
- Specify one to five ad texts (`ad_text_list`)
- Do not specify `music_info` and `tiktok_item_id` | 
         |
        
| 
            Carousel only creatives | 
            
- one to 50 carousels with each carousel created through one to 35 images and one piece of music
- one to five ad texts | 
            
- Specify one to 50 carousels with each carousel created through one to 35 images (`image_info`) and one piece of music (`music_info`)
- Specify one to five ad texts (`ad_text_list`)
- Do not specify `video_info` and `tiktok_item_id` | 
         |
        
| 
            Combination of videos and carousel creatives | 
            
- A combination of up to 50 videos with cover images and carousels, with each carousel created through one to 35 images and one piece of music
- one to five ad texts | 
            
- Specify a combination of up to 50 videos (`video_info`) with cover images (`image_info`) and carousels, with each carousel created through one to 35 images (`image_info`) and one piece of music (`music_info`)
- Specify one to five ad texts (`ad_text_list`)
- Do not specify `tiktok_item_id` | 
         |
        
| 
            TikTok User
/TikTok Account User in Business Center
(`identity_type` within the `creative_info` object is `TT_USER` or `BC_AUTH_TT`) | 
            Spark Ads created through Spark Ads PUSH | 
            Videos only creatives | 
            
- one to 50 videos with cover images
- one to five ad texts
- (Optional) Enable "Show through ads only" to limit your posts to paid traffic or disable the setting to allow the post to appear on your TikTok profile and be eligible to receive organic traffic. | 
            
- Specify one to 50 videos (`video_info`) with cover images (`image_info`)
- Specify one to five ad texts (`ad_text_list`)
- Do not specify `music_info` and `tiktok_item_id`
- You can either set et `dark_post_status` to `ON` to enable "Show through ads only" or `OFF` to disable "Show through ads only". | 
         |
        
| 
            Carousel only creatives | 
            
- one to 50 carousels with each carousel created through one to 35 images and one piece of music
- one to five ad texts
- (Optional) Enable "Show through ads only" to limit your posts to paid traffic or disable the setting to allow the post to appear on your TikTok profile and be eligible to receive organic traffic. | 
            
- Specify one to 50 carousels with each carousel created through one to 35 images (`image_info`) and one piece of music (`music_info`)
- Specify one to five ad texts (`ad_text_list`)
- Do not specify `video_info` and `tiktok_item_id`
- You can either set et `dark_post_status` to `ON` to enable "Show through ads only" or `OFF` to disable "Show through ads only". | 
         |
        
| 
            Combination of videos and carousel creatives | 
            
- A combination of up to 50 videos with cover images and carousels, with each carousel created through one to 35 images and one piece of music
- one to five ad texts
- (Optional) Enable "Show through ads only" to limit your posts to paid traffic or disable the setting to allow the post to appear on your TikTok profile and be eligible to receive organic traffic. | 
            
- Specify a combination of up to 50 videos (`video_info`) with cover images (`image_info`) and carousels, with each carousel created through one to 35 images (`image_info`) and one piece of music (`music_info`)
- Specify one to five ad texts (`ad_text_list`)
- Do not specify `tiktok_item_id`
- You can either set et `dark_post_status` to `ON` to enable "Show through ads only" or `OFF` to disable "Show through ads only". | 
         |
        
| 
            TikTok User
/TikTok Account User in Business Center
/Authorized User 
(`identity_type` within the `creative_info` object is `TT_USER`,`BC_AUTH_TT`, or `AUTH_CODE`) | 
            Spark Ads created through Spark Ads PULL | 
            Video posts only creatives | 
            one to 50 TikTok video posts | 
            
- Specify one to 50 TikTok video posts through `tiktok_item_id`. 
- Do not specify  `video_info`, `image_info`, `music_info`, and `ad_text_list` | 
         |
        
| 
            Photo posts only creatives | 
            one to 50 TikTok photo posts | 
            
- Specify one to 50 TikTok photo posts through `tiktok_item_id`. 
- Do not specify  `video_info`, `image_info`, `music_info`, and `ad_text_list` | 
         |
        
| 
            Combination of video and photo post creatives | 
            a combination of up to 50 TikTok video posts and photo posts | 
            
- Specify a combination of up to 50 TikTok video posts and photo posts through `tiktok_item_id`. 
- Do not specify  `video_info`, `image_info`, `music_info`, and `ad_text_list` | 
         |
