# Get ad groups

**Doc ID**: 1739314558673922
**Path**: API Reference/Ad Groups/Get ad groups

---

Use this endpoint to obtain detailed information of an ad group or ad groups. 

The returned information from this query can be customized by specifying the information needed in the `fields` field of the request. Use the `filtering` field to specify which ad group is returned. Supported filters include campaign ID,  advertising objective , ad group ID, ad group name, ad group creation time, billing event, and the ad group status.

>  **Note**
If you wish to include deleted data in your query,  either specify the value of `STATUS_DELETE` in the `primary_status` field or `ADGROUP_STATUS_DELETE` /`ADGROUP_STATUS_CAMPAIGN_DELETE` in the `secondary_status` field. By default deleted data is not queried. 

## Comparing v1.2 and v1.3 
 The following table outlines the differences between v1.2 and v1.3 endpoints. 
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path|/v1.2/adgroup/get/|/v1.3/adgroup/get/|
|Request parameter name|`create_start_time` 
`create_end_time`
 `status`  |  `creation_filter_start_time`
 `creation_filter_end_time`
`secondary_status`  |
|Request parameter data type|`advertiser_id`: number
`campaign_ids`: number[]
`adgroup_ids`: number[]|`advertiser_id`: string 
`campaign_ids`: string[]
`adgroup_ids`: string[]|
|New request parameters|/|`promotion_type`
`exclude_field_types_in_response`
`creative_material_mode`
`bid_strategy`
`optimization_goal` 
`campaign_system_origins` 
`buying_types`
`split_test_enabled`
`campaign_automation_type`|
|Response parameter name|`is_share_disable`
`placement`
`enable_inventory_filter`
`external_type`
 `external_action`
 `deep_external_action` 
`age`
`operation_system` 
`connection_type`
 `device_price`
 `android_osv`
 `ios_target_device` 
`ios_osv`
 `optimize_goal`
 `bid`
`conversion_bid`
`deep_cpabid`
`daily_retention_ratio`
`status`
`opt_status`
`action_v2`
`user_actions`
`rf_buy_type`
`buy_impression`
`buy_reach`
`rf_predict_cpr`
`rf_predict_frequency`
`include_custom_actions`
`exclude_custom_actions`
`dpa_retargeting_type`
`brand_safety`
`enable_expansion`
`ad_app_profile_page_type`
`display_mode`|`share_disabled`
`placements`
`inventory_filter_enabled`
`promotion_type`
`optimization_event`
`secondary_optimization_event`
`age_groups`
`operating_systems`
`network_types`
`device_price_ranges`
`min_android_version`
`ios14_targeting`
`min_ios_version`
`optimization_goal`
`bid_price`
`conversion_bid_price`
`deep_cpa_bid`
`next_day_retention`
`secondary_status`
`operation_status`
`actions`
`video_user_actions`
`rf_purchased_type`
`purchased_impression`
`purchased_reach`
`rf_estimated_cpr`
`rf_estimated_frequency`
`included_custom_actions`
`excluded_custom_actions`
`shopping_ads_retargeting_type`
`brand_safety_type`
`expansion_enabled`
`adgroup_app_profile_page_state`
`delivery_mode`|
|Response parameter data type|`advertiser_id`: number
`campaign_id`: number
`adgroup_id`: number
`app_id`: number 
`store_id`: number 
`pixel_id`: number
`skip_learning_phase`: number
`catalog_id`: number
`schedule_id`: number |`advertiser_id`: string 
`campaign_id`: string
`adgroup_id`: string
`app_id`: string 
`store_id`: string
`pixel_id`: string 
`skip_learning_phase`: boolean
`catalog_id`: string 
`schedule_id`: string |
|Response parameter name and data type|`is_comment_disable`: number
 `shop_authorized_bc`: number
 `audience`: number[]
 `excluded_audience`: number[]  
`location`: number[]  
`interest_category_v2`: number[]
`interest_keywords`: number[] 
`device_models`: number[]
`carriers_v2`: number[] 
 `video_download`: string  
 `pangle_block_app_list_id`: number[]
 `action_categories`: number[]  
 `pangle_audience_package_include`: number[]
 `pangle_audience_package_exclude`: number[]
`catalog_authorized_bc`: number
`automated_targeting`: string |`comment_disabled`: boolean
 `store_authorized_bc_id`: string
 `audience_ids`: string[] 
 `excluded_audience_ids`: string[]
 `location_ids`: string[]
`interest_category_ids`: string[]
` interest_keyword_ids `: string[] 
` device_model_ids `: string[] 
`carrier_ids`: string[] 
` video_download_disabled`: boolean 
 `blocked_pangle_app_ids`: string[]
 `action_category_ids`: string[]
 ` included_pangle_audience_package_ids`: string[]
 ` excluded_pangle_audience_package_ids`: string[] 
`catalog_authorized_bc_id`: string
`auto_targeting_enabled`: boolean |
|New response parameters|/ | `shopping_ads_type`
 `product_source`
`split_test_group_id`
`split_test_status`
 `contextual_tag_ids`
 `purchase_intention_keyword_ids`
`spending_power`
`zipcode_ids`
`isp_ids`
`category_exclusion_ids`
`vertical_sensitivity_id`
`is_smart_performance_campaign`
 `search_result_enabled`
`click_attribution_window` 
`view_attribution_window`
`attribution_event_count` 
`shopping_ads_retargeting_custom_audience_relation`   
`smart_audience_enabled` 
`smart_interest_behavior_enabled` 
`campaign_system_origin` 
`engaged_view_attribution_window`  
`vbo_window`
`predict_impression` 
`topview_reach_range`
`pre_discount_cpm` 
`cpm`
 `discount_type`
 `discount_amount`
 `discount_percentage`
`pre_discount_budget`
`tiktok_subplacements`
 `messaging_app_type` 
`messaging_app_account_id` 
 `phone_region_code`
 `phone_region_calling_code`
`phone_number`
`message_event_set_id` 
 `deep_funnel_optimization_status` 
`deep_funnel_event_source`  
 `deep_funnel_event_source_id`   
`deep_funnel_optimization_event`
 `search_keywords`
 `automated_keywords_enabled`
 `app_config` 
 `custom_conversion_id`
`is_lhf_compliance`
`campaign_automation_type` |
|Response parameters deprecated in v1.3|/ |`carriers` |
```

## Request

**Endpoint** 

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162). |
```

**Parameters**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|advertiser_id {Required}|string| Advertiser ID. |
|fields |string[]| Fields that you want to get. When not specified, all fields are returned by default. For allowed fields, see the fields under `list` in the response section.|
|exclude_field_types_in_response| string[]|The type of fields that you want to remove from the response.
Allowed enum values: 
- `NULL_FIELD`: Fields with null values.|
|filtering |object|Filter conditions. Set these conditions according to your requirements. If not set, all ad groups under the advertiser will be returned. 

Example: `filtering={"campaign_automation_type":"UPGRADED_SMART_PLUS"}`|
#| campaign_automation_type | string | Campaign automation type.

