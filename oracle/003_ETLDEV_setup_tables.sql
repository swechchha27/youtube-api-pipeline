
-- Create staging table in staging schema
CREATE TABLE staging.youtube_video_data (
    video_id VARCHAR2(255) PRIMARY KEY,
    title VARCHAR2(255),
    description CLOB,
    published_at TIMESTAMP,
    channel_id VARCHAR2(255),
    channel_title VARCHAR2(255),
    view_count NUMBER,
    like_count NUMBER,
    dislike_count NUMBER,
    comment_count NUMBER,
    thumbnail_url VARCHAR2(255),
    tags CLOB
);

-- Create fact and dimension tables for star type schema in ODS schema
CREATE TABLE ods.youtube_video_fact (
    video_id VARCHAR2(255) PRIMARY KEY,
    view_count NUMBER,
    like_count NUMBER,
    dislike_count NUMBER,
    comment_count NUMBER
);

-- dimension table for video metadata
CREATE TABLE ods.youtube_video_metadata_dim (
    video_id VARCHAR2(255) PRIMARY KEY,
    title VARCHAR2(255),
    description CLOB,
    published_at TIMESTAMP,
    channel_id VARCHAR2(255),
    channel_title VARCHAR2(255),
    tags CLOB
);

-- dimension table for channel metadata
CREATE TABLE ods.youtube_channel_metadata_dim (
    channel_id VARCHAR2(255) PRIMARY KEY,
    channel_title VARCHAR2(255),
    description CLOB,
    published_at TIMESTAMP
);

-- dimension table for category metadata
CREATE TABLE ods.youtube_category_metadata_dim (
    category_id VARCHAR2(255) PRIMARY KEY,
    title VARCHAR2(255),
    description CLOB
);

-- dimension table for time metadata
CREATE TABLE ods.youtube_time_metadata_dim (
    time_id TIMESTAMP PRIMARY KEY,
    year NUMBER,
    month NUMBER,
    day NUMBER,
    hour NUMBER,
    minute NUMBER,
    second NUMBER
);