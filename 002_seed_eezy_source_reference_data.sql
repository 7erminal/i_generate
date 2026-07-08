-- Seed data for eezy_source reference tables
-- Safe to re-run (uses ON DUPLICATE KEY UPDATE)
-- MySQL 8+

SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- ---------------------------------------------------------------------------
-- eezy_source_business
-- ---------------------------------------------------------------------------
INSERT INTO eezy_source_business (
    businessId,
    businessName,
    businessPhone,
    businessEmail,
    businessAddress,
    active,
    created_at,
    updated_at
) VALUES (
    1,
    'Eezy Source',
    '0557881327',
    'bede.abbe@gmail.com',
    NULL,
    1,
    '2026-06-26 22:27:24',
    '2026-06-26 22:27:24'
)
ON DUPLICATE KEY UPDATE
    businessName = VALUES(businessName),
    businessPhone = VALUES(businessPhone),
    businessEmail = VALUES(businessEmail),
    businessAddress = VALUES(businessAddress),
    active = VALUES(active),
    created_at = VALUES(created_at),
    updated_at = VALUES(updated_at);

-- ---------------------------------------------------------------------------
-- eezy_source_currency
-- ---------------------------------------------------------------------------
INSERT INTO eezy_source_currency (
    currencyId,
    currencyName,
    currencyCode,
    currencySymbol,
    active,
    created_at,
    updated_at
) VALUES
(
    1,
    'Ghana Cedi',
    'GHS',
    'GH₵',
    1,
    '2026-06-26 20:17:44',
    '2026-06-26 20:17:44'
),
(
    2,
    'Yuan',
    'CNY',
    '¥',
    1,
    '2026-06-26 20:25:34',
    '2026-06-26 20:25:34'
)
ON DUPLICATE KEY UPDATE
    currencyName = VALUES(currencyName),
    currencyCode = VALUES(currencyCode),
    currencySymbol = VALUES(currencySymbol),
    active = VALUES(active),
    created_at = VALUES(created_at),
    updated_at = VALUES(updated_at);

-- ---------------------------------------------------------------------------
-- eezy_source_systemunits
-- ---------------------------------------------------------------------------
INSERT INTO eezy_source_systemunits (
    systemUnitId,
    unitName,
    unitCode,
    unitSymbol,
    unitDescription,
    unitType,
    active,
    created_at,
    updated_at
) VALUES
(
    1,
    'Kilogram',
    'KG',
    'kg',
    'Weight',
    'Weight',
    1,
    '2026-06-26 20:28:50',
    '2026-06-26 20:28:50'
),
(
    2,
    'Percentage',
    'PER',
    '%',
    'percentage',
    'Percentage',
    1,
    '2026-06-26 21:21:18',
    '2026-06-26 21:21:18'
)
ON DUPLICATE KEY UPDATE
    unitName = VALUES(unitName),
    unitCode = VALUES(unitCode),
    unitSymbol = VALUES(unitSymbol),
    unitDescription = VALUES(unitDescription),
    unitType = VALUES(unitType),
    active = VALUES(active),
    created_at = VALUES(created_at),
    updated_at = VALUES(updated_at);

-- ---------------------------------------------------------------------------
-- eezy_source_processconfig
-- ---------------------------------------------------------------------------
INSERT INTO eezy_source_processconfig (
    processConfigId,
    processCode,
    sellerShipperDeliveryFee,
    sellerShipperDeliveryFeeUnit,
    handlingFee,
    handlingFeeUnit,
    weightUnit,
    shippingMode,
    customRate,
    customRateUnit,
    shippingMargin,
    shippingMarginUnit,
    defaultCurrency,
    active,
    created_at,
    updated_at,
    business_id
) VALUES (
    1,
    'EEZY',
    10,
    'KG',
    2,
    'KG',
    'KG',
    'Normal',
    1,
    'KG',
    2,
    '%',
    'GHS',
    1,
    '2026-06-26 22:27:24',
    '2026-06-27 00:44:22',
    1
)
ON DUPLICATE KEY UPDATE
    processCode = VALUES(processCode),
    sellerShipperDeliveryFee = VALUES(sellerShipperDeliveryFee),
    sellerShipperDeliveryFeeUnit = VALUES(sellerShipperDeliveryFeeUnit),
    handlingFee = VALUES(handlingFee),
    handlingFeeUnit = VALUES(handlingFeeUnit),
    weightUnit = VALUES(weightUnit),
    shippingMode = VALUES(shippingMode),
    customRate = VALUES(customRate),
    customRateUnit = VALUES(customRateUnit),
    shippingMargin = VALUES(shippingMargin),
    shippingMarginUnit = VALUES(shippingMarginUnit),
    defaultCurrency = VALUES(defaultCurrency),
    active = VALUES(active),
    created_at = VALUES(created_at),
    updated_at = VALUES(updated_at),
    business_id = VALUES(business_id);
