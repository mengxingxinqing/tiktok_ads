# Get products

**Doc ID**: 1740564136678402
**Path**: API Reference/Catalog Products/Get products

---

Use this endpoint to get the list of products in your product catalog. 

You can filter the products you want to get by specifying product IDs, SKU IDs, product set IDs or by using custom conditions (`conditions`). You can also order the results by product availability or custom conditions. 

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path| /v1.2/catalog/product/get/| /v1.3/catalog/product/get/|
|Request parameter data type |`bc_id`: number
`catalog_id`: number|`bc_id`: string
 `catalog_id`: string |
|Request parameter name and data type | `products`: number[]  
`product_sets`: number[] 
`sens_type`: string|`product_ids`: string[] 
`product_set_ids`: string[] 
`case_sensitive`: boolean|
|Response parameter name|`image_link`
 `video_link`
`additional_image_link` 
`gtin`
`mpn`
`product_type` 
`landing_url`
 `link`
`ext`|`image_url`
`video_url`
`additional_image_urls`
`global_trade_item_number`
`manufacturer_part_number`
`product_category`
`landing_page`
`landing_page_url`
`extra_info`|
|New response parameters |/|For E-commerce catalogs: 
`ad_creation_eligible`
 For hotel catalogs: 
`hotel_id`
`name`
`hotel_retailer_id`
 `address`
`postal_code` 
`latitude` 
`longitude` 
`margin_level` 
`loyalty_program` 
`guest_ratings`
`star_rating` 
 `room_type`
`hotel_category`
`neighborhood`
 `priority` 
 `internal_label_0`
 `internal_label_1`
 For flight catalogs:
`flight_id`
 `origin_airport`
`destination_airport` 
`origin_city`
`destination_city`
 `cabin_class`
`airline_company`
`priority`
For destination catalogs:
`destination_id` 
`destination_name`
`address`
`postal_code`
`latitude`
`longitude`
`types`
`neighborhood`
For entertainment catalogs:
`media_title_id` 
`star_rating`
`timeline`
`category`
`genres`
`qid`
For Auto-Inventory catalogs
`vehicle_id`
`address`
`latitude` 
`longitude`
`state_of_vehicle` 
`vehicle_type`
`make`
`model` 
`trim`
`year`
`vin` 
`mileage`
`body_style`
`exterior_color`
 `interior_color`
`transmission`
`drivetrain`
`fuel_type`
`dealer`
`date_first_on_lot`
`days_on_lot`
`offer_type`
`term_length` 
`offer_term_qualifier` 
`amount_price`
`amount_percentage`
`amount_qualifier`
 `downpayment`
`downpayment_qualifier`
 `offer_disclaimer`
`offer_disclaimer_url` 
`emission_disclaimer`
`emission_disclaimer_url`
`emission_overlay_disclaimer`
`emission_image_link`
`video_url`
For Auto-Model catalogs:
`vehicle_id`
`make`
 `model`
`trim`
`year`
 `exterior_color`
`offer_type`
`term_length` 
`offer_term_qualifier` 
`amount_price`
`amount_percentage` 
`amount_qualifier`
`downpayment`
`downpayment_qualifier`
`offer_disclaimer`
`offer_disclaimer_url`
`emission_disclaimer`
`emission_disclaimer_url`
`emission_overlay_disclaimer`
`emission_image_link`
`video_url`
 For mini series catalogs: 
`series_id`
`series_name` 
`type`
`purchase_unit`
`cost` 
`company_type`
 `copyright_holder_name`
`app_id`
`minis_id` 
`total_episodes`
`initial_paid_episodes`
 `per_episode_duration`
`spoken_language`
 `subtitle_language`
`production_type`
`target_audience`
`characters`
`genres`
`historical_context`
`actors`
` target_config`
`additional_product_list`
`video_url`|
```
## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/catalog/product/get/

**Method** GET

**Header**

``` xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request content type. 
Accepted Value: `"application/json"` . |
```

**Parameters**

``` xtable
| Field{35%} | Type{15%} | Description{50%} |
|--- |--- |--- |
| bc_id {Required} | string | Business Center ID. |
| catalog_id {Required} | string | Catalog ID. |
| page | number | Current page number.

