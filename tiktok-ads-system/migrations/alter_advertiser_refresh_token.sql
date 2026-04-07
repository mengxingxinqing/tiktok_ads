-- 修改 advertisers 表的 refresh_token 列为 nullable
-- 原因：TikTok OAuth 返回的 access_token 响应中可能不包含 refresh_token

ALTER TABLE advertisers 
MODIFY COLUMN refresh_token TEXT NULL COMMENT '刷新 token（可能不返回），1年有效';

ALTER TABLE advertisers 
MODIFY COLUMN refresh_token_expire_at DATETIME(6) NULL COMMENT 'refresh_token 过期时间';
