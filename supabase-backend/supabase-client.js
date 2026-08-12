import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

export const SUPABASE_URL = 'YOUR_SUPABASE_URL';
export const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
export const DEMO_MODE = true;

const supabase = DEMO_MODE ? null : createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export async function logLoadSheddingEvent(event) {
  if (DEMO_MODE) return;
  const { error } = await supabase.from('load_shedding_events').insert([event]);
  if (error) throw error;
}

export async function savePrediction(prediction) {
  if (DEMO_MODE) return { id: 'mock-id' };
  const { data, error } = await supabase.from('predictions').insert([prediction]).select().single();
  if (error) throw error;
  return data;
}

export async function evaluatePredictionAccuracy(predictionId, actualStage) {
  if (DEMO_MODE) return;
  // Normally you'd fetch the prediction, compare, and insert to prediction_accuracy
}

export async function getHistoricalEvents(area) {
  if (DEMO_MODE) return [];
  const { data, error } = await supabase.from('load_shedding_events').select('*').eq('area', area).order('scheduled_start', { ascending: false });
  if (error) throw error;
  return data;
}

export async function getTrendsByArea(area) {
  if (DEMO_MODE) return [];
  // Return aggregated trends
  return [];
}

export async function getEnergyTips(stage) {
  if (DEMO_MODE) return [
    { title: 'Test Tip', tip_text: 'Buy a UPS', category: 'battery', upvotes: 10 }
  ];
  const { data, error } = await supabase.from('energy_tips').select('*').lte('stage_applicable', stage).order('upvotes', { ascending: false });
  if (error) throw error;
  return data;
}