**Note**: Only 100,000 results can be returned at most. You need to ensure that `page` multiplied by `page_size` is no more than 100,000. |
| page_size | number | Page size. Default is 10. The maximum supported size is 500.|
| product_ids | string[] | IDs of the products that you want to get. You can specify up to 1,000 product IDs. 
**Note**:  
- `product_ids` and `sku_ids` cannot be specified at the same time. 
- For mini series catalogs, the only supported filter is `product_ids`.|
|sku_ids| string[]| IDs of the SKUs that you want to get information for. Max size: 1000.
Length limit: 100 characters for each SKU ID and cannot contain emojis.
**Note**:
- Duplicate SKU IDs are not supported. 
- `product_ids` and `sku_ids` cannot be specified at the same time.|
|product_set_ids|string[]| IDs of the product sets that you want to get. Max size: 100.|
|order|object|Ordering settings. When `product_ids` or `sku_ids` is specified, this field will be ignored.|
#|order_condition|string| Order-by condition. Currently, the only supported value is `PRODUCT_AVAILABILITY`. Do not pass in this field and `custom_order` at the same time. |
#|custom_order|object[]|Custom ordering / sorting conditions. Do not pass in this field and `order_condition` at the same time.|
##|field|string|Data field that you want to order your products by. For supported ordering-by fields, see the Supported fields section below.|
##|type|string|Ordering / sorting type. Enum values: `ASC` (ascending order), `DES` (descending).|
|conditions|object|Filtering conditions. When you specify a filtering condition, all data fields in this object are required except `case_senstive`. When `product_ids` or `sku_ids` is specified, this field will be ignored.|
#|and / or| object[]| Logic operator for the conditions. Either `and` or `or`.|
##|field|string| Data field to filter by. For the supported fields, see the [Supported fields](#item-link-Supported fields) section below.|
##|operator|string|Filter operator. Enum values: `EQ`, `NE`, `GT`, `GTE`,  `LT`,  `LTE`,  `RNG`,  `WILDCARD`, `NOT_WILDCARD`,  `PREFIX`, `EXIST`, `IN`,  `NOT_IN`.|
##|values|string[]| Filter values. Multiple values are allowed when `operator` is `RNG`, `IN`, or `NOT_IN`.|
##|case_senstive|boolean|Whether it is case-sensitive.|
```

### Supported fields
#### For E-commerce catalog products
```xtable
|Data Field{30%}| Supports ordering-by?{20%}| Can be used as `field` under `conditions`?{30%}|Case-sensitive?{20%}|
|---|---|---|---|
|sku_id|Yes|Yes|No|
|product_id|Yes|Yes|Yes|
|audit_status|No|Yes|Yes|
|title|Yes|Yes|No|
|description|Yes|Yes|No|
|brand|Yes|Yes|No|
|item_group_id|Yes|Yes|No|
|google_product_category|Yes|Yes|No|
|price_info|Yes|Yes|Yes|
|sale_price|Yes|Yes|Yes|
|sale_price_effective_start_date|Yes|Yes|Yes|
|sale_price_effective_end_date|Yes|Yes|Yes|
|condition|No|Yes|Yes|
|age_group|No|Yes|Yes|
|color|Yes|Yes|No|
|gender|No|Yes|Yes|
|size|Yes|Yes|No|
|material|Yes|Yes|No|
|pattern|Yes|Yes|No|
|product_category|Yes|Yes|No|
|custom_label_0|Yes|Yes|No|
|custom_label_1|Yes|Yes|No|
|custom_label_2|Yes|Yes|No|
|custom_label_3|Yes|Yes|No|
|custom_label_4|Yes|Yes|No|
|active_status|No|Yes|Yes|
```

#### For flight catalog products

```xtable
|Data Field{30%}| Supports ordering-by?{20%}| Can be used as `field` under `conditions`?{30%}|Case-sensitive?{20%}|
|---|---|---|---|
| flight_id | Yes | Yes | No |
| origin_airport | Yes | Yes | No |
| destination_airport | Yes | Yes | No |
| origin_city | Yes | Yes | No |
| destination_city | Yes | Yes | No |
| description | Yes | Yes | Yes |
| cabin_class | Yes | Yes | No |
| airline_company | Yes | Yes | No |
| price | Yes | Yes | No |
| custom_label_0 | Yes | Yes | No |
| custom_label_1 | Yes | Yes | No |
| custom_label_2 | Yes | Yes | No |
| custom_label_3 | Yes | Yes | No |
| custom_label_4 | Yes | Yes | No |
```

#### For entertainment catalog products

```xtable
| Data Field {30%}| Can be used as `field` under `conditions`?{70%} |
|---|---|
| media_title_id | Yes |
| product_id | Yes |
| audit_status | Yes |
| title | Yes |
| description | Yes |
| availability | Yes |
| timeline | Yes |
| genres | Yes |
```
#### For Auto-Inventory catalog products

```xtable
|Data Field{30%}| Supports ordering-by?{20%}| Can be used as `field` under `conditions`?{30%}|Case-sensitive?{20%}|
|---|---|---|---|
| vehicle_id | Yes | Yes | Yes |
| title | Yes | Yes | Yes |
| description | Yes | Yes | Yes |
| availability | No | Yes | No |
| condition | No | Yes | No |
| state_of_vehicle | No | Yes | No |
| make | Yes | Yes | Yes |
| model | Yes | Yes | Yes |
| trim | Yes | Yes | Yes |
| year | Yes | Yes | No |
| vin | Yes | Yes | Yes |
| mileage | Yes | Yes | No |
| body_style | No | Yes | No |
| drivetrain | No | Yes | No |
| fuel_type | No | Yes | No |
| city | Yes | No | Yes |
```

#### For Auto-Model catalog products

```xtable
|Data Field{30%}| Supports ordering-by?{20%}| Can be used as `field` under `conditions`?{30%}|Case-sensitive?{20%}|
|---|---|---|---|
| vehicle_id | Yes | Yes | Yes |
| title | Yes | Yes | Yes |
| make | Yes | Yes | Yes |
| model | Yes | Yes | Yes |
| year | Yes | Yes | Yes |
| trim | Yes | Yes | Yes |
```

### Example
```xcodeblock

