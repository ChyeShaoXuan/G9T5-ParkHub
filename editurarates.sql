DELETE FROM ura_rates
WHERE weekdayRate = 0.0
   OR satdayRate = 0.0
   OR sunPHRate = 0.0;

-- ALTER TABLE ura_rates ADD UNIQUE INDEX idx_unique (ppCode, startTime, endTime);