Enum values:
- `MANUAL`: Manual Campaigns.
- `SMART_PLUS`: Smart+ Campaigns.
- `UPGRADED_SMART_PLUS`: Upgraded Smart+ Campaigns, a new automated campaign type. To learn more about Upgraded Smart+ Campaigns, see [Upgraded Smart+ Campaign](https://business-api.tiktok.com/portal/docs?id=1853452461203458). |
#|campaign_ids |string[]| List of campaign IDs. 
Max size: 100. |
#| campaign_system_origins| string[] | The origins (sources) of the campaigns that the ad groups belong to. 
 
 Enum values: 
- `PROMOTE`: The campaign is a Promote campaign created through the TikTok mobile App.
- `TT_ADS_PLATFORM`: The campaign is a non-Promote campaign created through the API or in TikTok Ads Manager.  Default value: `["TT_ADS_PLATFORM"]`.

Only the following settings can be retrieved for a Promote ad group: 
- `advertiser_id`
- `campaign_id`
-  `campaign_name`
- `adgroup_id` 
- `adgroup_name` 
- `create_time`
- `budget` 
- `schedule_type`
- `schedule_start_time`
-  `schedule_end_time`
- `operation_status`
- `secondary_status`
 To learn more about the availability of and the supported filters for Promote ad groups, see [Promote campaigns](https://business-api.tiktok.com/portal/docs?id=1785880454546433). |
#|adgroup_ids |string[]| List of Ad group IDs. 
Max size: 100. |
#|adgroup_name |string|Ad group name. |
#|primary_status |string|Primary status. For enum values, see [Enumeration - Primary Status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). The default value is `STATUS_NOT_DELETE`, which returns ad groups in all statuses excluding `STATUS_DELETE`. If you want to get ad groups in all statuses including `STATUS_DELETE`, use `STATUS_ALL` instead.|
#|secondary_status|string| Ad group secondary status. For enum values, see [Enumeration - Ad Group Status - Secondary Status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 

**Note**: 
- This field is not returned in the sandbox environment because the ad group is not actually delivered.
- See [Supported secondary statuses for a primary status](https://ads.tiktok.com/marketing_api/docs?id=1757239620352002) to learn about the valid values you can pass in via `secondary_status` for the primary status you specify.|
#|objective_type |string| Advertising objective. 

For details, see [Enumeration - Advertising Objective](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).

**Note**: Whether you choose `WEB_CONVERSIONS` or  `CONVERSIONS` as the objective filter, we will return data of both `WEB_CONVERSIONS` and  `CONVERSIONS`.  |
#| buying_types | string[] | Filter by buying types. 

Enum values: 
-  `AUCTION`: Auction ads. 
- `RESERVATION_RF`: Reservation Reach & Frequency ads and TikTok Pulse ads.
- `RESERVATION_TOP_VIEW`: Reservation TopView ads.
Default value: `["AUCTION", "RESERVATION_RF"]`.

 To learn more about the availability of TopView ads in the API, see [TopView](https://business-api.tiktok.com/portal/docs?id=1804258360285186). 

**Note**: The enum value `RESERVATION_TOP_VIEW` cannot be combined with other values. To filter TopView ads, set this field to `["RESERVATION_TOP_VIEW"]`. |
#|optimization_goal|string|Optimization goal.   Enum values:  [Enumeration - Optimization Goal](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138#item-link-Optimization%20Goal).|
#|promotion_type |string| The promotion type (optimization location) that you want to filter by. 
Enum values: 
- `APP`: App. 
- `WEBSITE`: Landing page. 
- `INSTANT_FORM`: Instant Form. 
- `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`: TikTok direct message.
- `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`: Social media app.  
-  `LEAD_GEN_CLICK_TO_CALL`: Phone call. 
**Note**: 
-  This filter field is different from the `promotion_type` used for ad group creation, which is also returned in the response of this endpoint. `promotion_type` as filter is also supported in synchronous basic reports and synchronous DSA reports.
-  See [Appendix-Mapping between different promotion types](https://ads.tiktok.com/marketing_api/docs?id=1758485431181314) to learn about how you can set this field to filter out certain promotion types that are used for ad group creation. |
#|bid_strategy |string| Bidding strategy. Enum values: `BID_STRATEGY_COST_CAP`,` BID_STRATEGY_BID_CAP`, `BID_STRATEGY_MAX_CONVERSION` and `BID_STRATEGY_LOWEST_COST`|
#|creative_material_mode |string| The strategy that your creatives will be delivered.  

Enum values: `CUSTOM`(custom), `SMART_CREATIVE`(Smart Creative). |
#|billing_events |string[]|Events that you want to pay for.  For enum values, see [Enumeration - Billing Event](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|creation_filter_start_time |string|Filter by lower range of ad group creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time zone). Ad groups created later than this time will be returned.
Suggestion: A time range within 6 months is suggested when applying a creation time filter, to ensure that the success and speed of the task won't be affected.|
#|creation_filter_end_time|string|Filter by higher range of ad group creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time zone). Ad groups created earlier than this time will be returned.
Suggestion: A time range within 6 months is suggested when applying a creation time filter, to ensure that the success and speed of the task won't be affected.|
#|split_test_enabled|boolean|Filter by whether split test has been enabled for the ad group or not.
`true`: Only get ad groups with enabled split test,  `false`: Only get disabled ad groups. 
**Note**: If you do not specify this field, you will get all ad groups.|
|page |number|Current page number. 

Default value: 1. Value range: ≥ 1.|
|page_size |number|Page size. 

Default value is: 10. Value range: 1-1,000.

**Note**: If you use the enum value `RESERVATION_TOP_VIEW` for the filter field `buying_types`, the maximum value you can specify for this field is 100. |
```

### Example
#### Get undeleted ad groups within your ad account
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/adgroup/get/?advertiser_id={{advertiser_id}}' \
--header 'Access-Token: {{Access-Token}}'
(/code)
(code Java java)
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.*;
import org.apache.http.client.utils.URIBuilder;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Demo {
    private static final String ACCESS_TOKEN = "xxx";
    private static final String PATH = "/open_api/v1.3/adgroup/get/";

    /**
     * Build request URL
     *
     * @param path Request path
     * @return Request URL
     */
    private static String buildUrl(String path) throws URISyntaxException {
        URI uri = new URI("https", "business-api.tiktok.com", path, "", "");
        return uri.toString();
    }

    /**
     * Send GET request
     *
     * @param jsonStr:Args in JSON format
     * @return Response in JSON format
     */
    private static String get(String jsonStr) throws IOException, URISyntaxException {
        OkHttpClient client = new OkHttpClient().newBuilder().build();
        URIBuilder ub = new URIBuilder(buildUrl(PATH));
        ObjectMapper mapper = new ObjectMapper();
        Map map = mapper.readValue(jsonStr, Map.class);
        map.forEach((k, v) -> {
            try {
                ub.addParameter(k, v instanceof String ? (String) v : mapper.writeValueAsString(v));
            } catch (JsonProcessingException e) {
                e.printStackTrace();
            }
        });
        URL url = ub.build().toURL();

        Request request = new Request.Builder()
                .url(url)
                .method("GET", null)
                .addHeader("Access-Token", ACCESS_TOKEN)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
    }

    public static void main(String[] args) throws IOException, URISyntaxException {
        Long advertiser_id = ADVERTISER_ID;
        List fields_list = FIELDS;
        String fields = fields_list.stream().map(s -> String.format("\"%s\"", s)).collect(Collectors.joining(", "));
        String status = STATUS;
        List adgroup_ids_list = ADGROUP_IDS;
        String adgroup_ids = adgroup_ids_list.stream().collect(Collectors.joining(", "));
        String adgroup_name = ADGROUP_NAME;
        List campaign_ids_list = CAMPAIGN_IDS;
        String campaign_ids = campaign_ids_list.stream().collect(Collectors.joining(", "));
        List billing_events_list = BILLING_EVENTS;
        String billing_events = billing_events_list.stream().map(s -> String.format("\"%s\"", s)).collect(Collectors.joining(", "));
        String primary_status = PRIMARY_STATUS;
        String objective_type = OBJECTIVE_TYPE;
        Long page = PAGE;
        Long page_size = PAGE_SIZE;

        // Args in JSON format
        String myArgs = String.format("{\"advertiser_id\": \"%s\", \"fields\": [%s], \"filtering\": {\"status\": \"%s\", \"adgroup_ids\": [%s], \"adgroup_name\": \"%s\", \"campaign_ids\": [%s], \"billing_events\": [%s], \"primary_status\": \"%s\", \"objective_type\": \"%s\"}, \"page\": \"%s\", \"page_size\": \"%s\"}",advertiser_id, fields, status, adgroup_ids, adgroup_name, campaign_ids, billing_events, primary_status, objective_type, page, page_size);
        System.out.println(get(myArgs));
    }
}

(/code)

(code Python python)
# coding=utf-8
import json
import requests

from six import string_types
from six.moves.urllib.parse import urlencode, urlunparse  # noqa

ACCESS_TOKEN = "xxx"
PATH = "/open_api/v1.3/adgroup/get/"

def build_url(path, query=""):
    # type: (str, str) -> str
    """
    Build request URL
    :param path: Request path
    :param query: Querystring
    :return: Request URL
    """
    scheme, netloc = "https", "business-api.tiktok.com"
    return urlunparse((scheme, netloc, path, "", query, ""))

def get(json_str):
    # type: (str) -> dict
    """
    Send GET request
    :param json_str: Args in JSON format
    :return: Response in JSON format
    """
    args = json.loads(json_str)
    query_string = urlencode({k: v if isinstance(v, string_types) else json.dumps(v) for k, v in args.items()})
    url = build_url(PATH, query_string)
    headers = {
        "Access-Token": ACCESS_TOKEN,
    }
    rsp = requests.get(url, headers=headers)
    return rsp.json()

if __name__ == '__main__':
    advertiser_id = ADVERTISER_ID
    fields_list = FIELDS
    fields = ",".join('"%s"' % _ for _ in fields_list)
    status = STATUS
    adgroup_ids_list = ADGROUP_IDS
    adgroup_ids = ",".join("%s" % _ for _ in adgroup_ids_list)
    adgroup_name = ADGROUP_NAME
    campaign_ids_list = CAMPAIGN_IDS
    campaign_ids = ",".join("%s" % _ for _ in campaign_ids_list)
    billing_events_list = BILLING_EVENTS
    billing_events = ",".join('"%s"' % _ for _ in billing_events_list)
    primary_status = PRIMARY_STATUS
    objective_type = OBJECTIVE_TYPE
    page = PAGE
    page_size = PAGE_SIZE

    # Args in JSON format
    my_args = "{\"advertiser_id\": \"%s\", \"fields\": [%s], \"filtering\": {\"status\": \"%s\", \"adgroup_ids\": [%s], \"adgroup_name\": \"%s\", \"campaign_ids\": [%s], \"billing_events\": [%s], \"primary_status\": \"%s\", \"objective_type\": \"%s\"}, \"page\": \"%s\", \"page_size\": \"%s\"}" % (advertiser_id, fields, status, adgroup_ids, adgroup_name, campaign_ids, billing_events, primary_status, objective_type, page, page_size)
    print(get(my_args))

(/code)

(code PHP php)

$ACCESS_TOKEN = "xxx";
$PATH = "/open_api/v1.3/adgroup/get/";

/**
 * Build request URL
 * @param $path : Request path
 * @return string
 */
function build_url($path)
{
    return "https://business-api.tiktok.com" . $path;
}

/**
 * Send GET request
 * @param $json_str : Args in JSON format
 * @return boolean|string : Response in JSON format
 */
function get($json_str)
{
    global $ACCESS_TOKEN, $PATH;
    $curl = curl_init();

    $args = json_decode($json_str, true);

    /* Values of querystring is also in JSON format */
    foreach ($args as $key => $value) {
        $args[$key] = is_string($value) ? $value : json_encode($value);
    }

    $url = build_url($PATH) . "?" . http_build_query(
            $args
        );

    curl_setopt_array($curl, array(
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 0,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
        CURLOPT_HTTPHEADER => array(
            "Access-Token: " . $ACCESS_TOKEN,
        ),
    ));

    $response = curl_exec($curl);
    curl_close($curl);
    return $response;
}

$advertiser_id = ADVERTISER_ID;
$fields_list = FIELDS;
$fields = join(",",array_map(function($value) {return sprintf("\"%s\"",$value) ;},$fields_list));
$status = STATUS;
$adgroup_ids_list = ADGROUP_IDS;
$adgroup_ids = join(",",$adgroup_ids_list);
$adgroup_name = ADGROUP_NAME;
$campaign_ids_list = CAMPAIGN_IDS;
$campaign_ids = join(",",$campaign_ids_list);
$billing_events_list = BILLING_EVENTS;
$billing_events = join(",",array_map(function($value) {return sprintf("\"%s\"",$value) ;},$billing_events_list));
$primary_status = PRIMARY_STATUS;
$objective_type = OBJECTIVE_TYPE;
$page = PAGE;
$page_size = PAGE_SIZE;

/* Args in JSON format */
$my_args = sprintf("{\"advertiser_id\": \"%s\", \"fields\": [%s], \"filtering\": {\"status\": \"%s\", \"adgroup_ids\": [%s], \"adgroup_name\": \"%s\", \"campaign_ids\": [%s], \"billing_events\": [%s], \"primary_status\": \"%s\", \"objective_type\": \"%s\"}, \"page\": \"%s\", \"page_size\": \"%s\"}", $advertiser_id, $fields, $status, $adgroup_ids, $adgroup_name, $campaign_ids, $billing_events, $primary_status, $objective_type, $page, $page_size);
echo get($my_args);
(/code)
```

#### Get all ad groups within your ad account
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/adgroup/get/?advertiser_id={{advertiser_id}}&filtering={"primary_status":"STATUS_ALL"}' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

#### Get ad groups within a specific campaign
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/adgroup/get/?advertiser_id={{advertiser_id}}&filtering={"campaign_ids":["{{campaign_id}}"]}' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```
#### Get ad groups created within a specific time range
```xcodeblock
(code curl http)
curl --location --request GET  'https://business-api.tiktok.com/open_api/v1.3/adgroup/get/?advertiser_id={{advertiser_id}}&filtering={"creation_filter_start_time":"2024-01-01 00:00:00","creation_filter_end_time":"2024-01-30 00:00:00"}' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```

## Response

```xtable
|Field{42%}|Data Type{10%}|Description{48%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message |string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|request_id |string|The log id of a request, which uniquely identifies the request.|
|data |object|Returned data. The returned list is sorted by ad group ID (`adgroup_id`) in reverse order by default. 

**Note**: The data for [Product GMV max ads](https://ads.tiktok.com/help/article/about-automated-product-ads?lang=en) and LIVE GMV max ads created from TikTok Shop is excluded from the response. Shopping Ads created via API or TikTok Ads Manager are not affected.|
#|list |object[]|Data list. The returned fields are generated based on the `fields` field in the request parameters. If not specified in the request, all fields are returned by default.|
##|advertiser_id |string|Advertiser ID|
##|campaign_id |string| Campaign ID |
##|campaign_name |string|The name of the campaign that the ad group belongs to.|
##| campaign_system_origin | string | Returned for Promote ad groups only. 
Not returned for non-Promote ad groups. 

The origin (source) of the campaign that the ad group belongs to. 

Enum values: 
-  `PROMOTE`: The campaign is a Promote campaign created through the TikTok mobile App. 
Only the following settings can be retrieved for a Promote ad group (`campaign_system_origin` is `PROMOTE` at the campaign level): 
- `advertiser_id`
- `campaign_id`
-  `campaign_name`
- `adgroup_id` 
- `adgroup_name` 
- `create_time`
- `budget` 
- `schedule_type`
- `schedule_start_time`
-  `schedule_end_time`
- `operation_status`
- `secondary_status`|
##| campaign_automation_type | string | Campaign automation type.

Enum values:
- `MANUAL`: Manual Campaigns.
- `SMART_PLUS`: Smart+ Campaigns.
- `UPGRADED_SMART_PLUS`: Upgraded Smart+ Campaigns, a new automated campaign type. To learn more about Upgraded Smart+ Campaigns, see [Upgraded Smart+ Campaign](https://business-api.tiktok.com/portal/docs?id=1853452461203458). |
##| is_smart_performance_campaign | boolean | Whether the campaign is an automated campaign type.

Supported values:
- `true`: The campaign is a legacy Smart+ Campaign.
- `false`: The campaign is a Manual Campaign or an Upgraded Smart+ Campaign.To determine whether a campaign is a Manual Campaign or an Upgraded Smart+ Campaign, check the returned `campaign_automation_type`.When `campaign_automation_type` is `MANUAL`, the campaign is a Manual Campaign.
- When `campaign_automation_type` is `UPGRADED_SMART_PLUS`, the campaign is an Upgraded Smart+ Campaign . |
##|adgroup_id |string| Ad group ID |
##|adgroup_name |string| Ad group name|
##| create_time | string | The time at which the ad group was created, in the format of `"YYYY-MM-DD HH:MM:SS"`. 

Example: `"2023-01-01 00:00:01"`. |
##| modify_time | string | The time at which the ad group was modified, in the format of `"YYYY-MM-DD HH:MM:SS"`.  

 Example: `"2023-01-01 00:00:01"`. |
##|shopping_ads_type|string|Returned when `objective_type` at the campaign level is `PRODUCT_SALES`.

Shopping ads type. 

Enum values: 
- `VIDEO`: Video Shopping Ads.
- `LIVE`: Live Shopping Ads.
- `PRODUCT_SHOPPING_ADS`: Product Shopping Ads.
- `CATALOG_LISTING_ADS`: Catalog Listing Ads.
- `UNSET`: Unset.|
##|identity_id |string|Returned when `shopping_ads_type` is `VIDEO` and `product_source` is `SHOWCASE` or `shopping_ads_type` is `LIVE`.

Identity ID. |
##|identity_type|string|Returned when `shopping_ads_type` is `VIDEO` and `product_source` is `SHOWCASE` or `shopping_ads_type` is `LIVE`.

Identity type. Enum values: `AUTH_CODE` (Authorized Post User), `TT_USER` (TikTok Business Account User), `BC_AUTH_TT`(the TikTok account that a Business Center is authorized to access). Returned when `objective_type` is `PRODUCT_SALES`. See [Identities](https://ads.tiktok.com/marketing_api/docs?id=1738958351620097) for details. |
##|identity_authorized_bc_id|string|Returned when `identity_type` is `BC_AUTH_TT`.

  ID of the Business Center that a TikTok Account User in Business Center identity is associated with.  |
##|product_source|string|Returned for Video Shopping Ads and Product Shopping Ads.

Product source where you want to get products for promotion. 
Enum values: `UNSET` ,`CATALOG`(Catalog), `STORE` (TikTok Shop) ,`SHOWCASE`(TikTok Showcase).|
##|catalog_id|string| Returned in any of the following scenarios:
- `product_source` is `CATALOG` or `STORE`.
- `shopping_ads_type` is `LIVE` and this field is specified in the request.
Catalog ID.

**Note**: Starting June 30th, 2024, `catalog_id` will no longer be returned for newly created Shopping Ads where `product_source` is `STORE` because the specified `catalog_id` will be ignored. Existing Shopping Ads where `product_source` is `STORE` will not be affected unless you update them. If you update the existing ad groups, the existing `catalog_id`, if present for the ad groups, will no longer be returned.|
##|catalog_authorized_bc_id|string| Returned in any of the following scenarios:
- `shopping_ads_type` is `VIDEO` and `product_source` is `CATALOG` or `STORE`.
- `shopping_ads_type` is `LIVE` and this field is specified in the request.
For catalogs in Business Center, this field returns the ID of the Business Center that a catalog belongs to.

**Note**: Starting June 30th, 2024, `catalog_authorized_bc_id` will no longer be returned for newly created Shopping Ads where `product_source` is `STORE` because the specified `catalog_authorized_bc_id` will be ignored. Existing Shopping Ads where `product_source` is `STORE` will not be affected unless you update them. If you update the existing ad groups, the existing `catalog_authorized_bc_id`, if present for the ad groups, will no longer be returned.|
##|store_id |string| Returned in any of the following scenarios:
- `shopping_ads_type` is `VIDEO` and `product_source` is `STORE`.
- `shopping_ads_type` is `PRODUCT_SHOPPING_ADS` and `product_source` is `STORE`.
- `shopping_ads_type` is `LIVE` and this field is specified in the request.
ID of the TikTok Shop.  |
##|store_authorized_bc_id |string|Returned when `store_id` is passed. 

ID of the Business Center that is authorized to access the store (`store_id`). |
##|promotion_type |string|Promotion type (Optimization location).
 You can decide where you'd like to promote your products using this field. For value definitions, see [Enumeration - Promotion Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
##|promotion_target_type |string| The promotion type for Lead Generation objective. 
Enum values: 
-  `INSTANT_PAGE`：Instant Form. To create a fast-loading in-app TikTok Instant Form to collect more leads.
-  `EXTERNAL_WEBSITE`：Website Form. To use a landing page that has the Website Form or the TikTok Instant Page that redirects to the website with the Website Form to collect more leads. 
- `UNSET`. |
##| messaging_app_type | string | The type of instant messaging app or customized URL to use in the Instant Messaging Ad Group.

Enum values:  
-  `MESSENGER`: Messenger. 
- `WHATSAPP`: WhatsApp.
- `ZALO`: Zalo. 
- `LINE`: Line.
- `IM_URL`: Instant Messaging URL.|
##| messaging_app_account_id | string | The ID of the instant messaging app account.
- When `messaging_app_type` is `MESSENGER`, this field represents the Facebook Page ID.
- When `messaging_app_type` is `LINE`, this field represents the LINE Business ID.
- When `messaging_app_type` is `WHATSAPP`, this field represents the WhatsApp phone number automatically populated based on the specified `phone_region_code`, `phone_region_calling_code`, and `phone_number`.|
##| phone_region_code | string | The region code for the WhatsApp or Zalo phone number. 

 Example: `US`. |
##| phone_region_calling_code | string | The region calling code for the WhatsApp or Zalo phone number. 

Example: `+1`. |
##| phone_number | string | The WhatsApp or Zalo phone number. |
##|promotion_website_type|string|TikTok Instant Page type in the ad group.  
Enum values:
- `UNSET`: To not use TikTok Instant Page. 
- `TIKTOK_NATIVE_PAGE`: To use TikTok Instant Page.  |
##|app_id |string|The App ID of the app to promote.You can get `app_id` by using the [/app/list/](https://ads.tiktok.com/marketing_api/docs?id=1740859313270786) endpoint.|
##|app_type |string| The type of the promoted app. Enum values: `APP_ANDROID` (Android), `APP_IOS` (iOS).|
##|app_download_url |string|App download link|
##|pixel_id |string|Pixel ID. Only applicable for landing pages. |
##|optimization_event |string|Conversion event for the ad group. See [Conversion events](https://ads.tiktok.com/marketing_api/docs?id=1739361474981889) for more. |
##|custom_conversion_id|string|The ID of the Custom Conversion used in the ad group.|
##| app_config | object[] | Returned when `sales_destination` is `WEB_AND_APP` at the campaign level.

  Details of the app or apps to promote. |
###| app_id | string | The App ID of the app to promote. |
##| deep_funnel_optimization_status | string | The status of deep funnel optimization. 
 With deep funnel optimization, you can select a secondary event alongside the primary optimization event, which can help improve campaign effectiveness.  
 
Enum values:  
- `ON`: enabled.  
-  `OFF`: disabled.  |
##| deep_funnel_event_source| string | Returned when `deep_funnel_optimization_status` is `ON`.   
 
 The event source type. 
 
Enum values: 
- `PIXEL`: Pixel.  
- `OFFLINE`: Offline Event Set. 
- `CRM`: CRM Event Set. |
##| deep_funnel_event_source_id | string | Returned when `deep_funnel_optimization_status` is `ON`. 
 
 Event Source ID.  
 

- When `deep_funnel_event_source` is `PIXEL` , this field represents a Pixel ID.
- When `deep_funnel_event_source` is `OFFLINE`, this field represents an Offline Event Set ID.  
- When `deep_funnel_event_source` is `CRM`, this field represents a CRM Event Set ID. |
##| deep_funnel_optimization_event | string | Returned when `deep_funnel_optimization_status` is `ON`.  
 
Deep funnel optimization event.   
 
Example: `SHOPPING`. |
##|placement_type |string|The placement strategy that decides where your ads will be shown. Enum values: `PLACEMENT_TYPE_AUTOMATIC` (Automatic placement), `PLACEMENT_TYPE_NORMAL` (Select placement). |
##|placements | string[] | The apps where you want to deliver your ads. For enum values, see [Enumeration - Placement](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
**Note**: 
-  If `placement_type` of the ad group is `PLACEMENT_TYPE_AUTOMATIC` (Automatic placement), the placements supported for your advertising objective will be returned for this field. For instance, if the actual supported placement is TikTok only, the returned value for this field will be `PLACEMENT_TIKTOK`.  However, if `PLACEMENT_GLOBAL_APP_BUNDLE` is supported for your objective, but you are not allowlisted for the Global App Bundle placement feature, `PLACEMENT_GLOBAL_APP_BUNDLE` will not be included in the returned value for this field.
-  If `placement_type` of the ad group is `PLACEMENT_TYPE_NORMAL` (Select placement), the placements you specified through `placements` in the request will usually be returned for this field.  The only exception is that if `PLACEMENT_GLOBAL_APP_BUNDLE` is specified through `placements` in the request, but you are not allowlisted for the Global App Bundle placement feature, `PLACEMENT_GLOBAL_APP_BUNDLE` will be filtered out from the returned value for this field. For instance, if you specify placements as `["PLACEMENT_TIKTOK", "PLACEMENT_GLOBAL_APP_BUNDLE"]` in the request, but you are not allowlisted for Global App Bundle, the returned value for this field will be `["PLACEMENT_TIKTOK"]`.  |
##| tiktok_subplacements | string[] | The subplacements within TikTok for your ads, allowing you to choose where your ads will appear. 

Enum value: 
- `IN_FEED`: In-feed. Ads will be placed in the For You feed and might also be placed in Profile Page and Following feeds.
- `SEARCH_FEED`: Search feed.
- `TIKTOK_LITE`: TikTok Lite, a streamlined version of TikTok that features a smaller app size and faster video loading speed. The TikTok Lite subplacement is currently available for Japan or South Korea as targeting locations.
- `LEMON8`: Lemon8, a community app for lifestyle content, focusing on real-life experiences, tips, guides, and product reviews. By including Lemon8 as a subplacement, your ads will appear in its For You feed, Search feed, and Immersive Video feed. [Learn more about Lemon8](https://ads.tiktok.com/help/article/about-lemon8-in-tiktok-ads-manager).
**Note**: If `tiktok_subplacements` is not specified when you create the ad group, the value of this field will be an empty list (`[]`). |
##| search_result_enabled | boolean | Whether to include your ads in Search Ads, namely to show your ads to users when they search for your business on TikTok. |
##|automated_keywords_enabled| boolean |Whether to enable automated keywords and let the system automatically generate keywords after you add ads. This expands high-quality traffic to improve performance. View high-performing automated keywords in reporting.

Supported values: `true`, `false`. |
##|search_keywords|object[] |Returned only for Search Ads Campaigns.

 A list of search keywords, that is, words or phrases that are used to match your ads with the terms people are searching for.  |
###|keyword | string | The search keyword. |
###|match_type | string | The match type for the search keyword.

Enum values:
- `PRECISE_WORD`: exact match. Your ads will only show for user search queries that exactly match these keywords.
- `PHRASE_WORD`: phrase match. Your ads will only show for these specific keywords if users search these keywords in the same order.
- `BROAD_WORD`: broad match. Your ads will show for user search queries for any of the words you have included, even if the words are in a different order. |
###|keyword_bid_type | string | The bid type for the keyword and match type combination.

Enum values:
- `FOLLOW_ADGROUP`: To use the ad group level bid (`bid_price`) as the `keyword_bid`.
- `CUSTOM`: To customize the bid via `keyword_bid`. |
###|keyword_bid | float | The bid price for the keyword and match type combination. |
###|audit_status | string | The review status of the search keyword.

Enum values:
- `AUDITING`: The keyword is under review.
- `PASS`: The keyword has passed review and can be delivered.
- `REJECTED`: The keyword failed to pass the review and cannot be delivered.|
###|reject_info | object[] | Returned only when `audit_status` is `REJECTED`.

Details about the rejection.|
####|forbidden_location| string |The targeted region that failed the review. 

For enum values, see [Appendix - Location codes](https://business-api.tiktok.com/portal/docs?id=1737585867307010).|
####|reject_reasons| object[] |List of rejection reasons.|
#####|reason| string |The rejection reason. |
##|comment_disabled |boolean|Whether to allow comments on your ads on TikTok.  |
##|video_download_disabled |boolean| Whether users can download your video ads on TikTok. |
##|share_disabled|boolean|Whether sharing to third-party platforms is disabled for ads in this ad group. |
##|blocked_pangle_app_ids |string[]|Pangle app block list ID.|
##|audience_type |string| App retargeting audience type. For enum values, see [Enumeration - App Retargeting Audience Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). |
##|audience_rule |object| Rules that specify your audience.  |
##|auto_targeting_enabled{-To be deprecated}|boolean|Whether to enable automated targeting. 

**Note**:  Starting June, 2024, you can no longer enable Automatic targeting or Targeting expansion for your ad groups. To ensure a smooth API integration, we recommend you migrate to [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
##| shopping_ads_retargeting_type | string | Returned when `shopping_ads_type` is `VIDEO` and `product_source` is `CATALOG`. 

The retargeting type of shopping ads. Enum values: 
- `LAB1`: Retargeting audiences who viewed products or added products to cart but didn't purchase products. 
- `LAB2`: Retargeting audiences who added products to cart but didn't purchase products. 
- `LAB3`: Retargeting audiences using custom combination. 
- `OFF`: No retargeting.  |
##| shopping_ads_retargeting_actions_days | number | The valid time range for the specified audience action. Audiences who have completed the specified action within the time range will be retargeted by the shopping ads. 

Value range: 1, 2, 3, 7, 14, 30, 60, 90, 180. |
##| included_custom_actions | object[] | The custom action that you want to use as "Include" conditions for filtering out the shopping ads audiences to be retargeted. |
###| code | string | The custom action used to filter out the audiences to be retargeted. Enum values: 
- `VIEW_PRODUCT`: The audience viewed the product. 
- `ADD_TO_CART`: The audience added the product to the cart. 
- `PURCHASE`: The audience purchased the product. |
###| days | integer | The time range used to filter out the audiences that completed the specified action. Value range: [1,180]. |
##| excluded_custom_actions | object[] | The custom action that you want to use as "Exclude" conditions for filtering out the shopping ads audiences to be retargeted. |
###| code | string | The custom action used to filter out the audiences to be retargeted. Enum values: 
- `VIEW_PRODUCT`: The audience viewed the product. 
- `ADD_TO_CART`: The audience added the product to the cart. 
- `PURCHASE`: The audience purchased the product. |
###| days | integer | The time range used to filter out the audiences that didn't complete the specified action. Value range: [1,180]. |
##| shopping_ads_retargeting_custom_audience_relation | string | The logical relation between the Video Shopping Ads (VSA) retargeting audience specified by `shopping_ads_retargeting_type` and the custom audience specified by `audience_ids`.

Enum values: 
- `OR`: To combine the VSA retargeting audience and the custom audience to create the targeted audience. The targeted audience will consist of individuals who belong to either the VSA retargeting audience or the custom audience. 
- `AND`: To intersect between the VSA retargeting audience and the custom audience to create the targeted audience. The targeted audience will consist of individuals who belong to both the VSA retargeting audience and the custom audience. |
##|location_ids |string[]|IDs of the targeted locations. |
##| zipcode_ids|string[]|Zip code IDs or postal code IDs of the targeted locations. 
**Note**:
-  Zip code targeting is currently only supported for the US and postal code targeting is currently only supported for Canada, Brazil, Indonesia, Thailand, and Vietnam. 
-  To get information about zip code IDs or postal code IDs, you can only use [/tool/targeting/info/](https://ads.tiktok.com/marketing_api/docs?id=1761237001980929).|
##|languages |string[]|Codes of the languages that you want to target. For the list of languages codes supported, see [Enumeration - Language Code](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
##|gender |string|Gender that you want to target. Enum values: `GENDER_FEMALE`,`GENDER_MALE`,`GENDER_UNLIMITED`|
##|age_groups |string[]|Age groups you want to target. For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
##|spending_power|string|Spending power that you want to target. Enum values: `ALL`, `HIGH`.   If it is set to `HIGH`, you can target high spending users who typically spend more on purchases on TikTok ads than average users.|
##|household_income| string[]| Household income that you want to target. Enum values: `TOP5`(Top 5% of ZIP codes), `TOP10`(Top 10% of ZIP codes), `TOP10_25`(Top 10% -25% of ZIP codes), `TOP25_50`(Top 25% - 50% of ZIP codes).  |
##|audience_ids|string[]|A list of audience IDs. |
##| smart_audience_enabled | boolean | Whether Smart audience is turned on. 

Enum values: `true`, `false`. 

To learn more about Smart audience and how to turn on Smart audience, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
##|excluded_audience_ids |string[]|A list of excluded audience ID.|
##|interest_category_ids |string[]|IDs of general interest keywords that you want to use to target audiences. |
##|interest_keyword_ids|string[]|IDs of additional interest keywords that you want to use to target audiences. |
##|purchase_intention_keyword_ids|string[]|IDs of purchase intention categories that you want to use to target audiences with an interest in purchases related to a content category. |
##|actions| object[] | A list of targeting behavioral category objects.|
###|action_scene | string | The type of user behavior that you want to target.

 Enum values: 
- `VIDEO_RELATED`: Video interactions.
- `CREATOR_RELATED`: Creator interactions.
- `HASHTAG_RELATED`: Hashtag interactions.|
###|action_period |number| The time period to include behaviors from.  |
###|video_user_actions|string[]| The specific user interactions that you want to target for the user behavior type.

- If `action_scene` is `VIDEO_RELATED`, the allowed values are: `WATCHED_TO_END`,`LIKED`,`COMMENTED`,`SHARED`.
-  If `action_scene` is `CREATOR_RELATED`, the allowed values are: `FOLLOWING`, `VIEW_HOMEPAGE`. 
- If `action_scene` is `HASHTAG_RELATED`, the allowed value is `VIEW_HASHTAG`. |
###|action_category_ids |string[]|IDs of the video interactions categories, creator interactions categories, hashtags, or hashtag bundles that you want to use to target audiences.|
##| smart_interest_behavior_enabled | boolean | Whether Smart interests & behaviors is turned on. 

Enum values: `true`, `false`. 

To learn more about Smart interests & behaviors and how to turn on Smart interests & behaviors, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
##|included_pangle_audience_package_ids |string[]| IDs of the Pangle audiences that you want to include. Valid only for Pangle placement. You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://ads.tiktok.com/marketing_api/docs?id=1740040177229826) endpoint. You need to set `bind_type` to `INCLUDE`.  Do not specify this field and `excluded_pangle_audience_package_ids` at the same time.|
##|excluded_pangle_audience_package_ids |string[]| IDs of the Pangle audiences that you want to exclude. Valid only for Pangle placement. You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://ads.tiktok.com/marketing_api/docs?id=1740040177229826) endpoint. You need to set `bind_type` to `EXCLUDE`. Do not specify this field and `included_pangle_audience_package_ids` at the same time.|
##|operating_systems |string[]|Device operating systems that you want to target. Only one value is allowed.  Enum: `ANDROID`, `IOS`|
##|min_android_version|string|Minimum Android version. For enum values, see [Enumeration - Minimum Android Version](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
##|ios14_targeting|string|The iOS devices that you want to target. 

Enum values:
- `UNSET`: Devices with iOS 14.4 or earlier versions. 
- `IOS14_MINUS`: Devices with iOS 14.0 or earlier versions, which are not affected by the iOS 14 privacy update. 
- `IOS14_PLUS`: Devices with iOS 14.5 or later versions. The iOS 14 privacy update has been enforced in this group of devices. This value is only supported for Dedicated Campaigns. 
- `ALL`:  Devices with iOS 14.5 or later versions. The iOS 14 privacy update has been enforced in this group of devices. This value is only supported for iOS App Retargeting ads and iOS retargeting Video Shopping Ads with product source as catalog and optimization location as App.  |
##|min_ios_version|string|Audience minimum ios version. For enum values, see [Enumeration - Minimum iOS Version](https://ads.tiktok.com/marketing_api/docs?id=1738308662898689).|
##|ios14_quota_type|string|Whether the campaign will be counted against the iOS 14 dedicated campaign quota. Enum: `OCCUPIED`, `UNOCCUPIED`. For non-R&F campaigns, when `ios14_targeting` is `IOS14_PLUS`, this field is automatically set to `OCCUPIED`.|
##|device_model_ids| string[]| List of device model IDs. For more details about device models, see [Device Models](https://ads.tiktok.com/marketing_api/docs?id=1737172880570369).|
##|network_types |string[]|Network types that you want to target. For enum values, see [Enumeration - Connection Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
##|carrier_ids |string[]| Carriers  that you want to target. A carrier is valid only when the `in_use` field for the carrier is `true`. For detailed information, see [get carriers](https://ads.tiktok.com/marketing_api/docs?id=1737168013095938). |
##| isp_ids | string[] |IDs of the targeted Internet service providers. |
##|device_price_ranges|number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50. 
**Important**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].|
##|targeting_expansion{-To be deprecated}| object | Settings about targeting expansion.

**Note**:  Starting June, 2024, you can no longer enable Automatic targeting or Targeting expansion for your ad groups. To ensure a smooth API integration, we recommend you migrate to [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586). |
###|expansion_enabled|boolean| Whether to enable targeting expansion. |
###|expansion_types |string[]| The target audience types that you want to expand.|
##|saved_audience_id|string|Returned when you have specified `saved_audience_id` when creating an ad group. 
Saved Audience ID.|
##|contextual_tag_ids |string[]|Contextual tag IDs. See [Contextual targeting](https://ads.tiktok.com/marketing_api/docs?id=1745292519923713)  to learn more about how to use contextual targeting.|
##|brand_safety_type|string|Brand safety type. Enum values: 
- `NO_BRAND_SAFETY`:  To not use any brand safety solution.  Full inventory, which means your ads may appear next to some content featuring mature themes.
- `EXPANDED_INVENTORY`: Use TikTok's brand safety solution. Expanded inventory means that your ads will appear next to content where most inappropriate content has been removed, and that does not contain mature themes. In the next API version, `EXPANDED_INVENTORY` will replace `NO_BRAND_SAFETY` and will be the default brand safety option. 
- `STANDARD_INVENTORY`: Use TikTok's brand safety solution. Standard inventory means that ads will appear next to content that is appropriate for most brands. 
- `LIMITED_INVENTORY`: Use TikTok's brand safety solution. Limited inventory means that your ads will not appear next to content that contains mature themes.
- `THIRD_PARTY`: Use a third-party brand safety solution. To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. 
**Note**: 
-  Pre-bid first-party Brand Safety filtering for `APP_PROMOTION`,  `WEB_CONVERSIONS`, `TRAFFIC`,  `LEAD_GENERATION` and `PRODUCT_SALES` objectives in Auction ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. 
-  Pre-bid third-party brand safety solutions are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. |
##|brand_safety_partner|string| Brand safety partner. Available only when `brand_safety_type` is `THIRD_PARTY`. Enum values: `IAS`, `OPEN_SLATE`(The partner is named **DoubleVerify** on TikTok Ads Manager because the partner has been acquired by DoubleVerify). 
To get the countries and regions that your ads can be deployed to based on your brand safety settings, use the [/tool/region/](https://ads.tiktok.com/marketing_api/docs?id=1737189539571713) endpoint. You need to pass in the brand safety type and brand safety partner.
**Note**: 
-  Pre-bid third-party brand safety solutions are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. |
##|inventory_filter_enabled|boolean|Inventory filtering (filtering security videos, hides unsafe videos), valid only for the `PLACEMENT_TIKTOK` placement. Optional values are: true to filter, false not to filter. |
##|category_exclusion_ids|string[]|Content exclusion category IDs.|
##|vertical_sensitivity_id|string|Vertical sensitivity category ID.  |
##|budget_mode |string|Budget mode. If Campaign Budget Optimization is enabled, `BUDGET_MODE_INFINITE` will be returned. For more information about budget modes, see [Budget](https://ads.tiktok.com/marketing_api/docs?id=1739381246298114). |
##|budget |float|Ad group budget. 

Returns 0.0 when Campaign Budget Optimization (`budget_optimize_on`) is on.

 For TopView ad groups, this field represents the estimated ad group budget after applying any discount.|
##|scheduled_budget|float|Scheduled ad budget for next day. A value not equal to 0 means the scheduled budget is set and the value represents the budget; a value equals to 0 means the scheduled budget is not set.|
##|schedule_type |string|The schedule type can be either `SCHEDULE_START_END` or `SCHEDULE_FROM_NOW`. If you choose `SCHEDULE_START_END`, you need to specify a start time and an end time. If you choose `SCHEDULE_FROM_NOW`, you only need to specify a start time.|
##|schedule_start_time |datetime|Ad delivery start time (UTC+0), in the format of `YYYY-MM-DD HH:MM:SS`.|
##|schedule_end_time |datetime|Ad delivery end time (UTC+0), in the format of `YYYY-MM-DD HH:MM:SS`.|
##| predict_impression | number | Returned only for TopView ads. 

The estimated number of impressions counted in thousands.

For example, a value of `1291` represents an estimated 1,291,000 impressions. |
##| topview_reach_range | number[] | Returned only for TopView ads. 

 The estimated range of reach counted in thousands. 

For example, a value of `[342, 456]` represents an estimated reach of between 342,000 and 456,000 individuals. 

To determine the estimated frequency range, use the following formula: 
- frequency = impressions /reachFor example, if `predict_impression` is `1291` (representing 1,291,000) and `topview_reach_range` is `[342, 456]` (representing 342,000 to 456,000), the estimated frequency range will be 2.8 to 3.8. |
##| pre_discount_cpm | number | Returned only for TopView ads. 

The estimated cost per mille (CPM) before applying any budget discount. 

Example: 11.33. |
##| cpm | number | Returned only for TopView ads.

The estimated cost per mille (CPM) after applying any budget discount. 

Example: 0. |
##| discount_type | string | Returned only for TopView ads.

The type of discount applied to the budget. 

 Enum values: 
- `NO_DISCOUNT`: No discount applied.
-  `BY_PERCENTAGE`: Discount applied as a percentage.
- `BY_AMOUNT`: Discount applied as a fixed amount. |
##| discount_amount | number | Returned only for TopView ads when `discount_type` is `BY_AMOUNT`.

The fixed amount by which the budget is discounted.

Example: 14615.8. |
##| discount_percentage | number | Returned only for TopView ads when `discount_type` is `BY_PERCENTAGE`. 

The percentage by which the budget is discounted. |
##| pre_discount_budget | number | Returned only for TopView ads.

The budget amount before applying any discount. 

 Example: 14616. |
##|schedule_infos |object[]| Ad delivery information of R&F ad groups. |
###|schedules |object[]| The details of the scheduled delivery for the ad. |
####|start_time |string| Ad delivery start time. |
####|end_time |string| Ad delivery end time. |
###|expected_orders |number[]| The delivery order for an ad within the ad group. 

For example, a value of `[1]` indicates that the ad will be delivered first.|
###|is_draft |boolean| Whether the ad delivery information is in draft mode.

If the value of this field is `true`, then the ad delivery information defined in `schedule_infos` has not been associated with any specific ads. 

To associate the ad delivery information with ads, pass the value of the returned `schedule_id` to the request parameter `schedule_id` in [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). After you associate the ad delivery information with an ad, the value of this field will automatically be set to `false`, and the value of `schedule_id` will be the ID of the ad that you have associated the ad delivery information with. |
###|schedule_id |string| Schedule ID. 

You can associate a schedule ID with an ad through the `schedule_id` in the request of [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). After you associate the `schedule_id` with an ad, the value of this field will set to the ID of the ad that you have associated the ad delivery information with, and `is_draft` will automatically be set to `false`.  |
##|delivery_mode |string|  The strategy for sequencing and scheduling your ad delivery in a Reach & Frequency ad group. 

Enum values:
- `STANDARD`: Standard delivery. Your ads will be distributed evenly and are expected to achieve similar traffic size. 
- `SCHEDULE`: Scheduled delivery.  Set specific time periods to deliver each ad in. 
- `SEQUENCE`: Sequenced delivery. Set a specific sequence to deliver your ads in. 
- `OPTIMIZE`: Optimized delivery that delivers ads to achieve the best performance.|
##|dayparting |string|"Ad delivery arrangement, in the format of a string that consists of 48 x 7 characters. Each character is mapped to a 30-minute timeframe from Monday to Sunday. Each character can be set to either 0 or 1.  1 represents delivery in the 30-minute timeframe, and 0 stands for non-delivery in the 30-minute timeframe. The first character is mapped to 0:01-0:30 of Monday; The second character is mapped to 0:31-1:00 of Monday, and the last character represents 23:31-0:00 Sunday.**Note**
Not specified, all-0, or all-1 are considered as full-time delivery. 
|
##|optimization_goal|string|The measurable results that you'd like to drive your ads with. For enum values, see [Enumeration - Optimization Goal](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
##|secondary_optimization_event|string|The secondary goal when `optimization_goal` is `INSTALL` or `VALUE`. For enum values, see [Conversion events - Secondary-goal events](https://ads.tiktok.com/marketing_api/docs?id=1739361474981889).|
##| message_event_set_id | string | The ID of the message event set to use in the Instant Messaging Ad Group. |
##|frequency |number| Frequency, together with `frequency_schedule`, controls how often people see your ad (only available for `REACH` ads). 
The below conditions should be both met:
- 1  Optional values include: `SIX_SECONDS` (video playback 6 seconds) and ` TWO_SECONDS` (video playback 2 seconds) |
##|next_day_retention | float | Day 2 retention ratio. Formula: `next_day_retention` = `conversion_bid_price`/`deep_cpa_bid`. Value range is (0,1]. Only valid when `placements` is `PLACEMENT_PANGLE` and `secondary_optimization_event` is `NEXT_DAY_OPEN`. |
##| click_attribution_window | string | Click-through window for the ad group. This attribution window is the time between when a person clicks your ad and then takes an action. 

Enum values: 
- `OFF`: Off. 
-  `ONE_DAY`: 1-day click.
- `SEVEN_DAYS`: 7-day click. 
- `FOURTEEN_DAYS`: 14-day click.
-  `TWENTY_EIGHT_DAYS`: 28-day click. |
##| engaged_view_attribution_window | string | Engaged view-through window for the ad group. This attribution window is the time after someone watches at least 6 seconds of your video ad that a conversion is counted.

Enum values: 
- `ONE_DAY`: 1-day engaged view.
- `SEVEN_DAYS`: 7-day engaged view.|
##| view_attribution_window | string | View-through window for the ad group. This attribution window is the time between when a person views your ad and then takes an action. 

Enum values: 
- `OFF`: Off.
- `ONE_DAY`: 1-day view.
- `SEVEN_DAYS`: 7-day view.|
##| attribution_event_count | string | Event count (Statistic type) for the ad group. 
The way that people's actions are counted after only viewing or clicking an ad. 

Enum values: 
- `UNSET`: Unset. 
-  `EVERY`: Every. To count multiple events from someone as separate conversions. 
-  `ONCE`: Once. To count multiple events from someone as 1 conversion.|
##|billing_event |string| Billing event. 
To learn about the enum values, see [Enumerations - Billing Event](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Billing%20Event).|
##|pacing |string| You can choose between `PACING_MODE_SMOOTH` and `PACING_MODE_FAST`. For `PACING_MODE_SMOOTH`, the budget is allocated evenly within the scheduled time. `PACING_MODE_FAST` would consume budget and produce results as soon as possible. When Campaign Budget Optimization (`budget_optimize_on`) is on, your setting will be ignored and it will be set as `PACING_MODE_SMOOTH`. Otherwise, this field is required. |
##|operation_status |string|Operation status.

Enum values:
- `ENABLE` : The ad group is enabled (in 'ON' status).
- `DISABLE`: The ad group is disabled (in 'OFF' status). 
- `FROZEN`: The ad group is terminated and cannot be enabled. |
##|secondary_status |string|Ad group status（secondary status). For enum values, see [Enumeration - Ad Group Status - Secondary Status](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
Note**: This field is not returned in the sandbox environment because the ad group is not actually delivered.|
##|statistic_type |string| Conversion bid statistic type, bid for `EVERYTIME` (Each Purchase)/ `NONE` (Unique Purchase)|
##|is_hfss |boolean|Whether the promoted content is HFSS (High Fat, Salt, Sugar) Product/Brand.

Supported values: `true`,`false`. |
##| is_lhf_compliance | boolean | Whether the promoted content complies with LHF (Less Healthy Foods) regulations.

When `is_lhf_compliance` is `true`, you confirm that any food or drink products you advertise on TikTok in the UK comply with the [2024 Less Healthy Foods Regulations](https://www.legislation.gov.uk/uksi/2024/1266/made) and all other applicable laws.

Supported values: `true`,`false`. |
##|creative_material_mode |string|The strategy that your creatives will be delivered. 

Enum values: `CUSTOM`(custom), `DYNAMIC`(Automated Creative Optimization), and `SMART_CREATIVE`(Smart Creative). 

For Upgraded Smart+ Ad Groups, this field will be null.|
##|adgroup_app_profile_page_state|string| Indicates whether the adgroup is using app profile page. Enum: `INVALID`, `UNSET`, `ON`, `OFF`.|
##|feed_type |string| Feed type option. Enum values: `STANDARD_FEED`, `TOP_FEED`.  |
##| rf_purchased_type  | string | Billing method of Reach & Frequency ad groups. For more details, see [Enumeration - Reach & Frequency Buy Type](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138). 
**Note**: For non-Reach & Frequency ads, the value of this field will always be null.|
##| purchased_impression | number | Impressions to be purchased. 
**Note**: For non-Reach & Frequency ads, the value of this field will always be null.|
##| purchased_reach  | number | Purchased user reach. 
**Note**: For non-Reach & Frequency ads, the value of this field will always be null. |
##| rf_estimated_cpr | number |  The estimated cost per mile reach. 
**Note**: For non-Reach & Frequency ads, the value of this field will always be null.|
##| rf_estimated_frequency | number | The estimated show frequency. 
**Note**: For non-Reach & Frequency ads, the value of this field will always be null.|
##| split_test_group_id | string | Split test group ID. Returned if the ad group is part of a split test. |
##| split_test_status | string | Split test status. Returned if the ad group is part of a split test. |
##|is_new_structure|boolean|Whether the campaign is a new structure |
##|skip_learning_phase |boolean|Whether to skip the learning stage. |
##|conversion_window (deprecated) |string| The time frame when you would like a conversion to happen after a user clicks on or views your ad. Your ad delivery will be optimized using the conversion data during the time frame you select. This setting will not impact your attribution data. For enum values, ee [Enumeration - Conversion Window](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138).|
#|page_info |object|Paging information |
##|page |number|current page number |
##|page_size |number|Paging Size |
##|total_number |number|Total, the total number of eligible ad groups |
##|total_page |number|total pages |
```

### Example

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "list": [
            {
                "budget_mode": "BUDGET_MODE_TOTAL",
                "included_custom_actions": [],
                "delivery_mode": null,
                "auto_targeting_enabled": false,
                "app_download_url": null,
                "placements": [
                    "PLACEMENT_TIKTOK"
                ],
                "pixel_id": null,
                "conversion_window": null,
                "schedule_type": "SCHEDULE_START_END",
                "brand_safety_partner": null,
                "interest_category_ids": [],
                "adgroup_id": "{{adgroup_id}}",
                "campaign_name": "{{campaign_name}}",
                "schedule_infos": null,
                "share_disabled": false,
                "brand_safety_type": "NO_BRAND_SAFETY",
                "campaign_id": "{{campaign_id}}",
                "ios14_quota_type": "UNOCCUPIED",
                "network_types": [],
                "app_type": null,
                "bid_type": "BID_TYPE_NO_BID",
                "conversion_bid_price": 0,
                "optimization_goal": "CLICK",
                "deep_bid_type": null,
                "video_download_disabled": false,
                "schedule_end_time": "{{schedule_end_time}}",
                "scheduled_budget": 0,
                "is_hfss": false,
                "frequency": null,
                "bid_price": 0,
                "actions": [],
                "deep_cpa_bid": 0,
                "adgroup_name": "{{adgroup_name}}",
                "category_id": "0",
                "purchased_impression": null,
                "budget": {{budget}},
                "app_id": null,
                "promotion_type": "WEBSITE",
                "age_groups": null,
                "next_day_retention": null,
                "pacing": "PACING_MODE_SMOOTH",
                "device_price_ranges": null,
                "location_ids": [
                    "{{location_id}}"
                ],
                "secondary_status": "ADGROUP_STATUS_CREATE",
                "billing_event": "CPC",
                "advertiser_id": "{{advertiser_id}}",
                "create_time": "{{create_time}}",
                "operation_status": "ENABLE",
                "placement_type": "PLACEMENT_TYPE_NORMAL",
                "optimization_event": null,
                "audience_ids": [],
                "secondary_optimization_event": null,
                "excluded_custom_actions": [],
                "languages": [],
                "modify_time": "{{modify_time}}",
                "excluded_audience_ids": [],
                "rf_estimated_cpr": null,
                "skip_learning_phase": false,
                "operating_systems": [
                    "ANDROID"
                ],
                "creative_material_mode": "CUSTOM",
                "search_result_enabled": false,
                "rf_purchased_type": null,
                "inventory_filter_enabled": false,
                "adgroup_app_profile_page_state": null,
                "rf_estimated_frequency": null,
                "gender": "GENDER_UNLIMITED",
                "statistic_type": null,
                "purchased_reach": null,
                "is_new_structure": true,
                "interest_keyword_ids": [],
                "bid_display_mode": "CPMV",
                "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
                "keywords": null,
                "schedule_start_time": "{{schedule_start_time}}",
                "comment_disabled": false,
                "frequency_schedule": null,
                "feed_type": null
            },
            {
                "budget_mode": "BUDGET_MODE_TOTAL",
                "included_custom_actions": [],
                "delivery_mode": null,
                "auto_targeting_enabled": false,
                "app_download_url": null,
                "placements": [
                    "PLACEMENT_TIKTOK"
                ],
                "pixel_id": null,
                "conversion_window": null,
                "schedule_type": "SCHEDULE_START_END",
                "brand_safety_partner": null,
                "interest_category_ids": [],
                "adgroup_id": "{{adgroup_id}}",
                "campaign_name": "{{campaign_name}}",
                "schedule_infos": null,
                "share_disabled": false,
                "brand_safety_type": "NO_BRAND_SAFETY",
                "campaign_id": "{{campaign_id}}",
                "ios14_quota_type": "UNOCCUPIED",
                "network_types": [],
                "app_type": null,
                "bid_type": "BID_TYPE_NO_BID",
                "conversion_bid_price": 0,
                "optimization_goal": "CLICK",
                "deep_bid_type": null,
                "video_download_disabled": false,
                "schedule_end_time": "{{schedule_end_time}}",
                "scheduled_budget": 0,
                "is_hfss": false,
                "frequency": null,
                "bid_price": 0,
                "actions": [],
                "deep_cpa_bid": 0,
                "adgroup_name": "{{adgroup_name}}",
                "category_id": "0",
                "purchased_impression": null,
                "budget": {{budget}},
                "app_id": null,
                "promotion_type": "WEBSITE",
                "age_groups": null,
                "next_day_retention": null,
                "pacing": "PACING_MODE_SMOOTH",
                "device_price_ranges": null,
                "location_ids": [
                    "{{location_id}}"
                ],
                "secondary_status": "ADGROUP_STATUS_CREATE",
                "billing_event": "CPC",
                "advertiser_id": "{{advertiser_id}}",
                "create_time": "{{create_time}}",
                "operation_status": "ENABLE",
                "placement_type": "PLACEMENT_TYPE_NORMAL",
                "optimization_event": null,
                "audience_ids": [],
                "secondary_optimization_event": null,
                "excluded_custom_actions": [],
                "languages": [],
                "modify_time": "{{modify_time}}",
                "excluded_audience_ids": [],
                "rf_estimated_cpr": null,
                "skip_learning_phase": false,
                "operating_systems": [
                    "ANDROID"
                ],
                "creative_material_mode": "CUSTOM",
                "search_result_enabled": false,
                "rf_purchased_type": null,
                "inventory_filter_enabled": false,
                "adgroup_app_profile_page_state": null,
                "rf_estimated_frequency": null,
                "gender": "GENDER_UNLIMITED",
                "statistic_type": null,
                "purchased_reach": null,
                "is_new_structure": true,
                "interest_keyword_ids": [],
                "bid_display_mode": "CPMV",
                "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
                "keywords": null,
                "schedule_start_time": "{{schedule_start_time}}",
                "comment_disabled": false,
                "frequency_schedule": null,
                "feed_type": null
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 10,
            "total_page": 1,
            "total_number": 2
        }
    }
}
(/code);
```