(code cURL http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/catalog/product/get/' \
--header 'Access-Token: xxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bc_id": 123456,
    "catalog_id": 123456
}'
(/code);
```

## Response

``` xtable
| Field | Type | Description |
|--- |--- |--- |
| code | number  |Return code, see [Appendix - Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
|message |string|Return message, see [Appendix-Return message](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
| request_id | string | The log id of a request, which uniquely identifies the request. |
|data |object | Returned data. |
#| list | object[] | Product list. |
##|audit|object| Audit information.|
###|audit_status|string| Ad audit status. It indicates if the ad promoting the product can be deployed. 

Enum values: `approved`, `rejected`, `processing`.|
###|rejected_info|object[]|Returned only when `audit_status` is `rejected`.

List of rejection reasons.  |
####|reason|string| Rejection reason.|
####|suggestion|string| Suggestions about how to revise to be approved.|
####|affected_placement|string[]| List of placements affected by the rejection.|
####|affected_country|string[]|List of countries or regions affected by the rejection.|
##| ad_creation_eligible | string | Returned only for E-commerce catalog products. 

Whether the E-commerce catalog product can be used to create ads. 

Enum values: `AVAILABLE`, `NOT_AVAILABLE`.

The `ad_creation_eligible` of an E-commerce catalog product will be `AVAILABLE` only when the following conditions are met: 
- `audit_status` is `approved`. 
-  `active_status` is `ACTIVATED`. 
-  `availability` is `IN_STOCK`, `AVAILABLE_FOR_ORDER`, or `PREORDER`. |
##|active_status|string|Whether the product is activated. 

Enum values: `ACTIVATED`, `DEACTIVATED`. 

This field represents the advertiser-controlled online or offline status of the product. However, it does not necessarily imply that the product can be used to create ads.|
##| sku_id | string | Advertiser-defined product ID.|
##| product_id | string | Product ID. |
##| title | string | Product title. |
##| description | string | Product description. |
##| availability | string | Inventory status. 

- For E-commerce catalog products, the enum values are: `IN_STOCK`: in stock. 
- `AVAILABLE_FOR_ORDER`: available for order. 
- `PREORDER`: available for pre-order.
- `OUT_OF_STOCK`: out of stock.
-  `DISCONTINUED`: discontinued.
- For hotel catalog products, the enum values are:`IN_STOCK`: available for booking. 
- `OUT_OF_STOCK`: unavailable for booking.
- For entertainment catalog products, the enum values are:`AVAILABLE`
- `SUBSCRIBERS_ONLY` 
- `ON_DEMAND`
- `NOT_AVAILABLE`
- For  Auto-Inventory catalog products, the enum values are:`AVAILABLE`: available for order.
- `NOT_AVAILABLE`: Not available for order. |
##| image_url | string | The URL for the product image.|
##| video_url | string | Ad video link.|
##| brand | string | Brand information. |
##| additional_image_urls | string[] | Additional image URLs for the product. |
##| item_group_id | string | Product SPU ID. |
##| google_product_category | string | Category information. |
##| global_trade_item_number | string |  The Global Trade Item Number (GTIN) for the product. |
##| manufacturer_part_number | string | The Manufacturer Part Number (MPN) for the product. |
##| hotel_id| string | A unique ID for the hotel. |
##| name | string | The name of the hotel. |
##| hotel_category | string[] | The categories of the hotel.
 
 For enum values, see [List of values for `hotel_category`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List of values for hotel_category). |
##| hotel_retailer_id | string | A unique ID for the hotel retailer. |
##| address | object | Address information. |
###| address | string | The address of the hotel, destination, or the dealership. |
###| secondary_address|string|The secondary street address of the hotel|
###| tertiary_address|string|The tertiary street address of the hotel.|
###| city | string | The city where the hotel, destination, or the dealership is located. |
###| region | string | The region (state/province) where the hotel, destination, or the dealership is located. |
###| country | string | The country where the hotel or destination is located. |
###| postal_code  | string | The postal code for the dealership's address.|
##| neighborhood | string | The neighborhood where the hotel or destination is located.  
 
Example: `Bangkok Old Town`. |
##| postal_code|string|The postal code or zip code of the hotel. |
##| latitude | float | The latitude of the hotel, destination, or the dealership's location. 
Example: 37.484100 |
##| longitude |float | The latitude of the hotel, destination, or the dealership's location. 
Example: -122.148252 |
##|series_id |string|A unique self-defined ID for the short drama series.|
##|series_name |string|The name of the short drama series.|
##| target_config | object | Details of the primary targeting region for the short drama series. |
###| region_code | string | The region code of the primary targeting region for the short drama series.

Example: `US`. |
###| currency | string | Currency for the primary targeting region for the short drama series.

For supported currencies, see the **Code** column in [Budget verification ratio and precision of each currency](https://business-api.tiktok.com/portal/docs?id=1737585839634433#item-link-Budget%20verification%20ratio%20and%20precision%20of%20each%20currency).

Example: `USD`. |
##|recharge |object[]|Information about the recharge for the short drama series.|
###|type |string|Recharge type for the short drama series.

Enum values:
- `BY_TIERS`: Recharge by tiers.
- `SUBSCRIPTION`: Recharge by subscription fee for a time period.
- `BY_EPISODES`: Recharge by episodes.|
###|purchase_unit |string[]|Units for the recharge.

When `recharge_type` is `BY_TIERS`, the enum values are:
- `TIER 1`: tier 1.
- `TIER_2`: tier 2.
- `TIER 3`: tier 3.
- `TIER 4`: tier 4.
- `TIER 5`: tier 5.When `recharge_type` is `SUBSCRIPTION`, the enum values are:
- `WEEKLY`: weekly.
- `MONTHLY`: monthly.
- `QUARTERLY`: quarterly.
- `YEARLY`: yearly.When `recharge_type` is `BY_EPISODES`, specify one or more numeric strings that represent numbers no more than the total episode count.|
###|cost |float[]|The prices for the tiers, subscription periods, or episodes.|
##| margin_level | string | The percentage of the base price (`price`) for a hotel room that the hotel charges as deposit. 
For instance, a value of 10 means the hotel charges 10 percent of the base price for a hotel room as deposit. |
##| loyalty_program | string | The loyalty program offered by the hotel. 

For enum values, see [List of values for `loyalty_program`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List of values for loyalty_program). |
##| guest_ratings | object[] | Information about guest ratings for the hotel. |
###| rating_system | string | The rating system for the hotel. |
###| max_score | integer | The highest score that the hotel has received. |
###| score | float | The average score of the hotel. |
###| number_of_reviewers | integer | The number of guests who have reviewed the hotel. |
##| star_rating | float | Hotel star rating that is assigned by professional organizations or travel review agencies based on a set of criteria. The highest possible rating is usually 5 stars. Uploading it might help increase Page View Rate. |
##| room_type | string[] | The hotel room types. 

For enum values, see [List of values for `room_type`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List of values for room_type). |
##| priority | integer | The priority of the hotel or flight. 
 
Value range: 0-5. 
A higher value indicates a higher priority. |
##| flight_id | string | A unique ID for the flight. 
 
The ID will be automatically generated by the system.|
##| origin_airport | string | The origin airport of the flight, in the format of a three-letter IATA (International Air Transport Association) code. 
Example: `AAR`. |
##| destination_airport | string | The destination airport of the flight, in the format of a three-letter IATA code. 
Example: `ABD`. |
##| origin_city | string | The name of the origin city. |
##| destination_city | string | The name of the destination city. |
##| cabin_class | string | The cabin class of the flight.

Enum values:
- `FIRST_CLASS`: First Class. Premium service with luxurious amenities and private spaces.
- `FIRST_CLASS_SUITE`: First Class Suite. Private suites offering luxury and exclusivity.
- `BUSINESS_CLASS`: Business Class. Enhanced comfort and amenities for business and leisure travelers.
- `BUSINESS_CLASS_SUITE`: Business Class Suite. Spacious and private cabins in business class.
- `COMFORT_CLASS`: Comfort Class. Improved seating and service between premium and economy.
- `ECONOMY_CLASS`: Economy Class. Standard travel option with basic amenities at an affordable price.
- `BASIC_ECONOMY`: Basic Economy. Budget-friendly option with limited services and restrictions.
- `STANDARD_ECONOMY`: Standard Economy. Typical economy service with basic features and pricing.
- `PREMIUM_ECONOMY`: Premium Economy. Extra legroom and better in-flight services compared to standard economy.
- `LIE_FLAT_SEAT`: Lie Flat Seat. Fully reclining seats for optimal comfort on long flights.
- `CHARTER_CLASS`: Charter Class. Custom private aircraft hire for tailored travel experiences.
- `ELITE_CLASS`: Elite Class. Top-tier service combining the best features of first and business classes.
- `QUIET_CLASS`: Quiet Class. Noise-reduced area for a serene travel experience.  |
##| airline_company | string | The name of the airline company operating the flight.

Enum values:
- `AEROFLOT`: Aeroflot.
- `AIR_FRANCE_KLM_GROUP`: Air France-KLM Group.
- `ALASKA_AIRLINES`: Alaska Airlines.
- `ANA`: ANA.
- `AMERICAN_AIRLINES`: American Airlines.
- `BRITISH_AIRWAYS`: British Airways.
- `CATHAY_PACIFIC`: Cathay Pacific.
- `CHINA_SOUTHERN_AIRLINES`: China Southern Airlines.
- `CHINA_EASTERN_AIRLINES`: China Eastern Airlines.
- `DELTA_AIR_LINES`: Delta Air Lines.
- `EMIRATES`: Emirates.
- `JAPAN_AIRLINES`: Japan Airlines.
- `JETBLUE_AIRWAYS`: JetBlue Airways.
- `KLM_ROYAL_DUTCH_AIRLINES`: KLM Royal Dutch Airlines.
- `LUFTHANSA_GROUP`: Lufthansa Group.
- `QANTAS_AIRWAYS`: Qantas Airways.
- `QATAR_AIRWAYS`: Qatar Airways.
- `SINGAPORE_AIRLINES`: Singapore Airlines.
- `SOUTHWEST_AIRLINES`: Southwest Airlines.
- `TURKISH_AIRLINES`: Turkish Airlines.
- `UNITED_AIRLINES`: United Airlines.
- `VIRGIN_ATLANTIC`: Virgin Atlantic. |
##| destination_id | string | A unique ID for the destination. |
##| destination_name | string | The name of the destination. |
##| postal_code | string | Postal code or zip code for the destination. |
##| types | string[] | The type or types of destination. |
##| media_title_id| string | A unique ID for the media title item. 

A media title item is a media product that is available for distribution or consumption, such as a movie, TV show, music, or sports game. |
##| timeline | string | The timeline for the media title item. 

Enum values: 
- `COMING_SOON`: The media title item is not available now, but will be released soon.
-  `ONLINE`: The media title item is currently available for purchase or view.
- `EXPIRE_SOON`: The media title item will no longer be available for purchase or view soon.  |
##| category | string | The category of the media title item. 

Enum values: 
- `MOVIE`: movie.
- `MUSIC`: music.
-  `TV_SHOW`: TV show.
-  `TV_SERIES`: TV series.
- `SPORTS_GAME`: sports game.
-  `LIVE_EVENT`: live event.  |
##| genres | string[] | The genres of the media title item. 

To find out the allowed values for this field, refer to the "[ List of values for `genres` ](#item-link-List of values for genres ) " section below.  |
##| qid | string | QID (or Q number), the unique identifier of the media title item on Wikidata, which consists of the letter "Q" followed by one or more digits. |
##|vehicle_id|string|A unique ID for the vehicle.|
##|state_of_vehicle |string|The state of the vehicle.

Enum values:
- `NEW`: new.
- `USED`: used.
- `CPO`: CPO (certified pre-owned). CPO vehicles are used vehicles that have undergone thorough inspection and are typically newer, have lower mileage, and come with additional warranty coverage compared to regular used cars.Example: `USED`.|
##|vehicle_type|string|The type of the vehicle.

Enum values:
- `BOAT`: boat.
- `CAR_TRUCK`: car or truck.
- `COMMERCIAL`: A vehicle used for commercial purposes, such as a delivery truck.
- `MOTORCYCLE`: motorcycle.
- `POWERSPORT`: powersport. Recreational vehicles that are designed for outdoor activities and adventure, such as a snowmobile.
- `RV_CAMPER`: recreational vehicle or camper designed for travel and camping purposes.
- `TRAILER`: trailer.
- `OTHER`: Any other vehicle type not covered above.|
##|make |string|The make (brand) of the vehicle.|
##|model |string|The model of the vehicle.|
##|trim|string|The trim of the vehicle. The trim represents the distinctive specification package of the vehicle, tailored specifically to that model.|
##|year |integer|The year when the vehicle was launched, in the format of `YYYY`.|
##|vin|string|The VIN (Vehicle Identification Number) of the vehicle.|
##|mileage |object|The mileage of the vehicle.|
###|value |integer|Mileage value.|
###|unit |string|Mileage unit.

Enum values:
- `MILE`: mile.
- `KILOMETER`: kilometer.|
##|body_style |string|The body style of the vehicle.

Enum values:
- `CONVERTIBLE`: convertible.
- `COUPE`: coupe.
- `CROSSOVER`: crossover.
- `HATCHBACK`: hatchback.
- `MINIVAN`: minivan.
- `SMALL_CAR`: small car.
- `SEDAN`: sedan.
- `SUV`: SUV.
- `TRUCK`: truck.
- `VAN`: van.
- `WAGON`: wagon.
- `OTHER`: other.|
##|exterior_color|string|The exterior color of the vehicle.|
##|interior_color|string|The interior color of the vehicle.|
##|transmission|string|The transmission type of the vehicle.

Enum values:
- `AUTOMATIC`: automatic.
- `MANUAL`: manual.|
##|drivetrain|string|The drivetrain type of the vehicle.

Enum values:
- `4X2`: four-wheel drive vehicle with two wheel drive (2WD). The drivetrain delivers power to either the front wheels or the rear wheels.
- `4X4`: four-wheel drive vehicle with four wheel drive. The drivetrain delivers power to all four wheels.
- `AWD`: all-wheel drive. The drivetrain delivers power to all wheels continuously.
- `FWD`: front-wheel drive. The drivetrain delivers power to the front wheels only.
- `RWD`: rear-wheel drive. The drivetrain delivers power to the rear wheels only.
- `OTHER`: any other drivetrain type not covered above, such as electric vehicles with unique drivetrain styles.|
##|fuel_type|string|The fuel type of the vehicle.

Enum values:
- `DIESEL`: diesel.
- `ELECTRIC`: electric.
- `FLEX`: flex fuel, a blend of gasoline and ethanol.
- `GASOLINE`: gasoline.
- `HYBRID`: hybrid.
- `OTHER`: other.|
##|dealer|object|Detailed information about the dealership.|
###|dealer_id|string|A unique ID for the dealership.|
###|dealer_name|string|The name of the dealership.|
###|dealer_phone|string|The phone number of the dealership.|
###|stock_number|string|The stock number assigned to the vehicle by the dealership. The stock number is usually assigned when the vehicle physically arrives at the dealership's lot.|
##|date_first_on_lot|string|The date when the vehicle physically arrives at the dealership's lot, in the format of `YYYY-MM-DD`.|
##|days_on_lot|integer|The number of days the vehicle has been on the dealership's lot.|
##| profession| object | Product other information. |
###| age_group | string | Age group of products. 

Enum values:`NEW_BORN`, `INFANT`, `TODDLER`, `KIDS`, `ADULT`. 

Example: `ADULT`. |
###| color | string | Color of products. |
###| condition | string | Current status of products. 

- For E-commerce catalog products, the enum values are `NEW`, `REFURBISHED`, and `USED`. 
- For entertainment catalog products, the enum values are `NEW`  and `USED`.
- For Auto-Inventory catalog products, the enum values are: `EXCELLENT`: excellent.
- `GOOD`: good.
- `FAIR`: fair.
- `POOR`: poor.
- `OTHER`: other. |
###| gender | string | The targeted gender for the product. The accuracy of this field is important to ensure products are delivered to the intended gender group.  Enum values: `MALE`, `FEMALE`, `UNISEX`. |
###| material | string | Materials used in products, such as cotton, denim or leather. |
###| pattern | string | Pattern or graphic printing on a product. |
###| product_category | string | The category that the product belongs to. 
Only the first three levels are required. |
###| shipping | string | The type of shipping for the product. 
Recommended format: `COUNTRY:STATE:SHIPPING_TYPE: PRICE`.
Use ";" to separate different regions. 
Example: `US:CA:Ground:9.99 USD`.|
###| shipping_weight | string | The shipping weight of the product. 
The allowed units are `lb`, `oz`, `g`, `kg`. 
Example: 1 oz, 1 kg. |
###| size | string | Size of the item. |
###| tax | string | Product tax. |
###|offer_type|string|The type of offer.|
###|term_length|string|The duration for which the offer applies.|
###|offer_term_qualifier|string|The unit for term of the offer.|
###|amount_price|string|The amount of the offer.|
###|amount_percentage|string|The percentage for the APR in a finance offer.|
###|amount_qualifier|string|The qualifier for the `amount_price` or `amount_percentage`.|
###|downpayment|string|The downpayment at the time of purchase or lease.|
###|downpayment_qualifier|string|Qualifier for the downpayment.|
###|offer_disclaimer|string|The full text of the offer disclaimer to appear in the in-app pop-up.|
###|offer_disclaimer_url|string|A URL that directs users to additional information related to the offer disclaimer, in the format of `http://xxx` or `https://xxx`.|
###|emission_disclaimer|string|The text of the emission disclaimer to appear within the in-app pop-up.|
###|emission_disclaimer_url|string|A URL that directs users to additional information related to the emission disclaimer, in the format of `http://xxx` or `https://xxx`.|
###|emission_overlay_disclaimer|string|The short text of the disclaimer to appear on-screen in the disclaimer banner.|
###|emission_image_link|string|The link to an image showing the emission level, in the format of `http://xxx` or `https://xxx`.|
###|company_type|string|The company type for the short drama series.

Enum values:
- `COPYRIGHT_HOLDER`: copyright holder.
- `DISTRIBUTOR`: distributor.|
###|copyright_holder_name|string|The name of the copyright holder company.|
###|app_id|string|The App ID of the app to promote in your ads.

To obtain a list of App IDs within your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).|
###|minis_id|string|Mini program ID.|
###|total_episodes|number|The number of episodes in the short drama series.|
###|initial_paid_episodes |number|The episode number at which viewers are required to pay to continue watching the short drama series. |
###|per_episode_duration|number|The average duration of each episode in minutes.|
###|spoken_language|string|The language that actors in the original short drama series speak.

Enum values:
- `ar`: Arabic.
- `de`: German.
- `cs`: Czech.
- `en`: English.
- `es`: Spanish.
- `fr`: French.
- `he`: Hebrew.
- `hi`: Hindi.
- `id`: Indonesian.
- `it`: Italian.
- `ja`: Japanese.
- `ko`: Korean.
- `ms`: Malay.
- `pl`: Polish.
- `pt`: Portuguese.
- `ro`: Romanian.
- `ru`: Russian.
- `ta`: Tamil.
- `th`: Thai.
- `tr`: Turkish.
- `vi`: Vietnamese.
- `zh`: Simplified Chinese.
- `zh-hant`: Traditional Chinese.|
###|subtitle_language |string|The language used for the subtitles in the short drama series.

Enum values:
- `ar`: Arabic.
- `de`: German.
- `cs`: Czech.
- `en`: English.
- `es`: Spanish.
- `fr`: French.
- `he`: Hebrew.
- `hi`: Hindi.
- `id`: Indonesian.
- `it`: Italian.
- `ja`: Japanese.
- `ko`: Korean.
- `ms`: Malay.
- `pl`: Polish.
- `pt`: Portuguese.
- `ro`: Romanian.
- `ru`: Russian.
- `ta`: Tamil.
- `th`: Thai.
- `tr`: Turkish.
- `vi`: Vietnamese.
- `zh`: Simplified Chinese.
- `zh-hant`: Traditional Chinese.|
###|production_type |string|Production type, whether the short drama series is locally produced or translated for export.

Enum values:
- `LOCAL`: Local drama. The short drama features local actors, and the language for actors, narration, and subtitles is the local official language.
- `TRANSLATION`: Translated drama. The short drama is packaged for international distribution with added subtitles, narration, and dubbing in another language.|
###|target_audience |string|The target audience for the short drama series.

Enum values:
- `MALE`: Male. The short drama is primarily targeted at male audiences, often centered around a male protagonist or narrated from a male perspective. Themes typically include the accumulation of power, wealth, and prestige, the enhancement of abilities, and strategic planning.
- `FEMALE`: Female. The short drama is primarily targeted at female audiences, often centered around a female protagonist or narrated from a female perspective. These dramas usually contain elements of romance and love.
- `NEUTRAL`: Neutral. The short drama doesn't have a specific gender target audience.|
###|characters |string[]|The list of characters in the short drama series.

For enum values, see [List of values for `characters`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List%20of%20values%20for%20characters).|
###|genres |string[]|The genres of the short drama series as indicated by the main storyline or plot.

For enum values, see [List of values for mini series `genres`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List%20of%20values%20for%20mini%20series%20genres).|
###|historical_context|string[]|The historical background or setting of the short drama series.

For enum values, see [List of values for `historical_context`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List%20of%20values%20for%20historical_context).|
###|actors|string[]|The names of the actors in the short drama series.|
##| price | object | Price information. |
###| price | float | The base price.
For destination catalog products, this field represents the average or lowest price for the destination. The `description` field may provide information on whether this is the average price or the lowest price.|
###| currency | string | Unit of currency that must match the unit of currency of catalog's target country. If you do not provide it, we will use the default unit of currency of the catalog's target country. |
###| sale_price | float | The discounted price. |
###| sale_price_effective_date | string[] | Start and end date and time of sale. |
##|landing_page | object | Landing page information. |
###| landing_page_url | string | URL of the landing page where you can view or purchase the product. |
###| ios_url | string | Custom scheme for iOS apps as URL. For iOS, provide both iPhone & iPad app information if they are different from the regular iOS app. |
###| ios_app_store_id | string |App Store ID for the iOS app.|
###| ios_app_name | string | The iOS App name to display. |
###| iphone_app_store_id | string |App Store ID for the iPhone app.  |
###| iphone_app_name | string | The iphone App name to display. |
###|ipad_app_store_id|string|App Store ID for the iPad app. |
###| ipad_app_name | string | The iPad App name to display.|
###| android_url | string | Custom scheme for Android apps as URL. |
###| android_package | string | The Android package name. |
###| android_app_name | string | The Android App name to display. |
##| extra_info | object | Additional information. |
###| custom_label_0 | string | Additional information about the products you want to include. |
###| custom_label_1 | string | Additional information about the products you want to include. |
###| custom_label_2 | string | Additional information about the products you want to include. |
###| custom_label_3 | string | Additional information about the products you want to include. |
###| custom_label_4 | string | Additional information about the products you want to include. |
###| internal_label_0 | string |An internal label assigned to the hotel or flight. You can use internal labels to filter items while creating product sets. These labels are exclusively visible to you.

Length Limit: 100 characters.

If you are using custom labels (`custom_label_0` to `custom_label_4`) for filtering items during product set creation, consider switching to internal labels. Unlike custom labels, internal labels can be added or modified as needed without the need for submitting items for review each time, avoiding potential interruptions in ad delivery.|
###| internal_label_1 | string | An internal label assigned to the hotel or flight. You can use internal labels to filter items while creating product sets. These labels are exclusively visible to you.

Length Limit: 100 characters.

If you are using custom labels (`custom_label_0` to `custom_label_4`) for filtering items during product set creation, consider switching to internal labels. Unlike custom labels, internal labels can be added or modified as needed without the need for submitting items for review each time, avoiding potential interruptions in ad delivery.|
##|image_status|string| Storage status of the product image. Enum values:
- `PROCESSING`: The image is being stored.  
- `SUCCESS`: The image is stored successfully. 
- `FAIL`: The image is not stored successfully. 
- `FILTERED`: The image was stored successfully but cannot be used because it does not meet the size requirements (must be equal to or larger than 500 px). For such images, the product audit status (`audit_status`) will stay at `processing` until you upload a new image.
- `NOT_SUPPORTED`: The image format is not supported.
- `NO_FOUND`: Cannot find the resource via the URL. Please ensure the URL is valid, and the file is publicly accessible. |
##| additional_product_list | object[] | Returned when you have configured additional targeting regions for the short drama series.

A list of additional targeting region settings for the short drama series of the same `series_id`. |
###| audit | object | Audit information. |
####| audit_status | string | Ad audit status. It indicates if the ad promoting the product can be deployed.

Enum values: `approved`, `rejected`, `processing`.|
###| rejected_info | object[] | Returned only when `audit_status` is `rejected`.

List of rejection reasons.  |
####| reason | string | Rejection reason. |
####| suggestion | string | Suggestions about how to revise to be approved. |
####| affected_placement | string[] | List of placements affected by the rejection. |
####| affected_country | string[] | List of countries or regions affected by the rejection. |
###| active_status | string | Whether the product is activated.

Enum values: `ACTIVATED`, `DEACTIVATED`. 

This field represents the advertiser-controlled online or offline status of the product. However, it does not necessarily imply that the product can be used to create ads. |
###| image_status | string | Storage status of the product image. 

Enum values:
- `PROCESSING`: The image is being stored.
- `SUCCESS`: The image is stored successfully.
- `FAIL`: The image is not stored successfully.
- `FILTERED`: The image was stored successfully but cannot be used because it does not meet the size requirements (must be equal to or larger than 500 px). For such images, the product audit status (`audit_status`) will stay at `processing` until you upload a new image.
- `NOT_SUPPORTED`: The image format is not supported.
- `NO_FOUND`: Cannot find the resource via the URL. Please ensure the URL is valid, and the file is publicly accessible. |
###| product_id | string | Product ID. |
###| series_id | string | A unique self-defined ID for the short drama series. |
###| series_name | string | The name of the short drama series. |
###| target_config | object | Details of the additional targeting region for the short drama series. |
####| region_code | string | The region code of the additional targeting region for the short drama series.

Example: `US`. |
####| currency | string | Currency for the additional targeting region for the short drama series.

For supported currencies, see the **Code** column in [Budget verification ratio and precision of each currency](https://business-api.tiktok.com/portal/docs?id=1737585839634433#item-link-Budget%20verification%20ratio%20and%20precision%20of%20each%20currency).

Example: `USD`. |
###| image_url | string | The URL for the short drama series poster image. |
###| recharge | object[] | Information about the recharge for the short drama series. |
####| type | string | Recharge type for the short drama series.

Enum values:
- `BY_TIERS`: Recharge by tiers.
- `SUBSCRIPTION`: Recharge by subscription fee for a time period.
- `BY_EPISODES`: Recharge by episodes. |
####| purchase_unit | string[] | Units for the recharge.

When `recharge_type` is `BY_TIERS`, the enum values are:
- `TIER 1`: tier 1.
- `TIER_2`: tier 2.
- `TIER 3`: tier 3.
- `TIER 4`: tier 4.
- `TIER 5`: tier 5.When `recharge_type` is `SUBSCRIPTION`, the enum values are:
- `WEEKLY`: weekly.
- `MONTHLY`: monthly.
- `QUARTERLY`: quarterly.
- `YEARLY`: yearly.When `recharge_type` is `BY_EPISODES`, specify one or more numeric strings that represent numbers no more than the total episode count. |
####| cost | float[] | The prices for the tiers, subscription periods, or episodes. |
###| profession | object | Product other information. |
####| company_type | string | The company type for the short drama series.

Enum values:
- `COPYRIGHT_HOLDER`: copyright holder.
- `DISTRIBUTOR`: distributor. |
####| copyright_holder_name | string | The name of the copyright holder company. |
####| app_id | string | The App ID of the app to promote in your ads.

To obtain a list of App IDs within your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). |
####| minis_id | string | Mini program ID. |
####| total_episodes | number | The number of episodes in the short drama series. |
####| initial_paid_episodes | number | The episode number at which viewers are required to pay to continue watching the short drama series. |
####| per_episode_duration | number | The average duration of each episode in minutes. |
####| spoken_language | string | The language that actors in the original short drama series speak.

Enum values:
- `ar`: Arabic.
- `de`: German.
- `cs`: Czech.
- `en`: English.
- `es`: Spanish.
- `fr`: French.
- `he`: Hebrew.
- `hi`: Hindi.
- `id`: Indonesian.
- `it`: Italian.
- `ja`: Japanese.
- `ko`: Korean.
- `ms`: Malay.
- `pl`: Polish.
- `pt`: Portuguese.
- `ro`: Romanian.
- `ru`: Russian.
- `ta`: Tamil.
- `th`: Thai.
- `tr`: Turkish.
- `vi`: Vietnamese.
- `zh`: Simplified Chinese.
- `zh-hant`: Traditional Chinese. |
####| subtitle_language | string | The language used for the subtitles in the short drama series.

Enum values:
- `ar`: Arabic.
- `de`: German.
- `cs`: Czech.
- `en`: English.
- `es`: Spanish.
- `fr`: French.
- `he`: Hebrew.
- `hi`: Hindi.
- `id`: Indonesian.
- `it`: Italian.
- `ja`: Japanese.
- `ko`: Korean.
- `ms`: Malay.
- `pl`: Polish.
- `pt`: Portuguese.
- `ro`: Romanian.
- `ru`: Russian.
- `ta`: Tamil.
- `th`: Thai.
- `tr`: Turkish.
- `vi`: Vietnamese.
- `zh`: Simplified Chinese.
- `zh-hant`: Traditional Chinese. |
####| production_type | string | Production type, whether the short drama series is locally produced or translated for export.

Enum values:
- `LOCAL`: Local drama. The short drama features local actors, and the language for actors, narration, and subtitles is the local official language.
- `TRANSLATION`: Translated drama. The short drama is packaged for international distribution with added subtitles, narration, and dubbing in another language. |
####| target_audience | string | The target audience for the short drama series.

Enum values:
- `MALE`: Male. The short drama is primarily targeted at male audiences, often centered around a male protagonist or narrated from a male perspective. Themes typically include the accumulation of power, wealth, and prestige, the enhancement of abilities, and strategic planning.
- `FEMALE`: Female. The short drama is primarily targeted at female audiences, often centered around a female protagonist or narrated from a female perspective. These dramas usually contain elements of romance and love.
- `NEUTRAL`: Neutral. The short drama doesn't have a specific gender target audience. |
####| characters | string[] | The list of characters in the short drama series.

For enum values, see [List of values for `characters`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List%20of%20values%20for%20characters). |
####| genres | string[] | The genres of the short drama series as indicated by the main storyline or plot.

For enum values, see [List of values for mini series `genres`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List%20of%20values%20for%20mini%20series%20genres). |
####| historical_context | string[] | The historical background or setting of the short drama series.

For enum values, see [List of values for `historical_context`](https://business-api.tiktok.com/portal/docs?id=1740497429681153#item-link-List%20of%20values%20for%20historical_context). |
####| actors | string[] | The names of the actors in the short drama series. |
###| video_url | string | Ad video link. |
###| additional_image_urls | string[] | Additional image URLs for the product.

**Note**: The value of this field will be null.
 |
###| global_trade_item_number | string | The Global Trade Item Number (GTIN) for the product.

**Note**: The value of this field will be null.
 |
###| manufacturer_part_number | string | The Manufacturer Part Number (MPN) for the product.

**Note**: The value of this field will be null.
 |
###| landing_page | object | Landing page information.

**Note**: The value of this field will be null.
 |
####| landing_page_url | string | URL of the landing page where you can view or purchase the product. |
###| extra_info | object | Additional information.

**Note**: The value of this field will be null.
 |
####| custom_label_0 | string | Additional information about the products you want to include. |
####| custom_label_1 | string | Additional information about the products you want to include. |
####| custom_label_2 | string | Additional information about the products you want to include. |
####| custom_label_3 | string | Additional information about the products you want to include. |
####| custom_label_4 | string | Additional information about the products you want to include. |
#| page_info | object | Pagination information. |
##| page | number | Current page number. |
##| page_size | number | Page size. |
##| total_number | number | Total number of results. |
##| total_page | number | Total pages of results. |
```

#### List of values for `genres`

```xtable
| Value {30%}| Description {60%}|
|---|---|
| `ACTION` | action |
| `ADULT_ANIMATION` | adult animation |
| `ADVENTURE` | adventure |
| `ANIMATION` | animation |
| `BIOGRAPHICAL` | biographical |
| `BLACK_COMEDY` | black comedy |
| `BUDDY` | buddy |
| `COMEDY` | comedy |
| `COMIC` | comic |
| `COOKING_SHOW` | cooking show |
| `CRIME` | crime |
| `DISASTER` | disaster |
| `DOCUMENTARY` | documentary |
| `DRAMA` | drama |
| `FAMILY` | family |
| `FANTASY` | fantasy |
| `GAME_SHOW` | game show |
| `HISTORY` | history |
| `HORROR` | horror |
| `LGBT` | LGBT |
| `MARTIAL_ARTS` | martial arts |
| `MILITARY` | military |
| `MUSIC` | music |
| `POLICE` | police |
| `POLICE_PROCEDURAL` | police procedural |
| `POLITIC` | politic |
| `REALITY_TV` | reality TV |
| `ROAD` | road |
| `ROMANCE` | romance |
| `SATIRE` | satire |
| `SCIENCE_FICTION` | science fiction |
| `SITCOM` | sitcom |
| `SOAP_OPERA` | soap opera |
| `SPORT` | sport |
| `SPY` | spy |
| `STEAMPUNK` | steampunk |
| `SUPERHERO` | superhero |
| `TALK_SHOW` | talk show |
| `TEEN` | teen |
| `THRILLER` | thriller |
| `TIME_TRAVEL` | time travel |
| `VAMPIRE` | vampire |
| `WAR` | war |
| `WESTERN` | western |
| `ZOMBIE` | zombie |
```

### Example
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
"message": "OK",
"code": 0,
"data": {
    "page_info": {
        "total_number": 2,
        "page": 1,
        "page_size": 100,
        "total_page": 1
    },
    "list": [
        {
            "audit": {
                    "audit_status": "rejected",
                    "rejected_info": [
                        {
                            "reason": "The product/service promoted on the ad/landing page belongs to a prohibited industry in your ad targeting location(s) as taking our own business evaluation, users' experience and value of advertisement impact, etc into consideration.",
                            "suggestion": "Please change the promoted product/service in your ad or change the targeting location in your ad group settings according to our policy. https://ads.tiktok.com/help/article?aid=6685586866860720134 Learn More.",
                            "affected_placement": [
                                "PLACEMENT_TIKTOK",
                                "PLACEMENT_PANGLE"
                            ],
                            "affected_country": [
                                "US"
                            ]
                        }
                    ]
                },
            "sku_id": "tiktok_item_12423",
            "product_id": "6872175464299923205",
            "title": "qgs test product",
            "manufacturer_part_number": "",
            "profession": {
                "product_category": "Apparel & Accessories > Clothing > Shirts",
                "color": "red",
                "pattern": "stripes1",
                "material": "cotton",
                "tax": "xxx",
                "shipping_weight": "1 kg",
                "shipping": "US:CA:Ground:9.99 USD",
                "condition": "USED",
                "size": "L"
            },
            "brand": "xiaoru",
            "landing_page": {
                "ios_app_store_id": "https://ios_app_store.com",
                "iphone_app_name": "iphone_app_name",
                "android_package": "a.b.com",
                "iphone_app_store_id": "https://iphone_app_store.com",
                "ios_app_name": "ios_app_name",
                "ipad_app_name": "ipad_app_name",
                "landing_page_url": "https://ads.tiktok.com",
                "android_app_name": "android_app_name",
                "android_url": "https://www.android.com",
                "ios_url": "https://www.ios.com",
                "ipad_app_store_id": "https://ipad_app_store.com"
            },
            "image_url": "http://p1.ipstatp.com/origin/ad-site-i18n/201912265d0d606810c7e88e46248eef",
            "additional_image_urls": [
                "http://p1.ipstatp.com/origin/ad-site-i18n/201912265d0d606810c7e88e46248eef",
                "http://p1.ipstatp.com/origin/ad-site-i18n/201912265d0d606810c7e88e46248eef"
            ],
            "extra_info": {
                "custom_label_1": "b",
                "custom_label_0": "a",
                "custom_label_4": "e"
            },
            "global_trade_item_number": "",
            "video_url": "ad-site-i18n/201911045d0db9f0eb2f8cc14bb4ae1a",
            "google_product_category": "2.22",
            "price": {
                "sale_price_effective_date": [
                    "2017-12-11 04:36",
                    "2017-12-31 12:06"
                ],
                "currency": "USD",
                "price": 100.0,
                "sale_price": 30.0
            },
            "availability": "AVAILABLE_FOR_ORDER",
            "item_group_id": "1.11",
            "description": "qgs test product description"
        },
        {
            "audit": {
                    "audit_status": "processing"
                },
            "sku_id": "tiktok_item_12424",
            "product_id": "6872175464299939589",
            "title": "qgs test product",
            "manufacturer_part_number": "4.44",
            "product_detail": {
                "color": "red",
                "material": "cotton",
                "tax": "xxx",
                "shipping": "US:CA:Ground:9.99 USD",
                "condition": "USED",
                "size": "L"
            },
            "brand": "xiaoru",
            "landing_page": {
                "ios_app_store_id": "https://ios_app_store.com",
                "iphone_app_name": "iphone_app_name",
                "android_package": "a.b.com",
                "iphone_app_store_id": "https://iphone_app_store.com",
                "ios_app_name": "ios_app_name",
                "ipad_app_name": "ipad_app_name",
                "landing_page_url": "https://ads.tiktok.com",
                "android_app_name": "android_app_name",
                "android_url": "https://www.android.com",
                "ios_url": "https://www.ios.com",
                "ipad_app_store_id": "https://ipad_app_store.com"
            },
            "image_url": "http://p1.ipstatp.com/origin/ad-site-i18n/201912265d0d606810c7e88e46248eef",
            "additional_image_urls": [],
            "extra_info": {},
            "global_trade_item_number": "3.33",
            "video_url": "ad-site-i18n/201911045d0db9f0eb2f8cc14bb4ae1a",
            "google_product_category": "2.22",
            "price_info": {
                "sale_price_effective_date": [],
                "currency": "USD",
                "price": 100.0,
                "sale_price": 0.0
            },
            "availability": "AVAILABLE_FOR_ORDER",
            "item_group_id": "1.11",
            "description": "qgs test product description"
        }
    ]
},
"request_id": "2020091405213901023125321411850"
}
(/code);
```
