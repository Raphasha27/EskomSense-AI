CREATE TABLE load_shedding_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stage INTEGER NOT NULL CHECK (stage >= 0 AND stage <= 8),
  area VARCHAR(255) NOT NULL,
  municipality VARCHAR(255) NOT NULL,
  province VARCHAR(255) NOT NULL,
  scheduled_start TIMESTAMPTZ NOT NULL,
  scheduled_end TIMESTAMPTZ NOT NULL,
  actual_start TIMESTAMPTZ,
  actual_end TIMESTAMPTZ,
  was_accurate BOOLEAN
);

CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  area VARCHAR(255) NOT NULL,
  predicted_stage INTEGER NOT NULL,
  confidence_score DECIMAL(5, 4) NOT NULL,
  prediction_for TIMESTAMPTZ NOT NULL,
  model_version VARCHAR(50) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE prediction_accuracy (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prediction_id UUID REFERENCES predictions(id) ON DELETE CASCADE,
  actual_stage INTEGER NOT NULL,
  was_correct BOOLEAN NOT NULL,
  deviation INTEGER NOT NULL,
  evaluated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TYPE tip_category AS ENUM ('battery', 'solar', 'generator', 'saving');

CREATE TABLE energy_tips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stage_applicable INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  tip_text TEXT NOT NULL,
  category tip_category NOT NULL,
  upvotes INTEGER DEFAULT 0
);

CREATE TABLE area_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email_hash VARCHAR(255) NOT NULL,
  area VARCHAR(255) NOT NULL,
  municipality VARCHAR(255) NOT NULL,
  notify_hours_before INTEGER DEFAULT 2,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE eskom_api_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  endpoint VARCHAR(255) NOT NULL,
  response_status INTEGER NOT NULL,
  data_snapshot JSONB,
  fetched_at TIMESTAMPTZ DEFAULT NOW()
);
