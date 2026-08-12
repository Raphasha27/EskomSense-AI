-- Mock Data for EskomSense AI Upgrade

INSERT INTO load_shedding_events (id, stage, area, municipality, province, scheduled_start, scheduled_end) VALUES
(gen_random_uuid(), 4, 'Sandton', 'City of Johannesburg', 'Gauteng', NOW() - INTERVAL '1 day', NOW() - INTERVAL '22 hours'),
(gen_random_uuid(), 6, 'Rondebosch', 'City of Cape Town', 'Western Cape', NOW() - INTERVAL '2 days', NOW() - INTERVAL '46 hours'),
(gen_random_uuid(), 2, 'Umhlanga', 'eThekwini', 'KwaZulu-Natal', NOW() - INTERVAL '3 days', NOW() - INTERVAL '70 hours');

INSERT INTO predictions (id, area, predicted_stage, confidence_score, prediction_for, model_version) VALUES
('p1000000-0000-0000-0000-000000000001', 'Sandton', 4, 0.95, NOW() - INTERVAL '1 day', 'v2.1.0'),
('p1000000-0000-0000-0000-000000000002', 'Rondebosch', 5, 0.72, NOW() - INTERVAL '2 days', 'v2.1.0');

INSERT INTO prediction_accuracy (id, prediction_id, actual_stage, was_correct, deviation) VALUES
(gen_random_uuid(), 'p1000000-0000-0000-0000-000000000001', 4, TRUE, 0),
(gen_random_uuid(), 'p1000000-0000-0000-0000-000000000002', 6, FALSE, 1);

INSERT INTO energy_tips (stage_applicable, title, tip_text, category, upvotes) VALUES
(4, 'Pre-chill your freezer', 'Turn your freezer to max setting 2 hours before Stage 4 hits to preserve food longer.', 'saving', 120),
(6, 'Generator maintenance', 'Ensure generator oil is topped up for extended Stage 6 runs.', 'generator', 85),
(2, 'Charge power banks', 'Keep all portable chargers topped up for minor outages.', 'battery', 210);
