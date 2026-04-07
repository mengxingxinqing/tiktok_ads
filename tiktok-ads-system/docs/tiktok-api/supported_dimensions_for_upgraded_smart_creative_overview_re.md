# Supported dimensions for Upgraded Smart+ Creative Overview Reports

**Doc ID**: 1843337892165889
**Path**: API Reference/Upgraded Smart+/Reporting/Run an Upgraded Smart+ Creative Overview Report/Supported dimensions for Upgraded Smart+ Creative Overview Reports

---

Dimension is an attribute to group your data by.

The following table outlines the available dimensions and supported dimension groupings in Upgraded Smart+ Creative Overview Reports.

```xtable
| Dimension name {23%} | Dimension type {14%} | Description {24%} | Supported dimension groupings {41%} |
| --- | --- | --- | --- |
| `advertiser_id` | Advertising dimension | Group by Advertiser ID. | 
- `advertiser_id` x `main_material_id`
- `advertiser_id` x `ad_text_entity_id`
- `advertiser_id` x `call_to_action_entity_id`
- `advertiser_id` x `interactive_add_on_entity_id` |
| `campaign_id` | Advertising dimension | Group by Campaign ID. | 
- `campaign_id` x `main_material_id`
- `campaign_id` x `ad_text_entity_id`
- `campaign_id` x `call_to_action_entity_id`
- `campaign_id` x `interactive_add_on_entity_id` |
| `adgroup_id` | Advertising dimension | Group by Ad group ID. | 
- `adgroup_id` x `main_material_id`
- `adgroup_id` x `ad_text_entity_id`
- `adgroup_id` x `call_to_action_entity_id`
- `adgroup_id` x `interactive_add_on_entity_id` |
| `smart_plus_ad_id` | Advertising dimension | Group by Ad ID. | 
- `smart_plus_ad_id` x `main_material_id`
- `smart_plus_ad_id` x `ad_text_entity_id`
- `smart_plus_ad_id` x `call_to_action_entity_id`
- `smart_plus_ad_id` x `interactive_add_on_entity_id` |
| `main_material_id` | Creative dimension | Group by main creative ID. | 
- `advertiser_id` x `main_material_id`
- `campaign_id` x `main_material_id`
- `adgroup_id` x `main_material_id`
- `smart_plus_ad_id` x `main_material_id` |
| `ad_text_entity_id` | Setting dimension | Group by ad text entity ID.

The ID is a system-generated unique identifier for an ad text. | 
- `advertiser_id` x `ad_text_entity_id`
- `campaign_id` x `ad_text_entity_id`
- `adgroup_id` x `ad_text_entity_id`
- `smart_plus_ad_id` x `ad_text_entity_id` |
| `call_to_action_entity_id` | Setting dimension | Group by call-to-action entity ID.

The ID is a system-generated unique identifier for a call-to-action. | 
- `advertiser_id` x `call_to_action_entity_id`
- `campaign_id` x `call_to_action_entity_id`
- `adgroup_id` x `call_to_action_entity_id`
- `smart_plus_ad_id` x `call_to_action_entity_id` |
| `interactive_add_on_entity_id` | Setting dimension | Group by interactive add-on entity ID.

The ID is a system-generated unique identifier for an interactive add-on. | 
- `advertiser_id` x `interactive_add_on_entity_id`
- `campaign_id` x `interactive_add_on_entity_id`
- `adgroup_id` x `interactive_add_on_entity_id`
- `smart_plus_ad_id` x `interactive_add_on_entity_id` |
```
